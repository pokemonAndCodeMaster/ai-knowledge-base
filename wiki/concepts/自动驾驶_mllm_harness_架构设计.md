---
domain: [mllm_architecture, harness_engineering, mllm_positional_encoding]
type: concept
status: active
created_at: 2026-06-14T07:11:08Z
updated_at: 2026-06-14T07:11:08Z
---

# 🚗 自动驾驶 MLLM Harness 架构设计 (Autonomous Driving MLLM Harness Architecture)

> **导航定位**：本架构归属于 [Agent 与多模态交叉分析](wiki/synthesis/agent与多模态交叉分析.md)，是感知（多模态大模型）与行动（智能体约束控制）结合的工业级端到端实战设计。

---

## 🏗️ 1. 五层数据流与控制链路拓扑

自动驾驶多模态 Harness（测试与约束基座）的核心目标是在将多模态大模型（感知与决策大脑）部署到车辆控制回路中时，确保其**时空一致性、低延迟和物理安全性**。

我们设计的五层拓扑架构如下：

```text
       [ Carla Simulator / Real Vehicle Sensors ]  (Environment Layer)
                           |
                           | 30fps Video Stream + IMU + CAN Bus
                           v
              +-------------------------+
              |   1. Perception Layer   |  (Conv3D Spatio-Temporal Patching)
              +-------------------------+
                           |
                           | Flattened Spatio-Temporal Tokens (T, H, W)
                           v
              +-------------------------+
              |   2. Alignment Layer    |  (MRoPE Alignment & State Fusion)
              +-------------------------+
                           |
                           | Positional Aware Tokens + Token Buffer
                           v
              +-------------------------+
              |   3. Cognitive Layer    |  (Full Attn & GatedDeltaNet MLLM)
              +-------------------------+
                           |
                           | Autoregressive Decision (CoT / discrete tokens)
                           v
              +-------------------------+
              | 4. Action Harness Layer |  (Control Safety Boundary Check)
              +-------------------------+
                           |
                           | Verified & Safe Control Command
                           v
                    [ Vehicle ECU ]
```

---

## 💻 2. 数据流 PyTorch 伪代码实现

下面是一个将 MLLM 的感知切分、MRoPE 注入以及控制 Harness 的拦截逻辑串联起来的硬核 PyTorch 代码推演：

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class Conv3dVideoEmbedder(nn.Module):
    """
    第一层: Perception Layer
    使用 Conv3d 对视频序列进行时空切块 (Spatio-Temporal Patching)
    """
    def __init__(self, patch_size=(2, 14, 14), in_channels=3, embed_dim=1152):
        super().__init__()
        self.patch_size = patch_size
        self.proj = nn.Conv3d(
            in_channels=in_channels,
            out_channels=embed_dim,
            kernel_size=patch_size,
            stride=patch_size
        )
        
    def forward(self, x):
        # x shape: [B, C, T, H, W] -> (Batch, Channels, Frames, Height, Width)
        x = self.proj(x) # -> [B, D, t, h, w]
        # 展平为 Token 序列
        x = x.flatten(2).transpose(1, 2) # -> [B, N, D]
        return x # N = t * h * w 是生成的视觉 Token 数量

class SpatioTemporalMRoPE(nn.Module):
    """
    第二层: Alignment Layer
    三维时空旋转位置编码 (Multimodal RoPE) 注入
    """
    def __init__(self, dim=1152):
        super().__init__()
        self.dim = dim
        self.head_dim = dim // 16 # 假定 16 个注意力头, head_dim=72
        
    def forward(self, tokens, time_ids, height_ids, width_ids):
        # tokens: [B, N, D]
        # time_ids, height_ids, width_ids: 标示每个 token 在物理时空中的索引位置
        # 对每一个 head_dim 进行三轴独立旋转
        # 此处省略复杂的正弦余弦矩阵计算，重点是融合绝对物理时间差 (Delta T)
        return tokens # 返回带有相对位置感知的高维表征

