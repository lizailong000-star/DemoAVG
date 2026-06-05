# ===== v2.2l 线索查看界面 =====
# v2.2r 新增 Clue Detail View（Phase 2A）
# 线索数据 + add_clue 函数已在 systems_clue.rpy 中定义

screen clue_test_screen():
    modal True
    zorder 200

    frame:
        xalign 0.5
        yalign 0.5
        background Solid("#000000EE")
        padding (50, 40)
        xmaximum 760
        vbox:
            spacing 12
            text "线索列表":
                size 36
                color "#FFD700"
                xalign 0.5
            null height 10
            if len(clue_list) == 0:
                text "（暂无线索）":
                    size 22
                    color "#888888"
                    xalign 0.5
            else:
                viewport:
                    xsize 660
                    ysize 420
                    mousewheel True
                    draggable True
                    vbox:
                        spacing 8
                        for _i, _c in enumerate(clue_list):
                            $ _title = _c.get("title", "未命名线索")
                            $ _category = _c.get("category", "未分类")
                            $ _source = _c.get("source", "未知")
                            $ _state = _c.get("state", "UNREAD")
                            $ _time = _c.get("time", "刚刚获得")
                            $ _important = bool(_c.get("is_important", False))
                            $ _star = "[[{color=#ffd700}★{/color}]] " if _important else "[[{color=#888888}★{/color}]] "
                            $ _line = str(_i + 1) + ". " + _star + _title
                            $ _cid = _c.get("id", None)
                            button:
                                background Solid("#1a1a1a")
                                hover_background Solid("#2a2a2a")
                                xsize 640
                                padding (12, 8)
                                action [Function(mark_clue_read, _cid), Show("clue_detail_screen", clue_index=_i)]
                                vbox:
                                    spacing 3
                                    text _line:
                                        size 22
                                        color "#FFFFFF"
                                    text ("分类：" + str(_category)):
                                        size 15
                                        color "#AAAAAA"
                                    text ("来源：" + str(_source)):
                                        size 15
                                        color "#AAAAAA"
                                    if _state == "READ":
                                        text "状态：{color=#66ff66}READ{/color}":
                                            size 15
                                            color "#AAAAAA"
                                    elif _state == "UNREAD":
                                        text "状态：{color=#ff6666}UNREAD{/color}":
                                            size 15
                                            color "#AAAAAA"
                                    elif _state == "IMPORTANT":
                                        text "状态：{color=#ffd700}IMPORTANT{/color}":
                                            size 15
                                            color "#AAAAAA"
                                    elif _state == "LOCKED":
                                        text "状态：{color=#888888}LOCKED{/color}":
                                            size 15
                                            color "#AAAAAA"
                                    elif _state == "ARCHIVED":
                                        text "状态：{color=#aaaaff}ARCHIVED{/color}":
                                            size 15
                                            color "#AAAAAA"
                                    else:
                                        text ("状态：" + str(_state)):
                                            size 15
                                            color "#AAAAAA"
                                    text ("时间：" + str(_time)):
                                        size 15
                                        color "#AAAAAA"
            null height 14
            text "点击线索查看详情  |  按 C / Esc / 右键 关闭":
                size 16
                color "#888888"
                xalign 0.5

    key "K_c" action Return()
    key "K_ESCAPE" action Return()
    key "mouseup_3" action Return()


# ===== v2.2r 线索详情页（Phase 2A）=====
# 入口：clue_test_screen 列表项点击 → Show("clue_detail_screen", clue_index=i)
# 返回：返回按钮 / ESC / 右键 → Hide("clue_detail_screen") + Show("clue_test_screen")

