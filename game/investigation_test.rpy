# ===== v2.3 Investigation MVP 测试目标与目标页面 =====
# 注册三个测试目标 + 提供 investigation_test_screen（O 键打开）
#
# 注意：register_objective 不能放 init python，因为 start 新游戏时 default 会重置 store，
# 导致 init 阶段填的数据被冲掉。改成 label，由 test_v22_explore 入口调用。
# register_objective 自带"重复 id 跳过"，多次调用安全幂等。

label register_test_objectives:
    python:
        register_objective(
            objective_id="obj_notice_board",
            title="查看公告栏",
            desc="先去公告栏看一眼，那里通常贴着养老院的日常通知。",
            activation_rule={"type": "manual"},
            completion_rule={"type": "clue", "clue_id": "notice_old"},
            linked_clues=["notice_old"],
        )
        register_objective(
            objective_id="obj_security_room",
            title="调查保安室",
            desc="公告栏看完后，去保安室找些值班记录。",
            activation_rule={"type": "objective_completed", "objective_id": "obj_notice_board"},
            completion_rule={"type": "clue", "clue_id": "security_note"},
            linked_clues=["security_note"],
        )
        register_objective(
            objective_id="obj_enter_lobby",
            title="进入大厅",
            desc="完成前期调查后，进入大厅。",
            activation_rule={"type": "objective_completed", "objective_id": "obj_security_room"},
            completion_rule={"type": "manual"},
        )

        # 默认激活第一个目标（已激活则 no-op）
        activate_objective("obj_notice_board")

        # 立刻扫一次，确保依赖目标在已满足条件时也正确激活/完成
        check_objective_conditions()
    return


# ===== Investigation 目标页面 =====
# v2.3a 升级为目标列表页：
# - 复用现有 investigation_test_screen（不重命名，保留 explore_scene.rpy 的 ShowMenu 引用）
# - 顶部当前目标高亮（保留）
# - 4 段分组：ACTIVE / COMPLETED / LOCKED / FAILED
# - 每条目标项加状态色块 [★]：ACTIVE绿 / COMPLETED 浅蓝绿 / LOCKED 灰 / FAILED 红
# - desc 显示策略：ACTIVE/COMPLETED/FAILED 显示；LOCKED 隐藏（保留悬念）
# - 关闭：Return()（v2.2s #29 ShowMenu 规范）
# - 严格只读：渲染期不调用副作用（v2.2s #27）

screen investigation_test_screen():
    modal True
    zorder 220

    # 渲染期只读：不要在这里做副作用调用
    $ _cur = get_current_objective()
    $ _active_list = [o for o in objective_data.values() if o.get("state") == "ACTIVE"]
    $ _completed_list = [o for o in objective_data.values() if o.get("state") == "COMPLETED"]
    $ _locked_list = [o for o in objective_data.values() if o.get("state") == "LOCKED"]
    $ _failed_list = [o for o in objective_data.values() if o.get("state") == "FAILED"]

    frame:
        xalign 0.5
        yalign 0.5
        background Solid("#000000EE")
        padding (40, 30)
        xmaximum 820
        ymaximum 640
        vbox:
            spacing 12
            text "调查目标":
                size 32
                color "#FFD700"
                xalign 0.5
            null height 6

            # 当前目标
            if _cur is None:
                text "当前目标：{color=#888888}（无）{/color}":
                    size 20
                    color "#FFFFFF"
            else:
                $ _cur_title = _cur.get("title", "")
                text ("当前目标：{color=#66ffcc}" + str(_cur_title) + "{/color}"):
                    size 20
                    color "#FFFFFF"

            null height 8

            viewport:
                xsize 740
                ysize 440
                mousewheel True
                draggable True
                vbox:
                    spacing 10

                    # ACTIVE
                    text "{color=#66ff66}ACTIVE{/color}":
                        size 22
                    if len(_active_list) == 0:
                        text "  （暂无）":
                            size 16
                            color "#888888"
                    else:
                        for _o in _active_list:
                            $ _t = _o.get("title", "")
                            $ _d = _o.get("desc", "")
                            vbox:
                                spacing 2
                                text ("  [[{color=#66ff66}★{/color}]] " + str(_t)):
                                    size 18
                                    color "#FFFFFF"
                                text ("    " + str(_d)):
                                    size 14
                                    color "#AAAAAA"

                    null height 6
                    # COMPLETED
                    text "{color=#66ffcc}COMPLETED{/color}":
                        size 22
                    if len(_completed_list) == 0:
                        text "  （暂无）":
                            size 16
                            color "#888888"
                    else:
                        for _o in _completed_list:
                            $ _t = _o.get("title", "")
                            $ _d = _o.get("desc", "")
                            vbox:
                                spacing 2
                                text ("  [[{color=#66ffcc}★{/color}]] " + str(_t)):
                                    size 18
                                    color "#AAAAAA"
                                text ("    " + str(_d)):
                                    size 14
                                    color "#777777"

                    null height 6
                    # LOCKED（隐藏 desc，保留悬念）
                    text "{color=#888888}LOCKED{/color}":
                        size 22
                    if len(_locked_list) == 0:
                        text "  （暂无）":
                            size 16
                            color "#888888"
                    else:
                        for _o in _locked_list:
                            $ _t = _o.get("title", "")
                            text ("  [[{color=#888888}★{/color}]] " + str(_t)):
                                size 18
                                color "#666666"

                    if len(_failed_list) > 0:
                        null height 6
                        text "{color=#ff6666}FAILED{/color}":
                            size 22
                        for _o in _failed_list:
                            $ _t = _o.get("title", "")
                            $ _d = _o.get("desc", "")
                            vbox:
                                spacing 2
                                text ("  [[{color=#ff6666}★{/color}]] " + str(_t)):
                                    size 18
                                    color "#AA6666"
                                text ("    " + str(_d)):
                                    size 14
                                    color "#774444"

            null height 10
            textbutton "关闭":
                xalign 0.5
                text_size 20
                text_color "#FFFFFF"
                text_hover_color "#FFD700"
                background Solid("#333333")
                hover_background Solid("#555555")
                padding (22, 6)
                action Return()

            text "O / Esc / 右键 关闭":
                size 13
                color "#666666"
                xalign 0.5

    key "K_o" action Return()
    key "K_ESCAPE" action Return()
    key "mouseup_3" action Return()
