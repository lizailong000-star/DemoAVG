# Dialogue_Audit_Report.md - 对话系统审计报告

> 项目：《祝寿》Ren'Py DemoAVG 原型
> 审计基线版本：**v2.2l.1**
> 最近更新：2026-05-29 14:47
> 本文档仅为审计记录，不修改任何代码

---

## 〇、关键发现

**项目没有 `screens.rpy` 源文件！**

- `D:\renpy-8.5.3\DemoAVG\game\` 下只有 `gui.rpy`，没有 `screens.rpy` 也没有 `options.rpy`
- 但 `game/cache/screens.rpyb`（73,724 bytes）存在且正常编译
- 该 rpyb 是从 SDK 默认模板（`D:\renpy-8.5.3\gui\game\screens.rpy`，42,548 bytes）编译而来
- **这意味着所有 Ren'Py 原生 UI screen 都在运行，但源文件不可编辑**
- 如需自定义任何 screen，必须先从 SDK 模板复制 `screens.rpy` 到 `game/` 目录

---

## 一、功能审计总表

| 功能 | Ren'Py 原生支持 | 当前项目状态 | 是否可直接启用 | 备注 |
|------|----------------|-------------|---------------|------|
| Auto（自动播放） | ✅ 原生 | ⚠️ 隐式存在 | ✅ 是 | quick_menu 里有 Auto 按钮，`Preference("auto-forward", "toggle")`；但 explore_scene_test 是 modal=True 的 screen，可能遮挡 quick_menu |
| Skip（跳过已读） | ✅ 原生 | ⚠️ 隐式存在 | ✅ 是 | quick_menu 里有 Skip 按钮，`Skip()` action；Ctrl 键按住跳过也原生支持 |
| Skip Unseen（未读跳过） | ✅ 原生 | ⚠️ 隐式存在 | ✅ 是 | preferences screen 里有 "Unseen Text" 开关，`Preference("skip", "toggle")` |
| History（历史记录） | ✅ 原生 | ⚠️ 隐式存在 | ✅ 是 | quick_menu 里有 History 按钮 → ShowMenu('history')；`config.history_length = 250`；gui.rpy 有完整 history 布局参数 |
| Text Speed（文本速度） | ✅ 原生 | ⚠️ 被强压 | ⚠️ 部分可用 | preferences screen 有 `Preference("text speed")` 滑条；但 `init 999 python: _preferences.text_cps = 7` 会覆盖玩家设置 |
| Auto Forward Time | ✅ 原生 | ⚠️ 隐式存在 | ✅ 是 | preferences screen 有 `Preference("auto-forward time")` 滑条 |
| Hide UI（隐藏界面） | ✅ 原生 | ✅ 可用 | ✅ 是 | H 键隐藏，中键隐藏；SDK 默认 keymap 支持 |
| Quick Menu（快捷菜单） | ✅ 原生 | ⚠️ 隐式存在 | ⚠️ 部分可用 | screen 存在（Back/History/Skip/Auto/Save/Q.Save/Q.Load/Prefs），但可能被探索 screen 的 modal=True 遮挡 |
| Rollback（回滚） | ✅ 原生 | ✅ 可用 | ✅ 是 | Page Up / 鼠标滚轮上 回滚；quick_menu Back 按钮 = `Rollback()` |
| Save / Load | ✅ 原生 | ✅ 可用 | ✅ 是 | saves 目录已有 auto-1~10 + 手动存档；3×2 网格布局；Q.Save / Q.Load 可用 |

---

## 二、重点检查

### 2.1 quick_menu 是否保留？

**✅ 保留，隐式存在**

- SDK 默认 `screens.rpy` 里定义了 `screen quick_menu()`，包含 8 个按钮：Back / History / Skip / Auto / Save / Q.Save / Q.Load / Prefs
- `config.overlay_screens.append("quick_menu")` 已注册为 overlay screen
- `default quick_menu = True` 控制显示/隐藏
- gui.rpy 里定义了 `gui.quick_button_borders` / `gui.quick_button_text_size` 等样式参数

**⚠️ 但有以下问题：**

1. **被 modal screen 遮挡** —— `explore_scene_test` 声明了 `modal True`，这意味着 quick_menu 的按钮在探索模式下**可能无法点击**（modal screen 拦截所有输入）
2. **没有 gui/button 图片资源** —— `game/gui/` 目录不存在，SDK 默认的 `gui/button/` 目录也没复制过来，quick_menu 按钮样式可能回退到文字按钮
3. **没有 textbox.png** —— SDK 默认 say screen 引用 `gui/textbox.png`，但项目用 `style.say_window.background = Frame("images/ui/dialog_box.png")` 覆盖了

### 2.2 history screen 是否保留？

**✅ 保留，隐式存在**

- SDK 默认 `screens.rpy` 里有完整 `screen history()` 定义
- gui.rpy 里有完整 history 布局参数（height=140, name_xpos=150, text_xpos=170 等）
- `config.history_length = 250`（保留 250 条历史）
- quick_menu 的 History 按钮 → `ShowMenu('history')` 可直接打开

**是否可直接打开：✅ 是** —— 在对话模式下按 quick_menu 的 History 按钮或 Esc → History 即可

### 2.3 preferences screen 是否保留？

**✅ 保留，隐式存在**

- SDK 默认 `screens.rpy` 里有完整 `screen preferences()` 定义
- 包含以下设置项：
  - Display：窗口 / 全屏
  - Skip：Unseen Text / After Choices / Transitions
  - **Text Speed 滑条**（`Preference("text speed")`）
  - **Auto-Forward Time 滑条**（`Preference("auto-forward time")`）
  - Music Volume / Sound Volume / Voice Volume / Mute All

**是否已有文本速度调节：✅ 是** —— 但被 `_preferences.text_cps = 7` 强压覆盖

### 2.4 config.default_text_cps 与 _preferences.text_cps 对系统设置菜单的影响

**⚠️ 有冲突**

- `config.default_text_cps = 7`（systems_ui.rpy 第 105 行）—— 设默认值，正常
- `init 999 python: _preferences.text_cps = 7`（systems_ui.rpy 第 108 行）—— **每次启动都强制覆盖**
- 影响：玩家在 preferences 里拖 Text Speed 滑条改了速度 → 下次启动游戏时 `init 999` 又把速度压回 7
- preferences screen 的 Text Speed 滑条在当前版本**形同虚设**
- 正式版必须移除 `init 999` 那行

---

## 三、已有功能（可直接使用，不需要开发）

| # | 功能 | 启用方式 | 当前可用场景 |
|---|------|----------|-------------|
| 1 | Auto（自动播放） | quick_menu Auto 按钮 / Tab 键 | 对话模式 |
| 2 | Skip（跳过已读） | quick_menu Skip 按钮 / Ctrl 键 / Tab 键 | 对话模式 |
| 3 | Skip Unseen | preferences → "Unseen Text" 开关 | 设置菜单 |
| 4 | History（历史记录） | quick_menu History 按钮 / 鼠标滚轮上 | 对话模式 |
| 5 | Text Speed 调节 | preferences → Text Speed 滑条 | 设置菜单（但被强压） |
| 6 | Auto Forward Time | preferences → Auto-Forward Time 滑条 | 设置菜单 |
| 7 | Hide UI | H 键 / 鼠标中键 | 对话模式 |
| 8 | Quick Menu | 默认 overlay 显示 | 对话模式 |
| 9 | Rollback（回滚） | Page Up / 鼠标滚轮上 / quick_menu Back | 对话模式 |
| 10 | Save / Load | quick_menu Save/Load 按钮 / Esc → Save/Load | 对话模式 |
| 11 | Q.Save / Q.Load | quick_menu 按钮 | 对话模式 |
| 12 | Fullscreen / Window | preferences → Display | 设置菜单 |
| 13 | Volume 调节 | preferences → Music/Sound/Voice 滑条 | 设置菜单 |

---

## 四、缺失功能（需开发或需恢复）

| # | 功能 | 性质 | 工作量 |
|---|------|------|--------|
| 1 | **screens.rpy 源文件** | 🔴 必须恢复 | 复制 SDK 模板 → 微调 |
| 2 | 探索模式下 quick_menu 兼容 | 🟠 需开发 | 修改 explore_scene_test 的 zorder / 或在探索 screen 内加等效按钮 |
| 3 | 标点停顿（逗号/句号延迟） | 🟡 需开发 | `config.text_cps_delay` 或自定义 callback |
| 4 | 旁白节奏调整 | 🟡 需开发 | 剧情写作层面 |
| 5 | gui/button 等默认 GUI 美术资源 | 🟠 需补 | 复制 SDK 默认或自制 |

---

## 五、被隐藏功能（存在但未显现）

| # | 功能 | 隐藏原因 | 恢复方式 |
|---|------|----------|----------|
| 1 | quick_menu 快捷按钮 | explore_scene_test modal=True 遮挡 | 探索模式下加自定义快捷栏，或降低 modal screen 的 zorder |
| 2 | preferences Text Speed 滑条 | `_preferences.text_cps = 7` 强压 | 移除 init 999 那行 |
| 3 | skip_indicator（跳过指示器） | 正常存在但可能被遮挡 | 无需恢复，正常显示 |
| 4 | NVL 模式 | screens.rpy 里有定义但项目未用 | 不需要恢复（AVG 不用 NVL） |
| 5 | Bubble 模式 | screens.rpy 里有定义但项目未用 | 不需要恢复 |

---

## 六、可直接启用功能（不需要写代码）

| # | 功能 | 当前状态 | 启用条件 |
|---|------|----------|----------|
| 1 | Auto（自动播放） | ✅ 已启用 | 无，按 quick_menu Auto 即可 |
| 2 | Skip（跳过） | ✅ 已启用 | 无，Ctrl / quick_menu Skip 即可 |
| 3 | History（历史记录） | ✅ 已启用 | 无，quick_menu History 即可 |
| 4 | Rollback（回滚） | ✅ 已启用 | 无，Page Up 即可 |
| 5 | Save / Load | ✅ 已启用 | 无，quick_menu Save 即可 |
| 6 | Hide UI | ✅ 已启用 | 无，H 键即可 |

> 以上功能在**对话模式**下全部可用。只在**探索模式**（explore_scene_test modal=True）下 quick_menu 被遮挡。

---

## 七、不建议重做的功能

| # | 功能 | 理由 |
|---|------|------|
| 1 | Auto（自动播放） | Ren'Py 原生完整，包含 forward-time 调节，重做无意义 |
| 2 | Skip（跳过） | Ren'Py 原生完整，含 fast/confirm/seen-only 多种模式 |
| 3 | History（历史记录） | Ren'Py 原生完整，`_history_list` 自动维护，含 name/what/color |
| 4 | Rollback（回滚） | Ren'Py 核心机制，无法也不应重做 |
| 5 | Save / Load | Ren'Py 原生完整，含 auto/quick/manual + screenshot |
| 6 | preferences screen | Ren'Py 原生完整，含 display/skip/text speed/volume 全套 |
| 7 | quick_menu | Ren'Py 原生完整，只需处理探索模式遮挡问题 |

---

## 八、推荐开发顺序

### Phase 1：恢复源文件（P0，必须先做）

1. **从 SDK 模板复制 `screens.rpy` 到 `game/`** —— 当前项目没有源文件，无法自定义任何 screen
2. **复制 `options.rpy` 到 `game/`**（如果项目也没有的话）—— 用于配置游戏名/版本等
3. **移除 `init 999 python: _preferences.text_cps = 7`** —— 让 preferences 的 Text Speed 滑条生效

### Phase 2：解决遮挡（P1）

4. **探索模式 quick_menu 兼容** —— 方案 A：在 explore_scene_test 内加迷你快捷栏；方案 B：探索 screen 改为非 modal + zorder 控制
5. **补充 gui/button 等默认资源** —— 或自制统一风格的按钮图

### Phase 3：增强对话体验（P2）

6. **标点停顿** —— 句号/逗号处增加短暂停顿，提升阅读节奏
7. **旁白/角色对话区分** —— 可通过 Character 的 what_prefix/what_suffix 或不同样式区分

### Phase 4：Polish（P3）

8. **quick_menu 美化** —— 从文字按钮换为自定义图标
9. **自定义 say screen** —— 如果需要更灵活的对话框布局（但这是高危区，按 ART_ASSET_GUIDE.md 规则不动 say screen）
10. **history screen 中文化** —— 按钮标签、空历史提示等

---

## 九、总结

**核心结论：Ren'Py 已经提供了 90% 的对话系统功能，不需要重做任何一项。**

当前项目"看起来缺功能"的原因是：
1. **没有 screens.rpy 源文件** —— 所有原生 UI 都在运行但不可编辑
2. **探索模式 modal=True 遮挡了 quick_menu** —— 在对话模式下所有功能都可用
3. **_preferences.text_cps 被强压** —— preferences 滑条形同虚设

真正需要开发的新功能只有：
- 探索模式的快捷栏兼容
- 标点停顿
- 自定义 UI 美化

**千万不要重新发明轮子。** Auto / Skip / History / Rollback / Save/Load / Preferences 全部用原生就行。
