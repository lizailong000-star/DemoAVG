# DIALOGUE_CONTROL_DESIGN.md

> 项目：《祝寿》DemoAVG 原型  
> 用途：对话控制系统设计文档  
> 原则：不重写 Ren'Py 默认 quick_menu，不复制 SDK screens.rpy，不一次性开发多个按钮。

---

## 1. 设计目标

当前项目已有：

- 对话框底板
- 头像 callback
- 打字机效果
- E 键推进文本
- Ren'Py 默认存档 / 读档 / 偏好设置能力

但当前缺少一个稳定、可控、适合本项目的对话控制逻辑。

本设计目标不是立即开发全部按钮，而是先确定：

- 哪些按钮应该有
- 哪些按钮互斥
- 哪些按钮可以共存
- 哪些场景中禁用
- 后续按什么顺序开发

---

## 2. 对话控制按钮范围

| 按钮 | 功能 | 当前建议 |
|---|---|---|
| Hide UI | 隐藏 / 显示对话框与控制按钮 | 优先做 |
| History | 查看历史对白 | 暂缓，需先确认可用入口 |
| Auto | 自动播放对白 | 后做 |
| Skip | 跳过对白 | 后做，风险高 |
| Fast | 临时加速打字机 | 可作为 Auto/Skip 前置 |
| Save | 打开存档 | 可保留，但不急 |
| Text Speed | 调整文字速度 | 后续做设置项 |

---

## 3. 全局状态机

建议维护一个轻量状态结构：

```renpy
default dialogue_auto = False
default dialogue_skip = False
default dialogue_fast = False
default dialogue_ui_hidden = False
default dialogue_panel_open = None
```

其中：

```text
dialogue_panel_open 可选值：
None
history
save
preferences
```

---

## 4. 按钮状态定义

### 4.1 Hide UI

| 状态 | 含义 |
|---|---|
| visible | 显示对话框、头像、控制按钮 |
| hidden | 隐藏对话框、头像、控制按钮 |

规则：

- Hide UI 不等于暂停剧情
- 鼠标点击 / E 键应恢复 UI 或推进文本，具体后续测试决定
- Hide UI 时不显示 Auto / Skip / Save / History 按钮

---

### 4.2 Auto

| 状态 | 含义 |
|---|---|
| off | 普通手动点击推进 |
| on | 自动播放对白 |

规则：

- Auto 只在普通对话场景可用
- 进入探索场景时自动关闭
- 打开 History / Save / Preferences 时自动暂停
- 玩家手动点击时是否关闭 Auto，后续测试决定；建议先不断开

---

### 4.3 Skip

| 状态 | 含义 |
|---|---|
| off | 不跳过 |
| skipping_read | 只跳过已读 |
| skipping_all | 跳过全部，危险，暂不推荐 |

规则：

- Skip 开启时必须关闭 Auto
- Skip 不应在探索场景启用
- Skip 不应在菜单选择中启用
- Skip 打开 History / Save 时自动停止
- 第一阶段不做 skipping_all

---

### 4.4 Fast

| 状态 | 含义 |
|---|---|
| normal | 默认 cps |
| fast_text | 临时提高 cps |
| instant_text | 瞬间显示当前句 |

规则：

- Fast 只影响当前文本显示速度
- Fast 不等于 Skip
- Fast 可以与 Auto 共存，但不建议第一阶段支持
- Fast 可以作为“点击一次显示完整句子”的已有行为保留

---

### 4.5 History

| 状态 | 含义 |
|---|---|
| closed | 不显示历史 |
| open | 打开历史面板 |

规则：

- History 打开时暂停 Auto
- History 打开时关闭 Skip
- History 打开时禁止继续推进剧情
- 当前项目 history_screen 入口不稳定，不能直接 ShowMenu("history") 硬接
- 后续应先做自定义轻量 History 或确认 Ren'Py 可用入口

---

### 4.6 Save

| 状态 | 含义 |
|---|---|
| closed | 不显示存档界面 |
| open | 打开存档界面 |

规则：

- Save 打开时暂停 Auto
- Save 打开时关闭 Skip
- Save 可以调用 Ren'Py 默认 ShowMenu("save")，但需确认 UI 不乱
- 探索场景是否允许 Save，需要后续单独测试

---

### 4.7 Text Speed

| 状态 | 含义 |
|---|---|
| slow | 慢速 |
| normal | 常规 |
| fast | 快速 |

当前项目特殊问题：

```renpy
config.default_text_cps = 7
init 999 python:
    _preferences.text_cps = 7
```

这会强制覆盖玩家设置。

后续正式方案：

- 删除 `_preferences.text_cps = 7`
- 保留 `config.default_text_cps`
- 允许玩家设置生效

---

## 5. 互斥规则

