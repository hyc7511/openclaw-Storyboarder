# 项目结构规范
## 版本: 2.1 | 更新日期: 2026-04-22

---

## 文件分类原则

### 📝 静态配置文件（.md）
**说明**: 智能体角色设定、系统提示词等 - 不需要机器频繁动态改写的配置
**优势**: 人类易读、易排版、易维护、Git友好

| 文件 | 说明 | 位置 |
|------|------|------|
| SOUL.md | 系统核心身份与原则 | 根目录 |
| AGENTS.md | Agent角色定义 | 根目录 |
| USER.md | 用户偏好配置 | 根目录 |
| BOOTSTRAP.md | 启动引导说明 | 根目录 |
| README.md | 使用说明文档 | 根目录 |
| UPDATE_LOG.md | 版本更新历史 | 根目录 |
| EVOLUTION_CONFIG.md | 演进机制配置 | 根目录 |
| EVOLUTION_GUIDE.md | 演进机制使用指南 | 根目录 |
| DATABASE_README.md | 数据库使用说明 | 根目录 |
| STRUCTURE_GUIDE.md | 本文件 | 根目录 |
| OpenClaw调用指南.md | OpenClaw集成说明 | 根目录 |
| 智能体进化机制.md | 演进机制详细说明 | 根目录 |
| 模型架构设计说明.md | 架构设计文档 | 根目录 |
| agents/*.md | 各Agent详细配置 | agents/ |
| skills/*.md | 各技能配置文件 | skills/ |

---

### 🔧 OpenClaw 配置文件（.json）
**说明**: OpenClaw 工作区配置文件
**范围**: Agent 配置、Skill 配置、工作流配置

| 文件 | 说明 | 位置 |
|------|------|------|
| openclaw.json | OpenClaw 工作区主配置 | 根目录 |

---

### 💾 动态数据文件（.sqlite）
**说明**: 高频读写的状态数据 - 需要事务管理、并发安全
**优势**: SQLite内置事务和锁机制，避免多Agent并发读写冲突
**范围**: Agent状态、问题记录、检查点、统计

| 文件 | 说明 | 位置 |
|------|------|------|
| evolution_log.db | 统一动态数据数据库 | project/ |

---

### 📁 工具与资源文件

| 文件 | 说明 | 位置 | 类别 |
|------|------|------|------|
| schema.sql | 数据库表结构定义 | project/ | 工具 |
| evolution_db.py | 数据库管理工具 | project/ | 工具 |
| init_db.py | 数据库初始化脚本 | project/ | 工具 |
| evolution_log_example.json | JSON数据示例（仅参考） | project/ | 参考 |
| .gitignore | Git版本控制规则 | 根目录 | 配置 |

---

### 📂 项目数据文件（半静态/半动态）

| 目录/文件 | 说明 | 状态 |
|-----------|------|------|
| project/script/ | 用户剧本 | 静态（用户提供） |
| project/assets/ | 素材库（人物/场景） | 半动态 |
| project/outputs/ | 输出内容 | 动态 |

---

## 数据库表结构详解

### 1. agent_state - Agent状态管理
记录当前进度、保存中间结果、支持断点续传
| 字段 | 说明 |
|------|------|
| version | 数据版本号 |
| current_episode | 当前集数 |
| current_stage | 当前阶段（init/director_analysis/art_design/storyboard） |
| stages_json | 各阶段状态（JSON） |
| agents_json | 各Agent上下文（JSON） |
| created_at/updated_at | 创建/更新时间戳 |

### 2. issue_log - 问题历史记录
| 字段 | 说明 |
|------|------|
| issue_id | 问题唯一ID |
| timestamp | 发生时间 |
| description | 问题描述 |
| problem_type | 问题类型 |
| responsible_agent | 责任Agent |
| affected_stage | 影响阶段 |
| checkpoint_added | 增加的检查点 |
| status | 状态（active/resolved） |
| occurrence_count | 发生次数 |

### 3. active_checkpoints - 活跃检查点
| 字段 | 说明 |
|------|------|
| checkpoint | 检查点名称 |
| stage | 对应阶段 |
| trigger_issue | 触发问题 |
| check_items | 检查项（JSON） |
| is_active | 是否活跃 |

### 4. evolution_summary - 统计汇总
| 字段 | 说明 |
|------|------|
| total_issues_identified | 问题总数 |
| issues_resolved | 已解决数 |
| active_checkpoints_count | 活跃检查点数 |

---

## 完整目录树

```
workspace-video-producer/
│
├── 📝 静态配置
│   ├── SOUL.md
│   ├── AGENTS.md
│   ├── USER.md
│   ├── BOOTSTRAP.md
│   ├── README.md
│   ├── UPDATE_LOG.md
│   ├── EVOLUTION_CONFIG.md
│   ├── EVOLUTION_GUIDE.md
│   ├── DATABASE_README.md
│   ├── STRUCTURE_GUIDE.md
│   ├── OpenClaw调用指南.md
│   ├── 智能体进化机制.md
│   ├── 模型架构设计说明.md
│   ├── .gitignore
│   ├── agents/
│   │   ├── director.md
│   │   ├── art-designer.md
│   │   └── storyboard-artist.md
│   └── skills/
│       ├── SKILLS_INDEX.md
│       ├── director-skill/SKILL.md
│       ├── script-analysis-review-skill/SKILL.md
│       ├── art-design-skill/SKILL.md
│       ├── art-direction-review-skill/SKILL.md
│       ├── seedance-storyboard-skill/SKILL.md
│       ├── seedance-prompt-review-skill/SKILL.md
│       ├── compliance-review-skill/SKILL.md
│       ├── quality-review/SKILL.md
│       ├── seedance-prompt/SKILL.md
│       └── video-production/SKILL.md
│
├── 🔧 OpenClaw 配置
│   └── openclaw.json
│
├── 💾 动态数据（SQLite）
│   └── project/
│       └── evolution_log.db      # 统一数据库（运行时生成）
│
├── 🛠️ 工具文件
│   └── project/
│       ├── schema.sql
│       ├── evolution_db.py
│       ├── init_db.py
│       └── evolution_log_example.json
│
└── 📁 项目数据
    └── project/
        ├── script/               # 用户剧本
        │   └── ep01-sample.md
        ├── assets/               # 素材库
        │   ├── character-prompts.md
        │   └── scene-prompts.md
        └── outputs/              # 输出内容
```

---

## 使用流程

### 1. 初始化数据库（智能）
数据库会在首次使用时自动创建，无需手动初始化。
也可以使用命令初始化：

```bash
cd workspace-video-producer/project
python init_db.py
```

### 2. 查看状态
```bash
python evolution_db.py state
```

### 3. 从旧JSON迁移（如有）
```bash
python evolution_db.py migrate .agent-state.json evolution_log.json
```

### 4. 常用命令
```bash
python evolution_db.py help
```

---

## 对话式操作（OpenClaw）

不需要命令行！直接在 OpenClaw 中说：

- "查看当前状态"
- "查看统计"
- "查看问题列表"
- "初始化数据库"
- "查看分镜师状态"
- "查看检查点"

---

## 维护原则

### 静态配置（.md）
- 由人类编辑维护
- 纳入Git版本控制
- 保持完整历史记录

### 动态数据（.sqlite）
- 由系统和工具管理
- **不纳入Git**（通过.gitignore）
- 定期备份（export为JSON）

### OpenClaw 配置（.json）
- OpenClaw 工作区主配置
- 纳入 Git 版本控制
- 保持与项目同步

---

## 快速索引

| 需求 | 操作 |
|------|------|
| 查看当前状态 | python evolution_db.py state |
| 查看统计 | python evolution_db.py summary |
| 导出数据备份 | python evolution_db.py export |
| 查看帮助 | python evolution_db.py help |
| 在 OpenClaw 中使用 | 直接说"查看状态"等 |
