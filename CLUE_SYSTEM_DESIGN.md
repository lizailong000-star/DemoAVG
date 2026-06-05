# CLUE_SYSTEM_DESIGN.md - 线索系统设计

> 项目：《祝寿》Ren'Py DemoAVG 原型  
> 创建时间：2026-06-02 09:59  
> 当前阶段：设计  
> 状态：不开发、不测试、不进入版本链  
> 目标：定义 Clue System 达到 95% 完成度需要具备的能力。

---

## 一、什么是线索？

线索是信息。

线索不是实体物品。

在《祝寿》中，线索用于记录玩家通过调查、对话、观察、录像、文件等方式获得的“可用于推理的信息”。

### 属于 Clue 的例子

```text
养老院公告
值班记录
监控异常
院长证词
王姐证词
死亡时间
通话记录
```

这些内容本质都是“信息”，因此属于 Clue System。

### 线索的用途

- 记录玩家已获得的信息
- 支撑推理和剧情分支判断
- 作为调查目标完成后的结果
- 作为回顾信息的 UI 内容
- 为后续 Flag / Event / Scene 提供判断依据

---

## 二、什么不是线索？

实体物品不是线索。

物品属于 Inventory System。

### 属于 Inventory 的例子

```text
钥匙
录像带
老照片
手机
工牌
```

这些内容是玩家可持有、可使用、可消耗、可改变状态的实体物品，因此属于 Inventory System，不属于 Clue System。

### 边界示例

| 内容 | 归属 | 说明 |
|------|------|------|
| 老照片 | Inventory | 实体物品 |
| 照片背面的日期信息 | Clue | 从物品中读取到的信息 |
| 录像带 | Inventory | 实体物品 |
| 录像带里出现的异常画面 | Clue | 录像内容提供的信息 |
| 手机 | Inventory | 实体物品 |
| 手机通话记录 | Clue | 信息记录 |
| 工牌 | Inventory | 实体物品，可用于通行 |
| 工牌上的名字 | Clue | 可用于推理的信息 |

---

## 三、线索有哪些状态？

## 3.1 线索状态机

至少包含：

```python
LOCKED
UNREAD
READ
```

允许扩展：

```python
IMPORTANT
ARCHIVED
```

### 状态说明

| 状态 | 含义 | 用途 |
|------|------|------|
| `LOCKED` | 尚未获得或不可见 | 用于提前登记线索，但不显示给玩家 |
| `UNREAD` | 已获得但未查看 | 用于提示新线索 |
| `READ` | 已查看 | 玩家已打开或确认过该线索 |
| `IMPORTANT` | 重点线索 | 用于高亮关键线索，可与 READ/UNREAD 组合或作为标记字段 |
| `ARCHIVED` | 已归档线索 | 用于后期整理，避免旧线索干扰当前调查 |

### 状态流转

```text
LOCKED
  ↓ add_clue()
UNREAD
  ↓ mark_clue_read()
READ
  ↓ archive_clue()
ARCHIVED
```

重点线索可以在任意阶段被标记：

```text
UNREAD + IMPORTANT
READ + IMPORTANT
ARCHIVED + IMPORTANT
```

---

## 四、线索字段设计

至少包含：

```python
clue_id
clue_title
clue_desc
clue_category
clue_source
clue_time
clue_state
```

### 字段说明

| 字段 | 类型建议 | 必填 | 说明 |
|------|----------|------|------|
| `clue_id` | string | 是 | 线索唯一 ID，例如 `clue_notice_old` |
| `clue_title` | string | 是 | 线索标题，例如“养老院旧公告” |
| `clue_desc` | string | 是 | 线索正文描述，用于线索详情页 |
| `clue_category` | string | 是 | 线索分类，如人物 / 地点 / 时间 / 证词 / 文件 / 异常事件 |
| `clue_source` | string | 是 | 线索来源，如公告栏、监控室、院长、王姐 |
| `clue_time` | string / int | 是 | 获得时间，不是案件时间 |
| `clue_state` | string enum | 是 | `LOCKED / UNREAD / READ / IMPORTANT / ARCHIVED` |

### 建议数据结构

```python
clue = {
    "clue_id": "clue_notice_old",
    "clue_title": "养老院旧公告",
    "clue_desc": "公告栏角落压着一张发黄的旧通知……",
    "clue_category": "文件",
    "clue_source": "公告栏",
    "clue_time": "chapter_01_activity_room",
    "clue_state": "UNREAD",
}
```

---

## 五、线索如何获得？

线索通过调查行为获得。

常见来源：

- Hotspot 调查
- Dialogue 对话
- Event 事件
- Video 录像内容
- Inventory 物品检查
- Scene 进入或切换

### 标准获得流程

```text
Objective ACTIVE
↓
Hotspot / Dialogue / Event
↓
add_clue()
↓
clue_state = UNREAD
↓
必要时 set_flag()
↓
必要时 complete_objective()
```

### 规则

