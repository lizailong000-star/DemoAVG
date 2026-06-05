# PLACEHOLDER_LIST.md - 占位资源 / 测试内容清单

> 项目：《祝寿》DemoAVG 原型
> 最近更新：2026-05-29 14:05
> 用途：列出所有"临时占位"的资源、Label、Screen，正式接入后逐项清零。

---

## 一、占位资源（图）

| 占位文件 | 类型 | 当前用途 | 替换为 | 状态 |
|----------|------|----------|--------|------|
| explore_placeholder/bg_far_placeholder.png | 背景 | 探索远景视差层 | 正式美术（养老院远景） | ⚠️ 待替换 |
| explore_placeholder/bg_mid_placeholder.png | 背景 | 探索中景视差层 | 正式美术（养老院中景） | ⚠️ 待替换 |
| explore_placeholder/bg_near_placeholder.png | 背景 | 探索近景视差层 | 正式美术（养老院地面） | ⚠️ 待替换 |
| explore_placeholder/player_placeholder.png | 角色 | 玩家行走单帧 | 周卫国行走精灵图（多帧） | ⚠️ 待替换 |
| character/char_placeholder.png | 角色 | 雨夜出租屋 intro_scene 立绘 | 周卫国正式立绘 | ⚠️ 待替换 |
| systems_ui.rpy `image bg_room_dark` | 背景 | 通用暗背景 Solid | 视情况可保留 | ⚠️ 待评估 |
| systems_ui.rpy `image char_placeholder` | 角色 | Solid 420×720 灰块 | 周卫国正式立绘 | ⚠️ 待替换 |
| systems_ui.rpy `image phone_off/on/ring_flash/glow_strong` | 道具 | Solid 色块表示手机不同状态 | 正式手机道具图 + Idle/亮屏/响铃帧 | ⚠️ 待替换 |
| systems_ui.rpy `image black_overlay` | 特效 | Solid 1280×720 黑屏 | 可保留 | ✅ 通用 |
| scene_test.rpy `image bg_lobby_placeholder` | 背景 | 大厅紫色 Solid | 养老院大厅正式背景 | ⚠️ 待替换 |

---

## 二、占位 Label / 剧情段

| Label | 文件 | 当前内容 | 替换为 | 状态 |
|-------|------|----------|--------|------|
| test_gate | event_test.rpy | 2 句台词 + 加 1 条占位线索 | 正式"养老院大门"剧情段 | ⚠️ 占位 |
| test_notice_board | event_test.rpy | 2 句台词 + 加 1 条占位线索 | 正式"公告栏"剧情段 | ⚠️ 占位 |
| test_security_room | event_test.rpy | 2 句台词 + 加 1 条占位线索 | 正式"保安室"剧情段 | ⚠️ 占位 |
| scene_lobby | scene_test.rpy | 紫色 Solid + 3 句台词 + 返回 menu | 正式"养老院大厅"探索 / 剧情 | ⚠️ 占位 |
| back_to_explore | scene_test.rpy | jump test_v22_explore | 可保留作返回工具 label | ✅ 通用 |
| chapter_02_placeholder | chapter_end.rpy | 转场到 chapter_02_start | 可保留 | ✅ 通用 |

---

## 三、占位 Screen / UI

| Screen | 文件 | 当前形态 | 替换为 | 状态 |
|--------|------|----------|--------|------|
| explore_scene_test | explore_scene.rpy | 黑底白字调试 HUD + 占位视差 | 正式探索 UI（去 HUD / 接美术） | ⚠️ 调试用 |
| clue_test_screen | clue_test.rpy | 黑底列表（仅标题） | 完整线索详情 UI | ⚠️ 占位 |
| chapter_end_screen | chapter_end.rpy | 黑底标题 + 2 个 textbutton | 章节结尾过场美化 | ⚠️ 占位 |

---

## 四、占位入口（start menu）

| 选项 | 当前指向 | 替换为 | 状态 |
|------|----------|--------|------|
| **【v2.2b TEMP】测试探索热点场景** | jump test_v22_explore | 正式接入剧情主线后移除 | ⚠️ TEMP |
| **正常剧情** | jump chapter_01_start | 正式主菜单 → 新游戏 | ⚠️ 临时 |

---

## 五、占位热点数据（explore_scene.rpy `hotspot_data`）

| id | name | 当前 label | 替换为 | 状态 |
|----|------|------------|--------|------|
| gate | 养老院大门 | test_gate | 正式剧情段 | ⚠️ 占位 |
| notice_board | 公告栏 | test_notice_board | 正式剧情段 | ⚠️ 占位 |
| security_room | 保安室 | test_security_room | 正式剧情段 | ⚠️ 占位 |
| to_lobby | 进入大厅 | scene_lobby | 正式大厅场景 | ⚠️ 占位 |

---

## 六、占位 HUD 显示

调试 HUD 在 v2.2 探索 screen 内长期开启，正式版要全部移除或改为开发者菜单切换：

- world_x / target_x / screen_x / camera_x 数值
- state / facing 文字
- hotspot 名称 / id
- last_hotspot_action
- last_event
- current_scene
- Clues 计数
- "按 C 查看线索" 提示

---

## 七、占位音效（ogg 空文件）

- ⚠️ audio/rain_loop.ogg（62 B 空文件）—— 需重新编码
- ⚠️ audio/phone_ring.ogg（62 B 空文件）—— 需重新编码

> wav 版本正常工作，ogg 是为了体积优化预留的占位。

---

## 八、占位文本（强压玩家偏好）

| 文件 | 占位代码 | 替换 / 移除时机 |
|------|----------|----------------|
| systems_ui.rpy | `init 999 python: _preferences.text_cps = 7` | 正式版上线前移除（否则强压玩家偏好） |

---

## 九、占位备份命名

| 备份名 | 状态 | 备注 |
|--------|------|------|
| DemoAVG_backup_v2.2b_hotspot_current_snapshot | ⚠️ 临时快照 | v2.2b 阶段紧急快照，已被 v2.2d 取代，可清理 |

---

## 占位清零进度

- 总占位项：~30 项
- 已清零：0 项
- 待办：30 项

> 每项替换为正式资源/Label 后，在此表里勾掉并删行。