class CognitiveDecisionBrain(nn.Module):
    """
    第三层: Cognitive Layer
    基于交错式 Full Attn 和 GatedDeltaNet 线性注意力层的大脑
    """
    def __init__(self, embed_dim=1152):
        super().__init__()
        self.decoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim, nhead=16, dim_feedforward=4096, batch_first=True
        )
        # 动作头部，预测 [加速, 转向, 刹车]
        self.action_head = nn.Linear(embed_dim, 3)
        
    def forward(self, x):
        features = self.decoder_layer(x) # [B, N, D]
        last_token_feature = features[:, -1, :] # 自回归提取最后一帧特征
        action_logits = self.action_head(last_token_feature) # -> [B, 3]
        # 归一化为 [-1, 1] 之间的连续动作区间值
        actions = torch.tanh(action_logits)
        return actions

class ControlSafetyHarness:
    """
    第四层: Action Harness Layer
    物理安全边界拦截 (Kinematic Safety Envelope)
    """
    def __init__(self, max_steering_rate=0.2, max_jerk=5.0):
        self.max_steering_rate = max_steering_rate
        self.max_jerk = max_jerk
        self.prev_steering = 0.0
        self.prev_acceleration = 0.0
        
    def verify_and_clamp(self, predicted_action, current_velocity):
        # predicted_action: [acceleration, steering, brake]
        acc, steer, brake = predicted_action[0], predicted_action[1], predicted_action[2]
        
        # 1. 转向角速率限制 (防失控侧翻)
        steer_diff = steer - self.prev_steering
        if abs(steer_diff) > self.max_steering_rate:
            steer = self.prev_steering + torch.sign(steer_diff) * self.max_steering_rate
            
        # 2. 运动学防碰撞硬干预 (假如速度过快且刹车不足)
        if current_velocity > 50.0 and brake < 0.2:
            # 强行重置加速，将刹车设为最大值 (紧急避险触发)
            acc = torch.tensor(-1.0)
            brake = torch.tensor(1.0)
            print("⚠️ [Harness Lock]: Collision danger! Autoregressive brake override activated.")
            
        # 更新状态
        self.prev_steering = steer.item()
        self.prev_acceleration = acc.item()
        
        return torch.stack([acc, steer, brake])

# ==========================================
# 模拟端到端训练与控制仿真运行流
# ==========================================
if __name__ == "__main__":
    # 仿真输入: 1个批次, 3通道, 8帧(时间), 224x224分辨率
    video_input = torch.randn(1, 3, 8, 224, 224)
    
    # 实例化五层组件
    embedder = Conv3dVideoEmbedder()
    mrope = SpatioTemporalMRoPE()
    brain = CognitiveDecisionBrain()
    safety_harness = ControlSafetyHarness()
    
    # 执行前向流动
    # 1. Spatio-Temporal Patching
    tokens = embedder(video_input) # -> Shape [1, 1024, 1152]
    # 2. Positional alignment
    aligned_tokens = mrope(tokens, None, None, None)
    # 3. Autoregressive Cognitive reasoning
    predicted_raw_action = brain(aligned_tokens)[0] # -> [acc, steer, brake]
    # 4. Action Harness gate check
    safe_action = safety_harness.verify_and_clamp(predicted_raw_action, current_velocity=60.0)
    
    print(f"Raw Brain Action: {predicted_raw_action.tolist()}")
    print(f"Safe Harness Action: {safe_action.tolist()}")
```

---

## 🛡️ 3. 控制安全边界与异常反馈回路

动作约束层（Action Harness Layer）不仅对动作进行限制，还必须将**拦截结果（异常度、削减程度）以反馈状态的形式，重新注入回下一帧的 Agent 上下文**中：

- **自反思感知闭环**：当控制被 Harness 紧急覆盖时，Harness 会在系统日志中生成特殊输入：“*Harness override triggered: Acceleration reduced by 80% to avoid slip.*”。这个文本输入被注入回 LLM 的下一轮 Prompt 缓存中，逼迫大模型在自回归解码中进行“认错与修正”。
- **运动学边界包络（Safety Envelope）**：基于车辆动力学（轮胎侧倾限度、刹车阻力上限），通过 PID/MPC 建立边界。Harness 拦截算法的执行开销必须控制在 **2ms** 以内，以确保智驾系统整体 10ms 环路的确定性。

---

> [!WARNING]
> MLLM Harness 的代码实现必须进行静态强类型分析，以防止多态运行时出现 `NoneType` 动作空值，破坏车辆 ECU 执行。所有动作输出必须采用 `Float32` 格式归一化。
