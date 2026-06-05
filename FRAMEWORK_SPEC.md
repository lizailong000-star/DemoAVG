# FRAMEWORK_SPEC.md - 系统框架设定与预留接口规范

> 项目：《祝寿》Ren'Py DemoAVG 原型  
> 当前基线：v2.2o（`DemoAVG_backup_v2.2o_hide_ui_disable_key_working`）  
> 创建时间：2026-06-02 09:26  
> 用途：确定各系统的基础设定项、状态字段、预留接口。暂不开发的功能也先预留字段和接口位置，避免后期推翻重做。

---

## 一、全局设计原则

1. **一个系统一个模块**
   - Dialogue / Explore / Clue / Scene / UI / Audio / Save / Asset 各自独立管理。
   - 不把多个系统的状态混写在同一个临时变量里。

2. **一个功能一个状态**
   - 每个功能必须有明确状态字段。
   - 例如 Auto 用 `dialogue_auto_enabled`，Skip 用 `dialogue_skip_enabled`，不要共用一个含糊变量。

3. **先配置，后逻辑**
   - 新功能先登记配置项、状态字段、默认值，再写具体逻辑。
   - 不允许在剧情正文里临时硬写功能参数。

4. **先接口，后实现**
   - 暂不开发的功能也先预留函数名和调用入口。
   - 后续实现时只补函数体，不改调用方结构。

5. **不重复造系统**
   - 已有 `clue_list / add_clue()` 就不要另起一套线索系统。
   - 已有 Explore System 就不要在新文件里再写一套不兼容的移动 / 热点逻辑。

6. **未实现功能先留字段，不写死**
   - Auto / Skip / History / Save 状态先留字段。
   - 即使当前不开放，也不能把未来扩展路径写死。

7. **状态字段必须可存档**
   - 所有长期状态字段都要考虑 Save System。
   - 临时 UI 状态与长期玩法状态必须区分。

8. **95% 完成度闸门**
   - 未达到 95%、未通过老李手动测试、未建 working 的功能，不允许进入下一功能。
   - 闸门结果同步记录到 `POLISH_AUDIT.md`。

---

## 二、全局状态字段规划

| 字段 | 类型建议 | 所属模块 | 当前是否已有 | 说明 |
|------|----------|----------|--------------|------|
| `current_scene_id` | string | Scene / Explore | 部分已有 | 当前场景 id，统一替代散落的 `scene_id` 用法 |
| `current_chapter_id` | string | Scene | 部分已有 | 当前章节 id，统一替代散落的 `chapter_id` 用法 |
| `current_mode` | string enum | Global / UI | 待建 | 当前模式：`dialogue` / `explore` / `menu` / `cutscene` / `system` |
| `dialogue_state` | dict | Dialogue | 待建 | 对话系统总状态，包含 auto / skip / history / cps / speaker 等 |
| `explore_state` | dict | Explore | 待建 | 探索系统总状态，包含 player、camera、hotspot 等 |
| `clue_state` | dict | Clue | 待建 | 线索系统总状态，包含已获得、已读、分类、来源等 |
| `ui_state` | dict | UI | 待建 | UI 显隐、HUD、控制栏、debug HUD、panel 状态 |
| `audio_state` | dict | Audio | 待建 | 当前 BGM / ambient / 音量 / channel 状态 |

### 全局状态建议结构

```renpy
# 仅作为框架草案；当前文档不要求立刻写入 .rpy。
default current_scene_id = ""
default current_chapter_id = ""
default current_mode = "dialogue"

default dialogue_state = {}
default explore_state = {}
default clue_state = {}
default ui_state = {}
default audio_state = {}
```

---

## 三、Dialogue System 设定项

### 3.1 状态字段规划

