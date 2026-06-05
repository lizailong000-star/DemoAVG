# -*- coding: utf-8 -*-
"""
extract_hotspots_from_mask.py
v3.0e-mask-pipeline-pre

从 hotspots_<scene>.png mask 图中解析热点数据。

用法：
    python tools/extract_hotspots_from_mask.py \
        --mask game/images/scene_yangloiyuan/hotspots_yangloiyuan.png \
        --reference game/images/scene_yangloiyuan/bg_near_yangloiyuan.png \
        --scene yangloiyuan

输出：
    tools/output/hotspots_<scene>_report.json
    tools/output/hotspots_<scene>_debug.png

颜色映射（当前硬编码养老院大门，未来可改 JSON 配置）：
    #FF0000 -> gate
    #00FF00 -> notice_board
    #0000FF -> security_room
    #FFFF00 -> to_lobby
"""

import os
import sys
import json
import argparse
import cv2
import numpy as np

# ===== 颜色映射（按场景维护，后续可外置 JSON）=====
SCENE_COLOR_MAP = {
    "yangloiyuan": {
        (0, 0, 255): "gate",            # OpenCV 是 BGR：#FF0000 -> (0,0,255)
        (0, 255, 0): "notice_board",    # #00FF00
        (255, 0, 0): "security_room",   # #0000FF
        (0, 255, 255): "to_lobby",      # #FFFF00
    }
}

# Debug 颜色（BGR）用于在 debug 图上画 bbox/label
DEBUG_DRAW_COLOR = {
    "gate": (0, 0, 255),
    "notice_board": (0, 255, 0),
    "security_room": (255, 0, 0),
    "to_lobby": (0, 255, 255),
}

MIN_AREA_PX = 500


def hex_from_bgr(b, g, r):
    return f"#{r:02X}{g:02X}{b:02X}"


def parse_mask(mask_path, ref_path, scene):
    errors = []
    warnings = []

    # ----- 读 mask -----
    mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
    if mask is None:
        return None, [f"cannot read mask: {mask_path}"], []

    if mask.ndim != 3 or mask.shape[2] != 4:
        errors.append(f"mask must be RGBA (4-channel), got shape={mask.shape}")

    mh, mw = mask.shape[:2]

    # ----- 读 reference（bg_near）-----
    ref_size = None
    if ref_path and os.path.exists(ref_path):
        ref = cv2.imread(ref_path, cv2.IMREAD_UNCHANGED)
        if ref is not None:
            ref_size = (ref.shape[1], ref.shape[0])
            if (mw, mh) != ref_size:
                errors.append(
                    f"mask size {mw}x{mh} != reference bg_near size {ref_size[0]}x{ref_size[1]}"
                )
    else:
        warnings.append(f"reference bg_near not provided or missing: {ref_path}")

    if errors:
        return None, errors, warnings

    color_map = SCENE_COLOR_MAP.get(scene)
    if color_map is None:
        return None, [f"unknown scene: {scene}, no color map registered"], warnings

    bgr = mask[:, :, :3]
    alpha = mask[:, :, 3]

    # 找所有 alpha > 0 的像素的颜色
    visible = alpha > 0
    unique_colors = set()
    if visible.any():
        flat = bgr[visible].reshape(-1, 3)
        for c in np.unique(flat, axis=0):
            unique_colors.add(tuple(int(x) for x in c))

    # 校验未知颜色
    known_colors = set(color_map.keys())
    unknown_colors = unique_colors - known_colors
    if unknown_colors:
        for c in sorted(unknown_colors):
            warnings.append(f"unknown color in mask: BGR={c}, hex={hex_from_bgr(*c)}")

    hotspots = []
    used_color_ids = set()

    # 用于检测重叠
    accumulated_mask = np.zeros((mh, mw), dtype=np.uint8)

    for color, hid in color_map.items():
        # 严格匹配该颜色 + alpha>0
        target_b, target_g, target_r = color
        mask_color = (
            (bgr[:, :, 0] == target_b)
            & (bgr[:, :, 1] == target_g)
            & (bgr[:, :, 2] == target_r)
            & visible
        ).astype(np.uint8) * 255

        area = int((mask_color > 0).sum())
        if area == 0:
            warnings.append(f"hotspot color {hex_from_bgr(*color)} -> {hid}: not found in mask")
            continue

        if area < MIN_AREA_PX:
            warnings.append(
                f"hotspot {hid} area too small: {area}px (threshold {MIN_AREA_PX})"
            )

        # bbox
        ys, xs = np.where(mask_color > 0)
        x1, y1, x2, y2 = int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())

        # 重心（用 OpenCV moments）
        m = cv2.moments(mask_color)
        if m["m00"] > 0:
            cx = int(m["m10"] / m["m00"])
            cy = int(m["m01"] / m["m00"])
        else:
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # 检测重叠
        overlap = (accumulated_mask > 0) & (mask_color > 0)
        if overlap.any():
            warnings.append(
                f"hotspot {hid} overlaps with previous hotspot(s) at {int(overlap.sum())}px"
            )

        accumulated_mask = np.maximum(accumulated_mask, mask_color)

        hotspots.append(
            {
                "id": hid,
                "color_hex": hex_from_bgr(*color),
                "bbox": [x1, y1, x2, y2],
                "center_x": cx,
                "center_y": cy,
                "top_y": y1,
                "bottom_y": y2,
                "area_px": area,
            }
        )
        used_color_ids.add(hid)

    return {
        "scene": scene,
        "mask_size": [mw, mh],
        "reference_size": list(ref_size) if ref_size else None,
        "hotspot_count": len(hotspots),
        "hotspots": hotspots,
    }, errors, warnings


