> 本节介绍 QK Norm，作为近期开源的大模型[ GLM-4.5](https://swfvqxo30ma.feishu.cn/wiki/FDScweKlXiSXWXkSGzRcAnlenpg?from=from_copylink)、[ dots.llm1](https://swfvqxo30ma.feishu.cn/wiki/DCYGwzbdGisGTzkVimVcCpVfnSg?from=from_copylink)、[ Qwen-3 & Qwen-3-MoE](https://swfvqxo30ma.feishu.cn/wiki/FbmXwWEL5idyzpkK62LcUsrFnMb?from=from_copylink)、[ LLaMA-4](https://swfvqxo30ma.feishu.cn/wiki/RFs6wxsz1ilsADkcaa3cGtYDngg?from=from_copylink)使用的技术，我们详细解释以下几个问题：
>
> * QK Norm 的 **<span style="color: rgb(216,57,49); background-color: inherit">理论来源</span>**？QK Norm **<span style="color: rgb(216,57,49); background-color: inherit">优化目标</span>**&#x662F;什么？理论上怎么做？
>
> * QK Norm 在[ GLM-4.5](https://swfvqxo30ma.feishu.cn/wiki/FDScweKlXiSXWXkSGzRcAnlenpg?from=from_copylink)、[ dots.llm1](https://swfvqxo30ma.feishu.cn/wiki/DCYGwzbdGisGTzkVimVcCpVfnSg?from=from_copylink)等大模型中&#x7684;**<span style="color: rgb(216,57,49); background-color: inherit">代码实现</span>**&#x6709;什么区别？
>
> * QK Norm 和 Attention 的 $$\sqrt{d}$$ scaling 有什&#x4E48;**<span style="color: rgb(216,57,49); background-color: inherit">关系</span>**？

## 1. QK Norm 从哪里来？

QK Norm 可考证的最早论文是 2020 年的 [《Query-Key Normalization for Transformers》](https://arxiv.org/abs/2010.04245)，目标是为了<span style="color: rgb(216,57,49); background-color: inherit">降低数值波动、提升稳定性（使 Softmax 函数在不牺牲表达能力的情况下不那么容易出现饱和）。</span>

怎么理解Softmax的饱和性，首先来看Attention的公式：

$$\operatorname{Attention}(Q, K, V)=\operatorname{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$$

这里使用的 Softmax 会遇到两个问题，来看[论文](https://arxiv.org/abs/2010.04245)里的例子：

$$\begin{aligned}
& \operatorname{softmax}([760,752,750]) \\ = & \operatorname{softmax}([12,4,2]) \\ = & {[0.99962,0.00034,0.00005] . }
\end{aligned}$$

两个问题是：

* softmax只关注值之间的相对差，稍大的差距（比如>10）就会造成某一个head\_dim上的值过饱和

* 由于$$\frac{Q K^T}{\sqrt{d_k}}$$无界，导致出现以上过饱和问题是不可控的

因此[《Query-Key Normalization for Transformers》](https://arxiv.org/abs/2010.04245)认为可以在 Q、K上分别做 L2 Norm 实现把 Q、K 两个 vector（这里是逐token计算视角，因此是vector）转化为单位向量，这样的话QK的单点乘积就可以变成

$$Q'K'^T = cosine\_similarity(Q',K')$$

其中 $$Q' = Q/\|Q\|$$，$$K' = K/\|K\|$$，<span style="color: rgb(216,57,49); background-color: inherit">而</span>$$cosine\_similarity$$<span style="color: rgb(216,57,49); background-color: inherit">是限制在</span>$$[-1,1]$$<span style="color: rgb(216,57,49); background-color: inherit">的，避免出现Softmax饱和问题。</span>

**<span style="color: rgb(216,57,49); background-color: inherit">那么现在有一个问题，Attention中的</span>$$\sqrt{d}$$<span style="color: rgb(216,57,49); background-color: inherit">还需要保留吗？</span>**

我认为是不需要了，因为[《Attention Is All You Need》](https://arxiv.org/abs/1706.03762)原论文里的假设是 head\_dim 上的每一个标量变量服从 N(0, 1)，而此时我们的Q、K 两个 vector 可以认为是两个随机标准向量，两者的内积服从 N(0,1/d)，因此不仅不应该除以$$\sqrt{d}$$，甚至还应该乘以$$\sqrt{d}$$呢！

当然，[《Query-Key Normalization for Transformers》](https://arxiv.org/abs/2010.04245)给出了另外一种解法，使用一个可学习标量$$g$$维持 scaling：

$$\operatorname{softmax}\left(g * \hat{Q} \hat{K}^T\right) V$$

其中 $$\hat{Q}$$ and $$\hat{K}$$ 是Q、K的 ℓ2-normalization 结果（在head\_dim上normalization）



## 2. 在近期开源的大模型中，QK Norm 的工程实现？

先说结论：从工程上看和 Section 1 的理论完全不一致，但是内在原理是一致的。

这里我们看[ GLM-4.5](https://swfvqxo30ma.feishu.cn/wiki/FDScweKlXiSXWXkSGzRcAnlenpg?from=from_copylink)的QKNorm实现，可&#x4EE5;**<span style="color: rgb(216,57,49); background-color: inherit">发现三点和Section 1 的理论的不同</span>**：

**<span style="color: rgb(216,57,49); background-color: inherit">1）本质上这个QKNorm是一个RMSNorm</span>**（参考[ 为什么最新的大模型普遍用RMSNorm？](https://swfvqxo30ma.feishu.cn/wiki/FyiMwG0BAiDT5Qk3Z0Ecs6CvnFb?from=from_copylink)），而RMSNorm不仅仅是执行了L2-Norm，还加上了一个可学习向量$$\gamma$$（忽略防止除零错误的$$\epsilon$$）：

$$y_i=\frac{x_i}{\operatorname{RMS}(x)} * \gamma_i, \quad \text { where } \quad \operatorname{RMS}(x)=\sqrt{\epsilon+\frac{1}{n} \sum_{i=1}^n x_i^2}$$

```python
@use_kernel_forward_from_hub("RMSNorm")
class Glm4MoeRMSNorm(nn.Module):
    def __init__(self, hidden_size, eps=1e-6):
        """
        Glm4MoeRMSNorm is equivalent to T5LayerNorm
        """
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.variance_epsilon = eps

    def forward(self, hidden_states):
        input_dtype = hidden_states.dtype
        hidden_states = hidden_states.to(torch.float32)
        variance = hidden_states.pow(2).mean(-1, keepdim=True)
        hidden_states = hidden_states * torch.rsqrt(variance + self.variance_epsilon)
        return self.weight * hidden_states.to(input_dtype)
```

2）**<span style="color: rgb(216,57,49); background-color: inherit">即使进行了QK Norm还是进行了  </span>$$\sqrt{d}$$<span style="color: rgb(216,57,49); background-color: inherit"> scaling。</span>**&#x53C2;考以下[ GLM-4.5](https://swfvqxo30ma.feishu.cn/wiki/FDScweKlXiSXWXkSGzRcAnlenpg?from=from_copylink)的代码，scaling是照做不误的：

```java
def eager_attention_forward(
    module: nn.Module,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    attention_mask: Optional[torch.Tensor],
    scaling: float,
    dropout: float = 0.0,
    **kwargs: Unpack[TransformersKwargs],
):
    key_states = repeat_kv(key, module.num_key_value_groups)
    value_states = repeat_kv(value, module.num_key_value_groups)

    attn_weights = torch.matmul(query, key_states.transpose(2, 3)) * scaling
    if attention_mask is not None:
        causal_mask = attention_mask[:, :, :, : key_states.shape[-2]]
        attn_weights = attn_weights + causal_mask

    attn_weights = nn.functional.softmax(attn_weights, dim=-1, dtype=torch.float32).to(query.dtype)
    attn_weights = nn.functional.dropout(attn_weights, p=dropout, training=module.training)
    attn_output = torch.matmul(attn_weights, value_states)
    attn_output = attn_output.transpose(1, 2).contiguous()

    return attn_output, attn_weights
```

**<span style="color: rgb(216,57,49); background-color: inherit">3）代码中并没有出现一个可学习标量</span>$$g$$<span style="color: rgb(216,57,49); background-color: inherit">用于替换</span>$$\sqrt{d}$$<span style="color: rgb(216,57,49); background-color: inherit"> scaling。</span>**

那么这三点，是否就证明[ GLM-4.5](https://swfvqxo30ma.feishu.cn/wiki/FDScweKlXiSXWXkSGzRcAnlenpg?from=from_copylink)、[ dots.llm1](https://swfvqxo30ma.feishu.cn/wiki/DCYGwzbdGisGTzkVimVcCpVfnSg?from=from_copylink)、[ Qwen-3 & Qwen-3-MoE](https://swfvqxo30ma.feishu.cn/wiki/FbmXwWEL5idyzpkK62LcUsrFnMb?from=from_copylink)、[ LLaMA-4](https://swfvqxo30ma.feishu.cn/wiki/RFs6wxsz1ilsADkcaa3cGtYDngg?from=from_copylink)的QK Norm 和论文[《Query-Key Normalization for Transformers》](https://arxiv.org/abs/2010.04245)不一样？

**<span style="color: rgb(216,57,49); background-color: inherit">不是的，两者表达的思想内核是一致的！</span>**

首先是问题1）和问题3），可学习向量$$\gamma$$恰好替代了可学习标&#x91CF;**$$g$$**，虽然看起来变复杂了（可学习参数变多），但是带来的好处是不必担心可学习标&#x91CF;**$$g$$**&#x7684;初始化问题，RMSNorm初始化保证和未使用QKNorm的分支输出的一致的！

其次是问题2， $$\sqrt{d}$$ scaling 是否使用其实是和 [《Query-Key Normalization for Transformers》](https://arxiv.org/abs/2010.04245)不违背的，因为RMSNorm的可学习向量$$\gamma$$会将值大小拉到合适的范围。并且 $$\sqrt{d}$$ scaling也是为了保证初始化时分支输出的一致性。



最后一个问题留给大家，就是QK Norm 和 Attention 的 $$\sqrt{d}$$ scaling 有什么关系？两者到底存在冲突吗？

> **<span style="color: rgb(216,57,49); background-color: inherit">欢迎加入大模型学习圈：</span>[<span style="color: rgb(216,57,49); background-color: inherit"> 代码熊大模型学习圈加入指南 🧭 </span>](https://swfvqxo30ma.feishu.cn/wiki/KVKAwBOY1iMLRZko6yYcVmYYnff?from=from_copylink)**
>
> 各位宝子参考以上文档申请学习圈权限，<span style="color: rgb(216,57,49); background-color: inherit">务必填写准确</span>，方便工作人员校验。
>
> 由于学习圈功能刚刚开启，每日申请量较大，申请会在<span style="color: rgb(216,57,49); background-color: inherit">当周通过</span>，麻烦各位宝子耐心等待

