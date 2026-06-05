# -*- coding: utf-8 -*-
"""
从 1123.mp4 提取一段完整的步行循环，解决两个问题：
1. 镜头跳动 -> 统一裁剪窗口（取所有帧 bbox 的外接矩形 Union，固定位置）
2. 太短 -> 取更长的帧序列找最佳循环点
"""
import os, numpy as np, cv2, imageio.v2 as imageio, json

VIDEO = r"D:\下龙虾下载\1123.mp4"
OUT_DIR = r"D:\renpy-8.5.3\DemoAVG\tools\output"
os.makedirs(OUT_DIR, exist_ok=True)

cap = cv2.VideoCapture(VIDEO)
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frames_all = []
for i in range(total):
    ok, img = cap.read()
    if ok:
        frames_all.append(img)
cap.release()
print(f"loaded {len(frames_all)} frames")

# bg estimation
def estimate_bg(img):
    h,w = img.shape[:2]; s=20
    patches = [img[0:s,0:s], img[0:s,w-s:w], img[h-s:h,0:s], img[h-s:h,w-s:w]]
    return np.median(np.concatenate([p.reshape(-1,3) for p in patches], axis=0), axis=0)

bg_color = estimate_bg(frames_all[0])

def find_bbox(img, bg, thresh=35):
    diff = np.abs(img.astype(np.int16) - bg.reshape(1,1,3)).sum(axis=2)
    mask = (diff > thresh).astype(np.uint8)*255
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    ys,xs = np.where(mask > 0)
    if len(xs)==0: return None, mask
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())), mask

# ---- 分析范围：从 A 和 D 都喜欢的区间 frame 60~110 ----
RANGE_START = 55
RANGE_END = 115

# 1. 先统计算这个区间所有 bbox 的 Union（外接矩形）
bboxes = []
for i in range(RANGE_START, min(RANGE_END, len(frames_all))):
    box, _ = find_bbox(frames_all[i], bg_color)
    if box:
        bboxes.append((i, box))

print(f"\nbbox count in range: {len(bboxes)}")

x1s = [b[0] for _,b in bboxes]
y1s = [b[1] for _,b in bboxes]
x2s = [b[2] for _,b in bboxes]
y2s = [b[3] for _,b in bboxes]

union_x1 = min(x1s)
union_y1 = min(y1s)
union_x2 = max(x2s)
union_y2 = max(y2s)
print(f"Union bbox: ({union_x1},{union_y1})-({union_x2},{union_y2})")
print(f"Union size: {union_x2-union_x1}x{union_y2-union_y1}")

# 再加 padding
PAD = 30
CROP_X1 = max(0, union_x1 - PAD)
CROP_Y1 = max(0, union_y1 - PAD)
CROP_X2 = min(frames_all[0].shape[1], union_x2 + PAD)
CROP_Y2 = min(frames_all[0].shape[0], union_y2 + PAD)
CW = CROP_X2 - CROP_X1
CH = CROP_Y2 - CROP_Y1
print(f"Fixed crop window: ({CROP_X1},{CROP_Y1})-({CROP_X2},{CROP_Y2}) = {CW}x{CH}")

