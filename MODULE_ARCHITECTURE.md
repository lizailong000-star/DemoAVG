# MODULE_ARCHITECTURE.md - 功能模块架构总览

> 项目：《祝寿》Ren'Py DemoAVG 原型  
> 当前基线：v2.2o（`DemoAVG_backup_v2.2o_hide_ui_disable_key_working`）  
> 创建时间：2026-06-02 09:16  
> 用途：整理所有功能模块、完成度、依赖、互斥规则与下一步开发方向。

---

## 一、核心模块总览

| 模块 | 当前完成度 | 当前状态 | 是否允许进入下一功能 | 说明 |
|------|------------|----------|----------------------|------|
| Dialogue System 对话系统 | 60% | 原型 | 否 | 基础对白、头像、对话框、打字机、choice 样式可用；Auto/Skip/History/Text Speed 设置未完成 |
| Explore System 探索系统 | 80% | 可用 | 否 | v2.2 横向探索主链路已跑通；HUD、路径反馈、正式剧情接入仍需 polish |
| Hotspot System 热点系统 | 80% | 可用 | 否 | 热点提示、标记、E 键交互、事件分发、Label 调用已完成；反馈与数据结构仍需统一 |
| Clue System 线索系统 | 50% | 原型 | 否 | clue_list / add_clue / C 键查看可用；详情、分类、来源、已读未读未完成 |
| Scene System 场景系统 | 40% | 原型 | 否 | 基础场景跳转可用；场景状态保存、角色位置保存、热点状态保存未完成 |
| Save System 存档系统 | 20% | 原型 | 否 | 依赖 Ren'Py 默认存档；项目自定义状态保存方案未设计 |
| UI System UI 系统 | 70% | 原型 | 否 | 头像 overlay、对话框底板、居中 choice、E 键推进已接入；完整控制栏未完成 |
| Audio System 音频系统 | 30% | 原型 | 否 | 雨声、电话铃等占位音频已接入；正式 BGM/音效体系未完成 |
| Asset System 资源系统 | 50% | 原型 | 否 | 基础资源目录与命名规范已建立；正式美术/音频资源仍缺 |

> 说明：这里的“是否允许进入下一功能”按 95% 闸门判断。当前只有 v2.2o 单项功能在 `POLISH_AUDIT.md` 中达到 95% 并允许进入下一功能；系统级模块尚未达到 95%。

---

## 二、模块详情

---

## 1. Dialogue System 对话系统

**模块名：** Dialogue System 对话系统

**当前完成度：** 60%

**当前状态：** 原型

**子功能：**

- Base Dialogue 基础对白
- Say Window 对话框
- Avatar Callback 头像
- Text CPS 打字机
- Phone Choice 菜单样式
- Hide UI 逻辑保留 / 快捷键屏蔽
- Auto 自动播放
- Skip 跳过
- History 历史记录
- Text Speed 文本速度设置
- Save 入口
- Hotkeys 快捷键
- 对话控制栏

**已完成：**

- 基础对白可正常推进
- `Character` callback 可驱动头像显示
- `avatar_dialog_overlay` 可显示周卫国头像框
- `style.say_window` 已接入 `dialog_box.png` 对话框底板
- `config.default_text_cps = 7` + `_preferences.text_cps = 7` 实现打字机速度
- `choice` 菜单已改为屏幕中央按钮样式
- `phone_choice` 走统一 choice 样式
- E 键已加入 dismiss，可推进对白和 menu
- Hide UI 逻辑保留：`dialogue_ui_hidden`、`toggle_hide_ui()`、`hide_ui_controller`、Character alpha 方案
- H 键快捷入口已屏蔽：自定义 `K_h` 注释，Ren'Py 原生 `hide_windows` 中的 `noshift_K_h / K_h` 已移除

**未完成：**

- Auto 自动播放
- Skip 跳过 / 快进
- History 历史记录
- 正式 Text Speed 设置界面
- 对话控制栏（Auto / Skip / History / Save / Hide / Text Speed）
- Save 入口与原生存档 UI 的安全接入
- 完整 hotkeys 设计
- Hide UI 尚未开放给玩家使用，当前只保留逻辑，不开放 H 键

