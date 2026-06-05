# POLISH_AUDIT.md - 功能完善阶段系统审计

> 项目：《祝寿》Ren'Py DemoAVG 原型
> 审计基线版本：**v2.2o**（DemoAVG_backup_v2.2o_hide_ui_disable_key_working）
> 最近更新：2026-06-02 09:06

---

## 一、系统完成度总表

| 系统 | 完成度 % | 是否达到 95% | 是否允许进入下一功能 | 可接剧情 | 缺失/待完善 |
|------|----------|--------------|----------------------|----------|-------------|
| 对话系统 | 60% | 否 | 否 | 否 | 自动播放、跳过、快进、历史记录、文本速度调节、UI 按钮 |
| UI 系统 | 70% | 否 | 否 | 基本可用 | 快进按钮、自动播放按钮、线索按钮、HUD 优化 |
| 探索系统 | 97% | 是 | 是 | 可用 | Frozen；最新 Working：v2.2q_move_interrupt_on_hotspot_working；剩余 polish：HUD 优化、路径指示视效 |
| 场景系统 | 40% | 否 | 否 | 否 | 场景状态保存、角色位置保存、热点状态保存 |
| 线索系统 | 90% | 否 | 否 | 部分可用 | Phase 2A 详情页 + Phase 2B 已读系统 + Phase 2C IMPORTANT（灰/金星标，v2.2t working）已完成；剩余：分类筛选、正式 UI、存档验证（详见 CLUE_SYSTEM_PHASE2_DESIGN.md / CLUE_SYSTEM_PHASE2C_IMPORTANT_DESIGN.md） |
| 存档系统 | 20% | 否 | 否 | 否 | 保存探索状态、场景状态、线索状态 |
| 角色系统 | 30% | 否 | 否 | 否 | 正式立绘接入、占位替换、动画/状态显示完善 |
| 音频系统 | 30% | 否 | 否 | 否 | BGM、环境音、音效正式接入、雨声/电话铃声替换 |
| 事件/Label 系统 | 80% | 否 | 否 | 基本可用 | 正式剧情整合、位置状态同步 |
| 文本显示系统 | 70% | 否 | 否 | 基本可用 | 打字机效果优化、标点停顿、旁白节奏调整 |
| 热点系统 | 97% | 是 | 是 | 可用 | Frozen；最新 Working：v2.2q_move_interrupt_on_hotspot_working；剩余 polish：热点反馈增强、可视化迭代 |

---

## 二、阅读注释

- 完成度基于 **v2.2o** 状态（v2.2l.1 文本速度基础 + v2.2n 选项居中 + v2.2o Hide UI 逻辑保留但 H 键禁用）
- "可接剧情"指该系统当前能否**直接承接正式剧情开发**，不需要先补功能
- 本文档**仅用于规划**，不修改任何 .rpy 文件
- 后续开发优先级参考"完成度"与"可接剧情"状态两个维度

---

## 三、优先级矩阵参考

按"完成度低 + 不可接剧情"双重维度排出最该补的系统：

| 优先级 | 系统 | 理由 |
|--------|------|------|
| 🔴 P0 | 存档系统（20%/否） | 完成度最低且阻塞剧情承接 |
| 🔴 P0 | 角色系统（30%/否） | 立绘缺失影响所有正式剧情展示 |
| 🔴 P0 | 音频系统（30%/否） | BGM 缺失严重影响氛围 |
| 🟠 P1 | 场景系统（40%/否） | 状态保存阻塞跨场景剧情 |
| 🟠 P1 | 线索系统（50%/否） | 主玩法之一，详情/分类必须补 |
| 🟠 P1 | 对话系统（60%/否） | 自动播放/历史记录是 AVG 玩家硬需求 |
| 🟡 P2 | UI 系统（70%/基本可用） | 已能跑，但发布前必须 polish |
| 🟡 P2 | 文本显示系统（70%/基本可用） | 节奏/停顿是 polish 项 |
| 🟢 P3 | 事件/Label 系统（80%/基本可用） | 已够用，等正式剧情驱动迭代 |
| 🟢 P3 | 探索系统（80%/可用） | 核心功能完整，反馈/路径增强为锦上添花 |

---

## 四、跨系统依赖标注

| 依赖关系 | 说明 |
|----------|------|
| 存档 ← 场景 / 探索 / 线索 | 存档必须先确定要存什么状态，三者数据结构是输入 |
| 角色 ← 美术资源 | 立绘到位前角色系统无法 polish |
| 音频 ← 音频资源 | BGM/音效正式资源到位前音频系统只能用占位 |
| 对话历史 ← 文本显示系统 | 历史记录需要文本显示稳定后才能可靠捕获 |
| UI 按钮 ← 对话系统 | 快进/自动播放等按钮依赖对话系统先实现底层逻辑 |

---

## 五、与已有文档的关系

- **FEATURE_LIST.md** — 颗粒度更细到具体功能项；本文按系统聚合
- **TECH_DEBT.md** — 列已知技术债；本文从完成度角度切入
- **PLACEHOLDER_LIST.md** — 列占位资源/Label；本文列系统级缺失
- **MISSING_ASSETS.md** — 资源缺失清单；本文系统级缺失含资源也含功能
- **ROADMAP.md** — 时间维度；本文系统维度，两者互补

---

## 六、功能完成闸门（每个 sub-version 必填）

