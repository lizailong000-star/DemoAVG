# ASSET_LIST.md - 资源清单

> 项目：《祝寿》DemoAVG 原型
> 最近更新：2026-05-29 14:05
> 状态标识：✅ 正式 / ⚠️ 占位 / ❌ 未制作

---

## 一、背景资源（game/images/bg/）

| 文件 | 用途 | 状态 | 大小 | 备注 |
|------|------|------|------|------|
| bg_room_rainy.png | 雨夜出租屋（Chapter 01 开场） | ✅ 正式 | 1.95 MB | 1280×720 |
| bg_activity_room.png | 养老院活动室（Chapter 01 后段） | ✅ 正式 | 2.06 MB | 1280×720 |
| bg_corridor.png | 养老院走廊（Chapter 02） | ✅ 正式 | 1.88 MB | 1280×720 |

## 二、探索场景占位背景（game/images/explore_placeholder/）

| 文件 | 用途 | 状态 | 大小 | 备注 |
|------|------|------|------|------|
| bg_far_placeholder.png | 远景视差层（0.2x） | ⚠️ 占位 | 8.7 KB | 2000×720 程序生成 |
| bg_mid_placeholder.png | 中景视差层（0.5x） | ⚠️ 占位 | 6.4 KB | 2000×720 程序生成 |
| bg_near_placeholder.png | 近景视差层（1.0x） | ⚠️ 占位 | 6.3 KB | 2000×720 程序生成 |
| player_placeholder.png | 玩家角色占位 | ⚠️ 占位 | 0.77 KB | 80×160 简笔小人 |

## 三、角色资源（game/images/character/）

| 文件 | 用途 | 状态 | 大小 | 备注 |
|------|------|------|------|------|
| char_placeholder.png | 周卫国早期占位立绘 | ⚠️ 占位 | 3.7 KB | v0.x 遗留，仅 intro_scene 用 |

## 四、头像资源（game/images/avatar/ 与 avatar_alpha/）

### 原始头像（avatar/）

| 文件 | 角色 / 表情 | 状态 | 大小 | 启用状态 |
|------|-------------|------|------|----------|
| zhou_neutral.png | 周卫国 中性 | ✅ 正式 | 1.74 MB | ✅ 启用 |
| zhou_worried.png | 周卫国 担忧 | ✅ 正式 | 1.71 MB | ❌ 未启用 |
| zhou_shocked.png | 周卫国 震惊 | ✅ 正式 | 1.72 MB | ❌ 未启用 |
| nurse_neutral.png | 护士 中性 | ✅ 正式 | 1.86 MB | ❌ 未启用 |
| phone_voice.png | 电话声 | ✅ 正式 | 1.61 MB | ❌ 未启用 |

### Alpha 镂空头像（avatar_alpha/）

| 文件 | 状态 | 大小 |
|------|------|------|
| zhou_neutral.png | ✅ 当前使用 | 1.95 MB |
| zhou_worried.png | ✅ 待用 | 1.91 MB |
| zhou_shocked.png | ✅ 待用 | 1.91 MB |
| nurse_neutral.png | ✅ 待用 | 2.06 MB |
| phone_voice.png | ✅ 待用 | 1.76 MB |

### 备份头像（avatar_backup_original_20260528/）
- 与 avatar/ 同名 5 张原图副本，做安全备份用，不参与运行时

## 五、UI 资源（game/images/ui/ 与 ui_alpha/）

| 文件 | 用途 | 状态 | 大小 | 备注 |
|------|------|------|------|------|
| ui/dialog_box.png | 对话框底板 | ✅ 正式 | 259 KB | 760×120 Frame 接入 |
| ui/frame_avatar.png | 头像框（外部边框） | ✅ 正式 | 843 KB | 160×160 |
| ui_alpha/frame_avatar_cutout.png | 头像框镂空版 | ✅ 正式 | 1.21 MB | 真镂空，alpha=0 中心 |

## 六、道具资源（game/images/props/）

| 文件 | 状态 | 备注 |
|------|------|------|
| （目录存在，无文件） | ❌ 未制作 | 待补：手机、宣传单、登记簿等 |

## 七、音效资源（game/audio/）

| 文件 | 用途 | 状态 | 大小 | 备注 |
|------|------|------|------|------|
| rain_loop.wav | 雨声循环 | ✅ 正式 | 6.17 MB | 大文件，可优化 |
| rain_loop.ogg | 雨声循环（压缩版） | ⚠️ 异常 | 62 B | 空文件，需重做 |
| phone_ring.wav | 电话铃声 | ✅ 正式 | 529 KB | |
| phone_ring.ogg | 电话铃声（压缩版） | ⚠️ 异常 | 62 B | 空文件，需重做 |
| knock.wav | 敲门声 | ✅ 正式 | 264 KB | |

## 八、BGM 资源

| 状态 | 备注 |
|------|------|
| ❌ 未制作 | 当前仅环境音 rain_loop 当 BGM 用，无专属配乐 |

## 九、字体（项目根 simhei.ttf）

| 文件 | 用途 | 状态 | 备注 |
|------|------|------|------|
| simhei.ttf | 中文字体 | ✅ 正式 | 已配置 init 0 强制使用 |

---

## 统计

- 背景：3 ✅ / 3 ⚠️ / 0 ❌
- 角色：0 ✅ / 1 ⚠️ / 多 ❌（详见 MISSING_ASSETS.md）
- 头像：5 ✅ 启用 1 / 待用 4
- UI：3 ✅
- 道具：0 ✅ / 全 ❌
- 音效：3 ✅ / 2 ⚠️（ogg 空文件）/ 部分 ❌
- BGM：全 ❌