**依赖模块：**

- UI System：对话框、头像、控制栏、按钮样式
- Save System：Save 入口与状态保存
- Scene System：跨场景对白状态与回放一致性
- Audio System：语音 / 打字音 / UI 音效

**互斥规则：**

- Auto 与 Skip 互斥
- History 打开时暂停 Auto / Skip
- Save 打开时暂停 Auto / Skip
- 探索场景禁用 Auto / Skip
- Hide UI 开启时不应影响对白推进状态
- Hide UI 与 choice 菜单必须同步显示 / 隐藏
- 对话控制栏不应出现在探索 modal screen 之上

**风险点：**

- 当前项目没有 `screens.rpy` 源文件，原生 UI 依赖 cache/screens.rpyb，不适合直接修改
- DemoAVG 的 `gui.rpy` 是精简版，直接复制 SDK 默认 `screens.rpy` 会缺变量 / 函数
- `ShowMenu("history")` 曾出现 `LabelNotFound` 风险
- 单独硬加 Auto / Skip / History 容易破坏 Ren'Py 原生 UI 生态
- Hide UI 在默认 say screen 下难以稳定隐藏对白文字，后续如恢复必须先设计完整 UI 架构

**下一步：**

- 先写 Dialogue Control 架构设计，再决定是否开发 Auto / Skip / History
- 不直接复制 SDK 默认 `screens.rpy`
- 若进入对话系统 polish，建议先做 Text Speed 设置或最小 History 设计验证

---

## 2. Explore System 探索系统

**模块名：** Explore System 探索系统

**当前完成度：** 80%

**当前状态：** 可用

**子功能：**

- 横向场景宽图
- 三层视差背景
- 鼠标点击寻路
- 镜头跟随
- 角色 idle / walking 状态
- 左右朝向镜像
- 探索 HUD
- 热点接近检测
- 探索内 E 键交互
- 场景切换入口

**已完成：**

- 三层视差：远 / 中 / 近景按不同倍率滚动
- 点击寻路：玩家点击屏幕后角色平滑移动
- 镜头跟随：角色移动时 camera 跟随并受边界限制
- 角色状态：`idle / walking`
- 角色朝向：`left / right` + `xzoom` 镜像
- 探索 screen 使用 `modal True`，可独立接管输入
- v2.2 探索入口 `test_v22_explore` 可用于测试

**未完成：**

- 正式美术资源接入
- 正式角色行走动画帧
- 路径指示 / 目标点反馈
- 探索 HUD 视觉 polish
- 探索状态持久化
- 与正式剧情主线完全整合

**依赖模块：**

- Hotspot System：热点检测与交互
- Scene System：场景切换与状态保存
- Asset System：横向背景、角色动画、前景遮挡
- Save System：保存角色位置、镜头位置、热点状态

**互斥规则：**

- 探索 screen modal 时，应吞掉剧情快捷键
- 探索场景禁用 Auto / Skip
- 探索内 E 键优先触发热点，不应误推进对白
- 场景切换 label 使用 `renpy.jump`，剧情段 label 使用 `call_in_new_context`

**风险点：**

- Ren'Py SL `add` 直接写负数 `xpos` 会导致图消失；必须用 `Transform(xpos=...)`
- 探索场景与 v1.x 点击热区系统目前并行，尚未统一
- 状态保存未完成前，读档可能无法恢复探索位置

**下一步：**

- 做探索 HUD polish
- 接正式横向场景美术
- 设计探索状态保存数据结构

---

## 3. Hotspot System 热点系统

**模块名：** Hotspot System 热点系统

**当前完成度：** 80%

**当前状态：** 可用

**子功能：**

- 热点数据表
- 世界坐标热点
- 接近检测
- 热点提示
- 可视化标记
- E 键交互
- 事件分发
- Label 调用
- 中央反馈弹窗