- 线索获得后默认进入 `UNREAD`。
- 已获得线索不能重复添加。
- 重复获得时可以提示“已获得”，但不新增重复数据。
- `add_clue()` 必须保留当前项目三参兼容：`add_clue(id, title, desc)`，后续扩展字段时不得破坏旧调用。

---

## 六、线索如何查看？

线索查看属于 UI 展示，不改变线索内容。

### 查看入口

- 剧情模式：线索按钮 / 对话控制栏入口（未来）
- 探索模式：C 键或 HUD 入口（当前已有原型）
- 系统菜单：线索档案（未来）

### 查看行为

```text
打开线索面板
↓
选择线索
↓
显示 clue_title / clue_desc / clue_category / clue_source / clue_time
↓
mark_clue_read()
↓
clue_state = READ
```

### 规则

- 查看线索时不应推进对白。
- 查看线索时不应触发热点。
- 查看线索时可暂停 Auto / Skip。
- 第一次查看 `UNREAD` 线索后改为 `READ`。

---

## 七、线索如何分类？

线索分类用于帮助玩家整理信息。

### 候选分类

```text
人物
地点
时间
证词
文件
异常事件
```

### 分类说明

| 分类 | 用途 | 示例 |
|------|------|------|
| 人物 | 与角色身份、关系、动机相关 | 院长证词、王姐证词 |
| 地点 | 与场景、空间、路线相关 | 监控室位置、楼梯间异常 |
| 时间 | 与时间线相关 | 死亡时间、电话时间、值班时间 |
| 证词 | 角色口述信息 | 院长说法、护工说法 |
| 文件 | 纸面 / 系统记录 | 养老院公告、值班记录、通话记录 |
| 异常事件 | 无法用正常逻辑解释的事件 | 监控异常、墙皮变化、重复铃声 |

### 是否采用

建议采用以上六类作为 v2.2p Clue System Polish 的初版分类。

原因：

- 覆盖当前养老院调查场景
- 数量适中，不会过度复杂
- 方便后续 UI 做筛选

---

## 八、线索如何记录来源？

必须有来源字段：

```python
clue_source
```

### 来源示例

```text
公告栏
监控室
院长
王姐
录像带
电话记录
```

### 来源用途

- 告诉玩家线索从哪里来
- 支持线索详情页展示
- 支持后续推理 UI 按来源筛选
- 支持 debug：确认线索是否由正确热点 / 事件产生

### 来源格式建议

```python
clue_source = {
    "type": "hotspot",
    "id": "hotspot_notice_board",
    "label": "公告栏"
}
```

初版可以简化为字符串：

```python
clue_source = "公告栏"
```

---

## 九、线索如何记录获得时间？

必须有：

```python
clue_time
```

`clue_time` 记录的是获得时间，而不是案件时间。

### 例子

```python
clue_time = "chapter_01_activity_room"
```

表示玩家在 Chapter 01 的活动室阶段获得该线索。

### 不是什么

`clue_time` 不等于案件发生时间。

例如：

- 死亡时间：属于线索内容，可写在 `clue_desc` 或扩展字段里
- 获得时间：玩家什么时候拿到这条线索，写在 `clue_time`

### 用途

- 线索排序
- 线索回顾
- 存档恢复
- Debug 追踪

---

## 十、线索如何与 Flag System 关联？

Flag 与 Clue 不同。

### 示例

```python
flag_notice_checked = True
clue_notice_old = READ
```

含义：

- `flag_notice_checked = True`：玩家调查过公告栏这个状态成立。
- `clue_notice_old = READ`：旧公告这条线索已读。

### 规则

- Flag 记录状态。
- Clue 记录信息。
- 获得线索时可以设置 Flag。
- 读取线索时也可以设置 Flag，例如 `flag_notice_clue_read = True`。
- Flag 不替代 Clue，Clue 也不替代 Flag。

### 示例流程

```text
add_clue("clue_notice_old")
↓
set_flag("flag_notice_checked", True)
```

---

## 十一、线索如何与 Investigation System 关联？

必须明确：

```text
Objective
↓
Clue
```

调查目标产生线索。

不是：

```text
Clue
↓
Objective
```

### 规则

- Objective 是调查方向。
- Clue 是调查结果。
- Objective 完成条件可以是“获得某条线索”。
- Clue 不直接创建 Objective。
- 如果获得线索后需要新目标，必须通过 Event / Flag 判断后再 `start_objective()`。

### 示例

```text
Objective: 查看公告栏
↓
Hotspot: 公告栏
↓
add_clue("clue_notice_old")
↓
complete_objective("OBJ_NOTICE_BOARD")
```

如果继续开启新目标：

```text
clue_notice_old 已获得
↓
Event: notice_reveals_monitor_room
↓
start_objective("OBJ_ENTER_MONITOR_ROOM")
```

---

## 十二、线索如何与 Inventory System 关联？

Inventory 是实体物品。

Clue 是信息。

### 必须明确边界

```text
老照片
```

属于：

```text
Inventory
```

但：

```text
照片背面的日期信息
```

属于：

```text
Clue
```

### 示例