| 字段 | 类型建议 | 默认值建议 | 当前状态 | 说明 |
|------|----------|------------|----------|------|
| `dialogue_auto_enabled` | bool | `False` | 预留 | Auto 自动播放是否开启 |
| `dialogue_skip_enabled` | bool | `False` | 预留 | Skip 跳过是否开启 |
| `dialogue_fast_mode` | bool | `False` | 预留 | 快速显示 / 快进模式 |
| `dialogue_history_enabled` | bool | `True` | 预留 | 是否允许打开历史记录 |
| `dialogue_ui_hidden` | bool | `False` | 已有 / 保留 | Hide UI 逻辑状态；当前 H 键禁用，不开放给玩家 |
| `dialogue_text_cps` | int | `7` | 部分已有 | 文本显示速度；当前通过 `config.default_text_cps` 和 `_preferences.text_cps` 强制 7 cps |
| `dialogue_current_speaker` | string / None | `None` | 预留 | 当前说话人 |
| `dialogue_current_line_id` | string / None | `None` | 预留 | 当前对白行 id，用于历史、已读、回放 |
| `dialogue_read_lines` | set / dict | `{}` | 预留 | 已读对白集合，用于 Skip 已读逻辑 |

### 3.2 预留接口

```renpy
# 当前暂不开发 Auto / Skip / History，只预留接口位置。
# 后续实现时必须接入互斥规则与 current_mode。

def enable_auto():
    pass

def disable_auto():
    pass

def enable_skip():
    pass

def disable_skip():
    pass

def open_history():
    pass

def close_history():
    pass

def set_text_speed(cps):
    pass

def record_dialogue_line(line_id, speaker, text):
    pass
```

### 3.3 当前说明

- 当前暂不开发 Auto / Skip / History，只预留字段和接口。
- Hide UI 逻辑保留，但快捷键屏蔽。
- H 键当前不触发自定义 Hide UI，也不触发 Ren'Py 原生 `hide_windows`。
- 后续若恢复 Hide UI，必须先补完整 UI 架构，不再临时 patch 默认 say screen。

### 3.4 互斥规则

- Auto 与 Skip 互斥。
- History 打开时暂停 Auto / Skip。
- Save 打开时暂停 Auto / Skip。
- 探索场景禁用 Auto / Skip。
- Hide UI 不得改变对白推进状态。
- `dialogue_current_line_id` 必须先记录，再进入下一句。

---

## 四、Explore System 设定项

### 4.1 状态字段规划

| 字段 | 类型建议 | 默认值建议 | 当前状态 | 说明 |
|------|----------|------------|----------|------|
| `current_scene_id` | string | `""` | 部分已有 | 当前探索场景 id |
| `player_world_x` | int / float | `300` | 已有 | 玩家世界坐标 x |
| `player_state` | string enum | `"idle"` | 已有 | `idle` / `walking` / 未来可扩展 `interacting` |
| `player_facing` | string enum | `"right"` | 已有 | `left` / `right` |
| `camera_x` | int / float | `0` | 部分已有 | 建议统一字段；当前实现为 `explore_camera_x` |
| `current_hotspot` | dict / None | `None` | 已有 | 当前可交互热点 |
| `hotspot_enabled_map` | dict | `{}` | 预留 | 每个热点是否启用 |
| `hotspot_visited_map` | dict | `{}` | 预留 | 每个热点是否已访问 / 已调查 |

### 4.2 预留接口

```renpy
def enter_scene(scene_id):
    pass

def exit_scene(scene_id):
    pass

def move_player_to(world_x):
    pass

def enable_hotspot(hotspot_id):
    pass

def disable_hotspot(hotspot_id):
    pass

def mark_hotspot_visited(hotspot_id):
    pass
```

### 4.3 说明

- `camera_x` 是框架命名，当前代码里的 `explore_camera_x` 可作为实现字段。
- `hotspot_enabled_map` 用于剧情控制热点显隐。
- `hotspot_visited_map` 用于保存玩家是否调查过热点。

---

## 五、Clue System 设定项

### 5.1 状态字段规划

| 字段 | 类型建议 | 默认值建议 | 当前状态 | 说明 |
|------|----------|------------|----------|------|
| `clue_list` | list | `[]` | 已有 | 已获得线索列表 |
| `clue_seen_map` | dict | `{}` | 预留 | 线索是否已读 / 已查看 |
| `clue_category_map` | dict | `{}` | 预留 | 线索分类，如人物 / 地点 / 物证 / 记忆 |
| `clue_source_map` | dict | `{}` | 预留 | 线索来源，如场景 id / 热点 id / 剧情段 |
| `clue_time_map` | dict | `{}` | 预留 | 线索获得时间或剧情时间 |

### 5.2 预留接口

```renpy
def add_clue(clue_id, title, desc):
    pass

def remove_clue(clue_id):
    pass

def mark_clue_read(clue_id):
    pass

def get_clue_detail(clue_id):
    pass

def get_clues_by_category(category):
    pass

def has_clue(clue_id):
    pass
```