**已完成：**

- `hotspot_data` 管理热点 id / name / world_x / radius / event / label
- `explore_check_hotspot()` 可判断当前最近热点
- 靠近热点显示提示
- 世界坐标可视化标记 `? / ★`
- E 键触发 `explore_press_e()`
- `trigger_hotspot_event()` 可分发占位事件
- `trigger_hotspot_label()` 可进入测试剧情或场景切换
- 中央大弹窗反馈已用于重要交互提示

**未完成：**

- 热点数据外部化 / 配置化
- 热点一次性状态 / 已调查状态
- 热点与 clue 获取联动规范
- 热点可点击范围可视化调试开关
- 正式交互文案与演出

**依赖模块：**

- Explore System：位置、镜头、输入
- Clue System：调查后获取线索
- Scene System：进入新场景或剧情段
- UI System：提示 / 弹窗 / HUD

**互斥规则：**

- 当前热点为空时 E 键不触发
- `hotspot_action_cooldown` 防止重复触发
- `scene_*` label 使用 jump，其余剧情段使用 call_in_new_context

**风险点：**

- dict 字段不要直接塞进 Ren'Py text 内联表达式，先取变量再显示
- 热点事件和 label 同时存在时必须明确优先级
- 与 v1.x 点击热区系统并行，后续可能重复维护

**下一步：**

- 统一热点数据结构
- 加入已调查状态
- 与 Clue System 建立正式联动

---

## 4. Clue System 线索系统

**模块名：** Clue System 线索系统

**当前完成度：** 50%

**当前状态：** 原型

**子功能：**

- clue_list
- add_clue
- 防重复获得
- C 键查看
- clue_log_screen
- clue_test_screen
- 线索详情
- 线索分类
- 线索来源
- 获得时间
- 已读 / 未读
- 正式线索 UI

**已完成：**

- `clue_list`
- `add_clue`
- 防重复获得
- v1.x 线索查看 UI：`clue_log_screen`
- v2.2 探索内 C 键线索表：`clue_test_screen`
- 测试剧情段可接入 `add_clue`

**未完成：**

- 线索详情
- 线索分类
- 线索来源
- 获得时间
- 已读 / 未读
- 正式线索 UI
- 线索排序
- 线索与热点 / 场景 / 存档的统一数据结构

**依赖模块：**

- Hotspot System：调查热点后获取线索
- Scene System：不同场景线索来源
- Save System：线索状态保存
- UI System：正式线索列表、详情页、未读提示

**互斥规则：**

- 防重复获得同一线索
- 打开线索 UI 时应暂停探索输入或明确 modal 层级
- 探索 screen 中 C 键打开线索，不应与对话推进冲突

**风险点：**

- 项目已有 `add_clue(id, title, desc)` 三参签名，后续不能误写成两参
- `default clue_list` 不可重复声明
- 当前存在两套线索 UI，后续需要合并或明确分工

**下一步：**

- v2.2p 建议方向：Clue System Polish
- 先统一线索数据结构，再做正式线索 UI
- 增加分类、来源、获得时间、已读未读

---

## 5. Scene System 场景系统

**模块名：** Scene System 场景系统

**当前完成度：** 40%

**当前状态：** 原型

**子功能：**

- chapter_id
- scene_id
- scene_title
- current_objective
- 场景设置 label
- 场景跳转
- 场景状态保存
- 角色位置保存
- 热点状态保存

**已完成：**

- `chapter_id / scene_id / scene_title / current_objective` 基础变量
- `set_scene_room_test`
- `set_scene_nursing_home_activity_room`
- `scene_*` label 可用于场景切换
- `trigger_hotspot_label()` 已区分 scene label 与普通剧情段

**未完成：**

- 场景状态保存
- 角色位置保存
- 热点状态保存
- 场景入口 / 出口统一规范
- v1.x 点击热区场景与 v2.2 横向探索场景统一

**依赖模块：**

- Explore System：角色位置、镜头位置
- Hotspot System：热点状态
- Clue System：场景线索状态
- Save System：所有场景状态持久化

