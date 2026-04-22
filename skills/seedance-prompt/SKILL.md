# Seedance 2.0 提示词技能

## 技能名称
Seedance 2.0 提示词生成

## 技能描述
专业的真人漫剧分镜提示词生成技能，支持Seedance 2.0标准格式，包含镜头设计、素材关联和节奏控制。

## 核心能力

- Seedance 2.0 标准格式提示词生成
- 镜头类型和运镜选择
- 人物和场景素材映射
- 节奏和时长控制
- 音频描述集成
- 真人漫剧风格适配

## Seedance 2.0 标准字段

```yaml
scene_id: 镜头唯一标识符
shot_type: wide|medium|close-up|extreme_close-up
duration: 时长（秒）
camera_movement: static|pan|tilt|dolly_in|dolly_out|tracking|handheld
character: 镜头中的人物
scene_desc: 场景描述
action_desc: 动作描述
audio_desc: 音频描述
lighting: 灯光描述
mood: 情绪和氛围
character_prompt_ref: 人物素材引用
scene_prompt_ref: 场景素材引用
notes: 额外备注
```

## 最佳实践

- 使用适当的镜头类型来增强情绪效果
- 保持镜头间的视觉连贯性
- 从全局素材库中引用素材
- 同时考虑视觉和音频元素
- 确保流畅的过渡和节奏
- 真人漫剧风格适配（realistic photography）
