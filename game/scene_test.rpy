# ===== v2.2k 场景切换系统测试场景 =====

# 当前场景状态（探索/大厅）
default current_scene_id = "explore"

# 大厅占位背景
image bg_lobby_placeholder = Solid("#3A2E5F", xysize=(1280, 720))

label scene_lobby:
    $ current_scene_id = "lobby"
    $ complete_objective("obj_enter_lobby")
    $ check_objective_conditions()
    scene bg_lobby_placeholder
    with dissolve

    "【测试大厅】"
    "这是场景 B。"
    "里面什么都没有，只是用来验证场景切换。"

    menu:
        "返回探索场景":
            jump back_to_explore
        "再看一眼":
            "你又转了一圈，确实什么都没有。"
            jump back_to_explore

label back_to_explore:
    $ current_scene_id = "explore"
    # v2.3 修复：返回探索前把 scene 切回黑底，避免大厅紫底残留漏到线索/调查页背景
    scene black
    jump test_v22_explore
