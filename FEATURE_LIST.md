# FEATURE_LIST.md - 功能清单

> 项目：《祝寿》DemoAVG 原型
> 最近更新：2026-05-29 14:05

---

| 模块 | 功能 | 引入版本 | 状态 | 所在文件 | 测试通过 | working 锁定 |
|------|------|----------|------|----------|----------|-------------|
| UI 系统 | Character callback 头像联动 | v2.1 | ✅ 完成 | systems_ui.rpy | ✅ 是 | v2.1_ui_base_locked |
| UI 系统 | overlay screen 头像框显示 | v2.1 | ✅ 完成 | systems_ui.rpy | ✅ 是 | v2.1_ui_base_locked |
| UI 系统 | dialog_box.png 对话框底板 | v2.1d | ✅ 完成 | systems_ui.rpy | ✅ 是 | v2.1_ui_base_locked |
| UI 系统 | E 键全局 dismiss（对话推进） | v2.2l | ✅ 完成 | systems_ui.rpy | ✅ 是 | v2.2l_clue_system_working |
| UI 系统 | 文本打字机效果（7 cps） | v2.2l.1 | ✅ 完成 | systems_ui.rpy | ✅ 是 | v2.2l1_text_cps_working |
| 探索系统 | 三层视差场景（远 0.2 / 中 0.5 / 近 1.0） | v2.2a | ✅ 完成 | explore_scene.rpy | ✅ 是 | v2.2d_rpg_click_move_working |
| 探索系统 | RPG 点击寻路（鼠标点击 + 平滑移动） | v2.2d | ✅ 完成 | explore_scene.rpy | ✅ 是 | v2.2d_rpg_click_move_working |
| 探索系统 | 镜头跟随 + 边界停镜 | v2.2d | ✅ 完成 | explore_scene.rpy | ✅ 是 | v2.2d_rpg_click_move_working |
| 探索系统 | 角色状态机 idle / walking | v2.2e | ✅ 完成 | explore_scene.rpy | ✅ 是 | v2.2e_player_state_facing_working |
| 探索系统 | 角色朝向 left / right + xzoom 镜像 | v2.2e | ✅ 完成 | explore_scene.rpy | ✅ 是 | v2.2e_player_state_facing_working |
| 探索系统 | 热点提示（靠近 → ★ 按 E 查看：xxx） | v2.2f | ✅ 完成 | explore_scene.rpy | ✅ 是 | v2.2f_hotspot_hint_working |
| 探索系统 | 热点可视化标记（世界坐标 ? / ★） | v2.2g | ✅ 完成 | explore_scene.rpy | ✅ 是 | v2.2g_hotspot_marker_working |
| 探索系统 | E 键交互（占位 action + HUD 反馈） | v2.2h | ✅ 完成 | explore_scene.rpy | ✅ 是 | v2.2h_hotspot_interact_working |
| 探索系统 | 事件分发器（trigger_hotspot_event + 中央弹窗） | v2.2i | ✅ 完成 | explore_scene.rpy | ✅ 是 | v2.2i_event_dispatcher_working |
| 探索系统 | Label 调用系统（call_in_new_context） | v2.2j | ✅ 完成 | explore_scene.rpy | ✅ 是 | v2.2j_label_event_working |
| 探索系统 | 场景切换（scene_xxx → renpy.jump） | v2.2k | ✅ 完成 | explore_scene.rpy / scene_test.rpy | ✅ 是 | v2.2k_scene_transition_working |
| 线索系统 | 线索数据管理（clue_list + add_clue） | v1.x | ✅ 完成 | systems_clue.rpy | ✅ 是 | v1.9_pre_avatar_system |
| 线索系统 | 线索查看 UI（clue_log_screen） | v1.x | ✅ 完成 | systems_clue.rpy | ✅ 是 | v1.9_pre_avatar_system |
| 线索系统 | 探索内 C 键线索表（clue_test_screen） | v2.2l | ✅ 完成 | clue_test.rpy | ✅ 是 | v2.2l_clue_system_working |
| 线索系统 | 测试剧情段接入 add_clue | v2.2l | ✅ 完成 | event_test.rpy | ✅ 是 | v2.2l_clue_system_working |
| 剧情系统 | Chapter 01 雨夜出租屋（4 热点 + 电话事件） | v0.7~v0.9 | ✅ 完成 | script.rpy | ✅ 是 | v0.9_visual_feedback_working |
| 剧情系统 | Chapter 01 养老院活动室（4 热点 + 结局转场） | v1.5 | ✅ 完成 | activity_room.rpy | ✅ 是 | v1.5_activity_room_working |
| 剧情系统 | Chapter 02 养老院走廊（4 热点 + 结尾） | v1.8 | ✅ 完成 | chapter_02_corridor.rpy | ✅ 是 | v1.8_chapter02_corridor_working |
| 剧情系统 | Chapter 01 结尾转场 screen | v1.6 | ✅ 完成 | chapter_end.rpy | ✅ 是 | v1.6_chapter_end_working |

---

### 备注

- v2.2 探索系统与 v1.x 点击热区系统是**两套并行系统**，尚未合并
- v2.2 探索入口是 `test_v22_explore`，v1.x 剧情入口是 `chapter_01_start`
- 线索查看有两套 UI：`clue_log_screen`（v1.x 剧情）和 `clue_test_screen`（v2.2 探索），功能重叠
