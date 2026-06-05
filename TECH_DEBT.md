# TECH_DEBT.md - 技术债清单

> 项目：《祝寿》Ren'Py DemoAVG 原型
> 最近更新：2026-05-29 14:33（Audit-03 建立）
> 用途：记录所有已知技术债，追踪到清零

---

| 编号 | 问题 | 现状 | 风险等级 | 解决方案 | 优先级 | 状态 |
|------|------|------|----------|----------|--------|------|
| TD-001 | 线索查看双 UI 并存 | `clue_log_screen`（systems_clue.rpy，v1.x 剧情用）和 `clue_test_screen`（clue_test.rpy，v2.2 探索用）功能重叠，两套并存 | 🟠 中 | 合并为统一线索查看 screen，保留一套，删另一套 | P1 | ⏳ 待处理 |
| TD-002 | 探索系统双系统并存 | v1.x 点击热区系统（room_explore_screen / activity_room_explore_screen / corridor_explore_screen）与 v2.2 RPG 探索系统（explore_scene_test）两套并存，玩家无法在两套之间无缝切换 | 🔴 高 | 决策：选一套为主，废弃或迁移另一套。v2.2 RPG 探索功能更完整，大概率以它为主，将 v1.x 剧情段迁移为 v2.2 热点 label | P0 | ⏳ 待决策 |
| TD-003 | 线索状态双轨管理 | v1.x 用 `clue_xxx_checked` 布尔变量追踪每个调查点是否已查看（如 `clue_banner_checked`、`clue_corridor_notice_checked`），v2.2 用 `clue_list` + `add_clue()` 集中管理。两套状态互不感知，同一线索可能被重复添加或遗漏 | 🟠 中 | 统一为 `clue_list` 单轨管理，`clue_xxx_checked` 布尔变量改为从 `clue_list` 派生查询（`any(c["id"]=="xxx" for c in clue_list)`），或直接废弃布尔变量 | P1 | ⏳ 待处理 |
| TD-004 | 文本速度双配置冲突 | `config.default_text_cps = 7`（只设默认值）+ `init 999 python: _preferences.text_cps = 7`（强压玩家偏好）。后者确保开发期生效，但正式版会覆盖玩家的自定义速度设置 | 🟡 低 | 正式版上线前移除 `init 999` 那行，只保留 `config.default_text_cps`；或在设置菜单里开放文字速度选项让玩家自己调 | P2 | ⏳ 待处理 |
| TD-005 | explore_scene.rpy 持续膨胀 | 单文件已达 12,218 字节，包含：场景参数 / 状态变量 / 热点数据 / 移动逻辑 / 热点检测 / 事件分发 / Label 调用 / 探索 screen / 测试 label。随着场景和热点增多还会继续增长 | 🟠 中 | 按职责拆分：`systems_explore_core.rpy`（参数/状态/移动/检测）、`systems_explore_event.rpy`（事件分发/Label调用）、`explore_scenes/`（各场景的热点数据和 screen）、`explore_test.rpy`（测试 label） | P1 | ⏳ 待处理 |

| TD-006 | 对话控制栏方案失败 | v2.2m 尝试了三种方案均失败：（1）直接复制 SDK screens.rpy → 与 gui.rpy 系统性不兼容（缺 gui.nvl_list_length / gui.scale 等）；（2）custom_screens.rpy 替换 quick_menu → NameError: quick_menu not defined；（3）最小 dialog_controls.rpy overlay → ShowMenu("history") 报 LabelNotFound，Skip 狂闪，UI 层级混乱。根因：项目缺少 screens.rpy 源文件，SDK 编译默认 screen 的 label/入口名与 ShowMenu 调用方式不匹配，overlay 与 explore modal 冲突 | 🔴 高 | 先做 UI 架构设计（screens.rpy 源文件恢复方案 + overlay/modal 层级规划 + screen 命名规范），再开发对话控制功能。不要在当前阶段硬接 | P1 | ⏳ 暂缓 |

---

## 技术债统计

- 总计：6 条
- 🔴 高风险：2 条（TD-002 / TD-006）
- 🟠 中风险：3 条（TD-001 / TD-003 / TD-005）
- 🟡 低风险：1 条（TD-004）
- 已清零：0 条

---

## 新增技术债入口

发现新的技术债时，按以下格式追加到上方表格：

```
| TD-NNN | 简述 | 现状 | 风险等级 | 解决方案 | 优先级 | 状态 |
```

编号规则：TD-NNN，NNN 三位递增。

---

## 清零流程

1. 标记状态为 `🔧 处理中`
2. 完成后在行尾标注 `✅ 已清零（版本号/日期）`
3. 保留已清零行（不删除），作为历史记录
