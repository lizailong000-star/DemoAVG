# -*- coding: utf-8 -*-
"""
从 1123.mp4 提取 8 帧关键帧用于周卫国 walking 测试。
- 按 frame 索引抓帧（24/31/38/45/52/59/66/73）
- 每帧自动找人物 bbox（基于背景色阈值，假设背景较单一）
- 统一画布尺寸，对齐 foot_y 和 center_x
- 生成 GIF 预览
"""
import os
import sys
import cv2
import numpy as np
import imageio.v2 as imageio

VIDEO = r"D:\下龙虾下载\1123.mp4"
OUT_DIR = r"D:\renpy-8.5.3\DemoAVG\game\images\player\zhou_video_extract_test"
GIF_OUT = r"D:\renpy-8.5.3\DemoAVG\tools\output\zhou_video_walk_preview.gif"
TARGET_FRAMES = [24, 31, 38, 45, 52, 59, 66, 73]

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(GIF_OUT), exist_ok=True)

cap = cv2.VideoCapture(VIDEO)
if not cap.isOpened():
    print("[ERR] cannot open video:", VIDEO)
    sys.exit(1)

total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"[INFO] video: {W}x{H}, fps={fps:.2f}, total_frames={total}")

# ---------- 抓原始帧 ----------
raw_frames = {}
for f in TARGET_FRAMES:
    cap.set(cv2.CAP_PROP_POS_FRAMES, f)
    ok, img = cap.read()
    if not ok:
        print(f"[ERR] cannot read frame {f}")
        continue
    raw_frames[f] = img
cap.release()

# ---------- 用第 0 帧附近做背景采样 ----------
cap2 = cv2.VideoCapture(VIDEO)
cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)
_, bg_img = cap2.read()
cap2.release()

# 用四角小块估计背景主色
def estimate_bg(img):
    h, w = img.shape[:2]
    s = 20
    patches = [
        img[0:s, 0:s], img[0:s, w-s:w],
        img[h-s:h, 0:s], img[h-s:h, w-s:w],
    ]
    arr = np.concatenate([p.reshape(-1, 3) for p in patches], axis=0)
    return np.median(arr, axis=0)

bg_color = estimate_bg(bg_img)
print(f"[INFO] estimated bg color (BGR): {bg_color}")

# ---------- 找 bbox ----------
def find_bbox(img, bg, thresh=35):
    diff = np.abs(img.astype(np.int16) - bg.reshape(1, 1, 3)).sum(axis=2)
    mask = (diff > thresh).astype(np.uint8) * 255
    # 形态学清理
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    ys, xs = np.where(mask > 0)
    if len(xs) == 0:
        return None, mask
    x1, x2 = xs.min(), xs.max()
    y1, y2 = ys.min(), ys.max()
    return (int(x1), int(y1), int(x2), int(y2)), mask

bboxes = {}
masks = {}
for f, img in raw_frames.items():
    box, mask = find_bbox(img, bg_color)
    bboxes[f] = box
    masks[f] = mask
    print(f"[BBOX] frame {f}: {box}")

# ---------- 统一画布：取所有 bbox 的最大宽 + 高，再加 padding ----------
valid = [b for b in bboxes.values() if b is not None]
if not valid:
    print("[ERR] no valid bbox detected")
    sys.exit(1)

max_w = max(b[2] - b[0] for b in valid)
max_h = max(b[3] - b[1] for b in valid)
pad = 20
CANVAS_W = max_w + pad * 2
CANVAS_H = max_h + pad * 2
print(f"[INFO] canvas size: {CANVAS_W}x{CANVAS_H}")

# 统一脚底 y = CANVAS_H - pad
FOOT_Y = CANVAS_H - pad
CENTER_X = CANVAS_W // 2

# ---------- 裁切 + 居中放到画布 ----------
report = []
out_imgs = []
for idx, f in enumerate(TARGET_FRAMES, start=1):
    img = raw_frames.get(f)
    box = bboxes.get(f)
    if img is None or box is None:
        print(f"[WARN] skip frame {f}")
        continue
    x1, y1, x2, y2 = box
    crop = img[y1:y2, x1:x2]
    ch, cw = crop.shape[:2]
    cx = (x1 + x2) // 2
    # mask 转 alpha
    sub_mask = masks[f][y1:y2, x1:x2]
    # 4 通道
    bgra = cv2.cvtColor(crop, cv2.COLOR_BGR2BGRA)
    bgra[:, :, 3] = sub_mask
    # 画布（透明）
    canvas = np.zeros((CANVAS_H, CANVAS_W, 4), dtype=np.uint8)
    # 目标：脚底贴 FOOT_Y、中心贴 CENTER_X
    dst_x = CENTER_X - cw // 2
    dst_y = FOOT_Y - ch
    canvas[dst_y:dst_y+ch, dst_x:dst_x+cw] = bgra

    out_path = os.path.join(OUT_DIR, f"zhou_explore_walk_{idx:02d}.png")
    cv2.imwrite(out_path, canvas)
    report.append({
        "idx": idx,
        "src_frame": f,
        "size": f"{CANVAS_W}x{CANVAS_H}",
        "bbox": box,
        "foot_y": FOOT_Y,
        "center_x": CENTER_X,
        "char_w": cw,
        "char_h": ch,
        "src_cx": cx,
        "src_foot_y": y2,
        "out": out_path,
    })
    # GIF 用 RGB（透明合白底）
    rgba = cv2.cvtColor(canvas, cv2.COLOR_BGRA2RGBA)
    white = np.ones((CANVAS_H, CANVAS_W, 3), dtype=np.uint8) * 255
    alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
    rgb = (rgba[:, :, :3].astype(np.float32) * alpha + white.astype(np.float32) * (1 - alpha)).astype(np.uint8)
    out_imgs.append(rgb)

# ---------- GIF ----------
imageio.mimsave(GIF_OUT, out_imgs, duration=0.12, loop=0)
print(f"[OK] gif saved: {GIF_OUT}")

# ---------- 报告 ----------
print("\n========== REPORT ==========")
print(f"canvas: {CANVAS_W}x{CANVAS_H}, FOOT_Y={FOOT_Y}, CENTER_X={CENTER_X}")
for r in report:
    print(f"  walk_{r['idx']:02d} src=frame{r['src_frame']:>3}  size={r['size']}  "
          f"bbox={r['bbox']}  char={r['char_w']}x{r['char_h']}  "
          f"src_cx={r['src_cx']}  src_foot_y={r['src_foot_y']}")
print(f"gif: {GIF_OUT}")
