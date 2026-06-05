# ===== v2.2h RPG 热点交互（E 键触发）fix =====
# 历史：v2.2a 视差 / v2.2b 热点 / v2.2c 角色中心 / v2.2d 点击寻路 / v2.2e 状态朝向 / v2.2f 提示 / v2.2g 标记 / v2.2h E 交互

# ----- 场景参数 -----
default EXPLORE_SCENE_WIDTH = 2089
default EXPLORE_SCREEN_WIDTH = 1280
default EXPLORE_SCREEN_HEIGHT = 720
default EXPLORE_MAX_CAMERA_X = EXPLORE_SCENE_WIDTH - EXPLORE_SCREEN_WIDTH

# ----- 状态变量 -----
default explore_camera_x = 0
default player_world_x = 300
default player_y = 660
default target_x = 300
default player_speed = 5
default player_zoom = 0.30

# ===== v3.0d 镜头运镜（Camera Polish）=====
# explore_camera_x_smooth: 平滑过渡的相机 x（实际用于渲染），跟 target 缓动
default explore_camera_x_smooth = 0.0
# camera_dead_zone_half: 角色在屏幕中心 ±N 内时相机不动（死区半宽）
default camera_dead_zone_half = 120
# camera_lerp: 相机缓动系数（0~1，越小越懒）
default camera_lerp = 0.12
# camera_breath_time: 镜头呼吸累积时间
default camera_breath_t = 0.0
# camera_breath_amplitude: 镜头呼吸偏移幅度（像素）
default camera_breath_amp = 2.0
# camera_breath_period: 呼吸周期（秒）
default camera_breath_period = 5.0

# v2.2e 状态/朝向
default player_state = "idle"
default player_facing = "right"

# v2.2f/h 热点（存 dict 或 None）
default current_hotspot = None

# v2.2h 交互
default last_hotspot_action = ""
default hotspot_action_cooldown = 0

# v2.2i 事件分发
default last_event = ""
default event_popup_text = ""
default event_popup_time = 0.0

default explore_feedback_text = ""
default show_explore_hotspots = False

# ----- 周卫国探索形态动画 -----
# v3.0c idle 呼吸：只用 2 帧序列帧切换（已包含视频里真实呼吸），不再叠加 transform 浮动
transform zhou_idle_breath:
    yoffset 0

image zhou_explore_idle:
    "images/player/zhou/zhou_explore_idle_v2_01.png"
    1.4
    "images/player/zhou/zhou_explore_idle_v2_02.png"
    1.4
    repeat

image zhou_explore_walk:
    "images/player/zhou/zhou_explore_walk_v2_01.png"
    0.11
    "images/player/zhou/zhou_explore_walk_v2_02.png"
    0.11
    "images/player/zhou/zhou_explore_walk_v2_03.png"
    0.11
    "images/player/zhou/zhou_explore_walk_v2_04.png"
    0.11
    "images/player/zhou/zhou_explore_walk_v2_05.png"
    0.11
    "images/player/zhou/zhou_explore_walk_v2_06.png"
    0.11
    "images/player/zhou/zhou_explore_walk_v2_07.png"
    0.11
    "images/player/zhou/zhou_explore_walk_v2_08.png"
    0.11
    repeat

