# INVESTIGATION_SYSTEM_DESIGN.md - 调查目标系统设计

> 项目：《祝寿》Ren'Py DemoAVG 原型  
> 创建时间：2026-06-02 09:56  
> 当前阶段：设计  
> 状态：不开发、不测试、不进入版本链  
> 目标：定义《祝寿》的调查循环，为后续 v2.2p+ 的系统开发提供边界。

---

## 一、什么是调查目标？

调查目标不是传统任务系统。

调查目标不是 MMO Quest。

调查目标不是 RPG Quest。

在《祝寿》里：

> **调查目标 = 当前调查方向。**

它告诉玩家“现在应该往哪里查”，但不把游戏变成打勾式任务清单。

调查目标用于维持 AVG 推理节奏：

- 给玩家一个当前方向
- 引导玩家去某个场景 / 热点
- 推动线索收集
- 控制剧情阶段
- 与 Event / Flag / Scene / Hotspot / Clue 联动

### 示例

| 目标 ID | 调查目标 | 含义 |
|---------|----------|------|
| OBJ_001 | 去养老院大厅 | 引导玩家进入正式调查场景 |
| OBJ_002 | 查看公告栏 | 引导玩家调查公告栏热点 |
| OBJ_003 | 询问院长 | 引导玩家触发人物对话事件 |
| OBJ_004 | 进入监控室 | 引导玩家寻找新场景入口 |
| OBJ_005 | 查看值班记录 | 引导玩家获取关键时间线信息 |
| OBJ_006 | 调查乙的死亡原因 | 更高层级的阶段目标，可跨多个场景 |

---

## 二、调查目标有哪些状态？

### 2.1 必须状态

```python
NOT_STARTED
ACTIVE
COMPLETED
FAILED
```

| 状态 | 含义 | 使用场景 |
|------|------|----------|
| `NOT_STARTED` | 目标尚未开始 | 目标已登记，但剧情尚未触发 |
| `ACTIVE` | 目标进行中 | 玩家当前应关注的调查方向 |
| `COMPLETED` | 目标已完成 | 玩家完成目标要求，如获得指定线索 |
| `FAILED` | 目标失败 | 目标因剧情分支、时间、选择或条件变化无法完成 |

### 2.2 允许扩展状态

```python
HIDDEN
OPTIONAL
LOCKED
```

| 状态 | 含义 | 用途 |
|------|------|------|
| `HIDDEN` | 隐藏目标 | 后台存在但不显示给玩家，用于暗线或伏笔 |
| `OPTIONAL` | 可选目标 | 不阻塞主线，但完成后可获得额外线索或分支信息 |
| `LOCKED` | 锁定目标 | 玩家已知道方向，但条件不足，暂时不能推进 |

### 2.3 目标状态机草案

```text
NOT_STARTED
    ↓ start_objective()
ACTIVE
    ↓ complete_objective()
COMPLETED

ACTIVE
    ↓ fail_objective()
FAILED

HIDDEN
    ↓ reveal / start_objective()
ACTIVE

LOCKED
    ↓ condition_met
ACTIVE

OPTIONAL
    ↓ complete_objective()
COMPLETED
```

---

## 三、调查目标如何开始？

调查目标开始，意味着它从 `NOT_STARTED / HIDDEN / LOCKED` 进入 `ACTIVE`。

### 3.1 开始条件

目标可以由以下系统触发开始：

- Event System：剧情事件触发目标
- Scene System：进入某场景后自动开始目标
- Flag System：某个状态达成后开始目标
- Hotspot System：调查某热点后开启后续目标
- Clue System：注意，Clue 本身不主动产生目标；只能通过 Event / Flag 规则间接影响目标

### 3.2 示例

```text
进入养老院活动室
↓
Event: enter_activity_room
↓
start_objective("OBJ_NOTICE_BOARD")
↓
目标 ACTIVE：查看公告栏
```

### 3.3 预留接口

```python
def start_objective(objective_id):
    pass
```

---

## 四、调查目标如何推进？

调查目标推进，指目标处于 `ACTIVE` 后，玩家通过场景探索、热点交互、对话、事件逐步满足完成条件。

### 4.1 推进来源

- Hotspot：点击 / 接近 / E 键调查热点
- Event：事件执行后更新目标阶段
- Flag：记录某条件已达成
- Scene：切换到目标相关场景
- Clue：目标推进后产生线索，线索作为结果被记录

