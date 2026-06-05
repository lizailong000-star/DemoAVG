# -*- coding: utf-8 -*-
"""
解决"首尾跳帧"：
策略 A：搜索全身姿态最匹配的(start,end)对作为循环点
策略 B：Ping-Pong 正放+倒放，强制无缝（适合走路这种对称动作）
策略 C：尾首交叉淡化过渡几帧
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

# 固定 crop window (来自 55~115 union)
bboxes = [find_bbox(frames_all[i], bg_color) for i in range(55, 115)]
bboxes = [b for b in bboxes if b]
union_x1 = min(b[0] for b in bboxes)
union_y1 = min(b[1] for b in bboxes)
union_x2 = max(b[2] for b in bboxes)
union_y2 = max(b[3] for b in bboxes)
PAD=30
H = frames_all[0].shape[0]; W = frames_all[0].shape[1]
CROP_X1 = max(0, union_x1-PAD); CROP_Y1 = max(0, union_y1-PAD)
CROP_X2 = min(W, union_x2+PAD); CROP_Y2 = min(H, union_y2+PAD)
CW = CROP_X2-CROP_X1; CH = CROP_Y2-CROP_Y1
print(f"crop: {CW}x{CH}")

# 所有 crop 后的帧（灰度，用于全身比对）
crops_gray = []
crops_color = []
for img in frames_all:
    sub = img[CROP_Y1:CROP_Y2, CROP_X1:CROP_X2]
    crops_color.append(sub)
    crops_gray.append(cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY))

# ---- 策略 A：扫描全身最佳循环点 ----
# 搜索范围 50~140，循环长度 40~80（@24fps = 1.6~3.3秒）
print("\n--- Scanning best full-body loop ---")
best = None
best_score = float('inf')
for start in range(45, 150):
    for length in range(40, 81, 2):
        end = start + length
        if end >= len(frames_all): break
        # 全身灰度差
        diff = np.abs(crops_gray[start].astype(np.int16) - crops_gray[end].astype(np.int16)).mean()
        if diff < best_score:
            best_score = diff
            best = (start, end, length)
print(f"Best loop: frames {best[0]}-{best[1]} (length {best[2]}), full-body diff={best_score:.3f}")

# 再找次优、第三优（备选）
candidates = []
for start in range(45, 150):
    for length in range(40, 81, 2):
        end = start + length
        if end >= len(frames_all): break
        diff = np.abs(crops_gray[start].astype(np.int16) - crops_gray[end].astype(np.int16)).mean()
        candidates.append((diff, start, end, length))
candidates.sort()
print("Top 5 loop candidates:")
for c in candidates[:5]:
    print(f"  diff={c[0]:.3f}  frames {c[1]}-{c[2]} (len {c[3]})")

def render(idx):
    sub = crops_color[idx]
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

def make_gif(frames, tag, fps):
    path = os.path.join(OUT_DIR, f"zhou_walk_SEAMLESS_{tag}.gif")
    imageio.mimsave(path, frames, duration=1.0/fps, loop=0)
    print(f"  {tag}: {len(frames)}f @ {fps}fps -> {path}")
    return path

print("\n--- Generating seamless loop GIFs ---")

# 1. 最佳循环点 x3 重复
s, e, L = best
indices = list(range(s, e))  # 不含末帧 e（因为 e 应该接回 s）
base = [render(i) for i in indices]
make_gif(base * 3, f"bestLoop_{s}_{e}_x3", fps=12)

# 2. 次优循环点 x3
s2, e2, L2 = candidates[1][1], candidates[1][2], candidates[1][3]
base2 = [render(i) for i in range(s2, e2)]
make_gif(base2 * 3, f"bestLoop2_{s2}_{e2}_x3", fps=12)

# 3. 第三优
s3, e3, L3 = candidates[2][1], candidates[2][2], candidates[2][3]
base3 = [render(i) for i in range(s3, e3)]
make_gif(base3 * 3, f"bestLoop3_{s3}_{e3}_x3", fps=12)

# 4. Ping-Pong（正放+倒放，强制无缝）
# 用 81~102 一个周期，但末尾不重复首尾帧避免双重抖动
indices_pp = list(range(81, 103))
base_pp = [render(i) for i in indices_pp]
# pingpong = forward + reverse[1:-1]（去掉两端避免重复）
pingpong = base_pp + base_pp[-2:0:-1]  # 反序去掉两端
make_gif(pingpong * 2, f"pingpong_81_102_x2", fps=12)

# 5. Ping-Pong wide range
indices_pp2 = list(range(60, 110))
base_pp2 = [render(i) for i in indices_pp2]
pingpong2 = base_pp2 + base_pp2[-2:0:-1]
make_gif(pingpong2 * 1, f"pingpong_60_109_x1", fps=12)

# 6. 最佳循环 + 末尾交叉淡化到首帧（4帧过渡）
def crossfade_loop(base_frames, fade_n=4):
    """末尾 fade_n 帧渐变到首帧"""
    if len(base_frames) < fade_n*2: return base_frames
    result = list(base_frames[:-fade_n])
    for i in range(fade_n):
        alpha = (i+1) / (fade_n+1)
        # 末段帧 alpha 混合到 首帧
        last = base_frames[-fade_n + i].astype(np.float32)
        first = base_frames[0].astype(np.float32)
        blend = (last * (1-alpha) + first * alpha).astype(np.uint8)
        result.append(blend)
    return result

s, e, L = best
indices_cf = list(range(s, e+1))
base_cf = [render(i) for i in indices_cf]
faded = crossfade_loop(base_cf, fade_n=4)
make_gif(faded * 3, f"crossfade_{s}_{e}_x3", fps=12)

print("\nDone.")