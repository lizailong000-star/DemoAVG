# -*- coding: utf-8 -*-
"""
基于已验证的无缝循环 138-188 (50帧)，抽取 8 帧 / 12 帧做 sprite 预览。
- 同样的固定 crop 窗口
- 同样的循环起点
- 输出 sprite 预览 GIF + 单帧 PNG（供后续接 Ren'Py）
"""
import os, numpy as np, cv2, imageio.v2 as imageio

VIDEO = r"D:\下龙虾下载\1123.mp4"
OUT_DIR = r"D:\renpy-8.5.3\DemoAVG\tools\output"
SPRITE_DIR_8 = r"D:\renpy-8.5.3\DemoAVG\game\images\player\zhou_walk_v2_8f"
SPRITE_DIR_12 = r"D:\renpy-8.5.3\DemoAVG\game\images\player\zhou_walk_v2_12f"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(SPRITE_DIR_8, exist_ok=True)
os.makedirs(SPRITE_DIR_12, exist_ok=True)

cap = cv2.VideoCapture(VIDEO)
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frames_all = []
for _ in range(total):
    ok, img = cap.read()
    if ok: frames_all.append(img)
cap.release()

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

# 用 130~195 的 union 作为固定 crop（包含最佳循环点 138-188）
bboxes = [find_bbox(frames_all[i], bg_color) for i in range(130, 195)]
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
print(f"crop: {CW}x{CH}, range:({CROP_X1},{CROP_Y1})-({CROP_X2},{CROP_Y2})")

# 抽帧策略：等间距，去掉末帧（因为末帧=首帧位置）
LOOP_START = 138
LOOP_END = 188
LOOP_LEN = LOOP_END - LOOP_START  # 50

def pick_indices(n):
    """从 LOOP_START 开始等间距抽 n 帧，末帧不到 LOOP_END（留给循环）"""
    step = LOOP_LEN / n
    return [LOOP_START + int(round(step * i)) for i in range(n)]

indices_8 = pick_indices(8)
indices_12 = pick_indices(12)
print(f"8-frame: {indices_8}")
print(f"12-frame: {indices_12}")

def render_to_alpha(img):
    """返回 BGRA 透明 PNG 和 白底 RGB 预览"""
    sub = img[CROP_Y1:CROP_Y2, CROP_X1:CROP_X2]
    diff = np.abs(sub.astype(np.int16) - bg_color.reshape(1,1,3)).sum(axis=2)
    mask = (diff > 30).astype(np.uint8) * 255
    kernel = np.ones((4,4), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    bgra = cv2.cvtColor(sub, cv2.COLOR_BGR2BGRA)
    bgra[:,:,3] = mask
    # 白底预览
    rgba = cv2.cvtColor(bgra, cv2.COLOR_BGRA2RGBA)
    white = np.ones_like(rgba[:,:,:3], dtype=np.uint8) * 255
    alpha = rgba[:,:,3:4].astype(np.float32) / 255.0
    rgb = (rgba[:,:,:3].astype(np.float32)*alpha + white.astype(np.float32)*(1-alpha)).astype(np.uint8)
    return bgra, rgb

def save_sprite_set(indices, sprite_dir, tag):
    bgras = []
    rgbs = []
    for idx, frame_i in enumerate(indices, start=1):
        bgra, rgb = render_to_alpha(frames_all[frame_i])
        # 保存透明 PNG（原始尺寸，供接 Ren'Py 时再缩放）
        out_png = os.path.join(sprite_dir, f"zhou_walk_{idx:02d}.png")
        cv2.imwrite(out_png, bgra)
        bgras.append(bgra)
        rgbs.append(rgb)
        print(f"  {tag} frame {idx:02d} (src={frame_i}) -> {out_png}")
    # 生成预览 GIF：缩放到 400 高，重复 3 遍看循环
    scale = 400.0 / CH
    rgbs_small = [cv2.resize(r, (int(CW*scale), 400)) for r in rgbs]
    gif_path = os.path.join(OUT_DIR, f"zhou_walk_SPRITE_{tag}_x3_12fps.gif")
    imageio.mimsave(gif_path, rgbs_small * 3, duration=1.0/12, loop=0)
    print(f"  preview GIF: {gif_path}")
    return gif_path

print("\n=== 8-frame sprite ===")
save_sprite_set(indices_8, SPRITE_DIR_8, "8f")

print("\n=== 12-frame sprite ===")
save_sprite_set(indices_12, SPRITE_DIR_12, "12f")

print(f"\nSprite PNG specs (原始未缩放):")
print(f"  size: {CW}x{CH}")
print(f"  transparent alpha mask")
print(f"  filenames: zhou_walk_01.png ~ zhou_walk_NN.png")
print(f"\n出图位置:")
print(f"  8 帧: {SPRITE_DIR_8}")
print(f"  12 帧: {SPRITE_DIR_12}")
print(f"  预览 GIF: {OUT_DIR}\\zhou_walk_SPRITE_*_x3_12fps.gif")