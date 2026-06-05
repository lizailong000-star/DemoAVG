# Flag System 设计文档

## 1. 模块概述
- **模块名称**：Flag System
- **状态**：未开发（预留设计）
- **优先级**：P0
- **功能**：全局状态管理，条件触发中心，提供给 Investigation / Event / Clue / Scene / Save 系统调用
- **目标**：建立统一、可追踪、可存档的全局 Flag 数据体系

## 2. 数据结构

| 字段 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| flag_id | string | 唯一标识符 | 必填 |
| value | int / bool / string | 标记的值 | 0 / False / "" |
| state | string | 状态 | "inactive" |
| source | string | 创建来源（热点、剧情、事件等） | "" |
| timestamp | string | 创建或修改时间 | 自动生成 |
| related_objective | string | 关联目标 id | None |

## 3. 预留接口

| 接口 | 参数 | 功能说明 |
|------|------|----------|
| set_flag(flag_id, value, state="active", source="", related_objective=None) | flag_id, value, state, source, related_objective | 创建或更新 Flag |
| check_flag(flag_id) | flag_id | 返回 flag 当前值和状态 |
| clear_flag(flag_id) | flag_id | 删除或重置指定 Flag |
| list_flags(filter_state=None) | filter_state | 返回所有 Flags，可按状态筛选 |

## 4. 系统依赖

- Event System
- Investigation System
- Clue System
- Scene System
- Save System

## 5. 使用规范

- 必须通过接口调用 Flag，不可直接修改数据
- Flag 状态需存档/回档
- Flag ID 命名规则：前缀表示模块，语义清晰
- 触发条件应通过 Event / Investigation 系统监听

## 6. 可扩展性

- Flag 分类 / 标签
- 历史记录
- 条件组合逻辑（AND/OR）
- 事件回调

## 7. 开发建议

1. 先实现基础数据层 + 接口
2. 接入 Save System
3. 测试与 Event / Investigation 交互
4. 后续可扩展 UI / 可视化 Flag 查看

## 8. 与 Framework Freeze 关系

- P0 一级模块
- 预留接口必须审计批准
- 核心基础模块，其他系统可依赖但不可篡改