def render_debug(mask_path, ref_path, report, out_path):
    """生成 debug 图：bg_near + bbox + label。"""
    if not os.path.exists(ref_path):
        # 找不到 ref 用 mask 自身的 BGR 当背景
        img = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
        bg = img[:, :, :3].copy()
    else:
        bg = cv2.imread(ref_path).copy()

    for h in report["hotspots"]:
        x1, y1, x2, y2 = h["bbox"]
        color = DEBUG_DRAW_COLOR.get(h["id"], (255, 255, 255))
        cv2.rectangle(bg, (x1, y1), (x2, y2), color, 3)
        cv2.circle(bg, (h["center_x"], h["center_y"]), 8, color, -1)
        label = f"{h['id']} ({h['color_hex']})"
        cv2.putText(
            bg,
            label,
            (x1, max(20, y1 - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2,
            cv2.LINE_AA,
        )

    cv2.imwrite(out_path, bg)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mask", required=True, help="path to hotspots mask png")
    parser.add_argument(
        "--reference", default=None, help="path to bg_near reference png (for size check)"
    )
    parser.add_argument(
        "--scene", required=True, help="scene id, must match SCENE_COLOR_MAP key"
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="output dir, default: <project>/tools/output",
    )
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = args.out_dir or os.path.join(script_dir, "output")
    os.makedirs(out_dir, exist_ok=True)

    print(f"[INFO] mask: {args.mask}")
    print(f"[INFO] reference: {args.reference}")
    print(f"[INFO] scene: {args.scene}")
    print()

    report, errors, warnings = parse_mask(args.mask, args.reference, args.scene)

    if errors:
        print("===== ERRORS =====")
        for e in errors:
            print(f"  [X] {e}")
        sys.exit(1)

    if warnings:
        print("===== WARNINGS =====")
        for w in warnings:
            print(f"  [!] {w}")
        print()

    print("===== REPORT =====")
    print(f"scene: {report['scene']}")
    print(f"mask size: {report['mask_size']}")
    print(f"reference size: {report['reference_size']}")
    print(f"hotspot count: {report['hotspot_count']}")
    print()
    for h in report["hotspots"]:
        print(
            f"  - {h['id']:15s} color={h['color_hex']}  "
            f"bbox={h['bbox']}  center=({h['center_x']},{h['center_y']})  "
            f"top_y={h['top_y']}  bottom_y={h['bottom_y']}  area={h['area_px']}px"
        )

    # 写 JSON
    json_path = os.path.join(out_dir, f"hotspots_{args.scene}_report.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n[OK] report saved: {json_path}")

    # 渲染 debug 图
    debug_path = os.path.join(out_dir, f"hotspots_{args.scene}_debug.png")
    render_debug(args.mask, args.reference, report, debug_path)
    print(f"[OK] debug image: {debug_path}")


if __name__ == "__main__":
    main()