**互斥规则：**

- 场景切换用 `renpy.jump`
- 临时剧情段用 `renpy.call_in_new_context`
- 场景切换时需清理旧 screen，避免残留 HUD

**风险点：**

- 若没有状态保存，跨场景后返回会丢失位置和热点状态
- v1.x 和 v2.2 场景系统并行，后续可能混乱

**下一步：**

- 设计场景状态对象
- 明确 v1.x 热区与 v2.2 横向探索的合并策略

---

## 6. Save System 存档系统

**模块名：** Save System 存档系统

**当前完成度：** 20%

**当前状态：** 原型

**子功能：**

- Ren'Py 默认保存 / 读取
- 场景状态保存
- 探索状态保存
- 线索状态保存
- 热点状态保存
- UI 状态恢复
- 存档入口

**已完成：**

- Ren'Py 默认存档系统由引擎提供
- 当前项目未主动破坏默认存档

**未完成：**

- 自定义保存字段设计
- 保存当前场景 id
- 保存探索角色位置 / 镜头位置
- 保存热点已调查状态
- 保存线索已读 / 未读
- 保存 UI 状态
- Save 入口与对话控制栏接入

**依赖模块：**

- Scene System：当前场景与章节
- Explore System：角色位置与镜头
- Hotspot System：热点状态
- Clue System：线索状态
- UI System：存档入口与界面

**互斥规则：**

- Save 打开时暂停 Auto / Skip
- 探索中打开 Save 时必须暂停移动 / 输入
- 不保存临时弹窗倒计时等短生命周期 UI 状态

**风险点：**

- 没有 `screens.rpy` 源文件，直接改原生 save/load UI 风险高
- 若状态变量未统一，读档后可能恢复到错误场景或错误热点状态

**下一步：**

- 先定义“哪些变量必须进存档”
- 再决定是否接入自定义 Save UI
- 优先保证读档后场景、线索、热点一致

---

## 7. UI System UI 系统

**模块名：** UI System UI 系统

**当前完成度：** 70%

**当前状态：** 原型

**子功能：**

- 头像 overlay
- 对话框底板
- choice 菜单样式
- 探索 HUD
- 线索 UI
- 中央反馈弹窗
- 对话控制栏
- 快捷键提示
- Debug 标记

**已完成：**

- `avatar_dialog_overlay` 头像 overlay
- `frame_avatar.png` 头像框
- `dialog_box.png` 对话框底板 style 接入
- 居中 choice 菜单样式
- 探索 HUD 基础文本
- 热点提示 / 热点标记
- 中央大弹窗反馈
- E 键推进
- H 键已禁用：自定义 Hide UI 快捷键未开放，Ren'Py 原生 H hide_windows 也已禁用

**未完成：**

- 对话控制栏
- Auto / Skip / History / Save / Text Speed 按钮
- 正式线索 UI
- 探索 HUD 美术化
- UI 音效
- 统一 UI 层级规范

**依赖模块：**

- Dialogue System：对话窗口、控制栏、菜单
- Explore System：探索 HUD
- Clue System：线索 UI
- Save System：存档入口
- Asset System：UI 图片资源

**互斥规则：**

- 探索 modal screen 不应被对话控制栏覆盖
- Hide UI 不应影响探索 HUD
- History / Save 打开时暂停 Auto / Skip
- choice 菜单与 Hide UI 状态同步

**风险点：**

- 没有 `screens.rpy` 源文件，原生 quick_menu / history / preferences 不能直接改
- 直接复制 SDK 默认 `screens.rpy` 与当前精简 `gui.rpy` 不兼容
- 单点接入按钮容易触发 UI 狂闪或 LabelNotFound

**下一步：**

- 先写 UI 架构设计文档
- 再做对话控制栏或 Text Speed 设置
- 避免继续 patch cache/screens.rpyb 体系

---

## 8. Audio System 音频系统

**模块名：** Audio System 音频系统

**当前完成度：** 30%

