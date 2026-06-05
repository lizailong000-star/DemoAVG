# SCENE_FLOW.md - 场景连接关系

> 项目：《祝寿》Ren'Py DemoAVG 原型
> 最近更新：2026-05-29 14:33（Audit-03 建立）
> 用途：管理场景之间的跳转/连接关系，追踪实际流程与未来规划

---

## 一、当前实际流程（v2.2l.1）

### 主线剧情流（v1.x 系统）

```
START MENU
  │
  ├─【正常剧情】→ chapter_01_start
  │     │
  │     ▼
  │  雨夜出租屋（room_explore_screen，点击热区）
  │     │  接/不接电话 → 均跳转
  │     ▼
  │  养老院活动室（activity_room_explore_screen，点击热区）
  │     │  关键线索满足 → 结束调查
  │     ▼
  │  chapter_01_end → chapter_end_screen
  │     │  点击"继续"
  │     ▼
  │  chapter_02_start → corridor_intro_scene
  │     │
  │     ▼
  │  养老院走廊（corridor_explore_screen，点击热区）
  │     │  关键线索满足 → 结束调查
  │     ▼
  │  chapter_02_corridor_end
  │     │  return（流程到此结束，无后续场景）
  │     ▼
  │  ⛔ 死路
  │
  └─【返回标题】→ MainMenu
```

### 测试探索流（v2.2 系统）

```
START MENU
  │
  ├─【v2.2b TEMP 测试探索热点场景】→ test_v22_explore
  │     │
  │     ▼
  │  explore_scene_test（横向 RPG 探索 screen）
  │     │
  │     ├─ 热点: 养老院大门 → test_gate（call_in_new_context，跑完回探索）
  │     ├─ 热点: 公告栏   → test_notice_board（call_in_new_context）
  │     ├─ 热点: 保安室   → test_security_room（call_in_new_context）
  │     └─ 热点: 进入大厅 → scene_lobby（renpy.jump，场景切换）
  │           │
  │           ▼
  │        scene_lobby（紫色 Solid 占位）
  │           │  menu: "返回探索场景" / "再看一眼"
  │           ▼
  │        back_to_explore → test_v22_explore（回到探索）
  │
  └─ Esc/右键 → 退出探索 screen
```

### 双系统隔离现状

```
┌─────────────────────────┐     ┌─────────────────────────┐
│   v1.x 剧情系统          │     │   v2.2 探索系统          │
│                         │     │                         │
│  点击热区 screen         │     │  RPG 横向探索 screen     │
│  clue_xxx_checked 布尔   │     │  clue_list + add_clue   │
│  clue_log_screen        │     │  clue_test_screen       │
│  Jump() 跳转 label      │     │  call_in_new_context    │
│                         │     │  + renpy.jump(scene_xxx)│
│  chapter_01_start 入口   │     │  test_v22_explore 入口   │
└─────────────────────────┘     └─────────────────────────┘
        互不连通                       互不连通
```

---

## 二、未来规划结构（养老院 Chapter 01-02 全景）

### 目标：统一为 v2.2 RPG 探索系统，主线剧情以热点 label 接入

```
START MENU
  │
  ▼
雨夜出租屋（开场演出，仍用传统 AVG 对话推进）
  │  接/不接电话
  ▼
养老院大门外（v2.2 横向探索）
  │  热点: 铁门 → 剧情"推门进入"
  ▼
养老院大厅（v2.2 横向探索）
  │  热点: 前台 → 剧情"登记来访"
  │  热点: 走廊入口 → 场景切换
  ▼
养老院一楼走廊（v2.2 横向探索）
  │  热点: 活动室门 → 场景切换
  │  热点: 监控室 → 剧情/场景切换
  │  热点: 护士站 → 剧情
  │  热点: 楼梯 → 场景切换（上楼）
  ▼
养老院活动室（v2.2 横向探索 或 点击热区保留待决策）
  │  热点: 祝寿字 / 安排表 / 座椅 / 水桶
  ▼
监控室（v2.2 横向探索）
  │  热点: 监控画面 / 值班记录 / 录像带
  ▼
病房区（v2.2 横向探索）
  │  热点: 病床 / 床头柜 / 输液架
  ▼
楼梯间（v2.2 横向探索，纵向连接层）
  │  上楼 / 下楼
  ▼
二楼走廊（v2.2 横向探索）
  │  热点: ……
  ▼
  ……
```

### 场景连接关系表（规划）

| 场景 | 可达场景 | 连接方式 | 开发状态 |
|------|----------|----------|----------|
| 雨夜出租屋 | 养老院大门外 | 剧情自动转场 | ✅ 已有（v1.x） |
| 养老院大门外 | 大厅 | 热点 → jump scene_lobby | ⚠️ 占位（test_gate） |
| 大厅 | 一楼走廊 | 热点 → jump scene_corridor | ⚠️ 占位（scene_lobby 只有 3 句台词） |
| 一楼走廊 | 活动室 | 热点 → jump scene_activity_room | 📋 未开始 |
| 一楼走廊 | 监控室 | 热点 → jump scene_security_room | 📋 未开始 |
| 一楼走廊 | 护士站 | 热点 → call_in_new_context | 📋 未开始 |
| 一楼走廊 | 楼梯间 | 热点 → jump scene_stairway | 📋 未开始 |
| 监控室 | 一楼走廊 | 返回 → back_to_corridor | 📋 未开始 |
| 楼梯间 | 二楼走廊 | 热点 → jump scene_floor2_corridor | 📋 未开始 |
| 活动室 | 一楼走廊 | 返回 → back_to_corridor | ✅ 已有（v1.x，非 v2.2） |

---

## 三、待决策事项

| 编号 | 决策点 | 选项 | 影响 | 建议默认 |
|------|--------|------|------|----------|
| SF-001 | 雨夜出租屋保留 v1.x 对话推进还是重做为 v2.2 探索 | A. 保留对话推进 B. 重做探索 | 工作量差异大 | A（出租屋空间小，不需要横向探索） |
| SF-002 | 活动室/走廊迁移到 v2.2 还是用 v1.x 点击热区 | A. 全迁移 v2.2 B. 保留 v1.x C. 混合 | TD-002 的核心决策 | A（v2.2 功能更完整，统一体验） |
| SF-003 | 场景间是 jump（全切换）还是 call_in_new_context（嵌套） | A. 全 jump B. 全 call C. 按场景大小判断 | 已有命名约定 scene_xxx → jump | C（现有约定已够用） |
| SF-004 | 养老院整体是一张大地图还是多段小场景串联 | A. 一张 4000px+ 大地图 B. 多段 2000px 场景 jump 串联 | 影响美术和内存 | B（控制单场景资源量） |

---

## 四、文档维护规则

- 场景新增/删除/连接变化时更新本文
- 待决策项决策后，将决策结果写入"建议默认"列
- 实际流程变化时同步更新第一节
