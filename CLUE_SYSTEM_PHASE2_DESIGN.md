# CLUE_SYSTEM_PHASE2_DESIGN.md - 线索系统 Phase 2 设计

> 项目：《祝寿》Ren'Py DemoAVG 原型
> 创建时间：2026-06-02 10:58
> 当前阶段：设计
> 状态：不开发、不测试、不进入版本链
> 目标：定义 Clue System 从当前 70% 提升到 95% 还缺什么
> 基线版本：v2.2p_clue_data_polish_working
> 关联文档：CLUE_SYSTEM_DESIGN.md（基础定义）

---
## 一、当前已完成内容（基线 v2.2p）

### 1.1 字段层（已完成）

- `clue_id`：线索唯一标识
- `clue_title`：标题
- `clue_desc`：描述
- `clue_category`：分类，默认 "未分类"
- `clue_source`：来源，默认 "未知"
- `clue_state`：状态，默认 "UNREAD"
- `clue_time`：获得时间，占位 "刚刚获得"

### 1.2 函数/逻辑层（已完成）

- `add_clue(clue_id, title, desc, category, source, state, clue_time)`：兼容三参旧调用 + 七参新调用
- 防重复：同 `clue_id` 不重复添加，返回 `False`
- `clue_time=None` 自动填 "刚刚获得"
- `normalize_clue_state`：保证只接受合法状态字符串
- `get_clue_count()`：线索总数

### 1.3 UI/查看层（已完成）

- `clue_test_screen`：C 键打开
- 显示编号、title、category、source、state、time，每字段独立一行
- 黑底简洁文字，不算正式 UI

### 1.4 数据结构升级（已完成）

- `clue_list` 从纯 `{id,title,desc}` 升级为 7 字段 dict
- 旧剧情三参 `add_clue()` 调用兼容运行
- 重复防护与状态校验已生效

### 1.5 完成度评估

- 数据层：约 90%
- 函数层：约 80%
- UI/查看层：约 40%（仅测试列表，无详情页、无交互）
- 存档层：约 20%（依赖 default 持久化，未显式接 Save 钩子）
- **综合：70%**

---
## 二、未完成内容拆分（Phase 2A / 2B / 2C）

Clue System 从 70% 提升到 95%，需要解决三类问题：
- **Phase 2A — 详情页**：让线索"可读"
- **Phase 2B — 已读系统**：让线索"被读过"可识别
- **Phase 2C — IMPORTANT 系统**：让关键线索"可强调"

每个 Phase 都是独立的最小可迭代功能，可单独 working 锁定。

---

## 三、Phase 2A — 线索详情页

### 3.1 目标

玩家在列表里点击单条线索后，进入详情视图，查看完整信息。

### 3.2 必须显示字段

- 标题（`title`）
- 描述（`desc`）
- 分类（`category`）
- 来源（`source`）
- 状态（`state`）
- 获得时间（`time`）

### 3.3 行为定义

- 入口：列表项点击 / 上下键选中后按 Enter
- 关闭：Esc / 右键 / "返回" 按钮
- 返回后：保留列表滚动位置（最小要求：不强制重置）
- 关闭详情后回到列表

### 3.4 不在 Phase 2A 范围

- 不做正式美术
- 不做立绘 / 插图
- 不做语音
- 不做关联线索跳转
- 不做搜索

### 3.5 完成度贡献

Phase 2A 通过后 Clue System 综合完成度预估：70% → 80%

---

## 四、Phase 2B — 已读系统

### 4.1 目标

线索被打开详情查看后，状态从 `UNREAD` 自动变为 `READ`。

### 4.2 状态流转

```
LOCKED  ──(满足解锁条件)──>  UNREAD
UNREAD  ──(打开详情页)─────>  READ
READ    ──(无)─────────────>  READ   （不回退）
```

### 4.3 必须实现

