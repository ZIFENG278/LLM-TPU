![](./assets/sophgo_chip.png)

<p align="center">
    <a href=""><img src="https://img.shields.io/badge/python-3.7+-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/os-x86%2C%20aarch-pink.svg"></a>
    <a href="https://github.com/sophgo/LLM-TPU/graphs/contributors"><img src="https://img.shields.io/github/contributors/sophgo/LLM-TPU?color=9ea"></a>
    <a href="https://github.com/sophgo/LLM-TPU/issues"><img src="https://img.shields.io/github/issues/sophgo/LLM-TPU?color=9cc"></a>
    <a href="https://github.com/sophgo/LLM-TPU/commits"><img src="https://img.shields.io/github/commit-activity/y/sophgo/LLM-TPU?color=3af"></a>
</p>
<p align="center">
    <a href="https://github.com/sophgo/LLM-TPU/forks"><img src="https://img.shields.io/github/forks/sophgo/LLM-TPU?color=9cc"></a>
    <a href="https://github.com/sophgo/LLM-TPU/stargazers"><img src="https://img.shields.io/github/stars/sophgo/LLM-TPU?color=9cc"></a>
</p>


# 最近更新！ 🔥🔥🔥

- **2025.04.29**：🚀 Qwen最新推理模型**Qwen3**，BM1684X/1688已支持，详情见[Qwen3 Demo](./models/Qwen3/)。
- **2025.03.07**：🚀 Qwen最新推理模型**QWQ-32B**和**DeepSeek-R1-Distill-Qwen-32B**，1684x多芯demo已适配，详情见[LLM Template](./template/)。
- **2025.02.05**：🚀 DeepSeek时刻！！我们适配了**DeepSeek-R1-Distill-Qwen**系列模型，包括1.5B、7B和14B版本，详情见[LLM Template](./template/)。


