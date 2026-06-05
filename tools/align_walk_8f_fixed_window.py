# -*- coding: utf-8 -*-
"""
正确的对齐方式：
- 8 张图都是 1254x1254 同画布，人物绝对位置已正确
- 只需取所有 alpha bbox 的 union 当固定窗口
- 所有帧用同一个窗口裁，保留人物在画面里的真实相对位置
- 不做"居中"，不做"脚底对齐"，因为原视频本身就是稳定的
"""
import os, cv2, numpy as np, imageio.v2 as imageio

IN_DIR = r"D:\renpy-8.5.3\DemoAVG\game\images\player\zhou_walk_v2_raw"
OUT_DIR = r"D:\renpy-8.5.3\DemoAVG\game\images\player\zhou_walk_v2_aligned"
GIF_DIR = r"D:\renpy-8.5.3\DemoAVG\tools\output"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(GIF_DIR, exist_ok=True)

files = sorted([f for f in os.listdir(IN_DIR) if f.startswith("zhou_walk_raw_") and f.endswith(".png")])
print(f"found {len(files)} files")

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

# Union bbox
ux1 = min(b[0] for b in bboxes)
uy1 = min(b[1] for b in bboxes)
ux2 = max(b[2] for b in bboxes)
uy2 = max(b[3] for b in bboxes)
print(f"\nUnion bbox: ({ux1},{uy1})-({ux2},{uy2}) = {ux2-ux1}x{uy2-uy1}")

# 加 padding
PAD = 20
H = imgs[0].shape[0]; W = imgs[0].shape[1]
cx1 = max(0, ux1 - PAD)
cy1 = max(0, uy1 - PAD)
cx2 = min(W, ux2 + PAD)
cy2 = min(H, uy2 + PAD)
CW = cx2 - cx1; CH = cy2 - cy1
print(f"Final crop window: ({cx1},{cy1})-({cx2},{cy2}) = {CW}x{CH}")

# 删旧的居中版输出
for f in os.listdir(OUT_DIR):
    os.remove(os.path.join(OUT_DIR, f))

out_imgs = []
out_imgs_white = []
out_imgs_black = []
for f, img in zip(files, imgs):
    crop = img[cy1:cy2, cx1:cx2].copy()  # 直接固定窗口裁，零调整
    idx = int(f.split("_")[3])
    out_path = os.path.join(OUT_DIR, f"zhou_walk_{idx:02d}.png")
    cv2.imwrite(out_path, crop)
    out_imgs.append(crop)
    # 预览（白底/黑底）
    rgba = cv2.cvtColor(crop, cv2.COLOR_BGRA2RGBA)
    alpha = rgba[:,:,3:4].astype(np.float32) / 255.0
    white = np.ones_like(rgba[:,:,:3], dtype=np.uint8) * 255
    rgb_w = (rgba[:,:,:3].astype(np.float32)*alpha + white.astype(np.float32)*(1-alpha)).astype(np.uint8)
    black = np.zeros_like(rgba[:,:,:3], dtype=np.uint8)
    rgb_b = (rgba[:,:,:3].astype(np.float32)*alpha + black.astype(np.float32)*(1-alpha)).astype(np.uint8)
    out_imgs_white.append(rgb_w)
    out_imgs_black.append(rgb_b)
    print(f"  {f} -> zhou_walk_{idx:02d}.png ({CW}x{CH})")

# 缩到 400 高生成预览 GIF
def downscale(img, target_h=400):
    h, w = img.shape[:2]
    sc = target_h / h
    return cv2.resize(img, (int(w*sc), target_h))

preview_w = [downscale(im) for im in out_imgs_white]
preview_b = [downscale(im) for im in out_imgs_black]

gif_w = os.path.join(GIF_DIR, "zhou_walk_FIXED_window_white_x3_12fps.gif")
gif_b = os.path.join(GIF_DIR, "zhou_walk_FIXED_window_black_x3_12fps.gif")
imageio.mimsave(gif_w, preview_w * 3, duration=1.0/12, loop=0)
imageio.mimsave(gif_b, preview_b * 3, duration=1.0/12, loop=0)
print(f"\npreview white: {gif_w}")
print(f"preview black: {gif_b}")

print(f"\n输出位置: {OUT_DIR}")
print(f"画布: {CW}x{CH} (统一固定窗口，无对齐变形)")