### 5.3 说明

- 当前项目已有 `add_clue(id, title, desc)` 三参签名，后续不得改成两参。
- `clue_list` 不得重复 `default`。
- 线索 polish 前必须先统一 v1.x `clue_log_screen` 与 v2.2 `clue_test_screen` 的分工。

---

## 六、Scene System 设定项

### 6.1 状态字段规划

| 字段 | 类型建议 | 默认值建议 | 当前状态 | 说明 |
|------|----------|------------|----------|------|
| `scene_id` | string | `""` | 已有 | 当前场景 id |
| `scene_type` | string enum | `"dialogue"` | 预留 | `dialogue` / `explore` / `cutscene` / `menu` |
| `scene_entry_point` | string | `""` | 预留 | 场景入口 label 或 screen |
| `scene_exit_points` | list / dict | `[]` | 预留 | 可离开的出口列表 |
| `scene_background_layers` | list | `[]` | 预留 | 背景层，支持横向探索多层视差 |
| `scene_music` | string / None | `None` | 预留 | 场景默认 BGM |
| `scene_ambient` | string / None | `None` | 预留 | 场景默认环境音 |
| `scene_default_player_x` | int | `300` | 预留 | 进入探索场景时玩家默认位置 |

### 6.2 预留接口

```renpy
def load_scene(scene_id):
    pass

def unload_scene(scene_id):
    pass

def switch_scene(from_scene_id, to_scene_id):
    pass

def return_to_previous_scene():
    pass

def save_scene_state(scene_id):
    pass

def restore_scene_state(scene_id):
    pass
```

### 6.3 说明

- `scene_*` label 走 `renpy.jump`。
- 普通剧情段走 `renpy.call_in_new_context`。
- 场景切换前必须清理旧 screen，避免 HUD 残留。

---

## 七、UI System 设定项

### 7.1 状态字段规划

| 字段 | 类型建议 | 默认值建议 | 当前状态 | 说明 |
|------|----------|------------|----------|------|
| `ui_mode` | string enum | `"dialogue"` | 预留 | UI 当前模式：dialogue / explore / menu / system |
| `hud_visible` | bool | `True` | 预留 | 普通 HUD 是否显示 |
| `debug_hud_visible` | bool | `False` | 预留 | Debug HUD 是否显示 |
| `dialogue_controls_visible` | bool | `False` | 预留 | 对话控制栏是否显示 |
| `clue_panel_visible` | bool | `False` | 预留 | 线索面板是否显示 |
| `choice_style_mode` | string enum | `"centered"` | 部分已有 | choice 菜单样式模式 |

### 7.2 预留接口

```renpy
def show_hud():
    pass

def hide_hud():
    pass

def show_debug_hud():
    pass

def hide_debug_hud():
    pass

def open_clue_panel():
    pass

def close_clue_panel():
    pass
```

### 7.3 说明

- 当前项目没有 `screens.rpy` 源文件，不允许直接 patch cache/screens.rpyb。
- 后续自定义 UI 应优先放在独立 screen / overlay 中，并明确层级。
- 探索 `modal True` 时，不应让对话控制栏抢输入。

---

## 八、Audio System 设定项

### 8.1 状态字段规划

| 字段 | 类型建议 | 默认值建议 | 当前状态 | 说明 |
|------|----------|------------|----------|------|
| `current_bgm` | string / None | `None` | 预留 | 当前 BGM id / path |
| `current_ambient` | string / None | `None` | 预留 | 当前环境音 id / path |
| `bgm_volume` | float | `1.0` | 预留 | BGM 音量 |
| `ambient_volume` | float | `1.0` | 预留 | 环境音音量 |
| `sfx_volume` | float | `1.0` | 预留 | 音效音量 |
| `voice_volume` | float | `1.0` | 预留 | 语音音量 |

### 8.2 预留接口

```renpy
def play_bgm(bgm_id, fadein=0.0):
    pass

def stop_bgm(fadeout=0.0):
    pass

def play_ambient(ambient_id, fadein=0.0):
    pass

def stop_ambient(fadeout=0.0):
    pass

def play_sfx(sfx_id):
    pass

def set_volume(channel, volume):
    pass
```

### 8.3 说明

