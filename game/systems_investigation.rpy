# ===== v2.3 Investigation System MVP =====
# 调查目标系统基础设施。
#
# 设计依据：INVESTIGATION_SYSTEM_DESIGN.md / FRAMEWORK_SPEC.md
#
# 数据：
#   objective_data           - dict: id -> objective dict
#   current_objective_id     - 当前 ACTIVE 高亮目标
#   objective_state_map      - dict: id -> state（冗余快速查询）
#   objective_history        - list: 状态变更历史 [(id, new_state, when_str), ...]
#
# 状态：LOCKED / ACTIVE / COMPLETED / FAILED / HIDDEN / OPTIONAL
# 本轮实际使用：LOCKED / ACTIVE / COMPLETED
#
# 重要原则：
# - 所有函数对未注册 objective_id 必须安全返回 None / False，不得 KeyError。
# - 状态变更后必须调用 check_objective_conditions() 触发依赖目标激活/完成扫描。
# - 接口供 button.action 链 Function() 调用时，必须 return None（v2.2s 教训 #27）。
# - init python 块在 default 变量提升之前执行，访问全局 default 必须走 store.xxx（不能裸名）。

default objective_data = {}
default current_objective_id = None
default objective_state_map = {}
default objective_history = []

init python:
    OBJ_STATE_LOCKED = "LOCKED"
    OBJ_STATE_ACTIVE = "ACTIVE"
    OBJ_STATE_COMPLETED = "COMPLETED"
    OBJ_STATE_FAILED = "FAILED"
    OBJ_STATE_HIDDEN = "HIDDEN"
    OBJ_STATE_OPTIONAL = "OPTIONAL"

    def _obj_log(objective_id, new_state):
        try:
            store.objective_history.append((objective_id, new_state, "刚刚"))
        except Exception:
            pass

    def has_objective(objective_id):
        try:
            return objective_id in store.objective_data
        except Exception:
            return False

    def get_objective_state(objective_id):
        if not has_objective(objective_id):
            return None
        return store.objective_data[objective_id].get("state")

    def get_current_objective():
        try:
            cid = store.current_objective_id
        except Exception:
            cid = None
        if cid and has_objective(cid):
            return store.objective_data[cid]
        return None

    def _set_obj_state(objective_id, new_state):
        # 内部辅助：纯粹改 state + 同步 map + 写 history；不触发条件扫描，避免递归。
        if not has_objective(objective_id):
            return False
        obj = store.objective_data[objective_id]
        if obj.get("state") == new_state:
            return False
        obj["state"] = new_state
        store.objective_state_map[objective_id] = new_state
        _obj_log(objective_id, new_state)
        return True

    def register_objective(objective_id, title, desc, activation_rule=None, completion_rule=None, linked_clues=None, linked_flags=None, linked_scene=None):
        # 注册一个调查目标。重复 id 不覆盖，安全跳过。
        try:
            if objective_id in store.objective_data:
                return None
        except Exception:
            return None
        store.objective_data[objective_id] = {
            "id": objective_id,
            "title": title,
            "desc": desc,
            "state": OBJ_STATE_LOCKED,
            "activation_rule": activation_rule or {"type": "manual"},
            "completion_rule": completion_rule or {"type": "manual"},
            "linked_clues": list(linked_clues) if linked_clues else [],
            "linked_flags": list(linked_flags) if linked_flags else [],
            "linked_scene": linked_scene,
        }
        store.objective_state_map[objective_id] = OBJ_STATE_LOCKED
        return None

    def activate_objective(objective_id):
        if not has_objective(objective_id):
            return None
        state = get_objective_state(objective_id)
        if state in (OBJ_STATE_COMPLETED, OBJ_STATE_FAILED):
            return None
        if state == OBJ_STATE_ACTIVE:
            return None
        _set_obj_state(objective_id, OBJ_STATE_ACTIVE)
        try:
            store.current_objective_id = objective_id
        except Exception:
            pass
        return None

    def complete_objective(objective_id):
        if not has_objective(objective_id):
            return None
        state = get_objective_state(objective_id)
        if state in (OBJ_STATE_COMPLETED, OBJ_STATE_FAILED):
            return None
        _set_obj_state(objective_id, OBJ_STATE_COMPLETED)
        try:
            if store.current_objective_id == objective_id:
                store.current_objective_id = None
        except Exception:
            pass
        return None

    def fail_objective(objective_id):
        if not has_objective(objective_id):
            return None
        state = get_objective_state(objective_id)
        if state in (OBJ_STATE_COMPLETED, OBJ_STATE_FAILED):
            return None
        _set_obj_state(objective_id, OBJ_STATE_FAILED)
        try:
            if store.current_objective_id == objective_id:
                store.current_objective_id = None
        except Exception:
            pass
        return None

    # ===== 条件检查器 =====

    def _has_clue(clue_id):
        try:
            for c in store.clue_list:
                if c.get("id") == clue_id:
                    return True
        except Exception:
            pass
        return False

    def _has_flag(flag_id):
        # Flag System 未正式建立时，安全返回 False（不抛错）。
        try:
            flag_map = getattr(store, "flag_map", None)
            if flag_map is None:
                return False
            return bool(flag_map.get(flag_id, False))
        except Exception:
            return False

    def _objective_completed(objective_id):
        return get_objective_state(objective_id) == OBJ_STATE_COMPLETED

    def _eval_condition(cond):
        if cond is None:
            return False
        ctype = cond.get("type") if isinstance(cond, dict) else None
        if ctype == "manual":
            return False
        if ctype == "clue":
            return _has_clue(cond.get("clue_id"))
        if ctype == "flag":
            return _has_flag(cond.get("flag_id"))
        if ctype == "objective_completed":
            return _objective_completed(cond.get("objective_id"))
        if ctype == "and":
            subs = cond.get("conditions", []) or []
            if not subs:
                return False
            for s in subs:
                if not _eval_condition(s):
                    return False
            return True
        if ctype == "or":
            subs = cond.get("conditions", []) or []
            if not subs:
                return False
            for s in subs:
                if _eval_condition(s):
                    return True
            return False
        return False

    def check_objective_conditions():
        # 扫描所有目标：
        # - LOCKED 且满足 activation_rule → activate_objective
        # - ACTIVE 且满足 completion_rule → complete_objective
        # 多扫几遍直到稳定（避免一次扫不出连锁激活）。
        try:
            ids = list(store.objective_data.keys())
        except Exception:
            ids = []
        for _pass in range(8):
            changed = False
            for oid in ids:
                state = get_objective_state(oid)
                if state == OBJ_STATE_LOCKED:
                    rule = store.objective_data[oid].get("activation_rule")
                    if rule and rule.get("type") != "manual":
                        if _eval_condition(rule):
                            activate_objective(oid)
                            changed = True
                elif state == OBJ_STATE_ACTIVE:
                    rule = store.objective_data[oid].get("completion_rule")
                    if rule and rule.get("type") != "manual":
                        if _eval_condition(rule):
                            complete_objective(oid)
                            changed = True
            if not changed:
                break
        return None
