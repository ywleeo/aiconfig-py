# aiconfig

全局 AI API Key 管理工具。配置一次，所有项目通用。

统一管理各 AI 厂商的 API Key、Base URL 和模型名。任何项目只需传入模型名，即可获取完整配置，无需重复配置。

## 快速开始

### 1. 安装（一次性）

aiconfig 不需要和你的项目在同一个目录，放在任意位置即可：

```bash
git clone <repo-url> ~/tools/aiconfig-py
cd ~/tools/aiconfig-py
pip install -e .
```

> 确保 aiconfig 和你的生产项目在同一个 Python 环境中（同一个 venv 或 conda env）。

### 2. 配置 Key（一次性）

```bash
# 命令行设置（自动加密）
aiconfig set qwen sk-xxx
aiconfig set openai sk-xxx
aiconfig set deepseek sk-xxx

# 或直接编辑 aiconfig/keys.yaml，再执行加密
aiconfig encrypt

# 查看已配置的厂商
aiconfig list
```

### 3. 在任何项目中使用

安装后 aiconfig 就是 Python 环境里的一个普通包，跟 `import requests` 一样，任何项目直接 import：

```python
from aiconfig import get_config

# 只需传模型名，返回全部配置
conf = get_config("qwen-plus")
# conf = {
#     "provider": "qwen",
#     "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
#     "api_key": "sk-xxx",
#     "model": "qwen-plus",
# }
```

配合各种 SDK 使用：

```python
# OpenAI 兼容的文本模型
from openai import OpenAI

conf = get_config("qwen-plus")
client = OpenAI(base_url=conf["base_url"], api_key=conf["api_key"])
resp = client.chat.completions.create(
    model=conf["model"],
    messages=[{"role": "user", "content": "你好"}],
)

# 图片/视频模型 — 拿到配置后按各厂商 SDK 调用
conf = get_config("qwen-image-2.0-pro")
# 用 conf["base_url"] 和 conf["api_key"] 调用对应的图片生成 API
```

## CLI 命令

| 命令 | 说明 |
|---|---|
| `aiconfig set <provider> <key>` | 设置 API Key（自动加密） |
| `aiconfig remove <provider>` | 删除 API Key |
| `aiconfig encrypt` | 加密 keys.yaml 中的明文 Key |
| `aiconfig list` | 查看已配置的厂商和模型 |
| `aiconfig models` | 查看所有支持的模型 |
| `aiconfig check <model>` | 检查某个模型是否可用 |
| `aiconfig test <model>` | 测试模型连通性 |

## 支持的厂商

| 厂商 | 文本 | 图片 | 视频 | 音频 |
|---|---|---|---|---|
| OpenAI | gpt-5.4, gpt-4.1, o3, o4-mini... | gpt-image-1.5, dall-e-3... | - | gpt-4o-mini-tts... |
| Google | gemini-3.1-pro, gemini-2.5-flash... | imagen-4.0... | veo-3.1... | - |
| Qwen | qwen3-max, qwen3.5... | qwen-image-2.0-pro, wan2.7... | wan2.6-t2v... | qwen-audio |
| DeepSeek | deepseek-chat, deepseek-reasoner | - | - | - |
| MiniMax | MiniMax-M2.7... | image-01 | Hailuo-2.3... | speech-2.8-hd... |
| Kimi | kimi-k2.5, kimi-k2-thinking... | - | - | - |
| 火山引擎 | doubao-seed-2.0... | seedream-4.5... | seedance-2.0... | - |

编辑 `aiconfig/providers.yaml` 可自行添加或更新模型。

## 工作原理

```
你的项目                        aiconfig
    |                              |
    |  get_config("qwen-plus")     |
    |----------------------------->|
    |                              |-- 读 providers.yaml（模型 → 厂商 + base_url）
    |                              |-- 读 keys.yaml（厂商 → 加密的 key）
    |                              |-- 内存中解密 key
    |  {base_url, api_key, model}  |
    |<-----------------------------|
    |
    |  拿到配置，用任何 SDK 调用
```

- Key 加密存储，基于机器指纹（MAC 地址 + 用户名）生成密钥
- 解密仅在内存中进行，Key 不会泄露到其他文件
- 厂商和模型配置在 `providers.yaml` 中，可随时编辑

## License

MIT
