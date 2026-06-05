# -*- coding: utf-8 -*-
"""
从原视频直接拆 8 帧原始画面（不抠背景、不转 alpha、不降低画质），供老李去水印。
"""
import os, cv2, numpy as np

VIDEO = r"D:\下龙虾下载\1123.mp4"
OUT_DIR = r"D:\renpy-8.5.3\DemoAVG\game\images\player\zhou_walk_v2_raw"
os.makedirs(OUT_DIR, exist_ok=True)

cap = cv2.VideoCapture(VIDEO)
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frames_all = []
for _ in range(total):
    ok, img = cap.read()
    if ok: frames_all.append(img)
cap.release()
print(f"loaded {len(frames_all)} frames, original size: {frames_all[0].shape}")

# 重点帧：之前选定的 8 帧
FRAMES = [138, 144, 150, 157, 163, 169, 176, 182]

# 看一下每帧的全画面（先保存一帧看看水印位置）
sample = frames_all[0]
cv2.imwrite(os.path.join(OUT_DIR, "_sample_frame0_full.png"), sample)
print(f"sample saved: full frame size {sample.shape[1]}x{sample.shape[0]}")

# 裁剪范围——尽量保留全身周边更多背景，方便去水印后重新裁切
# 之前 crop 是 (0,0)-(615,1108)，这次我放大一点留更多边缘
# 先算一下 130-190 范围 bbox 的 union
def find_bbox(img, thresh=30):
    # 用背景色中位数替代（四角）
    h,w = img.shape[:2]; s=15
    patches=[img[0:s,0:s], img[0:s,w-s:w], img[h-s:h,0:s], img[h-s:h,w-s:w]]
    bg = np.median(np.concatenate([p.reshape(-1,3) for p in patches], axis=0), axis=0)
    diff = np.abs(img.astype(np.int16) - bg.reshape(1,1,3)).sum(axis=2)
    mask = (diff > thresh).astype(np.uint8)*255
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    ys,xs = np.where(mask > 0)
    if len(xs)==0: return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))

bboxes = [find_bbox(frames_all[i]) for i in range(130, 195)]
bboxes = [b for b in bboxes if b]
ux1 = min(b[0] for b in bboxes)
uy1 = min(b[1] for b in bboxes)
ux2 = max(b[2] for b in bboxes)
uy2 = max(b[3] for b in bboxes)
# 加更大 padding（40px），保留更多周围画面对比，方便你去水印
PAD = 40
H = frames_all[0].shape[0]; W = frames_all[0].shape[1]
cx1 = max(0, ux1-PAD); cy1 = max(0, uy1-PAD)
cx2 = min(W, ux2+PAD); cy2 = min(H, uy2+PAD)
print(f"crop with padding: ({cx1},{cy1})-({cx2},{cy2}) = {cx2-cx1}x{cy2-cy1}")

# 保存 8 帧原始裁剪画面
for idx, frame_i in enumerate(FRAMES, start=1):
    img = frames_all[frame_i]
    crop = img[cy1:cy2, cx1:cx2].copy()  # 原始 BGR，未经任何处理
    out = os.path.join(OUT_DIR, f"zhou_walk_raw_{idx:02d}_f{frame_i}.png")
    cv2.imwrite(out, crop)
    print(f"  frame{idx:02d}=f{frame_i} -> {out} ({crop.shape[1]}x{crop.shape[0]})")

# 一张拼合大图方便你预览
tiles = []
for idx in range(1, 9):
    path = os.path.join(OUT_DIR, f"zhou_walk_raw_{idx:02d}_f{FRAMES[idx-1]}.png")
    tile = cv2.imread(path)
    # 缩略到 200px 高
    sc = 200.0 / tile.shape[0]
    small = cv2.resize(tile, (int(tile.shape[1]*sc), 200))
    tiles.append(small)

# 2行x4列拼合
row1 = np.hstack(tiles[:4])
row2 = np.hstack(tiles[4:])
montage = np.vstack([row1, row2])
montage_path = os.path.join(OUT_DIR, "_montage_8frames.png")
cv2.imwrite(montage_path, montage)
print(f"\nmontage: {montage_path}")

print(f"\n====== 输出去水印 ======")
print(f"8 帧原始 PNG 位置: {OUT_DIR}")
print(f"文件名: zhou_walk_raw_01_f138.png ~ zhou_walk_raw_08_f182.png")
print(f"原始分辨率: {cx2-cx1}x{cy2-cy1} (未缩放、未抠图、完整画质)")
print(f"水印位置: 在完整画面中查看 {OUT_DIR}\\sample_frame0_full.png 确定")
print(f"去完水印后告诉我，我来接 Ren'Py 状态机")