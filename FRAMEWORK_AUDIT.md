# FRAMEWORK_AUDIT.md - 框架冻结前审计

> 项目：《祝寿》Ren'Py DemoAVG 原型  
> 审计时间：2026-06-02 09:42  
> 审计范围：`FRAMEWORK_SPEC.md` / `MODULE_ARCHITECTURE.md`  
> 规则：本轮只改文档；不修改 `.rpy`、资源、剧情、UI；本轮结束前禁止开发功能。

---

## 一、检查结果总表

| 系统 | FRAMEWORK_SPEC.md 原状态 | MODULE_ARCHITECTURE.md 原状态 | 本轮处理 | 结论 |
|------|--------------------------|-------------------------------|----------|------|
| Event System 事件系统 | 缺失 | 缺失 | 新增 | 新增为触发中心 |
| Flag System 标记系统 | 缺失 | 缺失 | 新增 | 新增为状态记录中心 |
| Investigation System 调查目标系统 | 缺失 | 缺失 | 新增 | 新增为玩家当前目标系统 |
| Inventory System 物品系统 | 缺失 | 缺失 | 新增 | 新增为实体物品系统 |
| Camera System 镜头系统 | 已有 | 缺失 | 补入 MODULE_ARCHITECTURE.md | 已有 + 补齐 |
| Video System 视频系统 | 已有 | 缺失 | 补入 MODULE_ARCHITECTURE.md | 已有 + 补齐 |

---

## 二、已有 / 新增 / 暂缓 / 合并记录

| 系统 | 状态记录 | 处理说明 |
|------|----------|----------|
| Event System | 新增 | `FRAMEWORK_SPEC.md` 补字段与接口；`MODULE_ARCHITECTURE.md` 补模块说明 |
| Flag System | 新增 | `FRAMEWORK_SPEC.md` 补字段与接口；`MODULE_ARCHITECTURE.md` 补模块说明 |
| Investigation System | 新增 | `FRAMEWORK_SPEC.md` 补字段与接口；`MODULE_ARCHITECTURE.md` 补模块说明 |
| Inventory System | 新增 | `FRAMEWORK_SPEC.md` 补字段与接口；`MODULE_ARCHITECTURE.md` 补模块说明 |
| Camera System | 已有 / 补齐 | `FRAMEWORK_SPEC.md` 已有；本轮补入 `MODULE_ARCHITECTURE.md` |
| Video System | 已有 / 补齐 | `FRAMEWORK_SPEC.md` 已有；本轮补入 `MODULE_ARCHITECTURE.md` |
| 与 Clue System 合并 | 不合并 | Inventory 不并入 Clue；Flag 不并入 Clue |
| 与 Scene System 合并 | 不合并 | Objective 不并入 Scene；Video 不并入 Scene |
| 与 Explore System 合并 | 不合并 | Camera 不并入 Explore |
| 与 Label 合并 | 不合并 | Event 不并入 Label |
| 功能开发 | 暂缓 | 本轮只补框架，不开发功能，不进入版本链 |

---

## 三、Event System 审计结论

**用途：** 统一管理所有触发事件。

包括：

- 热点触发剧情
- 热点触发线索
- 热点触发场景切换
- 触发音效
- 触发视频
- 触发镜头
- 触发状态标记

**预留字段：**

```python
current_event_id = None
last_event_id = None
event_queue = []
event_lock = False
event_context = None
```

**预留接口：**

```python
def trigger_event(event_id, context=None):
    pass

def queue_event(event_id, context=None):
    pass

def finish_event(event_id):
    pass

def cancel_event(event_id):
    pass

def is_event_locked():
    pass
```

**结论：** Event System 是触发中心；不等于 Label。

---

## 四、Flag System 审计结论

**用途：** 统一管理剧情状态标记。

例如：是否调查过公告栏、是否获得旧通知、是否见过院长、是否进入过监控室、是否看过录像、是否触发过电话。

**预留字段：**

```python
flag_map = {}
flag_history = []
```

**预留接口：**

```python
def set_flag(flag_id, value=True):
    pass

def get_flag(flag_id, default=False):
    pass

def clear_flag(flag_id):
    pass

def has_flag(flag_id):
    pass
```

**结论：** Flag System 是状态记录中心；不等于 Clue。

---

## 五、Investigation System 审计结论

**用途：** 管理当前调查目标。

例如：去养老院大厅、查看公告栏、找到监控室、询问院长、获取值班表。

**预留字段：**

```python
current_objective_id = None
objective_state_map = {}
objective_history = []
```

**预留接口：**

```python
def start_objective(objective_id):
    pass

def complete_objective(objective_id):
    pass

def fail_objective(objective_id):
    pass

def get_current_objective():
    pass

def update_objective_state(objective_id, state):
    pass
```

**结论：** Investigation System 是玩家当前目标；Objective 不等于 Scene。

---

## 六、Inventory System 审计结论

**用途：** 管理可持有实体物品。