init python:
    hotspot_data = [
        {"id": "gate",           "name": "养老院大门", "world_x": 420,  "radius": 80, "action_label": None, "event": "event_gate",          "label": "test_gate"},
        {"id": "notice_board",   "name": "公告栏",     "world_x": 860,  "radius": 80, "action_label": None, "event": "event_notice_board",  "label": "test_notice_board"},
        {"id": "security_room",  "name": "保安室",     "world_x": 1320, "radius": 80, "action_label": None, "event": "event_security_room", "label": "test_security_room"},
        {"id": "to_lobby",       "name": "进入大厅",   "world_x": 1700, "radius": 80, "action_label": None, "event": "event_lobby",         "label": "scene_lobby"},
    ]

    def _eclamp(v, lo, hi):
        return max(lo, min(v, hi))

    def explore_update_camera():
        # v3.0d 升级：死区 + 缓动
        # 1. 计算 target_camera_x：角色相对相机的偏移在死区内则不动；超出死区只移动超出量
        char_screen_x = store.player_world_x - store.explore_camera_x_smooth
        screen_center = store.EXPLORE_SCREEN_WIDTH / 2
        offset_from_center = char_screen_x - screen_center

        target_camera = store.explore_camera_x_smooth
        if offset_from_center > store.camera_dead_zone_half:
            # 角色越过右死区，相机向右补偿
            target_camera += offset_from_center - store.camera_dead_zone_half
        elif offset_from_center < -store.camera_dead_zone_half:
            # 角色越过左死区，相机向左补偿
            target_camera += offset_from_center + store.camera_dead_zone_half

        # 钳制到合法范围
        target_camera = _eclamp(target_camera, 0, store.EXPLORE_MAX_CAMERA_X)

        # 2. 平滑缓动到 target
        store.explore_camera_x_smooth += (target_camera - store.explore_camera_x_smooth) * store.camera_lerp

        # 3. 镜头呼吸：累积时间产生轻微 x 偏移（不影响逻辑判定）
        import math
        store.camera_breath_t += 0.03  # 跟 timer tick 同步
        breath_offset = math.sin(store.camera_breath_t * 2 * math.pi / store.camera_breath_period) * store.camera_breath_amp

        # 4. 最终用于渲染的 explore_camera_x（含呼吸）
        store.explore_camera_x = _eclamp(int(store.explore_camera_x_smooth + breath_offset), 0, store.EXPLORE_MAX_CAMERA_X)

    def explore_check_hotspot():
        best = None
        best_dist = 999999
        for h in hotspot_data:
            dist = abs(store.player_world_x - h["world_x"])
            if dist <= h["radius"] and dist < best_dist:
                best = h
                best_dist = dist
        old_id = store.current_hotspot["id"] if store.current_hotspot else None
        new_id = best["id"] if best else None
        if old_id != new_id:
            store.current_hotspot = best
            renpy.restart_interaction()

    def explore_move_tick():
        if store.hotspot_action_cooldown > 0:
            store.hotspot_action_cooldown -= 1

        # 事件弹窗倒计时
        if store.event_popup_time > 0:
            store.event_popup_time -= 0.03
            if store.event_popup_time <= 0:
                store.event_popup_time = 0
                store.event_popup_text = ""
                renpy.restart_interaction()

        # v3.0d: 每 tick 推进相机（即使角色不动也要更新呼吸）
        explore_update_camera()

        diff = store.target_x - store.player_world_x
        if abs(diff) <= store.player_speed:
            if store.player_world_x != store.target_x:
                store.player_world_x = store.target_x
                explore_update_camera()
                explore_check_hotspot()
            if store.player_state != "idle":
                store.player_state = "idle"
                renpy.restart_interaction()
            return
        direction = 1 if diff > 0 else -1
        new_x = _eclamp(
            store.player_world_x + direction * store.player_speed,
            40,
            store.EXPLORE_SCENE_WIDTH - 40
        )
        if new_x != store.player_world_x:
            store.player_world_x = new_x
            store.player_facing = "right" if direction > 0 else "left"
            store.player_state = "walking"
            explore_update_camera()
            explore_check_hotspot()
            renpy.restart_interaction()
        else:
            if store.player_state != "idle":
                store.player_state = "idle"
                store.target_x = store.player_world_x
                explore_check_hotspot()
                renpy.restart_interaction()

    def explore_click_move():
        mx, _ = renpy.get_mouse_pos()
        new_target = _eclamp(
            store.explore_camera_x + mx,
            40,
            store.EXPLORE_SCENE_WIDTH - 40
        )
        if abs(new_target - store.player_world_x) <= 3:
            store.target_x = store.player_world_x
            store.player_state = "idle"
        else:
            store.target_x = new_target
            store.player_state = "walking"
            store.player_facing = "left" if new_target < store.player_world_x else "right"
        renpy.restart_interaction()

    def trigger_hotspot_event(event_id):
        # v2.2i 事件分发器
        msg = ""
        if event_id == "event_gate":
            msg = "这里是养老院大门。"
        elif event_id == "event_notice_board":
            msg = "公告栏贴着很多旧通知。"
        elif event_id == "event_security_room":
            msg = "里面似乎有人值班。"
        else:
            msg = "未知事件：" + str(event_id)
        store.last_event = event_id
        store.event_popup_text = msg
        store.event_popup_time = 2.0
        renpy.notify(msg)
        renpy.restart_interaction()

    def trigger_hotspot_label(label_name):
        # v2.2j 事件 → Label 调用
        # v2.2k：scene_xxx 类 label 走 jump（跨场景），其余走 call_in_new_context（剧情段）
        if not label_name:
            return
        if not renpy.has_label(label_name):
            renpy.notify("Label 不存在：" + str(label_name))
            return
        store.last_event = "label:" + str(label_name)
        if label_name.startswith("scene_"):
            # 场景切换：直接 jump 退出当前 screen 流，由目标 label 全权接管
            store.current_scene_id = "transitioning"
            renpy.jump(label_name)
        else:
            # 普通剧情段：开 new context，结束后自动回探索
            renpy.call_in_new_context(label_name)
            renpy.restart_interaction()

    def explore_cancel_movement():
        # v2.2q: 热点交互前打断当前寻路。把 target_x 拉到当前 player_world_x，并设为 idle。
        store.target_x = store.player_world_x
        if store.player_state != "idle":
            store.player_state = "idle"
        renpy.restart_interaction()

    def explore_press_e():
        if store.current_hotspot is None:
            return
        if store.hotspot_action_cooldown > 0:
            return
        store.hotspot_action_cooldown = 15

        # v2.2q: 触发热点事件前，先打断当前移动；事件结束后不再续走旧目标。
        explore_cancel_movement()

        hid = store.current_hotspot["id"]
        hname = store.current_hotspot["name"]
        label_name = store.current_hotspot.get("label", None)
        event_id = store.current_hotspot.get("event", None)
        print("[hotspot_action] triggered: " + str(hid) + " -> label=" + str(label_name) + " event=" + str(event_id))
        store.last_hotspot_action = "Action: " + str(hid) + " triggered"
        # 优先走 label，没有则 fallback 到事件分发
        if label_name:
            trigger_hotspot_label(label_name)
        elif event_id:
            trigger_hotspot_event(event_id)
        else:
            renpy.notify("查看：" + str(hname))
        renpy.restart_interaction()

