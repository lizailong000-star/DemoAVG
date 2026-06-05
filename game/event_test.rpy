# ===== v2.2j 事件 → Label 测试入口 =====
# ===== v2.2l 线索接入（用 systems_clue.rpy 的 add_clue）=====

label test_gate:
    "【测试】这里是养老院大门。"
    "门口的铁栏锈迹斑斑，挂着一块木牌。"
    $ add_clue("duty_table", "养老院值班表", "门口木牌上贴着的旧值班安排。", category="地点", source="养老院大门")
    "获得线索：养老院值班表"
    return

label test_notice_board:
    "【测试】公告栏贴着很多旧通知。"
    "纸张已经发黄，字迹有些模糊。"
    $ add_clue("notice_old", "旧通知", "公告栏上一张发黄的旧通知。", category="文件", source="公告栏")
    "获得线索：旧通知"
    $ check_objective_conditions()
    return

label test_security_room:
    "【测试】里面似乎有人值班。"
    "窗户里透出一点光，听得到收音机的声音。"
    $ add_clue("security_note", "保安记录", "保安室窗台留下的值班记录。", category="地点", source="保安室")
    "获得线索：保安记录"
    $ check_objective_conditions()
    return
