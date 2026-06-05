# ===== 系统：通用 UI 与占位图层 =====
# 跨所有章节通用的 transform 与占位 image

# ----- transform -----

transform hover_pulse:
    on hover:
        linear 0.12 xzoom 1.03 yzoom 1.03
    on idle:
        linear 0.12 xzoom 1.0 yzoom 1.0

transform soft_fade_in:
    alpha 0.0
    linear 0.2 alpha 1.0

# ----- 通用占位图层 -----

image bg_room_dark = Solid("#1a1c22", xysize=(1280, 720))

# ----- 真实场景背景图 -----

image bg_rainy_room = "images/bg/bg_room_rainy.png"
image bg_activity_room = "images/bg/bg_activity_room.png"
image bg_corridor = "images/bg/bg_corridor.png"

# ----- 占位立绘与 UI 图层 -----

image char_placeholder = Solid("#222222", xysize=(420, 720))
image phone_off = Solid("#0a0a0a", xysize=(80, 140))
image phone_on = Solid("#e8f0ff", xysize=(80, 140))
image phone_ring_flash = Solid("#ffcc66", xysize=(80, 140))
image black_overlay = Solid("#000000", xysize=(1280, 720))
image phone_glow_strong = Solid("#f4f8ff", xysize=(90, 150))

# v2.0 art asset definitions
image bg_rainy_room_art = "images/bg/bg_room_rainy.png"
image bg_activity_room_art = "images/bg/bg_activity_room.png"
image bg_corridor_art = "images/bg/bg_corridor.png"

image zhou_weiguo_neutral = "images/character/zhou_weiguo_neutral.png"
image woman_staff_neutral = "images/character/woman_staff_neutral.png"

# ===== v2.1c 周卫国头像 callback + overlay =====

default current_dialog_avatar = None

# v2.2o: Hide UI 状态变量
default dialogue_ui_hidden = False

init -10 python:
    hide_ui_style_backup = {}

    def dialog_avatar_zhou(event, interact=True, **kwargs):
        if event == "begin":
            store.current_dialog_avatar = "zhou"
            renpy.restart_interaction()
        elif event == "end":
            store.current_dialog_avatar = None
            renpy.restart_interaction()

    def dialog_avatar_none(event, interact=True, **kwargs):
        if event == "begin":
            store.current_dialog_avatar = None
            renpy.restart_interaction()

    # v2.2o: Hide UI 切换函数
    def toggle_hide_ui():
        store.dialogue_ui_hidden = not store.dialogue_ui_hidden

        # 首次切换时记录原始样式，恢复时按备份还原，避免写死后续 UI 调整值。
        if not hide_ui_style_backup:
            hide_ui_style_backup["say_window_background"] = style.say_window.background
            hide_ui_style_backup["say_dialogue_color"] = style.say_dialogue.color
            hide_ui_style_backup["say_dialogue_outlines"] = style.say_dialogue.outlines
            hide_ui_style_backup["say_dialogue_size"] = style.say_dialogue.size

        if store.dialogue_ui_hidden:
            store.dialogue_text_alpha = 0.0
            style.say_window.background = None
            style.say_dialogue.color = "#00000000"
            style.say_dialogue.outlines = []
            # 双保险：某些默认 say screen 不立即吃 color，压到 1px 确保视觉隐藏。
            style.say_dialogue.size = 1
        else:
            store.dialogue_text_alpha = 1.0
            style.say_window.background = hide_ui_style_backup["say_window_background"]
            style.say_dialogue.color = hide_ui_style_backup["say_dialogue_color"]
            style.say_dialogue.outlines = hide_ui_style_backup["say_dialogue_outlines"]
            style.say_dialogue.size = hide_ui_style_backup["say_dialogue_size"]

        # 动态修改 style 后必须 rebuild，否则 say text 可能继续沿用旧渲染属性。
        renpy.style.rebuild()
        renpy.restart_interaction()

init python:
    if "avatar_dialog_overlay" not in config.overlay_screens:
        config.overlay_screens.append("avatar_dialog_overlay")

    # v2.2o: Hide UI 功能逻辑保留，但快捷键入口暂时禁用。
    # 未来恢复 H 键时，重新 append "hide_ui_controller" 即可。
    # if "hide_ui_controller" not in config.overlay_screens:
    #     config.overlay_screens.append("hide_ui_controller")

    # Ren'Py 默认 H 键会触发 hide_windows；这里在项目内禁用默认 H，避免绕过自定义绑定。
    for _h_key in ("noshift_K_h", "K_h"):
        if _h_key in config.keymap.get("hide_windows", []):
            config.keymap["hide_windows"].remove(_h_key)

screen avatar_dialog_overlay():
    zorder 50

    # v2.2o: Hide UI 时隐藏头像
    if not dialogue_ui_hidden and current_dialog_avatar == "zhou":
        fixed:
            xpos 20
            ypos 540

            add "images/avatar_alpha/zhou_neutral.png":
                xysize (140, 140)
                xpos 10
                ypos 10

            add "images/ui/frame_avatar.png":
                xysize (160, 160)
                xpos 0
                ypos 0

# v2.2o: Hide UI 控制器
# 捕获 H 键切换 UI 显示
# 探索场景下，explore_scene_test 是 modal screen 且 zorder 低，自身吞掉 H 键
# 此 overlay 只在普通剧情时生效（modal screen 会拦截输入到自身，H 键到不了 overlay）
screen hide_ui_controller():
    zorder 200

    # v2.2o: 快捷键暂时禁用；保留 screen 和 toggle_hide_ui()，未来可直接恢复。
    # key "K_h" action Function(toggle_hide_ui)

# ===== v2.1d 对话框底板接入 =====
init 20 python:
    style.say_window.background = Frame("images/ui/dialog_box.png", 60, 60)
    style.say_window.xalign = 0.5
    style.say_window.yalign = 1.0
    style.say_window.xsize = 760
    style.say_window.ysize = 120
    style.say_window.xpadding = 40
    style.say_window.ypadding = 20

    style.say_dialogue.xpos = 170
    style.say_dialogue.xmaximum = 560
    style.say_dialogue.ypos = 20

# ===== v2.2l E 键推进对话 =====
init python:
    # E 键 = 点击/回车，在对话和 menu 中推进文本
    config.keymap["dismiss"].append("K_e")

# ===== v2.2l.1 文本打字机效果 =====
# config.default_text_cps 只是默认值；如果玩家偏好里 text_cps 不是 0，会被覆盖
# 强制把 preferences.text_cps 也设上，确保生效
define config.default_text_cps = 7

init 999 python:
    _preferences.text_cps = 7
