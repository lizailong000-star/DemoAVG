# 《祝寿》美术资源规范

## 总体风格

项目不是纯写实照片风格。

目标风格：
- 2D AVG 游戏背景
- 精致悬疑手绘感
- 中式恐怖氛围
- 参考《乌合之众》一类探索型悬疑 AVG 的气质
- 低饱和冷色
- 潮湿、阴郁、压抑
- 画面要有游戏美术感，不是摄影照片
- 不要夸张鬼片化
- 不要廉价恐怖海报
- 不要卡通低幼
- 不要纯照片写实

关键词：
精致悬疑手绘、低饱和、湿冷、暗部层次、中式现实恐怖、游戏背景图、可探索场景、留出 UI 空间。

## 背景图

**目录：** `game/images/bg/`
**尺寸：** 1280 × 720（横版 16:9，不带透明）
**格式：** `.png`（推荐）或 `.jpg`

| 文件名 | 用途 | 风格建议 |
|--------|------|----------|
| `bg_room_rainy.png` | 第一章：雨夜出租屋 | 暗灰冷调，窗外雨夜，烟灰缸+桌子 |
| `bg_activity_room.png | 第一章：养老院活动室 | 潮湿日光，红色"祝寿"横幅，塑料椅子 |
| `bg_corridor.png` | 第二章：养老院走廊 | 冷光走廊，护士站窗口+护理通知 |

**命名规则：** `bg_` 前缀 + 场景名（下划线小写）

## 角色立绘

**目录：** `game/images/character/`
**尺寸：** 推荐 600 × 1000（站姿，留头顶呼吸空间）
**格式：** `.png`（必须带透明背景）

| 文件名 | 用途 |
|--------|------|
| `zhou_weiguo_neutral.png` | 周卫国 - 平静 |
| `woman_staff_neutral.png` | 神秘女人 / 护工 / 王姐占位 |

**命名规则：** `角色名全拼_表情.png`（拼音小写）

## 头像

**目录：** `game/images/avatar/`
**尺寸：** 推荐 200 × 200
**格式：** `.png`（必须带透明背景）

| 文件名 | 用途 |
|--------|------|
| `zhou_neutral.png` | 周卫国头像 - 平静 |
| `zhou_worried.png` | 周卫国头像 - 担忧 |
| `zhou_shocked.png` | 周卫国头像 - 惊讶 |
| `nurse_neutral.png` | 女护士头像 - 平静 |
| `phone_voice.png` | 神秘电话来电头像 |

**命名规则：** `角色名_表情.png`（拼音小写）

## UI 资源

**目录：** `game/images/ui/`

当前 UI 暂不替换图片，继续使用现有资源（半透明对话框 + 头像框）。
后续可升级：
- 对话框底图
- 头像框
- 线索记录弹窗
- 调查按钮图标
- hover 高亮框

## 调查点小图标（可选）

**目录：** `game/images/hotspot/`
**尺寸：** 推荐 128 × 128 透明 PNG

| 文件名 | 用途 |
|--------|------|
| `hotspot_phone.png` | 手机 |
| `hotspot_table.png` | 桌子 |
| `hotspot_window.png` | 窗户 |
| `hotspot_door.png` | 门 |
| `hotspot_banner.png` | 祝寿字 |
| `hotspot_schedule.png` | 安排表 |
| `hotspot_chairs.png` | 座椅 |
| `hotspot_bucket.png` | 水桶 |
| `hotspot_notice.png` | 护理通知 |
| `hotspot_floor.png` | 地上水迹 |
| `hotspot_station.png` | 护士站 |
| `hotspot_camera.png` | 监控探头 |

## 手机屏幕状态图（可选）

**目录：** `game/images/phone/`
**尺寸：** 80 × 140

| 文件名 | 用途 |
|--------|------|
| `phone_off.png` | 熄屏 |
| `phone_on.png` | 亮屏（显示时间 23:17）|
| `phone_ring.png` | 来电闪烁 |

## 风格统一

- **主色调：** 暗色调（背景偏暗灰/深蓝）
- **强调色：** 橙黄 `#ffcc66`（标题/重要文字）
- **辅助色：** 冷蓝 `#66ccff`（已调查状态）
- **港片质感：** 偏冷光、潮湿、霓虹折射、雨夜倒影
- **避免：** 过亮、过饱和、卡通风格

## 注意事项

1. PNG 透明背景：立绘/头像必须透明，背景图必须不透明
2. 尺寸严格 16:9 比例（可做 1920×1080，比例必须对）
3. 文件名全小写 + 下划线，不要中文文件名
4. 图片由 ChatGPT 生成，OpenClaw 只负责接入工程

## 临时文件名备注

当前雨夜房间临时背景文件为：
`bg_room_rainy.png`

正式规范目标文件名为：
`bg_rainy_room.png`

后续正式替换时可以统一改名。

---

# v2.0 当前实际资源标准

## 1. 头像目录

路径：`images/avatar/`

当前使用：
- zhou_neutral.png
- zhou_worried.png
- zhou_shocked.png
- nurse_neutral.png
- phone_voice.png

说明：
- phone_voice.png 用于陌生电话/电话声音头像。
- 当前不使用 narrator.png。
- 当前头像原图尺寸为 1254×1254，暂不压缩到 256×256。

## 2. UI 目录

路径：`images/ui/`

当前使用：
- dialog_box.png
- frame_avatar.png

说明：
- dialog_box.png 是当前对话框底图标准文件名。
- frame_avatar.png 是当前头像框标准文件名。
- 当前不使用 images/avatar_frame/ 目录。
- 当前不拆分 frame_default / frame_protagonist / frame_npc。

## 3. 背景目录

路径：`images/bg/`

当前使用：
- bg_room_rainy.png
- bg_activity_room.png
- bg_corridor.png

## 4. 章节文件

当前第二章走廊文件名为：`chapter_02_corridor.rpy`

说明：
- corridor 为正确拼写。
- 不使用 chapter_02_coridor.rpy。

## 5. 当前可接受 lint warning

- zhou_weiguo_neutral.png not loadable
- woman_staff_neutral.png not loadable

说明：
这两个属于 character 立绘预留引用，不属于本轮 avatar 头像资源。