**当前状态：** 原型

**子功能：**

- BGM
- 环境音
- 音效
- 电话铃声
- UI 音效
- 音量控制
- 场景音乐切换

**已完成：**

- 雨声 `rain_loop.wav` 可播放并调节音量
- 电话铃声 `phone_ring.wav` 可触发
- 剧情中已有简单 `play music / play sound / stop music` 使用
- 部分场景音量变化已做演出

**未完成：**

- 正式 BGM
- 正式环境音
- 正式音效库
- UI 点击音
- 音量设置界面
- 场景音乐切换规范
- 音频资源命名规范细化

**依赖模块：**

- Scene System：不同场景音频切换
- Dialogue System：语音 / 对话音效 / 打字音
- UI System：按钮音效
- Asset System：音频资源清单

**互斥规则：**

- 电话铃声等短音效不应占用 BGM channel
- 场景切换时需 fadeout 旧 BGM
- UI 音效不能干扰剧情关键音效

**风险点：**

- 当前音频多为占位，正式氛围不足
- 若 channel 规划不清，音效可能互相覆盖

**下一步：**

- 建立音频资源清单
- 区分 BGM / BGS / SE / UI channel 规则
- 接正式雨声、电话铃、养老院环境音

---

## 9. Asset System 资源系统

**模块名：** Asset System 资源系统

**当前完成度：** 50%

**当前状态：** 原型

**子功能：**

- 背景资源
- 头像资源
- 角色立绘
- UI 图片
- 探索占位图
- 音频资源
- 命名规范
- 缺失资源清单
- 资源替换流程

**已完成：**

- `ART_ASSET_GUIDE.md` 已记录资源规范
- 背景命名规范：`bg_场景名.png`
- 头像命名规范：`角色名_表情.png`
- 基础背景资源已接入：雨夜房间、养老院活动室、走廊
- 头像 alpha 派生目录已使用
- UI 资源：`dialog_box.png`、`frame_avatar.png`
- 探索占位图可支撑 v2.2 测试
- `ASSET_LIST.md / MISSING_ASSETS.md / PLACEHOLDER_LIST.md` 已存在

**未完成：**

- 正式角色立绘
- 正式横向探索背景
- 正式热点图标 / HUD 图标
- 正式 UI 控制栏按钮
- 正式音频资源
- 资源版本管理规范
- 占位资源替换检查流程

**依赖模块：**

- Dialogue System：头像、对话框、角色立绘
- Explore System：横向背景、角色行走动画
- Hotspot System：热点图标
- UI System：按钮、面板、HUD
- Audio System：BGM / SE

**互斥规则：**

- 资源派生不覆盖原图，使用并行目录如 `xxx_alpha/`
- 不使用中文文件名
- 文件名全小写下划线
- 背景统一 1280×720 或按横向探索规格单独记录

**风险点：**

- 头像抠图对原图结构敏感，RGB 阈值不一定可靠
- UI 九宫格 / Frame 参数不当会导致对话框错位
- 占位资源若不清理，后续可能误当正式资源

**下一步：**

- 梳理正式资源缺口
- 明确哪些占位可继续用，哪些必须替换
- 为 v2.2 探索准备正式横向背景与角色动画帧

---

## 三、跨模块依赖总表

| 上游模块 | 下游模块 | 依赖说明 |
|----------|----------|----------|
| Asset System | Dialogue / Explore / UI / Audio | 所有显示与音频模块依赖正式资源 |
| Scene System | Save System | 存档必须知道当前章节、场景、目标 |
| Explore System | Save System | 存档需保存角色位置、镜头位置 |
| Hotspot System | Clue System | 调查热点后获得线索 |
| Clue System | Save System | 线索获得、已读状态必须保存 |
| Dialogue System | UI System | 对话控制栏、choice、头像、对话框均属 UI 呈现 |
| UI System | Dialogue / Explore / Clue | UI 必须根据当前模式切换层级和输入 |
| Audio System | Scene / Dialogue | 音乐和音效跟随场景与对白演出 |