- 打开详情页时调用 `mark_clue_read(clue_id)`
- `mark_clue_read` 只把 `UNREAD` 改成 `READ`
- 已经是 `READ` 或 `IMPORTANT` 的不变
- `LOCKED` 不允许打开详情（或显示遮罩）
- 列表 UI 区分未读/已读（例如未读高亮、已读灰色）

### 4.4 不在 Phase 2B 范围

- 不做"标为未读"逆操作
- 不做未读计数 HUD（属于 UI 系统）
- 不做提示音 / 提示动画

### 4.5 完成度贡献

Phase 2B 通过后 Clue System 综合完成度预估：80% → 88%

---

## 五、Phase 2C — IMPORTANT 重要线索系统

### 5.1 目标

关键剧情线索可以被标记为 `IMPORTANT`，便于玩家回看时识别。

### 5.2 必须实现

- `mark_clue_important(clue_id)`：把状态改为 `IMPORTANT`
- `unmark_clue_important(clue_id)`：把 `IMPORTANT` 改回 `READ`
- 列表 UI 高亮 `IMPORTANT` 线索（例如金色边框 / 图标）
- 详情页可显示"重要"标记

### 5.3 边界

- **IMPORTANT ≠ READ**：IMPORTANT 表示重要性，READ 表示是否被阅读
- **IMPORTANT ≠ CATEGORY**：CATEGORY 是分类（人物/地点等），IMPORTANT 是优先级
- IMPORTANT 与已读状态共存：一条 IMPORTANT 线索可以未被详细阅读，也可以已读
- 实际实现可以让 `state` 是字符串单值（共五种），也可以拆成 `state` + `is_important` 双字段
- **推荐方案**：拆成 `state` + `is_important`，避免状态机互斥

### 5.4 不在 Phase 2C 范围

- 不做剧情自动标记
- 不做导入/导出
- 不做与 Flag 的双向绑定

### 5.5 完成度贡献

Phase 2C 通过后 Clue System 综合完成度预估：88% → 93%

---
## 六、分类查看系统讨论

### 6.1 候选分类（基于 CLUE_SYSTEM_DESIGN.md）

- 人物
- 地点
- 时间
- 证词
- 文件
- 异常事件

### 6.2 分类查看的几种方案

**方案 A：左侧分类侧栏 + 右侧列表**
- 优点：分类切换直观，符合 PC AVG 习惯
- 缺点：屏幕窄时拥挤，需要更复杂 UI

**方案 B：顶部分类标签栏（Tab）**
- 优点：紧凑，移动端也合适
- 缺点：分类多时标签栏过长

**方案 C：单一列表 + 头部分类筛选下拉**
- 优点：最简实现，可快速上线
- 缺点：分类信息不够直观

**方案 D：不分类，按时间倒序**
- 优点：实现最简
- 缺点：线索多时玩家难以定位

### 6.3 推荐方案

- **MVP 阶段（Phase 2 内）**：采用 **方案 C（顶部下拉/横向 chip 筛选）**
- **正式发布前**：升级到 **方案 B（Tab 标签栏）**，与正式 UI 一同迭代

理由：
- 方案 C 实现成本低，能在 Phase 2 内通过
- 方案 B 体验更好，但 UI 设计成本高，留给正式 UI Polish

### 6.4 分类规则约束

- 分类必须是预定义白名单之一，不允许自由填写
- "未分类" 作为兜底分类
- 每条线索只属于一个分类（不支持多分类）
- 未来如需要"标签"，新增 `clue_tags` 字段而不是改 `category`

---

## 七、正式 UI 设计讨论

### 7.1 候选方案

**方案 A：左侧列表 + 右侧详情（双栏）**
- 优点：PC AVG 主流布局，符合玩家预期
- 优点：列表和详情同屏，切换快
- 缺点：屏幕需要足够宽（≥1280）
- 缺点：UI 实现复杂

**方案 B：全屏列表 + 跳转详情（单栏）**
- 优点：实现简单，移动端兼容
- 优点：详情可显示更长描述
- 缺点：列表和详情切换有延迟感
- 缺点：返回列表需要保留滚动位置