# 目录
  - [介绍](#介绍)
  - [模型库](#模型库)
  - [快速开始](#快速开始)
  - [常见问题](#常见问题)
  - [资料链接](#资料链接)

# 介绍

本项目实现算能BM1684X、BM1688(CV186X)芯片部署各类开源`生成式AI模型`，其中以LLM/VLM为主。通过[TPU-MLIR](https://github.com/sophgo/tpu-mlir)编译器将模型转换成bmodel，再基于tpu-runtime的推理引擎接口，采用python/c++代码将其部署到PCIE环境或者SoC环境。

如果要编译模型，需要配置[TPU-MLIR](https://github.com/sophgo/tpu-mlir)环境，包括安装docker和编译源码；
也可以直接用各类Demo中编译好的bmodel。

各个模型的Demo见此目录[models](./models)。

## 编译方法

以`Qwen2.5-VL`为例介绍模型编译方法。

然后下载LLM模型，注意优先使用AWQ或者GPTQ模型，如下：

```shell
git lfs install
git clone git@hf.co:Qwen/Qwen2.5-VL-3B-Instruct-AWQ
```

编译模型如下：
```shell
# -c 指定芯片，比如bm1684x/bm1688/cv186x
# -s 指定seqlen; -q 指定类型; -g 指定group_size，如果不是int4模型则需要指定
llm_convert.py -m /workspace/Qwen2.5-VL-3B-Instruct-AWQ -s 2048 -q w4bf16 -c bm1684x --max_pixels 672,896 -o qwen2.5vl_3b
```

支持如此一键编译的**VLM模型**包括：
* [Qwen2.5VL](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct-AWQ)
* [Qwen2VL](https://huggingface.co/Qwen/Qwen2-VL-2B-Instruct-AWQ)
* [InternVL3](https://huggingface.co/OpenGVLab/InternVL3-2B-AWQ)
* [Gemma3](https://huggingface.co/google/gemma-3-4b-it)

**LLM模型**包括：
* Qwen系列：Qwen1.5/Qwen2/Qwen2.5/[Qwen3](https://huggingface.co/Qwen/Qwen3-4B-AWQ)/[QwQ32B](https://huggingface.co/Qwen/QWQ-32B)
* Qwen延伸：[DeepSeek-R1-Distill-Qwen](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B)
* Llama系列：[Llama2](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)/[Llama3](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct)
* [MiniCPM4](https://huggingface.co/openbmb/MiniCPM4-0.5B-QAT-Int4-GPTQ-format)

除了一键编译外，其他模型可以采用传统方法编译，先转onnx再转bmodel，具体可以参考每个模型的Demo介绍。

## 模型库
我们已经部署过的LLM模型包括：

`Baichuan2`
`ChatGLM3`/`ChatGLM4`/`CodeFuse`
`DeepSeek-6.7B`/`DeepSeek-R1-Distill-Qwen`
`Falcon`
`Gemma`/`Gemma2`
`Llama2`/`Llama3`/`LWM-Text-Chat`
`MiniCPM`/`MiniCPM3`/`MiniCPM4`/`Mistral`
`Phi-3`
`Qwen`/`Qwen1.5`/`Qwen2`/`Qwen2.5`/`QwQ-32B`/`Qwen3`
`WizardCoder`
`Yi`

多模态模型包括：

`Qwen2.5-VL`/`Qwen2-VL`/`Qwen-VL`
`InternVL3`/`InternVL2`
`MiniCPM-V-2_6`
`Llama3.2-Vision`
`Stable Diffusion`
`Molmo-7B`
`OpenClip`
`NVILA-8b`
`DeepSeek-Janus-Pro`

如果您想要知道转换细节和源码，可以到本项目[models](./models)子目录查看各类模型部署细节。

如果您对我们的芯片感兴趣，也可以通过官网[SOPHGO](https://www.sophgo.com/)联系我们。

# 快速开始

克隆LLM-TPU项目，并执行run.sh脚本
```shell
git clone https://github.com/sophgo/LLM-TPU.git
./run.sh --model llama2-7b
```

详细请参考[Quick Start](./docs/Quick_Start.md)

### 效果图
跑通后效果如下图所示

![](./assets/qwen-7b.png)

### Command Table

目前用于演示的模型，全部命令如下表所示

| Model           | SoC                                         | PCIE                                         |
| :-------------- | :------------------------------------------ | :------------------------------------------- |
| ChatGLM3-6B     | ./run.sh --model chatglm3-6b --arch soc     | ./run.sh --model chatglm3-6b --arch pcie     |
| Llama2-7B       | ./run.sh --model llama2-7b --arch soc       | ./run.sh --model llama2-7b   --arch pcie     |
| Qwen-7B         | ./run.sh --model qwen-7b --arch soc         | ./run.sh --model qwen-7b     --arch pcie     |
| Qwen1.5-1.8B    | ./run.sh --model qwen1.5-1.8b --arch soc    | ./run.sh --model qwen1.5-1.8b  --arch pcie   |
| Qwen2.5-7B      |                     \                       | ./run.sh --model qwen2.5-7b  --arch pcie     |
| LWM-Text-Chat   | ./run.sh --model lwm-text-chat --arch soc   | ./run.sh --model lwm-text-chat  --arch pcie  |
| WizardCoder-15B | ./run.sh --model wizardcoder-15b --arch soc | ./run.sh --model wizardcoder-15b --arch pcie |
| InternVL2-4B    | ./run.sh --model internvl2-4b --arch soc    | ./run.sh --model internvl2-4b --arch pcie    |
| MiniCPM-V-2_6   | ./run.sh --model minicpmv2_6  --arch soc    | ./run.sh --model minicpmv2_6 --arch pcie     |
| Molmo-7B-D-0924 |                     \                       | ./run.sh --model molmo-7b --arch pcie        |

## 进阶功能
进阶功能说明：

| 功能        | 目录                                                                       | 功能说明              |
| ----------- | -------------------------------------------------------------------------- | --------------------- |
| 多芯        | [ChatGLM3/parallel_demo](./models/ChatGLM3/parallel_demo)                   | 支持ChatGLM3 2芯      |
|             | [Llama2/demo_parallel](./models/Llama2/demo_parallel)                       | 支持Llama2 4/6/8芯    |
|             | [Qwen/demo_parallel](./models/Qwen/demo_parallel)                           | 支持Qwen 4/6/8芯      |
|             | [Qwen1_5/demo_parallel](./models/Qwen1_5/demo_parallel)                     | 支持Qwen1_5 4/6/8芯   |
| 投机采样    | [Qwen/jacobi_demo](./models/Qwen/jacobi_demo)                               | LookaheadDecoding     |
|             | [Qwen1_5/speculative_sample_demo](./models/Qwen1_5/speculative_sample_demo) | 投机采样              |
| prefill复用 | [Qwen/prompt_cache_demo](./models/Qwen/prompt_cache_demo)                   | 公共序列prefill复用   |
|             | [Qwen/share_cache_demo](./models/Qwen/share_cache_demo)                     | 公共序列prefill复用   |
|             | [Qwen1_5/share_cache_demo](./models/Qwen1_5/share_cache_demo)               | 公共序列prefill复用   |
| 模型加密    | [Qwen/share_cache_demo](./models/Qwen/share_cache_demo)                     | 模型加密              |
|             | [Qwen1_5/share_cache_demo](./models/Qwen1_5/share_cache_demo)               | 模型加密              |


# 常见问题

请参考[LLM-TPU常见问题及解答](./docs/FAQ.md)

# 精度优化

1) 请优先用AWQ或者GPTQ模型转bmodel
2) 如果是浮点模型，如果要进一步提高W4A16的精度，请用[AutoAWQ](https://huggingface.co/docs/transformers/main/en/quantization/awq#awq)或者[AutoGPTQ](https://huggingface.co/docs/transformers/main/en/quantization/gptq)进行量化

# 资料链接

* [ChatGLM2流程解析与TPU-MLIR部署](https://zhuanlan.zhihu.com/p/641975976)
* [TPU-MLIR](https://github.com/sophgo/tpu-mlir)
* [TPU-MLIR快速入门手册](https://doc.sophgo.com/sdk-docs/v23.09.01-lts-sp4/docs_latest_release/docs/tpu-mlir/quick_start/html/index.html)
* [TPU-MLIR论文、整体工程讲解](https://www.bilibili.com/video/BV1My4y1o73Q)