| 版本/功能 | 完成度 % | 是否达到 95% | 是否允许进入下一功能 | 依据 |
|-----------|----------|--------------|----------------------|------|
| v2.2o Hide UI Disable Key | 95% | 是 | 是 | 老李手动测试通过；H 键不再触发隐藏；Hide UI 逻辑保留；lint 0；启动烟测无新 errors/traceback；working 已建立 |
| v2.2p Clue System Polish - 数据层增强 | 70% | 否 | 否 | 老李手动测试通过；add_clue 升级为 7 参兼容签名；clue_test_screen 显示 title/category/source/state/time；time 默认 "刚刚获得"；lint 0；启动烟测无新 errors/traceback；working 已建立。95% 需要正式 UI / 已读未读交互 / 分类筛选 / 存档验证 |
| v2.2q 热点交互打断寻路 | 95% | 是 | 是 | 老李手动测试通过；explore_press_e 调用 explore_cancel_movement 在事件触发前；target_x=player_world_x + idle；事件结束后角色不续走旧目标；lint 0；启动烟测无新 errors/traceback；working 已建立。Explore/Hotspot 双系统完成度提升至 97%，进入 Frozen |
| v2.2r Clue Detail View (Phase 2A) | 95% | 是 | 是 | 老李手动测试通过；clue_test_screen 列表项 button 化；新增 clue_detail_screen 显示六字段；返回按钮/ESC/右键回列表；systems_clue.rpy 未改；lint 0；启动烟测无新 errors/traceback；working 已建立。Clue System 综合完成度 70% → 80% |
| v2.2s Clue Read State (Phase 2B) | 95% | 是 | 是 | 老李手动测试通过（第五次迭代）；systems_clue.rpy 新增 mark_clue_read（return None）；列表 button action 链 Function(mark_clue_read) + Show(detail)；详情 zorder=210 叠加在列表上；返回出口仅 Hide(detail)；新增状态富文本染色 UNREAD红/READ绿/IMPORTANT金/LOCKED灰/ARCHIVED浅蓝；lint 0；启动烟测无新 errors/traceback；working 已建立。Clue System 综合完成度 80% → 85% |
| v2.3 Investigation System MVP | 70% | 否 | 否 | 老李手动测试通过；新增 systems_investigation.rpy（6 状态 / 8 接口 / 条件检查器 6 类型）+ investigation_test.rpy（3 测试目标 + investigation_test_screen 由 O 键打开）；explore_scene.rpy 接 O 键 + call register_test_objectives；event_test.rpy 两处 check_objective_conditions；scene_test.rpy scene_lobby 顶部 complete_objective("obj_enter_lobby")；scene_test.rpy back_to_explore 加 scene black 修紫底渗透；lint 0；启动烟测无新 errors/traceback；working 已建立。Investigation System 设计 → MVP 70%。95% 需要正式目标配置 / UI 整合 / Save 验证 / Flag 系统联动 / 正式剧情接入 |

### 闸门规则

- **完成度 %**：本轮功能自身的完成度，不等同于整个系统完成度。
- **是否达到 95%**：完成度 ≥ 95% 才填“是”。
- **是否允许进入下一功能**：必须同时满足：完成度 ≥ 95%、老李手动测试通过、lint 0 error、错误扫描 0、working 备份已建立。
- 未达到 95% 或未建立 working 时，默认不允许进入下一功能。

---

## 七、维护规则
- 每个 sub-version 锁定 working 后，复评涉及系统的完成度（±5% 起算调整）
- 每个 sub-version 完成后，必须在“功能完成闸门”表中填写：完成度 %、是否达到 95%、是否允许进入下一功能
- 完成度计算建议：核心功能权重 60% + polish 项权重 30% + 资源接入权重 10%
- 系统从"否"升级到"基本可用"或"可用"是里程碑，需在 PROJECT_LOG.md 同步记录
- 新系统加入时，直接追加表行，并补充优先级矩阵




---

## 八、Framework Freeze v1

> 生效时间：2026-06-02 09:48

框架已进入 **Framework Freeze v1**。

当前冻结一级系统：Dialogue / Explore / Hotspot / Clue / Scene / Save / UI / Audio / Asset / Camera / Video / Event / Flag / Investigation / Inventory。

### 预留接口控制规则

- 新增系统必须先经过 Framework Audit。
- 预留接口必须有明确使用场景。
- 一个系统只优先预留核心字段和核心接口。
- 所有预留接口必须可追踪：用途、所属模块、未来开发版本、依赖关系。
- 接口状态统一使用：`Reserved` / `Planned` / `In Progress` / `Implemented`。
- 每次 Framework Audit 必须检查未使用、过期、需要删除的接口。
- 允许删除预留接口，不允许永久堆积。
- 新增一级系统必须证明现有系统无法承载，并通过审计。

### 下一阶段

- 下一阶段：**v2.2p Clue System Polish**
- 在 v2.2p 开始前，不再新增一级系统。
- 若必须新增一级系统，先走 Framework Audit。

### Framework Freeze Rule 补充说明

- 本文档已写入 **Framework Freeze v1**。
- 本文档已写入 **预留接口控制规则**。
- 新增系统必须经过 Framework Audit。
- 控制预留接口数量：一个系统优先只预留核心字段和核心接口。
- 新增一级系统条件：现有系统无法承载，且必须通过审计。
- 允许删除预留接口，不允许永久堆积。

