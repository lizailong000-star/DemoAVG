# PROJECT_LOG.md - 项目开发主日志

> 项目：《祝寿》Ren'Py 2DAVG 原型（工程目录 DemoAVG）
> 引擎：Ren'Py 8.5.3
> 工程路径：`D:\renpy-8.5.3\DemoAVG\`
> 最近更新：2026-05-29 14:33

---

## 文档审计记录

| 审计 | 时间 | 输出文档 |
|------|------|----------|
| Audit-01 | 2026-05-29 14:12 | PROJECT_LOG.md / FEATURE_LIST.md / ASSET_LIST.md / MISSING_ASSETS.md / PLACEHOLDER_LIST.md / ROADMAP.md |
| Audit-03 | 2026-05-29 14:33 | TECH_DEBT.md / CONTENT_LIST.md / SCENE_FLOW.md（+ ROADMAP / PROJECT_LOG 同步） |

---

## 一、当前版本

- **代码当前版本**：`v2.2l.1`（文本打字机 7 cps）
- **最新 working 锁定**：`DemoAVG_backup_v2.2l1_text_cps_working`
- **下一计划版本**：`v2.2m`（方向待老李指定，本轮 Audit-01 不开发）

---

## 二、版本演进链（v2.1 → v2.2l.1）

```
v2.1  UI 基础版（头像 callback + dialog_box）
  ↓
v2.2a 横向探索分层场景原型（三层视差）
  ↓
v2.2d RPG 点击寻路（鼠标点击 + 平滑移动 + 镜头跟随）
  ↓
v2.2e 角色状态/朝向系统（idle/walking, left/right, xzoom 镜像）
  ↓
v2.2f 热点提示系统（靠近 → ★ 按 E 查看：xxx）
  ↓
v2.2g 热点可视化标记（世界坐标 ? / ★）
  ↓
v2.2h E 键交互（占位 action + 屏幕反馈）
  ↓
v2.2i 事件分发系统（trigger_hotspot_event + 中央弹窗）
  ↓
v2.2j 事件 → Label 调用（call_in_new_context 接剧情段）
  ↓
v2.2k 场景切换系统（scene_xxx 走 jump）
  ↓
v2.2l 线索系统接入探索（C 键查看 + add_clue）
  ↓