| 组合 | 规则 |
|---|---|
| Auto + Skip | 互斥，Skip 开启时 Auto 关闭 |
| Auto + History | History 打开时 Auto 暂停 |
| Auto + Save | Save 打开时 Auto 暂停 |
| Skip + History | History 打开时 Skip 关闭 |
| Skip + Save | Save 打开时 Skip 关闭 |
| Hide UI + History | History 打开时 UI 必须恢复 |
| Hide UI + Save | Save 打开时 UI 必须恢复 |
| 探索场景 + Auto | 禁用 |
| 探索场景 + Skip | 禁用 |
| 菜单选择 + Auto | 暂停 |
| 菜单选择 + Skip | 禁用 |

---

## 6. 输入规则

当前项目已有输入：

| 输入 | 当前用途 |
|---|---|
| E | 对话推进 / 探索互动 |
| C | 探索场景查看线索 |
| Esc | 退出 screen / 返回 |
| 右键 | 退出 screen / 返回 |
| 鼠标点击 | 推进文本 |
| Ctrl | Ren'Py 可能用于跳过 |
| H | Ren'Py 可能用于隐藏 UI |

建议：

| 功能 | 推荐输入 |
|---|---|
| Hide UI | H |
| Auto | 按钮优先，不急着绑定键盘 |
| Skip | Ctrl，先不自定义 |
| History | 按钮优先 |
| Save | 按钮优先 |
| Text Speed | 设置界面，不绑定快捷键 |

注意：

- 不要占用 C，C 已经给线索系统
- 不要改变 E 的现有双用途
- 不要让 Auto / Skip 在探索 screen 中响应

---

## 7. 场景限制

| 场景类型 | Auto | Skip | History | Save | Hide UI |
|---|---|---|---|---|---|
| 普通对白 | 可用 | 可用 | 可用 | 可用 | 可用 |
| 菜单选择 | 暂停 | 禁用 | 禁用 | 可用性待测 | 禁用 |
| v2.2 探索 | 禁用 | 禁用 | 暂缓 | 可用性待测 | 可用性待测 |
| 线索界面 | 禁用 | 禁用 | 禁用 | 禁用 | 禁用 |
| 存档界面 | 暂停 | 关闭 | 关闭 | 打开 | 禁用 |

---

## 8. 推荐开发顺序

### v2.2o：Hide UI

目标：

- 最小风险
- 不依赖 history / quick_menu / screens.rpy
- 只控制本项目已有 UI 显示状态

范围：

- H 键或小按钮隐藏 UI
- 再按一次恢复
- 不处理 Auto / Skip

---

### v2.2p：Text Speed 正式化

目标：

- 去掉 `_preferences.text_cps = 7`
- 保留默认 cps
- 让玩家设置可生效

范围：

- 不做复杂设置 UI
- 只修正强压偏好问题

---

### v2.2q：轻量 History 方案评估

目标：

- 不调用不存在的 history_screen
- 评估 Ren'Py 原生日志是否可读
- 或自建最小 history list

范围：

- 只做审计或最小原型
- 不重写完整 history screen

---

### v2.2r：Auto 自动播放

目标：

- 在普通对白中自动推进
- 遇到菜单 / 探索 / 线索界面自动暂停

范围：

- 先只支持普通对白
- 不支持探索场景

---

### v2.2s：Skip 跳过

目标：

- 跳过已读文本
- 不做跳过未读

范围：

- 不在探索中启用
- 不在菜单中启用

---

### v2.2t：对话控制栏 UI 整合

目标：

- 把 Hide / Auto / History / Save 等按钮做成统一控制栏
- 在前面功能稳定后再做

---

## 9. 不建议方案

明确禁止或暂缓：

1. 不复制 SDK 默认 screens.rpy  
   原因：与当前 gui.rpy 不兼容。

2. 不重写完整 quick_menu  
   原因：当前项目 quick_menu 源不可控，直接引用会报错。

3. 不直接调用 `ShowMenu("history")`  
   原因：当前已出现 `history_screen` label 缺失报错。

4. 不一次性开发 Auto + Skip + History + Save  
   原因：互斥逻辑复杂，容易引起 UI 闪烁和状态混乱。

5. 不在探索 screen 中启用 Auto / Skip  
   原因：探索是操作态，不是阅读态。

---

## 10. 第一阶段结论

当前对话系统完善不应从 Auto / Skip 开始。

建议第一步：

```text
v2.2o
Hide UI
```

理由：

- 风险最低
- 不依赖 Ren'Py 默认 screens
- 不依赖 quick_menu
- 不涉及自动推进
- 可以验证 UI 状态管理框架

完成 Hide UI 后，再处理 Text Speed 正式化。

---

## 11. 后续维护规则

每新增一个对话控制功能，必须更新：

- POLISH_AUDIT.md
- FEATURE_LIST.md
- PROJECT_LOG.md
- TECH_DEBT.md（如产生新债务）
- DIALOGUE_CONTROL_DESIGN.md（如规则变化）

每个功能单独版本、单独测试、单独 working。