screen clue_detail_screen(clue_index=0):
    modal True
    zorder 210

    # 直接读 clue_list，不建第二套数据
    $ _idx = clue_index
    $ _total = len(clue_list)
    $ _safe = (0 <= _idx < _total)
    if _safe:
        $ _c = clue_list[_idx]
        $ _title = _c.get("title", "未命名线索")
        $ _desc = _c.get("desc", "（无描述）")
        $ _category = _c.get("category", "未分类")
        $ _source = _c.get("source", "未知")
        $ _state = _c.get("state", "UNREAD")
        $ _time = _c.get("time", "刚刚获得")
        $ _cid = _c.get("id", None)
        $ _important = bool(_c.get("is_important", False))
    else:
        $ _title = "（线索不存在）"
        $ _desc = ""
        $ _category = ""
        $ _source = ""
        $ _state = ""
        $ _time = ""
        $ _cid = None
        $ _important = False

    frame:
        xalign 0.5
        yalign 0.5
        background Solid("#000000EE")
        padding (50, 40)
        xmaximum 820
        vbox:
            spacing 14

            text "线索详情":
                size 28
                color "#FFD700"
                xalign 0.5
            null height 6

            text _title:
                size 32
                color "#FFFFFF"

            null height 6

            viewport:
                xsize 720
                ysize 260
                mousewheel True
                draggable True
                vbox:
                    spacing 6
                    text _desc:
                        size 20
                        color "#E0E0E0"

            null height 8

            text ("分类：" + str(_category)):
                size 18
                color "#AAAAAA"
            text ("来源：" + str(_source)):
                size 18
                color "#AAAAAA"
            if _state == "READ":
                text "状态：{color=#66ff66}READ{/color}":
                    size 18
                    color "#AAAAAA"
            elif _state == "UNREAD":
                text "状态：{color=#ff6666}UNREAD{/color}":
                    size 18
                    color "#AAAAAA"
            elif _state == "IMPORTANT":
                text "状态：{color=#ffd700}IMPORTANT{/color}":
                    size 18
                    color "#AAAAAA"
            elif _state == "LOCKED":
                text "状态：{color=#888888}LOCKED{/color}":
                    size 18
                    color "#AAAAAA"
            elif _state == "ARCHIVED":
                text "状态：{color=#aaaaff}ARCHIVED{/color}":
                    size 18
                    color "#AAAAAA"
            else:
                text ("状态：" + str(_state)):
                    size 18
                    color "#AAAAAA"
            text ("获得时间：" + str(_time)):
                size 18
                color "#AAAAAA"

            # v2.2t IMPORTANT 状态展示
            if _important:
                text "重要：{color=#ffd700}是 ★{/color}":
                    size 18
                    color "#AAAAAA"
            else:
                text "重要：否":
                    size 18
                    color "#AAAAAA"

            null height 14

            # v2.2t IMPORTANT 切换按钮：toggle + 重新 Show 自身刷新
            if _safe and _cid is not None:
                if _important:
                    textbutton "取消重要标记":
                        xalign 0.5
                        text_size 20
                        text_color "#FFFFFF"
                        text_hover_color "#FFD700"
                        background Solid("#553333")
                        hover_background Solid("#774444")
                        padding (20, 6)
                        action [Function(toggle_clue_important, _cid), Show("clue_detail_screen", clue_index=_idx)]
                else:
                    textbutton "标记为重要":
                        xalign 0.5
                        text_size 20
                        text_color "#FFFFFF"
                        text_hover_color "#FFD700"
                        background Solid("#335533")
                        hover_background Solid("#447744")
                        padding (20, 6)
                        action [Function(toggle_clue_important, _cid), Show("clue_detail_screen", clue_index=_idx)]

            null height 10

            textbutton "返回":
                xalign 0.5
                text_size 22
                text_color "#FFFFFF"
                text_hover_color "#FFD700"
                background Solid("#333333")
                hover_background Solid("#555555")
                padding (24, 8)
                action Hide("clue_detail_screen")

            text "按 Esc / 右键 返回列表":
                size 14
                color "#666666"
                xalign 0.5

    key "K_ESCAPE" action Hide("clue_detail_screen")
    key "mouseup_3" action Hide("clue_detail_screen")