- BGM / Ambient / SFX / Voice 应分 channel 管理。
- 场景切换时应由 Scene System 提供默认音乐和环境音。
- Save System 应保存当前音频状态，用于读档恢复。

---

## 九、Save System 设定项

### 9.1 需要保存的状态

| 保存项 | 来源模块 | 字段建议 | 说明 |
|--------|----------|----------|------|
| 当前章节 | Scene | `current_chapter_id` | 当前剧情章节 |
| 当前场景 | Scene | `current_scene_id` | 当前场景 id |
| 玩家位置 | Explore | `player_world_x` / `camera_x` | 探索读档恢复位置 |
| 已获得线索 | Clue | `clue_list` | 玩家已获得线索 |
| 已读对白 | Dialogue | `dialogue_read_lines` | 支持 Skip 已读逻辑 |
| 已访问热点 | Explore / Hotspot | `hotspot_visited_map` | 防重复调查 / 控制反馈 |
| 当前音频状态 | Audio | `audio_state` | 当前 BGM、环境音、音量 |
| 当前 UI 状态 | UI | `ui_state` | 仅保存必要长期 UI 状态，不保存临时弹窗 |

### 9.2 预留接口

```renpy
def save_game_state():
    pass

def load_game_state():
    pass

def serialize_scene_state(scene_id):
    pass
def restore_scene_state(scene_id, state_data):
    pass
```

### 9.3 说明

- Save System 不应直接散落在剧情正文里。
- 先定义可序列化状态，再接 UI 入口。
- 临时状态如弹窗倒计时、hover 状态、瞬时动画不进入长期存档。

---

## 十、Asset System 设定项

### 10.1 资源字段规划

| 字段 | 类型建议 | 说明 |
|------|----------|------|
| `asset_id` | string | 资源唯一 id |
| `asset_type` | string enum | `bg` / `avatar` / `character` / `ui` / `audio` / `explore` / `effect` |
| `asset_path` | string | 文件路径 |
| `asset_status` | string enum | `placeholder` / `official` / `deprecated` / `missing` |
| `placeholder_of` | string / None | 如果是占位资源，记录它占位的正式资源 id |
| `replacement_target` | string / None | 替换目标路径或资源 id |

### 10.2 资源状态

| 状态 | 含义 | 使用规则 |
|------|------|----------|
| `placeholder` | 占位资源 | 可用于原型，不可当正式资源发布 |
| `official` | 正式资源 | 可用于稳定版 / 展示版 |
| `deprecated` | 已废弃资源 | 不再新增引用，后续清理 |
| `missing` | 缺失资源 | 文档登记，等待补齐 |

### 10.3 预留接口

```renpy
def register_asset(asset_id, asset_type, asset_path, asset_status="placeholder"):
    pass

def get_asset_path(asset_id):
    pass

def mark_asset_official(asset_id):
    pass

def mark_asset_deprecated(asset_id):
    pass

def list_missing_assets():
    pass
```

### 10.4 说明

- 资源派生不覆盖原图。
- 非必要下载内容默认存放 `D:\下龙虾下载`，用完清理。
- 项目资源命名：全小写下划线，不用中文文件名。
- 背景：`bg_场景名.png`。
- 头像：`角色名_表情.png`。

---

## 十一、禁止事项

1. **不允许临时变量无限扩散**
   - 新变量必须登记到对应系统。
   - 临时变量只允许在局部 screen / function 内短期使用。

2. **不允许同一功能出现两套系统**
   - 线索系统只能有一套核心数据源。
   - 热点系统只能有一套正式数据结构。
   - v1.x 与 v2.2 并行系统后续必须合并或明确边界。

3. **不允许直接写死剧情跳转**
   - 场景跳转必须走 Scene System 规范。
   - `scene_*` 用 jump，普通剧情段用 call_in_new_context。

4. **不允许未登记状态字段就开发功能**
   - Auto / Skip / History / Save / Clue Detail 等功能开发前，必须先登记字段和接口。

5. **不允许绕过 95% 完成度闸门**
   - 未通过老李手动测试，不建 working。
   - 未建 working，不允许标记允许进入下一功能。
   - `POLISH_AUDIT.md` 必须同步记录闸门结果。

6. **不允许直接修改 SDK / cache 编译产物**
   - 不修改 `cache/screens.rpyb`。
   - 不把 SDK 默认 `screens.rpy` 直接复制进项目后硬补变量。