screen explore_scene_test():
    modal True

    timer 0.03 repeat True action Function(explore_move_tick)

    # ===== 视差四层（v3.0d 养老院大门场景 0.1/0.4/0.7/1.0）=====
    add "images/scene_yangloiyuan/bg_far_yangloiyuan.png"  at Transform(xpos=int(-explore_camera_x * 0.1), ypos=0)
    add "images/scene_yangloiyuan/bg_mid_yangloiyuan.png"  at Transform(xpos=int(-explore_camera_x * 0.4), ypos=0)
    add "images/scene_yangloiyuan/bg_near_yangloiyuan.png" at Transform(xpos=int(-explore_camera_x * 0.7), ypos=0)

    # ===== 天气层（Reserved，v3.0d 预留 Environment FX 接口，当前空实现）=====
    use weather_layer

    # ===== 热点显示（v3.0d 改造：仅在范围内显示，高亮提示框）=====
    # 旧规则：所有热点常显 ?/★，文字提示
    # 新规则：角色未进入范围 = 不显示；进入范围 = 热点上方弹出高亮提示框 + "按 E"
    for _h in hotspot_data:
        $ _in_range = abs(player_world_x - _h["world_x"]) <= _h["radius"]
        if _in_range:
            $ _hint_screen_x = int(_h["world_x"] - explore_camera_x)
            $ _hint_name = _h["name"]
            # 头顶提示框（在 ypos 280 高度处弹出）
            frame:
                background Solid("#000000CC")
                padding (16, 8)
                xpos _hint_screen_x
                ypos 280
                xanchor 0.5
                yanchor 1.0
                vbox:
                    spacing 4
                    text _hint_name:
                        size 20
                        color "#FFFFFF"
                        xalign 0.5
                        outlines [(2, "#000000", 0, 0)]
                    text "按 E 探索":
                        size 14
                        color "#FFD700"
                        xalign 0.5
                        outlines [(1, "#000000", 0, 0)]
            # 提示框下方小三角箭头（指向热点位置）
            text "▼":
                size 18
                color "#FFD700"
                xpos _hint_screen_x - 9
                ypos 282
                outlines [(2, "#000000", 0, 0)]

    # ===== 角色 =====
    # v3.0c: 替换 walk 为视频提取版（zhou_walk_v2_aligned）+ 启用 walking 状态切换
    #        walk 资源：8 帧 458x955 透明 PNG，循环帧 138-188（无缝循环）
    #        idle 仍用旧资源 + zhou_idle_breath transform
    $ _player_xzoom = -player_zoom if player_facing == "left" else player_zoom
    $ _player_image = "zhou_explore_walk" if player_state == "walking" else "zhou_explore_idle"
    $ _player_transform = zhou_idle_breath if player_state == "idle" else None
    if _player_transform:
        add _player_image at Transform(xpos=int(player_world_x - explore_camera_x), ypos=player_y + 8, xanchor=0.5, yanchor=1.0, xzoom=_player_xzoom, yzoom=player_zoom), _player_transform
    else:
        add _player_image at Transform(xpos=int(player_world_x - explore_camera_x), ypos=player_y + 8, xanchor=0.5, yanchor=1.0, xzoom=_player_xzoom, yzoom=player_zoom)

    # ===== 视差第 4 层：前景 fore（在角色之上，可遮挡角色）=====
    add "images/scene_yangloiyuan/bg_fore_yangloiyuan.png" at Transform(xpos=int(-explore_camera_x * 1.0), ypos=0)

    # ===== 角色头顶状态标签 =====
    $ _state_color = "#00FF00" if player_state == "walking" else "#CCCCCC"
    text "[player_state] / [player_facing]":
        size 16
        color _state_color
        xpos int(player_world_x - explore_camera_x - 40)
        ypos player_y - 200
        outlines [(2, "#000000", 0, 0)]

    # ===== 角色头顶热点提示（v3.0d 移到热点上方框，这里去掉重复提示）=====
    # 原 ★ 按 E 查看：xxx 提示已迁移到热点物体上方的高亮框

    # ===== 目标点视觉标记 =====
    add Solid("#FF0000CC", xysize=(12, 12)) at Transform(xpos=int(target_x - explore_camera_x - 6), ypos=player_y + 8)

    # ===== v2.2i 屏幕中央事件弹窗 =====
    if event_popup_text != "":
        frame:
            xalign 0.5
            yalign 0.4
            background Solid("#000000DD")
            padding (40, 30)
            xmaximum 900
            text event_popup_text:
                size 32
                color "#FFFFFF"
                xalign 0.5
                outlines [(3, "#000000", 0, 0)]

    # ===== UI 调试 HUD =====
    frame:
        xpos 20
        ypos 15
        background Solid("#000000AA")
        padding (12, 8)
        vbox:
            spacing 2
            text "点击场景走过去 | 靠近热点按 E 交互 | Esc/右键 退出":
                size 18 color "#ffffff"
            $ _psx = player_world_x - explore_camera_x
            text "world_x=[player_world_x]  target_x=[target_x]  screen_x=[_psx]  camera_x=[explore_camera_x]":
                size 16 color "#FFD700"
            text "state=[player_state]  facing=[player_facing]":
                size 16 color "#00FF00"
            $ _hs_name = current_hotspot["name"] if current_hotspot else "None"
            $ _hs_id = current_hotspot["id"] if current_hotspot else "-"
            text "hotspot=" + _hs_name + "  id=" + _hs_id:
                size 16 color "#FF8800"
            if last_hotspot_action != "":
                text last_hotspot_action:
                    size 16 color "#00FFFF"
            if last_event != "":
                $ _le = "Last Event: " + last_event
                text _le:
                    size 16 color "#FF66CC"
            $ _cs = "Current Scene: " + current_scene_id
            text _cs:
                size 16 color "#AAAAFF"
            $ _cc = "Clues: " + str(len(clue_list))
            text _cc:
                size 16 color "#FFAAFF"
            text "按 C 查看线索":
                size 14 color "#CCCCCC"

    # ===== 鼠标点击移动 =====
    key "mousedown_1" action Function(explore_click_move)

    # ===== E 键交互 =====
    key "K_e" action Function(explore_press_e)

    # ===== C 键打开线索列表 =====
    key "K_c" action ShowMenu("clue_test_screen")

    # ===== O 键打开调查目标页 (v2.3) =====
    key "K_o" action ShowMenu("investigation_test_screen")

    # ===== 退出 =====
    key "K_ESCAPE" action Return()
    key "mouseup_3" action Return()

label test_v22_explore:
    $ explore_camera_x = 0
    $ explore_camera_x_smooth = 0.0
    $ camera_breath_t = 0.0
    $ player_world_x = 300
    $ target_x = 300
    $ player_speed = 5
    $ player_zoom = 0.30
    $ player_y = 660
    $ player_state = "idle"
    $ player_facing = "right"
    $ current_hotspot = None
    $ last_hotspot_action = ""
    $ last_event = ""
    $ event_popup_text = ""
    $ event_popup_time = 0.0
    $ hotspot_action_cooldown = 0
    $ explore_feedback_text = ""
    $ show_explore_hotspots = False
    $ current_scene_id = "explore"
    # v2.3 Investigation MVP: 进入探索前确保测试目标已注册（幂等）
    call register_test_objectives
    $ explore_update_camera()
    call screen explore_scene_test
    return

label test_v22_rpg_click:
    jump test_v22_explore