**方案 C：抽屉式（列表常驻 + 详情滑出）**
- 优点：动画感强
- 缺点：实现复杂，Ren'Py 动画支持有限

### 7.2 推荐方案

- **MVP（Phase 2 内）**：方案 B（全屏列表 + 跳转详情）
  - 复用现有 `clue_test_screen`，加详情子 screen
  - 实现成本最低，能在 Phase 2 内通过
- **正式发布前**：升级为方案 A（双栏）
  - 与角色立绘、正式美术一同迭代

### 7.3 UI 不在 Phase 2 范围

- 正式美术资源（线索框、图标、底纹）
- 动画切换
- 音效（翻页声、勾选声）
- 主题切换

### 7.4 完成度贡献

正式 UI 通过后 Clue System 综合完成度预估：93% → 95%

---
## 八、存档验证

### 8.1 必须进入 Save System 的数据

| 字段 | 用途 | 备注 |
|------|------|------|
| `clue_list` | 所有线索的完整 dict 列表 | 主存储 |
| `clue_state_map` | clue_id → state 的快速映射 | 用于 UI 高效查询 |
| `clue_seen_map` | clue_id → True/False（玩家是否打开过详情） | 用于"新线索"提示 |

### 8.2 可选进入 Save System 的扩展数据

- `clue_category_map`：clue_id → category 缓存
- `clue_source_map`：clue_id → source 缓存
- `clue_time_map`：clue_id → 获得时间字符串

> 备注：以上扩展可以从 `clue_list` 计算得出，存与不存看性能权衡。MVP 建议只存 `clue_list` + `clue_state_map` + `clue_seen_map`，其余即时计算。

### 8.3 Save 时机

- 玩家手动存档：跟随 Ren'Py 标准 save，由 `default` 自动持久化
- 获得新线索后：自动 quick save（与 Scene/Flag 一起进入下个 Save 框架）

### 8.4 Load 时验证

- 加载存档后：
  - `clue_list` 中每条线索字段补齐（旧存档没有 `category` 等，需自动补 "未分类"）
  - `clue_state_map` 重建
  - `clue_seen_map` 缺失时默认全 False

### 8.5 存档验证测试用例

1. 获得 3 条线索 → 存档 → 退出 → 加载 → 3 条线索仍存在
2. 打开详情让状态变 READ → 存档 → 重新加载 → 状态仍是 READ
3. 标记 IMPORTANT → 存档 → 重新加载 → IMPORTANT 标记仍存在
4. 旧存档（仅 3 字段）加载 → 自动补字段不报错
5. 同一 clue_id 重复添加不重复

---

## 九、与其他系统关系

### 9.1 Clue ↔ Flag

- **Flag** 是状态记录中心（开关 / 整数 / 字符串），用于剧情判断
- **Clue** 是信息载体，玩家"看得见"的资料
- 边界：拿到线索 ≠ 触发 Flag；Flag 用于剧情逻辑，Clue 用于玩家展示
- 关联点：剧情可以"获得线索时顺手 set 一个 Flag"，但不强制

### 9.2 Clue ↔ Investigation

- **Investigation/Objective** 是"当前调查方向"
- Objective 推进过程中产生 Clue，但 Clue 本身不创建 Objective
- 边界：Objective 完成可以依赖某条 Clue 是否被收集，但反过来不成立

### 9.3 Clue ↔ Inventory

- **Inventory** 是实体物品（钥匙、录像带、老照片）
- **Clue** 是信息（证词、记录、异常事件）
- 边界：录像带是 Inventory，录像带内容可以生成 Clue；老照片是 Inventory，照片描述可以生成 Clue
- 同一现实事物可以"同时进 Inventory 和 Clue"，但两个系统独立维护

### 9.4 Clue ↔ Scene

- Scene 是场景流转，与 Clue 无直接耦合
- 关联点：进入某场景可能触发 `add_clue()`，但 Scene 不存储 Clue 状态