Inventory 与 Clue 不完全相同：Clue 是信息；Inventory 是实体物品。例如钥匙、录像带、手机、工牌、纸条、老照片。

**预留字段：**

```python
inventory_items = []
inventory_item_state_map = {}
```

**预留接口：**

```python
def add_item(item_id):
    pass

def remove_item(item_id):
    pass

def has_item(item_id):
    pass

def get_item_state(item_id):
    pass

def set_item_state(item_id, state):
    pass
```

**结论：** Inventory System 是实体物品中心；不等于 Clue。

---

## 七、系统关系说明

- Event System 是触发中心。
- Flag System 是状态记录中心。
- Investigation System 是玩家当前目标。
- Clue System 是信息收集。
- Inventory System 是实体物品。
- Scene System 负责场景流转。
- Camera / Video 是表现层系统。

---

## 八、合并 / 不合并规则

- Clue 不等于 Inventory。
- Flag 不等于 Clue。
- Event 不等于 Label。
- Objective 不等于 Scene。
- Video 不等于 Scene。
- Camera 不等于 Explore。

---

## 九、冻结前结论

- 本轮已检查 6 个系统。
- `FRAMEWORK_SPEC.md` 已补齐 Event / Flag / Investigation / Inventory，并确认 Camera / Video 已存在。
- `MODULE_ARCHITECTURE.md` 已补齐 Event / Flag / Investigation / Inventory / Camera / Video。
- `FRAMEWORK_AUDIT.md` 已创建，记录已有 / 新增 / 暂缓 / 合并结论。
- 本轮未修改任何 `.rpy`。
- 本轮未开发功能。


---

# Framework Freeze Rule

> 版本：Framework Freeze v1  
> 生效时间：2026-06-02 09:48  
> 目的：冻结当前一级系统框架，规范后续系统新增与预留接口，防止未来接口无限扩散。

## 一、Framework Freeze v1 当前冻结系统

当前一级系统冻结为：

1. Dialogue
2. Explore
3. Hotspot
4. Clue
5. Scene
6. Save
7. UI
8. Audio
9. Asset
10. Camera
11. Video
12. Event
13. Flag
14. Investigation
15. Inventory

以上系统作为 **Framework Freeze v1** 当前冻结。

---

## 二、框架预留规范

### 原则一：新增系统必须经过 Framework Audit

框架冻结后，允许新增系统，但必须经过 **Framework Audit** 审批后才能进入框架。

禁止：

- 想到一个功能，立即创建一个系统。
- 为单个剧情段或单个 UI 按钮临时创建一级系统。

### 原则二：预留接口必须有明确使用场景

预留接口必须至少存在一个明确使用场景。

例如：Camera System 对应养老院走廊、病房区、楼梯间，属于有效接口。

禁止：

- 为了“以后可能有用”预留接口。
- 没有场景、没有模块归属、没有依赖关系的空接口。

### 原则三：控制预留接口数量

一个系统优先只预留：

- 核心字段
- 核心接口

禁止：

- 一次性预留几十个未来可能永远不用的接口。
- 把 polish 想象空间全部写成接口。

### 原则四：所有预留接口必须可追踪

每个预留接口必须记录：

- 用途
- 所属模块
- 未来开发版本
- 依赖关系

缺少以上信息的接口，不允许进入框架。

### 原则五：接口状态分级

未进入开发计划的接口标记：`Reserved`

进入开发计划后标记：`Planned`

开始开发时标记：`In Progress`

开发完成后标记：`Implemented`

### 原则六：Framework Audit 必须清理接口

每次 Framework Audit 必须检查：

- 哪些接口从未使用
- 哪些接口已经过期
- 哪些接口需要删除

允许：

- 删除预留接口
- 合并重复接口
- 将不再需要的系统降级为模块内功能

不允许：

- 永久堆积预留接口
- 只增不删

### 原则七：新增一级系统条件

新增一级系统必须同时满足：

1. 现有系统无法承载
2. 有明确使用场景
3. 有状态字段与接口草案
4. 有依赖关系说明
5. 通过 Framework Audit

否则：优先归属到现有模块。

### 原则八：框架优先级

Framework Freeze v1 后，开发优先级不按“想做什么”决定，而按以下顺序判断：

1. 是否属于当前冻结系统
2. 是否已有状态字段
3. 是否已有预留接口
4. 是否通过 95% 完成度闸门
5. 是否通过老李手动测试
6. 是否建立 working 备份

---

## 三、接口状态表规范

| 状态 | 含义 | 是否允许开发 |
|------|------|--------------|
| `Reserved` | 已预留，但未进入近期开发计划 | 否 |
| `Planned` | 已进入开发计划，等待开工 | 否 |
| `In Progress` | 正在开发 | 是 |
| `Implemented` | 已完成并通过测试 | 是 |

---

## 四、冻结后下一阶段

框架冻结后，下一阶段进入：

**v2.2p Clue System Polish**

前提：不再新增一级系统，除非先通过 Framework Audit。

### Freeze Rule 关键词补充

- 允许删除预留接口，不允许永久堆积。
