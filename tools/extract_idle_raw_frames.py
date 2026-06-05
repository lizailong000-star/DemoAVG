# -*- coding: utf-8 -*-
"""
找视频里"主角静止站立"的几帧（motion 最低的区域），抠图供做 idle 待机。
"""
import os, cv2, numpy as np

VIDEO = r"D:\下龙虾下载\1123.mp4"
OUT_DIR = r"D:\renpy-8.5.3\DemoAVG\game\images\player\zhou_idle_v2_raw"
os.makedirs(OUT_DIR, exist_ok=True)

cap = cv2.VideoCapture(VIDEO)
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frames_all = []
for _ in range(total):
    ok, img = cap.read()
    if ok: frames_all.append(img)
cap.release()
print(f"loaded {len(frames_all)} frames")

# 找运动幅度最低的几个连续区域（候选静止帧）
# 帧间灰度差均值
grays = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames_all]
motions = []
for i in range(1, len(grays)):
    diff = np.abs(grays[i].astype(np.int16) - grays[i-1].astype(np.int16)).mean()
    motions.append((i, diff))

# 排序找最低
motions_sorted = sorted(motions, key=lambda x: x[1])
print("\n最低运动帧（候选静止）:")
for f, v in motions_sorted[:25]:
    print(f"  frame {f}: motion={v:.3f}")

# 找连续 5 帧 motion 都极低的窗口
print("\n找 motion 持续低的窗口（候选 idle 序列）:")
WIN = 5
THRESH = 1.5  # 低于这个的算"静止"
candidates = []
for start in range(len(motions) - WIN):
    vals = [m[1] for m in motions[start:start+WIN]]
    if max(vals) < THRESH:
        candidates.append((motions[start][0], vals))

for start_f, vals in candidates[:10]:
    print(f"  frames {start_f}~{start_f+WIN-1}: {[f'{v:.2f}' for v in vals]}")

# 从最佳静止窗口里挑 4 张（间隔 5~8 帧，捕捉呼吸的微小变化）
# 取 frame 0~10 区域，间隔取
# 看上面统计：frame 1~5 motion 0.09~0.42，超静止
chosen = [5, 7, 9, 11]  # frame 5~11 都是相对静止的呼吸窗口

print(f"\n选定 idle 4 帧: {chosen}")

# 用同样的固定 crop 窗口策略
# 用 walk 的 union（已经包含人物完整身体）作参考
# walk 用的是 frame 138~188 的人物位置；idle 是 frame 1~13，人物可能在不同位置
# 算 idle 候选区间的 union bbox

def estimate_bg(img):
    h,w = img.shape[:2]; s=20
    patches=[img[0:s,0:s], img[0:s,w-s:w], img[h-s:h,0:s], img[h-s:h,w-s:w]]
    return np.median(np.concatenate([p.reshape(-1,3) for p in patches], axis=0), axis=0)

bg = estimate_bg(frames_all[0])

def find_bbox(img, thresh=35):
    diff = np.abs(img.astype(np.int16) - bg.reshape(1,1,3)).sum(axis=2)
    mask = (diff > thresh).astype(np.uint8)*255
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    ys, xs = np.where(mask > 0)
    if len(xs)==0: return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))

# 先粗抠看一下 idle 区域人物位置
bboxes = []
for i in chosen:
    b = find_bbox(frames_all[i])
    bboxes.append(b)
    print(f"  frame {i}: bbox={b}")

# 取 union + padding
ux1 = min(b[0] for b in bboxes)
uy1 = min(b[1] for b in bboxes)
ux2 = max(b[2] for b in bboxes)
uy2 = max(b[3] for b in bboxes)
PAD = 40
H = frames_all[0].shape[0]; W = frames_all[0].shape[1]
cx1 = max(0, ux1-PAD); cy1 = max(0, uy1-PAD)
cx2 = min(W, ux2+PAD); cy2 = min(H, uy2+PAD)
print(f"\nidle crop window: ({cx1},{cy1})-({cx2},{cy2}) = {cx2-cx1}x{cy2-cy1}")

# 输出原始裁剪 PNG（不抠图，由老李/AI 工具去水印+抠）
for idx, frame_i in enumerate(chosen, start=1):
    img = frames_all[frame_i]
    crop = img[cy1:cy2, cx1:cx2].copy()
    out = os.path.join(OUT_DIR, f"zhou_idle_raw_{idx:02d}_f{frame_i}.png")
    cv2.imwrite(out, crop)
    print(f"  -> {out}")

# 同时保存 sample 完整画面（方便看水印位置）
sample = frames_all[chosen[0]]
cv2.imwrite(os.path.join(OUT_DIR, "_sample_full_idle.png"), sample)

# 拼合 4 帧预览
tiles = []
for idx in range(1, 5):
    p = os.path.join(OUT_DIR, f"zhou_idle_raw_{idx:02d}_f{chosen[idx-1]}.png")
    t = cv2.imread(p)
    sc = 300.0 / t.shape[0]
    s = cv2.resize(t, (int(t.shape[1]*sc), 300))
    tiles.append(s)
montage = np.hstack(tiles)
cv2.imwrite(os.path.join(OUT_DIR, "_montage_4frames.png"), montage)

print(f"\n输出到: {OUT_DIR}")
print(f"文件: zhou_idle_raw_01_f1.png, _02_f5.png, _03_f9.png, _04_f13.png")
print(f"原始尺寸: {cx2-cx1}x{cy2-cy1} (未抠图，等老李去水印+抠背景)")