7. **不允许在 UI 架构未设计时硬加单点功能**
   - Auto / Skip / History / Save / Hide UI 这类 UI 生态功能必须先做架构设计。

8. **不允许覆盖原始资源**
   - 透明头像、裁剪图、测试图等派生资源必须放并行目录。

---

## 十二、模块字段登记清单

| 模块 | 必填字段是否已规划 | 预留接口是否已规划 | 备注 |
|------|------------------|------------------|------|
| Dialogue System | 是 | 是 | Auto / Skip / History 暂不开发，只预留 |
| Explore System | 是 | 是 | `camera_x` 与现有 `explore_camera_x` 后续需统一 |
| Clue System | 是 | 是 | 保持 `add_clue(id, title, desc)` 三参签名 |
| Scene System | 是 | 是 | 需统一 v1.x 与 v2.2 场景状态 |
| UI System | 是 | 是 | 不直接改原生 screens/cache |
| Audio System | 是 | 是 | 后续需规划 channel |
| Save System | 是 | 是 | 先序列化状态，再做 UI 入口 |
| Asset System | 是 | 是 | 与资源清单文档联动维护 |
| Camera System | 是 | 是 | 当前只预留接口，不开发；等 Dialogue / Clue / Scene 达到 95% 后再进入版本链 |
| Video System | 是 | 是 | 当前只预留接口，不开发；等 Dialogue / Clue / Scene 达到 95% 后再进入版本链 |

---

## 十三、后续执行顺序建议

1. 先根据本文件创建或整理各系统配置区。
2. 再为即将开发的功能补默认字段。
3. 然后实现预留接口的函数体。
4. 最后接入 screen / label / action。
5. 每个 sub-version 完成后更新：
   - `FEATURE_LIST.md`
   - `POLISH_AUDIT.md`
   - `MODULE_ARCHITECTURE.md`
   - 本文件对应字段状态

---

## 十四、当前结论

- 本文件只定义框架，不要求本轮改 `.rpy`。
- 当前最重要原则：**未开发功能先预留接口，不写死，不重复造系统。**
- 后续任何功能开发，都应先检查本文件是否已有字段和接口。

---

## 十五、预留接口索引（按审阅名原样列出）

### Dialogue System

- `enable_auto()`
- `disable_auto()`
- `enable_skip()`
- `disable_skip()`
- `open_history()`
- `close_history()`
- `set_text_speed()`
- `record_dialogue_line()`

### Explore System

- `enter_scene()`
- `exit_scene()`
- `move_player_to()`
- `enable_hotspot()`
- `disable_hotspot()`
- `mark_hotspot_visited()`

### Clue System

- `add_clue()`
- `remove_clue()`
- `mark_clue_read()`
- `get_clue_detail()`
- `get_clues_by_category()`
- `has_clue()`

### Scene System

- `load_scene()`
- `unload_scene()`
- `switch_scene()`
- `return_to_previous_scene()`
- `save_scene_state()`
- `restore_scene_state()`

### UI System

- `show_hud()`
- `hide_hud()`
- `show_debug_hud()`
- `hide_debug_hud()`
- `open_clue_panel()`
- `close_clue_panel()`

### Audio System

- `play_bgm()`
- `stop_bgm()`
- `play_ambient()`
- `stop_ambient()`
- `play_sfx()`
- `set_volume()`

### Save System

- `save_game_state()`
- `load_game_state()`
- `serialize_scene_state()`
- `restore_scene_state()`


---

## 十五·五、Environment FX / Weather Layer（Reserved，归属 Scene Presentation Layer）

**状态：** Reserved（v3.0d 2026-06-04 占位，不计入一级模块）

**用途：** 为未来天气效果（雨/雪/雾/雷/风等）预留接口和渲染挂载点；当前仅占接口，不实现任何具体动画。

**当前原则：**
- 只占接口，不实现任何天气动画
- 不接 Audio / Save / Camera / Video / Event System
- 不计入一级模块，归属 Scene Presentation Layer
- 当天气需要影响剧情 / 数值 / 事件 / 存档时，走 Framework Audit 升级为一级 Weather System

### 15.5.1 状态字段

