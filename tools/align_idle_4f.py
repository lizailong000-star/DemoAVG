# -*- coding: utf-8 -*-
"""
对齐 4 张 idle PNG：用与 walk 同样的策略
- 取 4 张 alpha union bbox 作固定窗口
- 不做位置归零（已对齐画布）
- 输出到 zhou_idle_v2_aligned
"""
import os, cv2, numpy as np, imageio.v2 as imageio

IN_DIR = r"D:\renpy-8.5.3\DemoAVG\game\images\player\zhou_idle_v2_raw"
OUT_DIR = r"D:\renpy-8.5.3\DemoAVG\game\images\player\zhou_idle_v2_aligned"
GIF_DIR = r"D:\renpy-8.5.3\DemoAVG\tools\output"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(GIF_DIR, exist_ok=True)

files = sorted([f for f in os.listdir(IN_DIR) if f.startswith("zhou_idle_raw_") and f.endswith(".png")])
print(f"found {len(files)} files: {files}")

imgs = []
bboxes = []
for f in files:
    img = cv2.imread(os.path.join(IN_DIR, f), cv2.IMREAD_UNCHANGED)
    alpha = img[:, :, 3]
    ys, xs = np.where(alpha > 0)
    bbox = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
    bboxes.append(bbox)
    imgs.append(img)
    print(f"  {f}: bbox={bbox}")

ux1 = min(b[0] for b in bboxes)
uy1 = min(b[1] for b in bboxes)
ux2 = max(b[2] for b in bboxes)
uy2 = max(b[3] for b in bboxes)
PAD = 20
H = imgs[0].shape[0]; W = imgs[0].shape[1]
cx1 = max(0, ux1-PAD); cy1 = max(0, uy1-PAD)
cx2 = min(W, ux2+PAD); cy2 = min(H, uy2+PAD)
CW = cx2-cx1; CH = cy2-cy1
print(f"\nUnion bbox: ({ux1},{uy1})-({ux2},{uy2})")
print(f"Final crop window: ({cx1},{cy1})-({cx2},{cy2}) = {CW}x{CH}")

for f in os.listdir(OUT_DIR):
    os.remove(os.path.join(OUT_DIR, f))

out_imgs = []
out_imgs_white = []
for f, img in zip(files, imgs):
    crop = img[cy1:cy2, cx1:cx2].copy()
    # 从文件名取序号：zhou_idle_raw_NN_fXX.png
    parts = f.split("_")
    idx = int(parts[3])
    out_path = os.path.join(OUT_DIR, f"zhou_idle_{idx:02d}.png")
    cv2.imwrite(out_path, crop)
    out_imgs.append(crop)
    rgba = cv2.cvtColor(crop, cv2.COLOR_BGRA2RGBA)
    alpha = rgba[:,:,3:4].astype(np.float32) / 255.0
    white = np.ones_like(rgba[:,:,:3], dtype=np.uint8) * 255
    rgb = (rgba[:,:,:3].astype(np.float32)*alpha + white.astype(np.float32)*(1-alpha)).astype(np.uint8)
    out_imgs_white.append(rgb)
    print(f"  {f} -> zhou_idle_{idx:02d}.png ({CW}x{CH})")

# 预览 GIF（呼吸节奏更慢，0.4s/帧）
def downscale(img, target_h=400):
    h, w = img.shape[:2]
    sc = target_h / h
    return cv2.resize(img, (int(w*sc), target_h))

preview = [downscale(im) for im in out_imgs_white]
gif_path = os.path.join(GIF_DIR, "zhou_idle_FINAL_aligned_x3.gif")
imageio.mimsave(gif_path, preview * 3, duration=0.4, loop=0)
print(f"\npreview GIF: {gif_path}")
print(f"\n输出位置: {OUT_DIR}")
print(f"画布: {CW}x{CH}")