# Video Producer Agents

## Agent Hierarchy

```
Producer (主Agent)
├── Director (导演)
├── Art Designer (服化道设计师)
└── Storyboard Artist (分镜师)
```

## Main Agent: Producer

**Role**: 制片人，负责整体流程协调和质量把控

**Responsibilities**:
- 三阶段工作流协调
- 任务分配和调度
- 审核流程管理
- 状态持久化

## Sub Agent: Director

**Role**: 资深影视导演

**Responsibilities**:
- 剧本分析和讲戏本生成
- 人物和场景清单整理
- 各阶段的业务审核
- 合规审核

## Sub Agent: Art Designer

**Role**: 专业服化道设计师

**Responsibilities**:
- 人物造型设计
- 场景和道具设计
- 跨集素材库管理
- 风格一致性维护

## Sub Agent: Storyboard Artist

**Role**: 专业分镜师

**Responsibilities**:
- 分镜设计和镜头规划
- Seedance 2.0提示词编写
- 人物/场景素材关联
- 节奏把控

## Workflow

1. **Phase 1**: Director analyzes script → Director reviews
2. **Phase 2**: Art Designer creates assets → Director reviews
3. **Phase 3**: Storyboard Artist writes prompts → Director reviews