---

## 四、全局互斥规则

- 剧情模式与探索模式的快捷键必须分层管理。
- 探索 screen `modal True` 时，优先处理探索输入。
- Auto / Skip 只允许在剧情模式启用。
- History / Save / Clue UI 打开时，应暂停 Auto / Skip。
- E 键在剧情模式推进对白，在探索模式触发热点；两者不可互相抢输入。
- H 键当前全局禁用，不触发自定义 Hide UI，也不触发 Ren'Py 原生 hide_windows。
- 任何 UI 新功能必须先确认是否依赖 `screens.rpy`；当前项目没有 `screens.rpy` 源文件。
- 修改功能文件前必须建立 pre 文件备份；测试通过后才允许建立 working 备份。

---

## 五、下一步建议

| 优先级 | 建议方向 | 理由 |
|--------|----------|------|
| P0 | Clue System Polish | 线索是 AVG 主玩法之一，当前只有原型能力 |
| P0 | Save System 状态设计 | 后续探索、线索、场景都依赖存档一致性 |
| P1 | Dialogue Control 架构设计 | Auto / Skip / History 不能再硬 patch，需要先设计 |
| P1 | Scene State 设计 | 解决跨场景和读档状态问题 |
| P2 | Explore HUD Polish | 探索核心功能已可用，适合做体验增强 |
| P2 | Asset 正式资源替换计划 | 为后续可展示 Demo 做准备 |

---

## 六、维护规则

- 每个 sub-version 完成并建立 working 后，更新对应模块的完成度。
- 如果某模块完成度达到 95%，必须标记“是否允许进入下一功能”。
- 如果新增模块，必须补齐：模块名、当前完成度、当前状态、子功能、已完成、未完成、依赖模块、互斥规则、风险点、下一步。
- 如果修改快捷键、UI 层级、存档状态，必须同步更新本文件的互斥规则和依赖关系。
- 本文件只记录架构，不替代 `FEATURE_LIST.md / POLISH_AUDIT.md / TECH_DEBT.md`。

---

## Framework Audit 补齐模块（2026-06-02）

### 10. Event System 事件系统

**模块名：** Event System 事件系统

**当前完成度：** 0%

**当前状态：** 原型

**子功能：** 热点触发剧情、热点触发线索、热点触发场景切换、触发音效、触发视频、触发镜头、触发状态标记、事件队列、事件锁。

**已完成：** v2.2 中有局部 `trigger_hotspot_event()`，但尚未形成全局 Event System。

**未完成：** `current_event_id / last_event_id / event_queue / event_lock / event_context`；`trigger_event / queue_event / finish_event / cancel_event / is_event_locked`。

**依赖模块：** Hotspot System、Clue System、Scene System、Audio System、Video System、Camera System、Flag System。

**互斥规则：** Event 不等于 Label；Event 是触发中心，Label 只是跳转目标；事件锁定时不允许重复触发强交互事件。

**风险点：** 如果热点继续直接 jump label，触发逻辑会散落；事件锁缺失会导致重复加线索、重复切场景。

**下一步：** 只预留，不开发；等 Clue / Scene 状态结构稳定后再统一 Event System。

---

### 11. Flag System 标记系统

**模块名：** Flag System 标记系统

**当前完成度：** 0%

**当前状态：** 原型

**子功能：** 设置 flag、查询 flag、清除 flag、flag 历史记录、与 Save System 同步。

**已完成：** 暂无全局 Flag System。

**未完成：** `flag_map / flag_history`；`set_flag / get_flag / clear_flag / has_flag`。

**依赖模块：** Event System、Scene System、Clue System、Video System、Save System。

**互斥规则：** Flag 不等于 Clue；Flag 是状态记录，Clue 是玩家获得的信息。

**风险点：** 如果把 flag 塞进零散变量，会导致读档和条件分支难维护。

**下一步：** 只预留，不开发；后续统一 flag 命名规范。

---

### 12. Investigation System 调查目标系统

