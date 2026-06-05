# ROADMAP.md - 开发路线图

> 项目：《祝寿》Ren'Py 2DAVG 原型
> 最近更新：2026-05-29 14:05

---

## ✅ 已完成

### v1.x 剧情基础框架
- [x] Chapter 01 雨夜出租屋：开场演出 + 4 热点调查 + 接/不接电话双分支
- [x] Chapter 01 养老院活动室：4 热点调查 + 关键线索解锁 + 结局转场
- [x] Chapter 02 养老院走廊：4 热点调查 + 线索收集 + 结尾悬念
- [x] Chapter 01 结尾转场 screen
- [x] 线索系统：clue_list + add_clue(id, title, desc) + clue_log_screen
- [x] 点击热区探索（room_explore_screen / activity_room_explore_screen / corridor_explore_screen）

### v2.0 美术接入
- [x] 3 张正式背景（雨夜房间 / 活动室 / 走廊）
- [x] 5 张头像（周卫国 × 3 表情 + 护士 + 电话声）
- [x] 头像框镂空 + Alpha 通道处理
- [x] dialog_box.png 对话框底板

### v2.1 UI 系统
- [x] Character callback 头像联动
- [x] overlay screen 头像框显示（左下角 160×160）
- [x] style.say_window 对话框接入
- [x] ART_ASSET_GUIDE.md 美术规范

### v2.2 横向探索系统
- [x] v2.2a 三层视差大场景（远 0.2 / 中 0.5 / 近 1.0）
- [x] v2.2d RPG 点击寻路（鼠标点击 + 平滑移动 + 红色目标点）
- [x] v2.2e 角色状态机（idle / walking + left / right + xzoom 镜像）
- [x] v2.2f 热点提示（靠近 → ★ 按 E 查看）
- [x] v2.2g 热点可视化标记（世界坐标 ? / ★）
- [x] v2.2h E 键交互（cooldown + HUD 反馈）
- [x] v2.2i 事件分发器（trigger_hotspot_event + 中央弹窗）
- [x] v2.2j Label 调用（call_in_new_context / jump 分流）
- [x] v2.2k 场景切换（scene_xxx → jump）
- [x] v2.2l 线索接入探索 + C 键 + E 键全局 dismiss
- [x] v2.2l.1 文本打字机效果（7 cps）

---

## 🔧 开发中（当前焦点）

> 文档审计阶段，暂不开发 v2.2m

- [x] **Audit-01 项目审计 + 文档体系建立**（2026-05-29 14:12）
  - 输出：PROJECT_LOG.md / FEATURE_LIST.md / ASSET_LIST.md / MISSING_ASSETS.md / PLACEHOLDER_LIST.md / ROADMAP.md
- [x] **Audit-03 项目认知统一阶段**（2026-05-29 14:33）
  - 输出：TECH_DEBT.md / CONTENT_LIST.md / SCENE_FLOW.md
  - 同步更新：ROADMAP.md / PROJECT_LOG.md
- [ ] 等老李 review 文档，决定后续方向

---

## 📋 待开发（近期，v2.2m 起）

### 探索系统完善
- [ ] 正式剧情段替换占位 Label（test_gate → 真实剧情）
- [ ] 多场景连通（2~3 个正式场景：大门 → 大厅 → 走廊）
- [ ] 角色行走动画帧（替换 player_placeholder.png 单帧）
- [ ] 调试 HUD 可开关（正式版开发者模式切换）
- [ ] 热点系统与 v1.x 点击热区合并决策

### UI 完善
- [ ] 线索查看 UI 合并（clue_test_screen / clue_log_screen 二选一或统一）
- [ ] 多角色头像启用（nurse / phone_voice / zhou worried / shocked）
- [ ] 打字机速度改为可调（去掉 init 999 强压，走玩家偏好）
- [ ] 存档 / 读档状态完善（探索位置 / 线索 / 场景 ID 都要存）

### 剧情推进
- [ ] 探索系统接入正式主线（Chapter 01 → 探索 → Chapter 02 无缝过渡）
- [ ] Chapter 02 后续场景开发
- [ ] 七宗罪副本设计文档细化（从概念到具体剧本）

---

## 📌 远期规划

### 核心玩法
- [ ] 七个副本 × 七宗罪完整剧本（当前只有概念框架）
- [ ] 多人格系统 / 结局分支
- [ ] 副本间线索串联
- [ ] 暴风雨山庄终极对决

### 引擎 / 技术
- [ ] 存档系统完善（探索状态持久化）
- [ ] 成就系统
- [ ] 音量 / 文字速度 / 全屏等设置菜单
- [ ] 多语言支持（可选）
- [ ] 移动端适配（触屏优化）

### 美术
- [ ] 所有占位资源替换为正式美术
- [ ] 角色立绘 × N 表情 × N 角色
- [ ] 横向探索场景 × N（每个副本需独立大背景）
- [ ] BGM 作曲 / 选购
- [ ] 音效库扩充
- [ ] CG 插画（关键剧情节点）

### 发布
- [ ] Windows / Mac / Linux 打包
- [ ] Steam 上架准备
- [ ] 宣传素材（PV / 截图 / 商店页）

---

## 版本里程碑时间线

```
v0.x   ████░░░░░░  剧情原型 + 点击热区
v1.x   ██████░░░░  多章节 + 线索系统
v2.0   ███████░░░  美术接入
v2.1   ████████░░  UI 系统
v2.2   █████████░  横向探索全功能
v2.3?  ░░░░░░░░░░  探索 + 剧情合并（待定）
```