### 4.2 示例：查看公告栏

```text
目标：查看公告栏
状态：ACTIVE
↓
玩家靠近公告栏热点
↓
按 E 调查公告栏
↓
Event: inspect_notice_board
↓
add_clue("old_notice", ...)
↓
set_flag("flag_notice_board_checked", True)
↓
complete_objective("OBJ_NOTICE_BOARD")
```

### 4.3 预留接口

```python
def update_objective_state(objective_id, state):
    pass
```

---

## 五、调查目标如何完成？

目标完成，指目标从 `ACTIVE / OPTIONAL` 进入 `COMPLETED`。

### 5.1 完成条件

目标完成必须满足明确条件，例如：

- 获得指定线索
- 触发指定事件
- 到达指定场景
- 与指定角色对话
- 设置指定 Flag
- 获得指定 Inventory 物品

### 5.2 示例：公告栏目标完成

```text
查看公告栏
ACTIVE
↓
获得公告栏线索
↓
COMPLETED
```

对应状态：

```python
objective_state_map["OBJ_NOTICE_BOARD"] = "COMPLETED"
flag_notice_board_checked = True
```

### 5.3 完成后可触发事件

目标完成后可以触发 Event System，例如：

```text
完成：查看公告栏
↓
触发：院长出现
```

伪流程：

```python
complete_objective("OBJ_NOTICE_BOARD")
trigger_event("EVENT_DIRECTOR_APPEARS")
```

### 5.4 预留接口

```python
def complete_objective(objective_id):
    pass
```

---

## 六、调查目标如何失败？

目标失败，指目标从 `ACTIVE / OPTIONAL / LOCKED` 进入 `FAILED`。

### 6.1 失败条件

失败不一定意味着 Game Over，而是调查方向失效。

可能原因：

- 剧情选择导致目标不再可达
- 场景状态变化，目标对象消失
- 玩家错过时机
- 目标被更高优先级目标替代
- 分支路线关闭

### 6.2 示例

```text
目标：询问院长
ACTIVE
↓
玩家先触发监控室事件
↓
院长离开活动室
↓
询问院长 FAILED
↓
新目标：追踪院长去向 ACTIVE
```

### 6.3 预留接口

```python
def fail_objective(objective_id):
    pass
```

---

## 七、调查目标与 Clue System 的关系

必须明确：

```text
Objective
↓
Clue
```

而不是：

```text
Clue
↓
Objective
```

### 7.1 规则

- 调查目标产生线索。
- 线索不直接产生调查目标。
- 线索可以被 Event / Flag 判断使用，但不直接开启目标。
- 如果获得线索后需要开启新目标，必须经过 Event System 或 Flag System。

### 7.2 示例

```text
Objective: 查看公告栏
↓
Hotspot: 公告栏
↓
Event: inspect_notice_board
↓
Clue: old_notice
↓
Objective: 查看公告栏 COMPLETED
```

如果需要开启新目标：

```text
Clue: old_notice 已获得
↓
Event: notice_reveals_monitor_room
↓
start_objective("OBJ_ENTER_MONITOR_ROOM")
```

### 7.3 边界

- Clue 是信息收集。
- Objective 是调查方向。
- Clue 不等于 Objective。

---

## 八、调查目标与 Flag System 的关系

Flag 记录状态。

Objective 记录阶段。

两者不同。

### 8.1 示例

```python
objective_notice_board = COMPLETED
flag_notice_board_checked = True
```

含义：

- `objective_notice_board = COMPLETED`：说明“查看公告栏”这个调查目标已经完成。
- `flag_notice_board_checked = True`：说明玩家确实调查过公告栏，可用于后续条件判断。

### 8.2 规则

- Objective 状态面向调查流程。
- Flag 状态面向剧情条件判断。
- Objective 完成时通常会写 Flag，但二者不能合并。
- Flag 可用于判断目标是否可开启、可完成、可失败。

### 8.3 示例流程

```text
complete_objective("OBJ_NOTICE_BOARD")
↓
set_flag("flag_notice_board_checked", True)
```

---

## 九、调查目标与 Scene System 的关系

目标可能绑定场景，但目标不等于场景。

### 9.1 目标绑定场景示例

```text
活动室
公告栏
监控室
楼梯间
```

### 9.2 规则