`python
default weather_type = "none"          # "none" / "rain" / "snow" / "fog" / "thunder" / "wind"
default weather_intensity = 0          # 0~100
default weather_wind = 0               # -100~100  (-=向左，+=向右)
`

### 15.5.2 预留接口（空实现）

- `set_weather(weather_type, intensity=50, wind=0, transition=1.0)`
- `stop_weather(transition=1.0)`
- `get_weather_state()`

当前实现：仅更新 state 变量，不触发渲染。

### 15.5.3 渲染挂载点

`enpy
screen weather_layer():
    pass  # Reserved 空实现
`

由 `explore_scene_test` 等场景 screen 通过 `use weather_layer` 嵌入，挂在视差三层之上、热点/UI 之下。

### 15.5.4 升级路径

未来当出现以下任一情况，必须走 Framework Audit 升级为一级 Weather System：
- 天气需要影响剧情走向
- 天气需要影响游戏数值
- 天气状态需要存档持久化
- 天气需要触发事件（雷击 jumpscare、暴雨阻挡通行）
- 天气需要联动音效 / 镜头 / 视频

升级时将接 Audio System / Save System / Camera System / Video System / Event System。

---

## 十六、Camera System 镜头系统（预留接口）

**状态：** 未开发

**用途：** 未来支持横向探索镜头、纵深推进镜头、电影化镜头运动、手持轻微摆动、特殊调查镜头。

**当前原则：** 只写框架；不开发功能；不修改 `.rpy`；不测试；不进入版本链。

### 16.1 状态字段规划

```python
# 镜头模式
camera_mode = "side_scroll"

# side_scroll
# depth_push
# cinematic

# 当前镜头位置
camera_x = 0
camera_y = 0

# 镜头缩放
camera_zoom = 1.0

# 纵深推进进度
camera_depth_progress = 0.0
# 0.0 ~ 1.0

# 镜头摆动
camera_sway_enabled = False
camera_sway_strength = 0.0

# 图层深度表
camera_layer_depth_map = {
    "bg_far": 0.2,
    "bg_mid": 0.5,
    "bg_near": 1.0,
}
```

| 字段 | 类型建议 | 默认值建议 | 当前状态 | 说明 |
|------|----------|------------|----------|------|
| `camera_mode` | string enum | `"side_scroll"` | 预留 | 镜头模式：side_scroll / depth_push / cinematic |
| `camera_x` | int / float | `0` | 部分已有 | 横向镜头位置；当前 v2.2 使用 `explore_camera_x`，后续统一到 Camera System |
| `camera_y` | int / float | `0` | 预留 | 纵向镜头位置 |
| `camera_zoom` | float | `1.0` | 预留 | 镜头整体缩放 |
| `camera_depth_progress` | float | `0.0` | 预留 | 纵深推进进度，范围 0.0 ~ 1.0 |
| `camera_sway_enabled` | bool | `False` | 预留 | 是否启用手持 / 摆动效果 |
| `camera_sway_strength` | float | `0.0` | 预留 | 镜头摆动强度 |
| `camera_layer_depth_map` | dict | `{bg_far:0.2,bg_mid:0.5,bg_near:1.0}` | 部分已有 | 统一管理远景 / 中景 / 近景视差深度 |

### 16.2 接口规划

```python
def set_camera_mode(mode):
    """
    切换镜头模式。

    参数：
        mode

        side_scroll
        横向探索

        depth_push
        纵深推进

        cinematic
        电影镜头

    当前版本：
        未实现。
    """
    pass
```

```python
def move_camera_x(x):
    """
    横向移动镜头。

    用于：
        v2.2 探索系统。

    当前版本：
        已有逻辑。
        后续统一接入 Camera System。
    """
    pass
```

```python
def push_camera_depth(progress):
    """
    纵深推进。

    参数：
        progress
        0.0 ~ 1.0

    未来效果：
        近景放大。
        中景缓慢放大。
        远景轻微放大。

    模拟：
        玩家向场景深处前进。

    当前版本：
        未实现。
    """
    pass
```

```python
def reset_camera():
    """
    重置镜头。

    恢复：
        x
        y
        zoom

    当前版本：
        未实现。
    """
    pass
```

```python
def apply_layer_parallax():
    """
    图层视差。

    使用：
        camera_layer_depth_map

    统一管理：
        远景
        中景
        近景

    当前版本：
        v2.2 探索已有实现。
        未来接入统一系统。
    """
    pass
```