### 9.5 Clue ↔ Event

- Event 是触发中心
- `add_clue()` 通常由 Event 调用，但 Clue System 本身不发布 Event
- 关联点：获得线索可以触发一个 `event_clue_added` 通知 Event 系统，但 Clue 不依赖 Event 才能工作

---
## 十、95% 完成标准

Clue System 标记为 95% 并进入 Frozen，必须同时满足以下条件：

### 10.1 数据能力（必须 100%）

- 七字段结构稳定
- 兼容旧三参调用
- 防重复有效
- `normalize_clue_state` 校验全部状态

### 10.2 状态机能力（必须 100%）

- 支持 `LOCKED / UNREAD / READ / IMPORTANT / ARCHIVED` 五状态（或 state + is_important 双字段实现）
- `mark_clue_read`、`mark_clue_important`、`unmark_clue_important` 三接口可用
- 状态转移规则文档化并实测通过

### 10.3 详情页能力（必须可用）

- 列表点击进入详情
- 详情显示六字段全部
- 关闭返回列表保留位置（最小要求：不强制重置）
- 打开详情自动 `READ`

### 10.4 分类查看（至少 MVP 方案 C）

- 顶部下拉或 chip 筛选
- 至少支持 "全部" + 6 个预定义分类 + "未分类"

### 10.5 正式 UI（至少 MVP 方案 B）

- 全屏列表 + 跳转详情
- 未读/已读视觉区分
- IMPORTANT 视觉强调

### 10.6 存档能力（必须验证）

- `clue_list` / `clue_state_map` / `clue_seen_map` 进入 Save System
- 五条测试用例（见 §8.5）全部通过

### 10.7 系统边界（必须文档化）

- 与 Flag / Investigation / Inventory / Scene / Event 关系明确（本文档 §9）
- 重复造系统的风险已识别

### 10.8 测试能力

- 提供至少一个测试入口 label 让老李手动验证
- lint 0 error
- 启动烟测无新 errors/traceback
- 所有 sub-version 都建有 working 备份

### 10.9 95% 判定条件汇总

| 条目 | 必须 | 说明 |
|------|------|------|
| 数据层 | 是 | 七字段 + 兼容 + 防重复 |
| 状态机 | 是 | 五状态可流转 |
| 详情页 | 是 | 六字段显示 + 自动 READ |
| 分类查看 | 是 | 至少方案 C |
| 正式 UI | 是 | 至少方案 B |
| 存档验证 | 是 | 五用例通过 |
| 系统边界 | 是 | §9 文档化 |
| 测试入口 | 是 | 手动可达 + lint 0 |

任一条不满足，不允许标记 95%。

### 10.10 95% 之后

- 95% 进入 Frozen
- 后续 polish（剧情整合、美术替换、动画、音效）不再改基础数据结构
- 95% → 100% 由正式美术资源 + 完整剧情驱动，与 Phase 2 解耦

---

## 十一、Phase 2 推进顺序建议

1. **Phase 2A 详情页** —— 最基础，所有后续功能依赖
2. **Phase 2B 已读系统** —— 依赖 2A 的"打开详情"动作
3. **Phase 2C IMPORTANT 系统** —— 与 2B 同层级，可并行也可在后
4. **分类查看** —— 在 2A/2B/2C 完成后接入
5. **正式 UI（MVP 方案 B）** —— 收尾，统一视觉
6. **存档验证** —— 全部跑通后统一接 Save System
7. **回归测试 + Frozen 标记**

每个 sub-version 严格遵守 Framework Freeze v1 流程：pre 备份 → 修改 → lint → 烟测 → 老李手动测试 → working 备份。

---

## 十二、本文档不在范围

- 不开发任何 .rpy
- 不修改 systems_clue.rpy / clue_test.rpy
- 不修改资源 / 剧情 / UI
- 不进入版本链

本文档仅作为 Clue System Phase 2 的设计基线，等待老李审阅后再决定是否进入 v2.2r 开发。