| 实体物品 | Inventory | 从中得到的信息 | Clue |
|----------|-----------|----------------|------|
| 老照片 | `item_old_photo` | 背面日期 | `clue_photo_date` |
| 录像带 | `item_vhs_tape` | 录像异常 | `clue_vhs_anomaly` |
| 手机 | `item_phone` | 通话记录 | `clue_call_log` |
| 工牌 | `item_badge` | 工牌姓名 | `clue_badge_name` |

### 规则

- 检查 Inventory 可以产生 Clue。
- Clue 不代表玩家持有物品。
- Inventory 的状态变化不等于 Clue 的已读状态。

---

## 十三、线索如何进入存档？

### 13.1 预留字段

```python
clue_list
clue_state_map
clue_seen_map
```

### 13.2 字段说明

| 字段 | 类型建议 | 保存内容 |
|------|----------|----------|
| `clue_list` | list | 已获得线索基础数据或线索 id 列表 |
| `clue_state_map` | dict | clue_id -> clue_state，如 LOCKED / UNREAD / READ |
| `clue_seen_map` | dict | clue_id -> bool，是否已查看 / 已读 |

### 13.3 Save System 保存内容

Save System 至少保存：

```python
save_data["clue_list"] = clue_list
save_data["clue_state_map"] = clue_state_map
save_data["clue_seen_map"] = clue_seen_map
```

如果采用扩展字段，还应保存：

```python
save_data["clue_category_map"] = clue_category_map
save_data["clue_source_map"] = clue_source_map
save_data["clue_time_map"] = clue_time_map
```

### 13.4 读档恢复

```python
clue_list = save_data.get("clue_list", [])
clue_state_map = save_data.get("clue_state_map", {})
clue_seen_map = save_data.get("clue_seen_map", {})
```

### 13.5 保存规则

- 已获得线索必须保存。
- 已读 / 未读状态必须保存。
- 分类 / 来源 / 获得时间必须保存。
- 不保存临时 hover / scroll / tooltip 状态。

---

## 十四、Clue System 95% 完成标准

Clue System 达到 95%，必须满足以下标准。

### 14.1 数据能力

- 有统一线索数据结构。
- 每条线索至少包含：`clue_id / clue_title / clue_desc / clue_category / clue_source / clue_time / clue_state`。
- 支持防重复获得。
- 支持 `LOCKED / UNREAD / READ` 状态。
- 支持 `IMPORTANT / ARCHIVED` 扩展或明确暂缓。

### 14.2 获取能力

- Hotspot 可获得线索。
- Dialogue / Event 可获得线索。
- Inventory 检查可产生线索。
- 获得线索后默认 `UNREAD`。

### 14.3 查看能力

- 有正式线索 UI。
- 可查看线索标题、正文、分类、来源、获得时间。
- 查看后可从 `UNREAD` 变为 `READ`。
- 新线索有明显提示。

### 14.4 分类能力

- 至少支持：人物、地点、时间、证词、文件、异常事件。
- 可按分类筛选或至少按分类展示。

### 14.5 来源与时间

- 每条线索必须记录来源。
- 每条线索必须记录获得时间。
- 获得时间必须区别于案件时间。

### 14.6 系统边界

- 明确 Clue 不等于 Inventory。
- 明确 Clue 不等于 Flag。
- 明确 Objective 产生 Clue，不是 Clue 直接产生 Objective。
- 与 Event / Flag / Investigation / Inventory 的关系在文档和代码结构中一致。

### 14.7 存档能力

- `clue_list` 可保存和恢复。
- `clue_state_map` 可保存和恢复。
- `clue_seen_map` 可保存和恢复。
- 分类 / 来源 / 获得时间可保存和恢复。

### 14.8 测试能力

- lint 0 error。
- 错误扫描 0。
- 老李手动测试通过。
- 建立 working 备份。
- `POLISH_AUDIT.md` 中完成度达到 95%，并标记允许进入下一功能。

### 14.9 95% 判定

只有满足以下条件，才可判定 Clue System 95%
```text
统一数据结构完成
+ 正式 UI 可用
+ 分类 / 来源 / 获得时间完成
+ 已读未读状态完成
+ 存档恢复完成
+ 与 Objective / Flag / Inventory 边界清楚
+ 老李手动测试通过
+ working 备份建立
```

否则不得标记 95%。

---

## 十五、当前阶段结论

- 当前只做设计。
- 当前不开发。
- 当前不测试。
- 当前不进入版本链。
- 禁止直接开发 Clue System。
- 下一步如果进入 v2.2p Clue System Polish，必须先按本文档确认开发范围，再动 `.rpy`。

---

## 十六、最终边界总结

- Clue 是信息，不是物品。
- Inventory 是实体物品，不是线索。
- Flag 是状态记录，不是线索。
- Objective 是调查方向，不是线索。
- Objective 产生 Clue，不是 Clue 直接产生 Objective。
- Clue 必须可分类、可追溯来源、可记录获得时间、可保存。
- Clue System 95% 的核心是：数据统一、UI 可用、状态明确、边界清楚、可存档、测试通过。