```python
def apply_depth_zoom():
    """
    纵深缩放。

    根据：
        camera_depth_progress

    自动计算：
        far zoom
        mid zoom
        near zoom

    当前版本：
        未实现。
    """
    pass
```

```python
def apply_camera_sway():
    """
    镜头摆动。

    用途：
        楼道
        病房
        调查镜头
        楼梯间

    营造：
        观察感
        纪录片感

    当前版本：
        未实现。
    """
    pass
```

### 16.3 未来适用场景

```text
养老院走廊
病房区
活动室
监控室
楼梯间
家属院楼道
厂区办公楼
```

### 16.4 开发原则

- 当前只预留接口。
- 当前不开发。
- 当前不测试。
- 当前不进入版本链。
- 等 Dialogue / Clue / Scene 达到 95% 后，再开发 Camera System。
- Camera System 后续应接管 Explore System 中的 `explore_camera_x`、视差层倍率和镜头运动逻辑。
- Camera System 不应直接写死剧情场景；场景使用的镜头参数应由 Scene System 配置。

### 16.5 接口索引（审阅名）

- `set_camera_mode()`
- `move_camera_x()`
- `push_camera_depth()`
- `reset_camera()`
- `apply_layer_parallax()`
- `apply_depth_zoom()`
- `apply_camera_sway()`

---

## 十七、Video System 视频系统（预留接口）

**状态：** 未开发

**用途：** 未来支持游戏内播放视频，包括片头视频、概念宣传片、过场动画、监控录像、手机录像、旧录像带、动态 Logo、剧情 CG 动画。

**当前原则：** 只预留接口；不开发功能；不修改 `.rpy`；不测试；不进入版本链。

### 17.1 状态字段规划

```python
# 当前视频 ID
current_video_id = None

# 当前视频路径
current_video_path = None

# 当前视频播放状态
video_state = "stopped"

# stopped
# playing
# paused
# finished

# 视频是否可跳过
video_skippable = True

# 视频结束后跳转 label
video_next_label = None

# 视频是否阻塞交互
video_modal = True

# 视频播放音量
video_volume = 1.0

# 视频字幕开关
video_subtitle_enabled = False

# 视频字幕 ID
video_subtitle_id = None
```

| 字段 | 类型建议 | 默认值建议 | 当前状态 | 说明 |
|------|----------|------------|----------|------|
| `current_video_id` | string / None | `None` | 预留 | 当前播放的视频 id |
| `current_video_path` | string / None | `None` | 预留 | 当前播放的视频文件路径 |
| `video_state` | string enum | `"stopped"` | 预留 | `stopped` / `playing` / `paused` / `finished` |
| `video_skippable` | bool | `True` | 预留 | 当前视频是否允许跳过 |
| `video_next_label` | string / None | `None` | 预留 | 视频结束后跳转的 label |
| `video_modal` | bool | `True` | 预留 | 视频播放期间是否阻塞普通交互 |
| `video_volume` | float | `1.0` | 预留 | 视频播放音量 |
| `video_subtitle_enabled` | bool | `False` | 预留 | 是否启用视频字幕 |
| `video_subtitle_id` | string / None | `None` | 预留 | 视频字幕 id |

### 17.2 接口规划

```python
def play_video(video_id, path, next_label=None, skippable=True):
    """
    播放视频。

    用途：
        片头
        过场
        监控录像
        手机录像
        动态 Logo

    当前版本：
        未实现。
    """
    pass
```

```python
def stop_video():
    """
    停止视频。

    当前版本：
        未实现。
    """
    pass
```

```python
def pause_video():
    """
    暂停视频。

    当前版本：
        未实现。
    """
    pass
```

```python
def resume_video():
    """
    继续播放视频。

    当前版本：
        未实现。
    """
    pass
```

```python
def skip_video():
    """
    跳过视频。

    仅当 video_skippable == True 时允许。

    当前版本：
        未实现。
    """
    pass
```

```python
def on_video_finished():
    """
    视频播放完成回调。

    如果存在 video_next_label：
        跳转到目标 label。

    当前版本：
        未实现。
    """
    pass
```

### 17.3 资源规范

**建议目录：**

```text
game/videos/
```

**命名规则：**

```text
video_intro_logo.webm
video_ch01_opening.webm
video_monitor_001.webm
video_phone_recording_001.webm
video_vhs_001.webm
```