- 一个目标可以只在一个场景内完成。
- 一个目标也可以跨多个场景。
- Scene System 负责场景流转。
- Investigation System 负责目标状态。

### 9.3 示例

```text
目标：进入监控室
相关场景：活动室 → 走廊 → 监控室
```

这个目标跨越多个 Scene，因此不能把 Objective 直接写死成 Scene。

### 9.4 Scene 进入触发目标

```text
enter_scene("activity_room")
↓
trigger_event("EVENT_ENTER_ACTIVITY_ROOM")
↓
start_objective("OBJ_NOTICE_BOARD")
```

---

## 十、调查目标与 Hotspot System 的关系

目标通过热点推进。

Hotspot 是玩家实际交互点。

Objective 是玩家当前方向。

### 10.1 示例

```text
目标：查看公告栏
↓
点击公告栏热点
↓
获得线索
↓
目标完成
```

### 10.2 规则

- Hotspot 不直接决定主线阶段。
- Hotspot 触发 Event。
- Event 更新 Objective / Flag / Clue。
- 同一 Hotspot 在不同 Objective 状态下可以触发不同 Event。

### 10.3 示例伪逻辑

```python
if current_objective_id == "OBJ_NOTICE_BOARD":
    trigger_event("EVENT_INSPECT_NOTICE_BOARD")
else:
    trigger_event("EVENT_NOTICE_BOARD_DEFAULT")
```

---

## 十一、调查目标与 Event System 的关系

Event System 是触发中心。

Investigation System 不应直接调用所有下游系统，而应由 Event System 统一调度。

### 11.1 目标开始由 Event 触发

```text
Event: enter_activity_room
↓
start_objective("OBJ_NOTICE_BOARD")
```

### 11.2 目标完成后触发 Event

```text
完成：查看公告栏
↓
触发：院长出现
```

伪流程：

```python
complete_objective("OBJ_NOTICE_BOARD")
trigger_event("EVENT_DIRECTOR_APPEARS")
```

### 11.3 规则

- Event 可以开始目标。
- Event 可以推进目标。
- Event 可以完成目标。
- Event 可以在目标完成后触发新剧情、镜头、视频、音效、Flag。
- Objective 不等于 Event。

---

## 十二、调查目标如何保存进存档？

### 12.1 预留字段

```python
current_objective_id
objective_state_map
objective_history
```

### 12.2 字段说明

| 字段 | 类型建议 | 说明 |
|------|----------|------|
| `current_objective_id` | string / None | 当前正在进行的调查目标 |
| `objective_state_map` | dict | objective_id -> state，用于记录每个目标状态 |
| `objective_history` | list | 目标开始、推进、完成、失败的历史记录 |

### 12.3 Save System 接入方式

Save System 需要保存：

```python
save_data["current_objective_id"] = current_objective_id
save_data["objective_state_map"] = objective_state_map
save_data["objective_history"] = objective_history
```

读档时恢复：

```python
current_objective_id = save_data.get("current_objective_id")
objective_state_map = save_data.get("objective_state_map", {})
objective_history = save_data.get("objective_history", [])
```

### 12.4 保存规则

- Objective 状态必须是可序列化数据。
- 不保存临时 HUD 动画。
- 不保存 hover / tooltip 等瞬时 UI 状态。
- 保存目标历史是为了 debug 和分支回溯，不一定展示给玩家。

---

## 十三、调查循环总结

《祝寿》的调查循环：

```text
Objective ACTIVE
↓
Scene 提供调查空间
↓
Hotspot 提供交互点
↓
Event 统一触发
↓
Clue 记录获得的信息
↓
Flag 记录剧情状态
↓
Objective COMPLETED / FAILED
↓
Event 开启下一阶段
```

### 核心方向

- Objective 负责“现在查什么”。
- Hotspot 负责“点哪里查”。
- Event 负责“触发什么”。
- Clue 负责“得到什么信息”。
- Flag 负责“状态是否发生”。
- Scene 负责“在哪里查”。
- Save 负责“下次回来还能不能恢复”。

---

## 十四、当前阶段结论

- 当前只做设计。
- 当前不开发。
- 当前不测试。
- 当前不进入版本链。
- 禁止直接开发 Investigation System。
- 后续如果进入开发，必须先走 Framework Freeze v1 的规则：已有系统内实现，不新增一级系统；接口状态从 `Reserved` 更新为 `Planned / In Progress / Implemented`。