# ---- 2. 找最佳循环区间：用足部运动 ----
# 对每帧算下三分之一区域的质心 x 变化（步态）
crop_ys = []
for i in range(RANGE_START, min(RANGE_END, len(frames_all))):
    crop = frames_all[i][CROP_Y1:CROP_Y2, CROP_X1:CROP_X2]
    # 下 1/3 区域找前景质心
    sub = crop[CH*2//3:, :]
    diff = np.abs(sub.astype(np.int16) - bg_color.reshape(1,1,3)).sum(axis=2)
    mask = (diff > 30).astype(np.uint8)
    ys, xs = np.where(mask > 0)
    if len(xs) > 0:
        centroid_x = xs.mean()
    else:
        centroid_x = CW // 2
    crop_ys.append(centroid_x)

# 找信号中的周期（检测峰值区间）
# 简单滑动：找足部质心 x 的峰-谷模式
# 更直接的：找一段起点和终点姿态最相似的（帧差分最小）
# 对每个可能的周期起点 ~终点，算首帧和末帧的足部区域差分
FOOT_PCT = 0.25  # 足部占比从下往上

best_cycle = None
best_diff = float('inf')
MIN_CYCLE = 14  # 最少帧数
MAX_CYCLE = 24  # 最大帧数

foot_h = int(CH * FOOT_PCT)

for start in range(RANGE_START, RANGE_END - MIN_CYCLE):
    for end in range(start + MIN_CYCLE, min(start + MAX_CYCLE + 1, RANGE_END)):
        img_start = frames_all[start][CROP_Y2-foot_h:CROP_Y2, CROP_X1:CROP_X2]
        img_end = frames_all[end][CROP_Y2-foot_h:CROP_Y2, CROP_X1:CROP_X2]
        diff_val = np.abs(img_start.astype(np.int16) - img_end.astype(np.int16)).mean()
        if diff_val < best_diff:
            best_diff = diff_val
            best_cycle = (start, end)

print(f"\nBest cycle: frames {best_cycle[0]}-{best_cycle[1]}, {best_cycle[1]-best_cycle[0]} frames, foot_diff={best_diff:.2f}")

# ---- 3. 用最佳循环提帧 ----
cycle_start, cycle_end = best_cycle
cycle_len = cycle_end - cycle_start

# 提 16 帧（偶数，方便循环）
NUM_FRAMES = 16
step = cycle_len / NUM_FRAMES
frame_indices = [cycle_start + int(round(step * i)) for i in range(NUM_FRAMES)]
# 确保末帧 <= cycle_end
frame_indices = [min(f, cycle_end) for f in frame_indices]
# 去重
seen = set()
unique_indices = []
for f in frame_indices:
    if f not in seen:
        seen.add(f)
        unique_indices.append(f)
frame_indices = unique_indices[:NUM_FRAMES]
# 补齐如果不够
while len(frame_indices) < NUM_FRAMES:
    frame_indices.append(frame_indices[-1])
frame_indices = frame_indices[:NUM_FRAMES]

# 再加一个更密版本（步长更小，16 帧但帧间隔 1~2）
NUM_FRAMES_DENSE = 16
frame_indices_dense = list(range(frame_indices[0], frame_indices[0] + NUM_FRAMES_DENSE))

print(f"Cycle {cycle_start}-{cycle_end} ({cycle_len}f):")
print(f"  Sparse ({NUM_FRAMES}f): {frame_indices}")
print(f"  Dense ({NUM_FRAMES_DENSE}f): {frame_indices_dense}")

# ---- 4. 生成裁剪图（固定窗口）+ 抠背景 ----
def frames_to_gif(frames, indices, tag, fps=12):
    out_imgs = []
    for idx in indices:
        if idx >= len(frames):
            continue
        img = frames[idx][CROP_Y1:CROP_Y2, CROP_X1:CROP_X2].copy()
        # 抠背景
        diff = np.abs(img.astype(np.int16) - bg_color.reshape(1,1,3)).sum(axis=2)
        mask = (diff > 30).astype(np.uint8) * 255
        kernel = np.ones((4,4), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        # 转 BGRA
        bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        bgra[:,:,3] = mask
        # 贴白底
        rgba = cv2.cvtColor(bgra, cv2.COLOR_BGRA2RGBA)
        white = np.ones_like(rgba[:,:,:3], dtype=np.uint8) * 255
        alpha = rgba[:,:,3:4].astype(np.float32) / 255.0
        rgb = (rgba[:,:,:3].astype(np.float32)*alpha + white.astype(np.float32)*(1-alpha)).astype(np.uint8)
        # 缩放高度到 400
        scale = 400.0 / CH
        rgb = cv2.resize(rgb, (int(CW*scale), 400))
        out_imgs.append(rgb)
    out_path = os.path.join(OUT_DIR, f"zhou_walk_{tag}.gif")
    imageio.mimsave(out_path, out_imgs, duration=1.0/fps, loop=0)
    print(f"  -> {out_path} ({len(out_imgs)} frames)")
    return out_path

print("\n--- Generating GIFs ---")

# A1: 16帧等间距（来自最佳周期）
a1 = frames_to_gif(frames_all, frame_indices, "A1_cycle16", fps=12)

# A2: 16帧密集（连续帧）
a2 = frames_to_gif(frames_all, frame_indices_dense, "A2_cycle16_dense", fps=12)

# B: 扩展为更长循环（24帧等间距）
step24 = cycle_len / 24
indices24 = [cycle_start + int(round(step24 * i)) for i in range(24)]
indices24 = [min(f, cycle_end) for f in indices24]
b = frames_to_gif(frames_all, indices24, "B_cycle24", fps=12)

# C: 更密的 16 帧步长 1（从 A 区间更早的开始）
c_start = cycle_start - 2
c_indices = list(range(max(0, c_start), max(0, c_start) + 16))
c = frames_to_gif(frames_all, c_indices, "C_cycle16_consecutive", fps=12)

# D: 用同一固定窗口但取之前 D 的帧号范围 step2
d_range_s = 60
d_range_e = 84
d_indices = list(range(d_range_s, min(d_range_e, len(frames_all))))
d = frames_to_gif(frames_all, d_indices, "D_fixed_range_60_84", fps=12)

print("\nDone!")
print(f"Fixed crop window: {CW}x{CH}")
print(f"Union bbox: ({union_x1},{union_y1})-({union_x2},{union_y2})")