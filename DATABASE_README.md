# 数据库使用说明
## 版本: 2.1 | 更新日期: 2026-04-22

---

## 概述

所有动态数据现在都存储在 **SQLite 数据库**中，提供更好的并发安全性和事务支持！

---

## 核心特性

### 🎉 对话式操作（v2.1）

不需要命令行！在OpenClaw中直接说：
- "查看当前状态"
- "查看统计"
- "列出问题"
- "查看检查点"
- 等等...

### 🛡️ 智能初始化（v2.1）

- 数据库不存在？自动创建！
- 数据库已存在？安全连接！
- 只创建缺失的表，不覆盖已有数据！
- 零风险初始化！

---

## 快速开始

### 最简单方式

在OpenClaw中说："开始制作"，系统会自动初始化数据库！

### 命令行初始化（可选）

```bash
cd project
python init_db.py
```

---

## 对话式命令参考

### 📊 状态查询

| 自然语言命令 | 功能 |
|------------|------|
| 查看当前状态 | 显示整体工作进度 |
| 查看导演状态 | 查看导演阶段状态 |
| 查看服化道状态 | 查看服化道阶段状态 |
| 查看分镜师状态 | 查看分镜师阶段状态 |

### 📈 统计信息

| 自然语言命令 | 功能 |
|------------|------|
| 查看统计 | 显示全局统计摘要 |
| 查看问题统计 | 显示问题历史统计 |
| 查看检查点统计 | 显示检查点统计 |

### 🐛 问题管理

| 自然语言命令 | 功能 |
|------------|------|
| 列出问题 | 显示所有问题列表 |
| 查看活跃问题 | 显示未解决问题 |
| 查看已解决问题 | 显示已解决问题 |

### 🔍 检查点管理

| 自然语言命令 | 功能 |
|------------|------|
| 查看检查点 | 显示所有活跃检查点 |
| 查看分镜师检查点 | 显示分镜师检查点 |
| 查看服化道检查点 | 显示服化道检查点 |

### 💾 数据管理

| 自然语言命令 | 功能 |
|------------|------|
| 初始化数据库 | 安全初始化数据库 |
| 导出数据备份 | 导出JSON备份 |
| 检查数据库状态 | 检查数据库状态 |

---

## 命令行工具（备用）

如果需要命令行操作：

### 初始化数据库

```bash
cd project
python init_db.py
```

### 查看当前状态

```bash
python evolution_db.py state
```

### 查看统计摘要

```bash
python evolution_db.py summary
```

### 列出问题列表

```bash
python evolution_db.py list-issues
```

### 查看活跃检查点

```bash
python evolution_db.py checkpoints
```

### 导出JSON备份

```bash
python evolution_db.py export
```

### 从旧JSON迁移（如需要）

```bash
python evolution_db.py migrate .agent-state.json evolution_log.json
```

### 检查数据库状态

```bash
python evolution_db.py status
```

### 查看完整帮助

```bash
python evolution_db.py help
```

---

## 数据库结构

### 表说明

| 表名 | 说明 | 操作频率 |
|------|------|---------|
| `agent_state` | Agent状态管理（当前进度、中间结果） | 读写频繁 |
| `issue_log` | 问题历史记录 | 写频繁 |
| `active_checkpoints` | 活跃检查点 | 读频繁 |
| `evolution_summary` | 统计汇总 | 写较少 |

### 索引优化

表上都有相应的索引优化查询性能：
- `issue_log_status` - 问题状态索引
- `issue_log_agent` - 责任Agent索引
- `issue_log_type` - 问题类型索引
- `active_checkpoints_stage` - 阶段索引

---

## 安全机制

### 事务支持

所有写操作都在事务中，ACID保证。

### 锁机制

SQLite内置锁机制，支持并发读。

### 安全初始化

- 使用 `CREATE TABLE IF NOT EXISTS`
- 使用 `INSERT OR IGNORE`
- 验证缺失表，自动创建

---

## 文件位置

### 数据库文件

```
project/evolution_log.db      # 主数据库文件
```

### 临时文件（自动管理）

```
project/evolution_log.db-shm  # 共享内存文件
project/evolution_log.db-wal  # WAL日志文件
```

这些临时文件由SQLite自动管理，无需担心。

### Git忽略

数据库文件已添加到 `.gitignore`，不会提交到版本控制。

---

## 备份与恢复

### 备份（导出JSON）

```bash
python evolution_db.py export
```

会生成 `data_export.json`。

### 从备份恢复

```bash
python evolution_db.py import data_export.json
```

### 文件级备份（可选）

直接复制 `evolution_log.db` 文件也可以。

---

## 从旧JSON迁移（如需要）

如果还有旧的JSON数据：

```bash
cd project
python evolution_db.py migrate .agent-state.json evolution_log.json
```

迁移后，可以安全删除旧JSON文件。

---

## 数据库初始化详解

### 自动初始化流程

当使用 `EvolutionDB(auto_init=True)` 时：

1. 检查 `evolution_log.db` 是否存在
2. 如果不存在：
   - 执行 `schema.sql` 创建表结构
   - 初始化默认数据
3. 如果存在：
   - 连接数据库
   - 验证所有表是否存在
   - 缺失表自动创建
4. 准备就绪

### 安全特性

- ✅ 不会覆盖已有数据
- ✅ 只创建缺失的表
- ✅ 零风险初始化
- ✅ 自动验证完整性

---

## Python API 使用

### 基本用法

```python
from evolution_db import EvolutionDB

# 初始化（自动检查）
db = EvolutionDB(auto_init=True)

# 获取状态
state = db.get_agent_state()
summary = db.get_summary()
issues = db.get_issues()
checkpoints = db.get_checkpoints()

# 更新状态
db.update_agent_state(
    current_stage="分镜编写",
    current_episode="ep01"
)

# 关闭连接
db.close()
```

### 高级用法

```python
# 导入导出
db.export_to_json("backup.json")
db.import_from_json("backup.json")

# 数据迁移
db.migrate_from_json(".agent-state.json", "evolution_log.json")

# 问题管理
issue_id = db.add_issue(...)
db.resolve_issue(issue_id)
```

---

## 故障排除

### 数据库锁定

如果出现 "database is locked" 错误：
- 检查是否有其他进程在访问数据库
- 确保每次使用后都调用了 `close()`

### 数据库损坏

SQLite非常健壮，但如果出现问题：
1. 检查WAL文件是否存在
2. 使用备份恢复
3. 重新初始化

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v2.1 | 2026-04-22 | 对话式命令，智能初始化 |
| v2.0 | 2026-04-22 | SQLite数据库，完整分类重构 |
