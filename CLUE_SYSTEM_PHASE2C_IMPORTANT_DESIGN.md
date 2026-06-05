# Clue System Phase 2C — IMPORTANT 标记系统设计

## 1. 模块概述
- **模块名称**：Clue System — IMPORTANT 标记
- **状态**：未开发（预留设计）
- **优先级**：P0（数据层）
- **功能**：
  - 允许玩家为线索标记“重要”状态
  - 与已读系统 (`UNREAD → READ`) 兼容
  - 与线索列表和详情页可视化显示
- **目标**：
  - 提供可靠、可存档的线索重要标记功能
  - 保留对 Clue 数据层兼容性
  - 保留与 Save System、探索/剧情/事件的接口调用

## 2. 数据结构扩展

| 字段 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| is_important | bool | 是否为重要线索 | False |

- 保留原有字段：
  - `id`
  - `title`
  - `desc`
  - `category`
  - `source`
  - `state`
  - `time`

## 3. 预留接口

| 接口 | 参数 | 功能说明 |
|------|------|----------|
| mark_clue_important(clue_id) | clue_id: string | 将线索标记为重要，更新 `is_important=True` |
| unmark_clue_important(clue_id) | clue_id: string | 取消重要标记，更新 `is_important=False` |
| check_clue_important(clue_id) | clue_id: string | 返回线索当前 `is_important` 状态 |
| toggle_clue_important(clue_id) | clue_id: string | 切换重要标记状态 |

## 4. UI 设计预留

- 列表视图显示标记（星号/颜色）
- 详情页显示标记，可切换
- ESC / 右键 / 返回按钮 → 返回列表
- 可绑定快捷键标记/取消标记

## 5. 存档与兼容性

- `is_important` 随 Clue 存档/回档
- 不破坏列表/详情页结构
- 与 Save System、Explore、Event、Investigation 兼容

## 6. 系统依赖

- Clue System 数据层
- Investigation System
- Save System
- Scene / Hotspot / Event（可读取重要状态）

## 7. 开发优先级与顺序

| 功能点 | 优先级 | 状态 |
|---------|-------|------|
| 数据层字段扩展 `is_important` | P0 | 预留 |
| mark/unmark/toggle 接口 | P0 | 预留 |
| 列表视图显示标记 | P1 | 预留 |
| 详情页显示与切换 | P1 | 预留 |
| 存档兼容 | P0 | 预留 |
| 美术/动画效果 | P2 | 预留 |
| 搜索 / 分类筛选联动 | P3 | 预留 |

## 8. 开发建议

1. 实现数据层 + 接口
2. 接入 Save System 测试存档
3. 列表/详情页占位显示逻辑
4. 后续可扩展 UI / 动画 / 分类筛选
5. 避免修改现有列表/详情页数据结构
6. 与已读系统 Phase2B 兼容
