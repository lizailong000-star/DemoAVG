# -*- coding: utf-8 -*-
"""
对比测试：从 1123.mp4 不同时间段抽 12 帧做循环 GIF，看哪段最连贯。
"""
import os
import cv2
import numpy as np
import imageio.v2 as imageio

VIDEO = r"D:\下龙虾下载\1123.mp4"
OUT_DIR = r"D:\renpy-8.5.3\DemoAVG\tools\output"
os.makedirs(OUT_DIR, exist_ok=True)

cap = cv2.VideoCapture(VIDEO)
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"total={total}")

frames_all = []
for i in range(total):
    ok, img = cap.read()
    if not ok:
        break
    frames_all.append(img)
cap.release()
print(f"loaded {len(frames_all)} frames")

# 背景采样（用第 0 帧四角）
def estimate_bg(img):
    h, w = img.shape[:2]
    s = 20
    patches = [img[0:s, 0:s], img[0:s, w-s:w], img[h-s:h, 0:s], img[h-s:h, w-s:w]]
    arr = np.concatenate([p.reshape(-1, 3) for p in patches], axis=0)
    return np.median(arr, axis=0)

bg_color = estimate_bg(frames_all[0])

def find_bbox(img, bg, thresh=35):
    diff = np.abs(img.astype(np.int16) - bg.reshape(1, 1, 3)).sum(axis=2)
    mask = (diff > thresh).astype(np.uint8) * 255
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    ys, xs = np.where(mask > 0)
    if len(xs) == 0:
        return None, mask
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())), mask

# 多个候选窗口，每段 12 帧均匀采样
candidates = {
    "A_mid_60_95": list(range(60, 96, 3)),       # 12 帧
    "B_late_100_135": list(range(100, 136, 3)),  # 12 帧
    "C_end_175_210": list(range(175, 211, 3)),   # 12 帧
    "D_step_60_90_step2": list(range(60, 84, 2)),# 12 帧，步长 2（更慢动作）
    "E_full_24_240_step18": list(range(24, 241, 18))[:12],  # 全片均分 12 帧
}

def build_gif(frame_indices, tag, fps_out=12):
    frames_picked = [(i, frames_all[i]) for i in frame_indices if i < len(frames_all)]
    bboxes = []
    for i, img in frames_picked:
        box, _ = find_bbox(img, bg_color)
        bboxes.append((i, img, box))
    valid = [b for b in bboxes if b[2] is not None]
    if not valid:
        print(f"[{tag}] no valid frames")
        return
    max_w = max(b[2][2]-b[2][0] for b in valid)
    max_h = max(b[2][3]-b[2][1] for b in valid)
    pad = 20
    CW, CH = max_w + pad*2, max_h + pad*2
    FOOT_Y = CH - pad
    CENTER_X = CW // 2

    out_imgs = []
    for i, img, box in bboxes:
        if box is None:
            continue
        x1, y1, x2, y2 = box
        crop = img[y1:y2, x1:x2]
        ch, cw = crop.shape[:2]
        # 简单 mask
        sub_diff = np.abs(crop.astype(np.int16) - bg_color.reshape(1,1,3)).sum(axis=2)
        sub_mask = (sub_diff > 35).astype(np.uint8) * 255
        kernel = np.ones((5,5), np.uint8)
        sub_mask = cv2.morphologyEx(sub_mask, cv2.MORPH_OPEN, kernel)
        sub_mask = cv2.morphologyEx(sub_mask, cv2.MORPH_CLOSE, kernel)
        bgra = cv2.cvtColor(crop, cv2.COLOR_BGR2BGRA)
        bgra[:, :, 3] = sub_mask
        canvas = np.zeros((CH, CW, 4), dtype=np.uint8)
        dst_x = CENTER_X - cw // 2
        dst_y = FOOT_Y - ch
        canvas[dst_y:dst_y+ch, dst_x:dst_x+cw] = bgra
        rgba = cv2.cvtColor(canvas, cv2.COLOR_BGRA2RGBA)
        white = np.ones((CH, CW, 3), dtype=np.uint8) * 255
        alpha = rgba[:,:,3:4].astype(np.float32) / 255.0
        rgb = (rgba[:,:,:3].astype(np.float32)*alpha + white.astype(np.float32)*(1-alpha)).astype(np.uint8)
        # 缩放到 max 高度 400 保持比例
        scale = 400.0 / CH
        new_w = int(CW * scale)
        rgb_small = cv2.resize(rgb, (new_w, 400))
        out_imgs.append(rgb_small)
    out_path = os.path.join(OUT_DIR, f"zhou_walk_test_{tag}.gif")
    imageio.mimsave(out_path, out_imgs, duration=1.0/fps_out, loop=0)
    print(f"[{tag}] frames={[i for i,_,_ in bboxes]}  out={out_path}")

for tag, idxs in candidates.items():
    build_gif(idxs, tag)

print("done.")