v2.2l.1 文本打字机效果（config.default_text_cps + preferences.text_cps = 7）
```

> 注：v2.2b/v2.2c 在迭代过程中被覆盖，未单独留 working。
> v2.2c-fix 在 v2.2d 中合并，未单独留 working。

---

## 三、所有正式 working 锁定备份

| 版本 | 锁定日期 | 路径 | 内容 |
|------|----------|------|------|
| v2.1 | 2026-05-29 09:48 | DemoAVG_backup_v2.1_ui_base_locked | UI 基础版（callback 头像 + dialog_box） |
| v2.2d | 2026-05-29 10:55 | DemoAVG_backup_v2.2d_rpg_click_move_working | 三层视差 + 点击寻路 + 镜头 |
| v2.2e | 2026-05-29 11:14 | DemoAVG_backup_v2.2e_player_state_facing_working | 状态机 + 朝向 xzoom |
| v2.2f | 2026-05-29 11:33 | DemoAVG_backup_v2.2f_hotspot_hint_working | 热点提示 |
| v2.2g | 2026-05-29 11:40 | DemoAVG_backup_v2.2g_hotspot_marker_working | 热点可视化标记 |
| v2.2h | 2026-05-29 12:14 | DemoAVG_backup_v2.2h_hotspot_interact_working | E 键交互（占位） |
| v2.2i | 2026-05-29 12:28 | DemoAVG_backup_v2.2i_event_dispatcher_working | 事件分发 + 中央弹窗 |
| v2.2j | 2026-05-29 13:04 | DemoAVG_backup_v2.2j_label_event_working | 事件→Label（call_in_new_context） |
| v2.2k | 2026-05-29 13:10 | DemoAVG_backup_v2.2k_scene_transition_working | 场景切换（scene_xxx → jump） |
| v2.2l | 2026-05-29 13:30 | DemoAVG_backup_v2.2l_clue_system_working | 线索系统 + C 键 + E 键全局 dismiss |
| **v2.2l.1** | **2026-05-29 13:47** | **DemoAVG_backup_v2.2l1_text_cps_working** | **文本打字机 7 cps（最新）** |

| **v2.2n** | **2026-05-29 15:52** | **DemoAVG_backup_v2.2n_scene_fix_and_choice_polish_working** | **场景切换修复 + 雨声调小 + 选项菜单居中** |

> 早期备份（v0.x ~ v1.x、v2.0）仍在磁盘上，为历史阶段成果，不在本轮焦点。

---

## 四、所有安全回滚点

按"功能完整 + 可独立运行"标准列出，从新到旧：

1. **v2.2l1_text_cps_working** ← 推荐回滚点（含完整 v2.2 探索全功能）
2. v2.2l_clue_system_working
3. v2.2k_scene_transition_working
4. v2.2j_label_event_working
5. v2.2d_rpg_click_move_working（最初探索基线）
6. v2.1_ui_base_locked（仅 UI 基础，不含探索）
7. v2.0_actual_assets_locked（v2.0 art 接入完成态）

> Pre 小备份（vXXpre_files_only）只含修改前的几个文件，不能整体回滚启动。

---

## 五、当前测试入口

| 入口 | 触发方式 | 用途 |
|------|----------|------|
| **【v2.2b TEMP】测试探索热点场景** | start menu 第一项 → jump `test_v22_explore` | v2.2 系列探索系统的唯一入口（开发中） |
| **正常剧情** | start menu 第二项 → jump `chapter_01_start` | 跑 v1.x 已有 AVG 主线（雨夜房间 → 活动室 → 走廊） |

测试 label 一览：
- `test_v22_explore` —— 主探索 screen
- `test_gate` / `test_notice_board` / `test_security_room` —— v2.2j 测试剧情段
- `scene_lobby` —— v2.2k 测试场景切换

---

## 六、当前技术决策（v2.2 阶段）

### 6.1 探索系统架构
- 横向 2000×720 大场景，三层视差（远 0.2 / 中 0.5 / 近 1.0）
- 鼠标点击寻路（timer 0.03 / 5px / tick）
- 角色状态机：`player_state = idle / walking`，`player_facing = left / right`，朝左用 `xzoom = -1.0` 镜像
- 热点判定：每 tick 算 `player_world_x` 与 `hotspot_data[*].world_x` 的距离，最近且 ≤ radius 的为 current_hotspot
- 热点交互：E 键触发 `explore_press_e()`，优先走 label，没有则 fallback 到 event 分发器

### 6.2 事件 / Label 调用约定
- 普通剧情段（如 test_gate）：用 `renpy.call_in_new_context(label_name)`，跑完自动回探索 screen
- 场景切换段（命名以 `scene_` 开头，如 scene_lobby）：用 `renpy.jump(label_name)`，原 screen 不保留

### 6.3 UI 架构
- 头像：Character callback + overlay screen + `renpy.restart_interaction()`，不动 say screen
- 对话框：`style.say_window.background = Frame("images/ui/dialog_box.png", 60, 60)`
- 打字机：`config.default_text_cps = 7` + `init 999 python: _preferences.text_cps = 7`（正式版上线前要去掉 init 999 那行，否则会强压玩家偏好）

### 6.4 线索系统
- 数据：`clue_list`（global）由 `systems_clue.rpy` 声明
- 添加：`add_clue(clue_id, title, desc)`（**3 参签名**）
- 查看：探索内 C 键 → `clue_test_screen`；旧 AVG 流程内 → `clue_log_screen`（两套查看 UI 并存，未合并）

### 6.5 按键约定
- E：探索 screen 内 = 触发热点；对话/menu 内 = dismiss（推进文本）
- C：探索 screen 内 = 打开线索表
- Esc / 右键：退出当前 screen / 返回

---

## 七、当前开发规则（硬性）

### 7.1 备份纪律
- **修改前先做 pre 小备份**（`vXXpre_files_only/`，只复制要改的文件，几秒）
- **测试通过后才建 working 完整备份**（`vXX_xxx_working/`，整个 DemoAVG 复制）
- 老李说"等测试通过再备份" ≠ "不做 pre 备份"

### 7.2 sub-version 流程
1. 新需求来 → 先 pre 备份要改的文件
2. 改 → lint 0 error → 错误字符串扫描
3. 给老李测试
4. 老李明确说"测试通过"后再建 working
5. 然后才允许进下一 sub-version

### 7.3 资源接入
- 不覆盖原图，派生到 `xxx_alpha/` 之类的并行目录
- 命名全小写下划线，不要中文文件名
- 背景：`bg_场景名.png`（1280×720，game/images/bg/）
- 头像：`角色名_表情.png`（game/images/avatar/）

### 7.4 记忆保存
- **每 10 分钟自动保存**进度/决定/未完事项到 `memory/YYYY-MM-DD.md`（硬规定）
- 长期值得记的（里程碑/规则/教训）也写入 `MEMORY.md`

### 7.5 沟通节奏
- 不要每句话"老李 XX"，他烦套话
- 干活直接干，不要废话
- 截图通道：老李把截图存 `D:\renpy-8.5.3\bug\N.png` 或 `screenshot.png`，AI 用 read 工具读
- 当前消息通道**收不到图片附件**（已验证 2026-05-28）

---

## 八、关键技术坑（已踩过，长期记）

> 完整列表见 `MEMORY.md` "Ren'Py 技术坑"段（共 16 条）。这里只列最高频：

1. **SL `add` 的 xpos 不能直接负数** → 必须用 `at Transform(xpos=int(value), ypos=0)`
2. **text 字面方括号 `[E]` 会被当变量插值** → 写 `★ 按 E` 或转义 `[[E]]` 或字符串拼接
3. **text 不能同时写 xpos 和 xalign** → 二选一
4. **同一变量 `default` 两次 = exception** → 加新文件前先 grep 已有 default
5. **config.default_text_cps 单独设可能不生效** → 必须同时 `init 999 python: _preferences.text_cps = N`
6. **场景切换 label 用 jump，剧情段用 call_in_new_context** → 命名约定 `scene_xxx`
7. **复用项目函数前先 read 签名** → `add_clue` 是 3 参不是 2 参
8. **renpy.notify 通知字小老李容易看不到** → 重要交互配屏幕中央大弹窗

---