**推荐格式：**

```text
.webm
```

**备用格式：**

```text
.ogv
```

**不建议：**

```text
.mp4
```

**说明：** Ren'Py 对 `.webm / .ogv` 支持更稳定，`.mp4` 不作为首选格式。

### 17.4 未来适用场景

```text
片头动态Logo

祝寿二字墙皮变化动画

监控室监控录像

手机录像

旧录像带

养老院宣传片

关键回忆片段

章节转场视频
```

### 17.5 与其它系统关系

Video System 依赖：

- Scene System
- Dialogue System
- Audio System
- Save System

规则：

1. 播放视频时暂停普通对话。
2. 播放视频时暂停探索操作。
3. 视频结束后可跳回指定 label。
4. 可跳过视频必须记录是否已看过。
5. 视频播放期间不允许打开线索界面。
6. 视频播放期间不允许触发热点。

### 17.6 开发原则

- 当前只预留接口。
- 当前不开发。
- 当前不测试。
- 当前不进入版本链。
- 等 Dialogue / Clue / Scene 达到 95% 后，再开发 Video System。
- Video System 后续必须接入 Save System，记录已播放 / 已跳过 / 是否可再次跳过等状态。
- Video System 不应直接写死剧情跳转，视频结束跳转由 `video_next_label` 或 Scene System 控制。

### 17.7 接口索引（审阅名）

- `play_video()`
- `stop_video()`
- `pause_video()`
- `resume_video()`
- `skip_video()`
- `on_video_finished()`

---

## 二十三、Framework Audit 补齐：Event / Flag / Investigation / Inventory System

> 来源：2026-06-02 Framework Audit。当前只补框架字段与接口，不开发功能。

### 23.1 Event System 事件系统（预留接口）

**用途：** 统一管理所有触发事件，包括热点触发剧情、热点触发线索、热点触发场景切换、触发音效、触发视频、触发镜头、触发状态标记。

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

**规则：** Event System 是触发中心，不等于 Label。Label 是跳转目标；Event 可以触发 Label、Clue、Flag、Audio、Video、Camera、Scene。

### 23.2 Flag System 标记系统（预留接口）

**用途：** 统一管理剧情状态标记，例如是否调查过公告栏、是否获得旧通知、是否见过院长、是否进入过监控室、是否看过录像、是否触发过电话。

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

**规则：** Flag System 是状态记录中心。Flag 不等于 Clue；Flag 记录剧情状态，Clue 记录玩家获得的信息。

### 23.3 Investigation System 调查目标系统（预留接口）

**用途：** 管理当前调查目标，例如去养老院大厅、查看公告栏、找到监控室、询问院长、获取值班表。

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

**规则：** Investigation System 是玩家当前目标。Objective 不等于 Scene；一个目标可以跨多个场景存在。

### 23.4 Inventory System 物品系统（预留接口）

**用途：** 管理可持有实体物品。Inventory 与 Clue 不完全相同：Clue 是信息，Inventory 是实体物品。例如钥匙、录像带、手机、工牌、纸条、老照片。

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

**规则：** Inventory System 是实体物品中心，不等于 Clue。录像带可以是 Inventory，录像内容可以生成 Clue。

### 23.5 系统关系说明

- Event System 是触发中心。
- Flag System 是状态记录中心。
- Investigation System 是玩家当前目标。
- Clue System 是信息收集。
- Inventory System 是实体物品。
- Scene System 负责场景流转。
- Camera / Video 是表现层系统。

### 23.6 合并 / 不合并规则

- Clue 不等于 Inventory。
- Flag 不等于 Clue。
- Event 不等于 Label。
- Objective 不等于 Scene。
- Video 不等于 Scene。
- Camera 不等于 Explore。

### 23.7 模块登记补充

| 模块 | 必填字段是否已规划 | 预留接口是否已规划 | 备注 |
|------|------------------|------------------|------|
| Event System | 是 | 是 | 新增；统一触发中心，当前只预留接口 |
| Flag System | 是 | 是 | 新增；统一剧情状态标记中心，当前只预留接口 |
| Investigation System | 是 | 是 | 新增；玩家当前调查目标系统，当前只预留接口 |
| Inventory System | 是 | 是 | 新增；实体物品系统，当前只预留接口 |


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
