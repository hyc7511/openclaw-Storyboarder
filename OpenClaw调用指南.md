# OpenClaw Agent调用指南

## 📋 目录
1. [环境准备](#环境准备)
2. [安装OpenClaw](#安装openclaw)
3. [启动工作区](#启动工作区)
4. [📤 如何上传剧本文件](#如何上传剧本文件)
5. [Agent调用方式](#agent调用方式)
6. [工作流程示例](#工作流程示例)
7. [常见问题](#常见问题)

---

## 🔧 环境准备

### 系统要求
- **操作系统**：macOS / Linux (Windows 可使用 WSL)
- **Node.js**：v22.12.0+
- **npm**：最新版本

### 检查Node.js
```bash
node -v
```
如果版本低于22.12.0，请使用以下命令安装：

**macOS：**
```bash
brew install node@22
brew link node@22 --overwrite --force
```

**Linux：**
```bash
# 使用 NodeSource
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt-get install -y nodejs
```

---

## 💻 安装OpenClaw

### 方法1：一键安装（推荐）
```bash
# 在桌面的"新建文件夹"目录下运行
./openclaw_install.sh
```

### 方法2：使用curl
```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
```

### 验证安装
```bash
openclaw --version
```

---

## 🚀 启动工作区

### 步骤1：进入工作区目录
```bash
cd ~/Desktop/新建文件夹/workspace-video-producer
```

### 步骤2：启动OpenClaw
```bash
openclaw
```

### 步骤3：首次配置
首次启动时，OpenClaw会引导你完成配置：
- 登录你的OpenClaw账户
- 配置API密钥
- 选择AI模型

---

## 👥 Agent调用方式

### 主Agent（制片人）
**角色**：总协调者，负责流程管理

**调用方式**：直接在对话中说出你的需求

**示例**：
```
用户：我有一个剧本，想制作成视频提示词
系统：好的！让我先检查一下你的剧本...
```

---

### 导演Agent
**角色**：剧本分析专家

**调用时机**：
- 自动调用：当你提供剧本时
- 手动触发：说出"让导演分析一下"

**能力范围**：
```yaml
剧本分析：
  - 讲戏本生成
  - 人物清单
  - 场景清单
  - 分集建议

质量把控：
  - 业务审核
  - 合规审核
```

**使用示例**：
```
用户：帮我分析一下ep01-sample.md这个剧本
导演：好的，我来详细分析...

[导演分析完成后]
导演：分析完成！需要我审核一下吗？
用户：好的，请审核
```

---

### 服化道设计师Agent
**角色**：视觉设计专家

**调用时机**：
- 自动调用：导演分析完成后
- 手动触发：说出"让服化道设计师来设计"

**能力范围**：
```yaml
人物设计：
  - 服装造型
  - 发型设计
  - 妆容设计
  - 配饰细节

场景设计：
  - 空间布局
  - 道具陈设
  - 光影效果
  - 色彩基调
```

**使用示例**：
```
用户：请设计主角张三的造型
服化道设计师：好的，基于导演的分析...
[生成详细设计方案]

用户：把这个设计加入素材库
服化道设计师：好的，已保存到character-prompts.md
```

---

### 分镜师Agent
**角色**：Seedance提示词生成专家

**调用时机**：
- 自动调用：服化道设计完成后
- 手动触发：说出"让分镜师来制作"

**能力范围**：
```yaml
分镜设计：
  - 镜头类型选择
  - 景别运用
  - 镜头运动
  - 节奏把控

提示词生成：
  - Seedance 2.0格式
  - 素材关联
  - 动作描述
  - 音效说明
```

**使用示例**：
```
用户：开始制作分镜吧
分镜师：好的，我来生成Seedance提示词...

用户：s001这个镜头再调整一下
分镜师：好的，我来修改...
```

---

## 📖 工作流程示例

### 完整流程示例1：单集制作（推荐 - 直接上传文件）

#### 第1步：上传剧本文件
```
用户：[上传剧本文件 我的剧本.md]
系统：收到你的剧本！已保存为 ep01-我的剧本.md
是否开始制作？
用户：开始制作
```

#### 第2步：导演分析
```
系统：好的！让导演先分析一下剧本...
导演：收到，我来详细分析...
[导演分析报告]

导演：分析完成！需要我审核一下吗？
用户：好的，请审核
[导演自审报告]
```

---

### 完整流程示例2：传统方式（预先准备文件）

#### 第1步：准备剧本
将你的剧本文件放入 `project/script/` 目录

#### 第2步：启动流程
```
用户：开始制作视频提示词
系统：好的！让我先检查一下你的剧本...
```

#### 第3步：导演分析
```
系统：正在调用导演Agent...
导演：好的，我来分析剧本...
[导演分析报告]

导演：需要我审核一下吗？
用户：好的
[导演自审报告]
```

#### 第4步：服化道设计
```
系统：导演分析完成！现在请服化道设计师来设计...
服化道设计师：好的，我来设计人物和场景...
[生成设计方案]

系统：需要导演审核一下吗？
用户：好的
[导演审核报告]
```

#### 第5步：分镜制作
```
系统：服化道设计完成！现在请分镜师来制作...
分镜师：好的，我来生成Seedance提示词...
[生成分镜提示词]

系统：需要导演审核一下吗？
用户：好的
[导演审核报告]
```

#### 第6步：完成交付
```
系统：所有流程完成！
- 导演分析：saved to project/outputs/ep01/
- 服化道设计：saved to project/assets/
- Seedance提示词：saved to project/outputs/ep01/
```

---

### 完整流程示例2：多集制作

#### 第1步：准备多集剧本
```
project/script/
├── ep01-sample.md
├── ep02-sample.md
└── ep03-sample.md
```

#### 第2步：批量制作
```
用户：我要制作3集，请按顺序来
系统：好的！让我先从第1集开始...

[第1集完成]
系统：第1集完成！现在开始第2集？
用户：好的
```

#### 第3步：利用素材库
```
用户：第2集可以沿用第1集的人物设计吗？
服化道设计师：好的，我会使用素材库中的已有设计...
```

---

## ⌨️ 快捷命令

### 状态查询
```bash
# 查询当前进度
用户：现在到哪一步了？
系统：当前状态：服化道设计阶段（已完成80%）

# 查询已完成内容
用户：给我看看已生成的所有内容
系统：好的，正在整理...
```

### 流程控制
```bash
# 跳过审核
用户：这次可以跳过审核，直接下一步吗？
系统：好的，跳过审核环节...

# 重新来
用户：我想从导演分析阶段重新开始
系统：好的，重置到导演分析阶段...

# 暂停/继续
用户：先暂停，我稍后回来
系统：好的，已保存状态，随时可以继续...
```

### 内容编辑
```bash
# 修改特定部分
用户：把人物张三的发型改一下
服化道设计师：好的，我来修改...

# 添加补充内容
用户：场景里再加点细节，比如...
服化道设计师：好的，我来补充...
```

---

## 🔍 文件结构说明

### 工作区完整结构
```
workspace-video-producer/
├── 📄 SOUL.md                    # 系统核心配置
├── 📄 AGENTS.md                  # Agent定义
├── 📄 USER.md                    # 用户配置
├── 📄 BOOTSTRAP.md               # 启动引导
├── 📄 README.md                  # 使用说明
├── 📄 UPDATE_LOG.md              # 更新日志
├── 📄 OpenClaw调用指南.md       # 本文件
│
├── 📂 .openclaw/
│   └── 📄 workspace-state.json   # 工作区状态
│
├── 📂 agents/                    # Agent配置
│   ├── 📄 director.md
│   ├── 📄 art-designer.md
│   └── 📄 storyboard-artist.md
│
├── 📂 skills/                    # 技能模块
│   ├── 📄 SKILLS_INDEX.md
│   ├── 📂 director-skill/
│   ├── 📂 script-analysis-review-skill/
│   ├── 📂 art-direction-review-skill/
│   ├── 📂 seedance-prompt-review-skill/
│   ├── 📂 compliance-review-skill/
│   ├── 📂 art-design-skill/
│   └── 📂 seedance-storyboard-skill/
│
└── 📂 project/                   # 项目数据
    ├── 📂 script/               # 剧本存放
    │   └── 📄 ep01-sample.md
    ├── 📂 assets/               # 素材库
    │   ├── 📄 character-prompts.md
    │   └── 📄 scene-prompts.md
    ├── 📂 outputs/              # 输出文件
    │   └── 📂 ep01/
    │       ├── 📄 01-director-analysis.md
    │       └── 📄 02-seedance-prompts.md
    └── 📄 .agent-state.json    # Agent状态
```

---

## ⚙️ 配置说明

### SOUL.md（核心配置）
定义系统的身份、原则、能力等，一般不需要修改。

### AGENTS.md（Agent定义）
定义各个Agent的角色、职责、能力范围。

### USER.md（用户配置）
可以在这里自定义：
```yaml
language: zh-CN
review_style: detailed
max_episodes: 10
```

---

## 🔐 常见问题

### Q1：OpenClaw启动失败怎么办？
```bash
# 检查Node.js版本
node -v

# 尝试重新安装
./openclaw_install.sh --repair

# 检查状态
./openclaw_install.sh --status
```

### Q2：如何修改Agent配置？
- 直接编辑 `agents/` 目录下的Markdown文件
- 重启OpenClaw即可生效

### Q3：如何备份项目？
- 完整备份整个 `workspace-video-producer/` 目录
- 或单独备份 `project/` 目录

### Q4：可以同时制作多个项目吗？
- 建议一个workspace对应一个项目
- 可以创建多个workspace文件夹

### Q5：如何重置工作区？
```bash
# 保留配置文件
rm -rf project/.agent-state.json
rm -rf project/outputs/*
```

---

## 📚 更多帮助

### 查看文档
- `README.md` - 快速开始
- `UPDATE_LOG.md` - 更新历史
- `skills/SKILLS_INDEX.md` - 技能说明

### 官方文档
- OpenClaw官网：https://openclaw.ai
- OpenClaw文档：https://openclaw.ai/docs

### 社区支持
- GitHub仓库：https://github.com/openclaw
- 问题反馈：https://github.com/openclaw/issues

---

## 🎯 快速开始检查清单

- [ ] 安装Node.js v22.12.0+
- [ ] 安装OpenClaw
- [ ] 准备剧本文件到 `project/script/`
- [ ] 启动 `openclaw`
- [ ] 完成首次配置
- [ ] 说出你的需求，开始制作！

---

**祝你使用愉快！🎉**
如有问题，随时查看文档或联系支持。