**模块名：** Investigation System 调查目标系统

**当前完成度：** 0%

**当前状态：** 原型

**子功能：** 当前目标、目标开始 / 完成 / 失败、目标状态表、目标历史、HUD 展示。

**已完成：** 当前存在 `current_objective` 文本，但不是完整目标系统。

**未完成：** `current_objective_id / objective_state_map / objective_history`；`start_objective / complete_objective / fail_objective / get_current_objective / update_objective_state`。

**依赖模块：** Event System、Scene System、UI System、Save System。

**互斥规则：** Objective 不等于 Scene；一个调查目标可以跨多个 Scene。

**风险点：** 只用文本目标会导致目标状态不可保存、不可判断、不可回溯。

**下一步：** 只预留，不开发；等 Scene / Clue 达到 95% 后再做正式目标系统。

---

### 13. Inventory System 物品系统

**模块名：** Inventory System 物品系统

**当前完成度：** 0%

**当前状态：** 原型

**子功能：** 添加物品、移除物品、查询物品、物品状态、与 Clue / Flag / Event 联动。

**已完成：** 暂无全局 Inventory System。

**未完成：** `inventory_items / inventory_item_state_map`；`add_item / remove_item / has_item / get_item_state / set_item_state`。

**依赖模块：** Event System、Flag System、Clue System、Save System、UI System。

**互斥规则：** Clue 不等于 Inventory；Clue 是信息，Inventory 是实体物品。

**风险点：** 如果把实体物品当 clue 存，后续道具使用、消耗、状态变化会很难维护。

**下一步：** 只预留，不开发；后续再决定是否需要正式物品栏 UI。

---

### 14. Camera System 镜头系统

**模块名：** Camera System 镜头系统

**当前完成度：** 0%

**当前状态：** 原型

**子功能：** 横向探索镜头、纵深推进镜头、电影化镜头运动、手持轻微摆动、特殊调查镜头。

**已完成：** `FRAMEWORK_SPEC.md` 已有预留字段和接口；v2.2 Explore 内已有局部横向镜头逻辑。

**未完成：** 全局 Camera System、纵深推进、电影镜头、手持摆动、统一图层深度表。

**依赖模块：** Explore System、Scene System、Event System、Asset System。

**互斥规则：** Camera 不等于 Explore；Camera 是表现层系统，Explore 是玩家移动 / 交互系统。

**风险点：** 若继续把镜头逻辑写死在 Explore 中，后续纵深推进和电影镜头难复用。

**下一步：** 只预留，不开发；等 Dialogue / Clue / Scene 达到 95% 后再开发。

---

### 15. Video System 视频系统

**模块名：** Video System 视频系统

**当前完成度：** 0%

**当前状态：** 原型

**子功能：** 片头视频、概念宣传片、过场动画、监控录像、手机录像、旧录像带、动态 Logo、剧情 CG 动画。

**已完成：** `FRAMEWORK_SPEC.md` 已有预留字段、接口、资源规范和系统关系。

**未完成：** 实际视频播放、跳过逻辑、完成回调、字幕、已看记录、视频资源接入。

**依赖模块：** Scene System、Dialogue System、Audio System、Save System、Event System。

**互斥规则：** Video 不等于 Scene；视频播放期间暂停对话、探索、线索界面和热点触发。

**风险点：** 若把视频结束跳转写死在剧情里，会破坏 Scene / Event 体系。

**下一步：** 只预留，不开发；等 Dialogue / Clue / Scene 达到 95% 后再开发。

---

### 系统边界总结

- Event System 是触发中心。
- Flag System 是状态记录中心。
- Investigation System 是玩家当前目标。
- Clue System 是信息收集。
- Inventory System 是实体物品。
- Scene System 负责场景流转。
- Camera / Video 是表现层系统。

### 合并 / 不合并规则

- Clue 不等于 Inventory。
- Flag 不等于 Clue。
- Event 不等于 Label。
- Objective 不等于 Scene。
- Video 不等于 Scene。
- Camera 不等于 Explore。
