# -*- coding: utf-8 -*-
"""
继续优化：完整循环 + 重复播放多遍 + 调速
- 用完整的 22 帧循环（81~102，每一帧都用）
- 每个 GIF 重复 4 遍循环，看清"走了好几步"
- 提供不同速度版本
"""
import os, numpy as np, cv2, imageio.v2 as imageio

VIDEO = r"D:\下龙虾下载\1123.mp4"
OUT_DIR = r"D:\renpy-8.5.3\DemoAVG\tools\output"
os.makedirs(OUT_DIR, exist_ok=True)

cap = cv2.VideoCapture(VIDEO)
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frames_all = []
for _ in range(total):
    ok, img = cap.read()
    if ok: frames_all.append(img)
cap.release()
print(f"loaded {len(frames_all)} frames")

def estimate_bg(img):
    h,w = img.shape[:2]; s=20
    patches=[img[0:s,0:s], img[0:s,w-s:w], img[h-s:h,0:s], img[h-s:h,w-s:w]]
    return np.median(np.concatenate([p.reshape(-1,3) for p in patches], axis=0), axis=0)
bg_color = estimate_bg(frames_all[0])

def find_bbox(img, bg, thresh=35):
    diff = np.abs(img.astype(np.int16) - bg.reshape(1,1,3)).sum(axis=2)
    mask = (diff > thresh).astype(np.uint8)*255
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    ys,xs = np.where(mask > 0)
    if len(xs)==0: return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))

# Union bbox 来自 range 55~115
bboxes = [find_bbox(frames_all[i], bg_color) for i in range(55, 115)]
bboxes = [b for b in bboxes if b]
union_x1 = min(b[0] for b in bboxes)
union_y1 = min(b[1] for b in bboxes)
union_x2 = max(b[2] for b in bboxes)
union_y2 = max(b[3] for b in bboxes)
PAD = 30
H = frames_all[0].shape[0]
W = frames_all[0].shape[1]
CROP_X1 = max(0, union_x1 - PAD)
CROP_Y1 = max(0, union_y1 - PAD)
CROP_X2 = min(W, union_x2 + PAD)
CROP_Y2 = min(H, union_y2 + PAD)
CW = CROP_X2 - CROP_X1
CH = CROP_Y2 - CROP_Y1
print(f"Fixed crop: {CW}x{CH}")

def render_frame(img):
    sub = img[CROP_Y1:CROP_Y2, CROP_X1:CROP_X2]
    diff = np.abs(sub.astype(np.int16) - bg_color.reshape(1,1,3)).sum(axis=2)
    mask = (diff > 30).astype(np.uint8) * 255
    kernel = np.ones((4,4), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    bgra = cv2.cvtColor(sub, cv2.COLOR_BGR2BGRA)
    bgra[:,:,3] = mask
    rgba = cv2.cvtColor(bgra, cv2.COLOR_BGRA2RGBA)
    white = np.ones_like(rgba[:,:,:3], dtype=np.uint8) * 255
    alpha = rgba[:,:,3:4].astype(np.float32) / 255.0
    rgb = (rgba[:,:,:3].astype(np.float32)*alpha + white.astype(np.float32)*(1-alpha)).astype(np.uint8)
    scale = 400.0 / CH
    return cv2.resize(rgb, (int(CW*scale), 400))

def make_gif(indices, tag, fps, repeat=1):
    base_frames = [render_frame(frames_all[i]) for i in indices if i < len(frames_all)]
    final_frames = base_frames * repeat
    out_path = os.path.join(OUT_DIR, f"zhou_walk_LOOP_{tag}.gif")
    imageio.mimsave(out_path, final_frames, duration=1.0/fps, loop=0)
    print(f"  {tag}: {len(indices)}f x{repeat} = {len(final_frames)}f @ {fps}fps -> {out_path}")
    return out_path

print("\n--- Long Loop GIFs ---")

# 1. 完整 22 帧循环周期 81~102，每帧都用，重复 4 次 = 88 帧 @ 12fps = 7.3秒
make_gif(list(range(81, 103)), "full_cycle_x4_12fps", fps=12, repeat=4)

# 2. 同上但 10fps（慢一点，更清晰）
make_gif(list(range(81, 103)), "full_cycle_x4_10fps", fps=10, repeat=4)

# 3. 扩展循环：60~110 连续 50 帧 重复 2 次 @ 12fps = 8.3秒
make_gif(list(range(60, 110)), "wide_range_x2_12fps", fps=12, repeat=2)

# 4. 60~110 连续 50 帧 重复 3 次 @ 12fps = 12.5秒，超长版
make_gif(list(range(60, 110)), "wide_range_x3_12fps", fps=12, repeat=3)

# 5. 全片 24~240 step1 部分（中段最稳） 60~120 共 60 帧 重复 2 次
make_gif(list(range(60, 120)), "wide60_x2_12fps", fps=12, repeat=2)

print("\nDone.")