# ===== 系统：线索记录 =====
# 跨所有章节通用的线索数据 + 添加/统计函数 + 弹窗 screen

default clue_list = []

init python:
    CLUE_STATE_LOCKED = "LOCKED"
    CLUE_STATE_UNREAD = "UNREAD"
    CLUE_STATE_READ = "READ"
    CLUE_STATE_IMPORTANT = "IMPORTANT"
    CLUE_STATE_ARCHIVED = "ARCHIVED"

    def get_current_clue_time():
        # v2.2u: 系统真实时间，格式 MM-DD HH:MM（如 06-02 18:35）
        # 后续 Clue / Objective / Event Log 统一采用该格式
        import datetime
        return datetime.datetime.now().strftime("%m-%d %H:%M")

    def normalize_clue_state(state):
        valid_states = [
            CLUE_STATE_LOCKED,
            CLUE_STATE_UNREAD,
            CLUE_STATE_READ,
            CLUE_STATE_IMPORTANT,
            CLUE_STATE_ARCHIVED,
        ]
        if state in valid_states:
            return state
        return CLUE_STATE_UNREAD

    def add_clue(clue_id, title, desc, category="未分类", source="未知", state=CLUE_STATE_UNREAD, clue_time=None, is_important=False):
        # 兼容旧三参数调用：add_clue(clue_id, title, desc)
        # v2.2p: 扩展 category/source/state/time
        # v2.2t: 扩展 is_important（独立字段，与 state 解耦）
        # 重复 clue_id 不重复添加。
        if any(c["id"] == clue_id for c in clue_list):
            return False

        if clue_time is None:
            clue_time = get_current_clue_time()

        clue_list.append({
            "id": clue_id,
            "title": title,
            "desc": desc,
            "category": category,
            "source": source,
            "state": normalize_clue_state(state),
            "time": clue_time,
            "is_important": bool(is_important),
        })
        return True

    def get_clue_count():
        return len(clue_list)

    def mark_clue_read(clue_id):
        # v2.2s Phase 2B: 把指定线索状态从 UNREAD 改为 READ。
        # - 第一次打开详情页时调用
        # - 已经是 READ / IMPORTANT / ARCHIVED 不变
        # - LOCKED 不打开详情（详情页层面拦截，本函数不主动转换）
        # 注意：必须返回 None，否则在 SL button action 列表里会被 Ren'Py
        # 当成"interaction 结果"，导致父 menu screen 提前 Return（v2.2s 踩坑）
        for c in clue_list:
            if c["id"] == clue_id:
                if c.get("state") == CLUE_STATE_UNREAD:
                    c["state"] = CLUE_STATE_READ
                break
        return None

    # ===== v2.2t Phase 2C: IMPORTANT 标记系统 =====
    # 与 state 完全解耦的独立字段 is_important（bool）。
    # 4 个接口全部安全：未知 clue_id 不报错；全部 return None（v2.2s 教训 #27）。

    def _find_clue(clue_id):
        try:
            for c in clue_list:
                if c.get("id") == clue_id:
                    return c
        except Exception:
            pass
        return None

    def check_clue_important(clue_id):
        c = _find_clue(clue_id)
        if c is None:
            return False
        return bool(c.get("is_important", False))

    def mark_clue_important(clue_id):
        c = _find_clue(clue_id)
        if c is None:
            return None
        c["is_important"] = True
        return None

    def unmark_clue_important(clue_id):
        c = _find_clue(clue_id)
        if c is None:
            return None
        c["is_important"] = False
        return None

    def toggle_clue_important(clue_id):
        c = _find_clue(clue_id)
        if c is None:
            return None
        c["is_important"] = not bool(c.get("is_important", False))
        return None

screen clue_log_screen():

    modal True

    frame at soft_fade_in:
        xalign 0.5
        yalign 0.5
        xsize 820
        ysize 520
        background Solid("#111111")
        padding (24, 20)

        vbox:
            spacing 14

            text "线索记录" size 30 color "#ffcc66" xalign 0.5

            if not clue_list:
                text "尚未获得线索。" size 20 color "#ffffff" xalign 0.5
            else:
                viewport:
                    xsize 760
                    ysize 360
                    mousewheel True
                    draggable True

                    vbox:
                        spacing 12
                        for clue in clue_list:
                            frame:
                                background Solid("#222222")
                                padding (14, 10)
                                vbox:
                                    spacing 6
                                    text clue["title"] size 22 color "#66ccff"
                                    text clue["desc"] size 18 color "#ffffff"

            textbutton "关闭":
                xalign 0.5
                background Solid("#333333")
                hover_background Solid("#555555")
                text_color "#ffffff"
                text_hover_color "#ffcc66"
                action Hide("clue_log_screen")
