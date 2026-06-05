# -*- coding: utf-8 -*-
"""
对齐 8 帧已抠图素材：
- 输入：D:\renpy-8.5.3\DemoAVG\game\images\player\zhou_walk_v2_raw\zhou_walk_raw_NN_fXXX.png
- 输出：对齐后的 8 张 PNG 到 player\zhou_walk_v2_aligned\
- 对齐策略：脚底贴 canvas 底部，中心 x 居中
- 同时生成预览 GIF（白底 + 透明黑底两版）
"""
import os, cv2, numpy as np, imageio.v2 as imageio

IN_DIR = r"D:\renpy-8.5.3\DemoAVG\game\images\player\zhou_walk_v2_raw"
OUT_DIR = r"D:\renpy-8.5.3\DemoAVG\game\images\player\zhou_walk_v2_aligned"
GIF_DIR = r"D:\renpy-8.5.3\DemoAVG\tools\output"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(GIF_DIR, exist_ok=True)

files = sorted([f for f in os.listdir(IN_DIR) if f.startswith("zhou_walk_raw_") and f.endswith(".png")])
print(f"found {len(files)} files")

bboxes = []
imgs = []
for f in files:
    img = cv2.imread(os.path.join(IN_DIR, f), cv2.IMREAD_UNCHANGED)
    alpha = img[:, :, 3]
    ys, xs = np.where(alpha > 0)
    bbox = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
    bboxes.append(bbox)
    imgs.append(img)

# 取所有 bbox 的宽高最大值作为人物外接框
max_w = max(b[2]-b[0] for b in bboxes)
max_h = max(b[3]-b[1] for b in bboxes)
print(f"max bbox: {max_w}x{max_h}")

# 画布尺寸：给左右各 30px padding，底部 20px，顶部 30px
PAD_X = 30
PAD_TOP = 30
PAD_BOTTOM = 20
CW = max_w + PAD_X * 2
CH = max_h + PAD_TOP + PAD_BOTTOM
FOOT_Y = CH - PAD_BOTTOM  # 脚底统一到这个 y
CENTER_X = CW // 2  # 中心 x 统一到这里

print(f"output canvas: {CW}x{CH}, foot_y={FOOT_Y}, center_x={CENTER_X}")

# 对每张图：抠出人物（按 alpha bbox 裁），居中放到画布
out_imgs = []
out_imgs_white = []  # 白底预览
for f, img, box in zip(files, imgs, bboxes):
    x1, y1, x2, y2 = box
    crop = img[y1:y2, x1:x2]  # BGRA
    ch, cw = crop.shape[:2]
    # 中心 x 计算
    center_x_in_crop = cw // 2
    # 画布
    canvas = np.zeros((CH, CW, 4), dtype=np.uint8)
    dst_x = CENTER_X - cw // 2
    dst_y = FOOT_Y - ch
    canvas[dst_y:dst_y+ch, dst_x:dst_x+cw] = crop
    # 保存
    idx = int(f.split("_")[3])  # zhou_walk_raw_NN_fXXX.png
    out_path = os.path.join(OUT_DIR, f"zhou_walk_{idx:02d}.png")
    cv2.imwrite(out_path, canvas)
    out_imgs.append(canvas)
    # 白底预览
    rgba = cv2.cvtColor(canvas, cv2.COLOR_BGRA2RGBA)
    white = np.ones_like(rgba[:,:,:3], dtype=np.uint8) * 255
    alpha = rgba[:,:,3:4].astype(np.float32) / 255.0
    rgb = (rgba[:,:,:3].astype(np.float32) * alpha + white.astype(np.float32) * (1-alpha)).astype(np.uint8)
    out_imgs_white.append(rgb)
    print(f"  {f} -> zhou_walk_{idx:02d}.png  (crop={cw}x{ch}, placed at dst=({dst_x},{dst_y}))")

# GIF: 白底预览（重复 3 次）
def downscale(img, target_h=400):
    h, w = img.shape[:2]
    sc = target_h / h
    return cv2.resize(img, (int(w*sc), target_h))

# 重复 3 遍循环
preview_frames = [downscale(im) for im in out_imgs_white]
gif_white_path = os.path.join(GIF_DIR, "zhou_walk_FINAL_aligned_x3_12fps.gif")
imageio.mimsave(gif_white_path, preview_frames * 3, duration=1.0/12, loop=0)
print(f"\nwhite-bg preview: {gif_white_path}")

# 黑底版（更好看透明区）
out_imgs_black = []
for canvas in out_imgs:
    rgba = cv2.cvtColor(canvas, cv2.COLOR_BGRA2RGBA)
    black = np.zeros_like(rgba[:,:,:3], dtype=np.uint8)
    alpha = rgba[:,:,3:4].astype(np.float32) / 255.0
    rgb = (rgba[:,:,:3].astype(np.float32) * alpha + black.astype(np.float32) * (1-alpha)).astype(np.uint8)
    out_imgs_black.append(downscale(rgb))
gif_black_path = os.path.join(GIF_DIR, "zhou_walk_FINAL_aligned_blackbg_x3_12fps.gif")
imageio.mimsave(gif_black_path, out_imgs_black * 3, duration=1.0/12, loop=0)
print(f"black-bg preview: {gif_black_path}")

print(f"\n输出 8 帧对齐 PNG: {OUT_DIR}")
print(f"画布尺寸: {CW}x{CH}, 脚底统一={FOOT_Y}, 中心x统一={CENTER_X}")