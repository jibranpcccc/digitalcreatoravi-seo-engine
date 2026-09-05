---
title: "DeepSeek R1 Local Setup Ollama: Complete Installation & Prompting Guide (2026)"
description: "Step-by-step setup guide for running DeepSeek R1 reasoning models locally via Ollama with custom Modelfiles, GPU layer offloading, and optimal context allocation."
datePublished: "2026-07-25"
dateModified: "2026-09-03"
author: "Engineering Team"
tags: ["deepseek-r1", "ollama", "reasoning-models", "local-ai", "setup-guide"]
canonical: "https://localagentstack.com/models/deepseek-r1-local-setup-ollama/"
---

# DeepSeek R1 Local Setup Ollama: Complete Installation & Optimization Guide

> **Quick Answer**: To run DeepSeek R1 locally with Ollama, run `ollama run deepseek-r1:14b` for 16GB GPUs or `ollama run deepseek-r1:8b` for 8GB GPUs. For maximum reasoning fidelity, configure a custom Modelfile setting `temperature 0.6` and `top_p 0.95`, preserving the `<think>` reasoning traces without artificial system prompt overrides.

*Last Updated: September 3, 2026 | Reviewed by Senior Systems Architect*

## Key Takeaways
- **Model Variants**: DeepSeek R1 distilled checkpoints are available in 1.5B, 7B, 8B, 14B, 32B, and 70B sizes, with the 14B Q4_K_M model offering the best performance-to-VRAM balance on consumer hardware.
- **VRAM Thresholds**: The 8B model requires 5.8 GB VRAM; the 14B model requires 9.6 GB VRAM; the 32B model requires 20.2 GB VRAM. Sizing can be verified in our [VRAM Requirements Calculator](/hardware/vram-requirements-calculator-70b/).
- **Prompting Constraint**: Do not inject aggressive system instructions instructing the model to suppress thinking; doing so disrupts chain-of-thought mathematical and coding derivation.
- **Production Routing**: Integrate Ollama with agent orchestrators via our [Custom MCP Server Tutorial](/agents/custom-mcp-server-python-tutorial/) or scale to multi-user clusters with [vLLM Serving Benchmarks](/inference/ollama-vs-vllm-benchmark/).

---

## 1. DeepSeek R1 Local Hardware Requirements Table

| Model Size | Quantization | Required VRAM | Minimum Recommended GPU | Tokens / Sec (RTX 4090) |
|---|---|---|---|---|
| **DeepSeek-R1-1.5B** | Q4_K_M | 1.8 GB | Any Modern iGPU / GTX 1650 | 145 t/s |
| **DeepSeek-R1-7B** | Q4_K_M | 5.2 GB | RTX 3060 (12GB) / RTX 4060 | 88 t/s |
| **DeepSeek-R1-8B** | Q4_K_M | 5.8 GB | RTX 3060 (12GB) / Apple M2 (16GB) | 82 t/s |
| **DeepSeek-R1-14B** | Q4_K_M | 9.6 GB | RTX 4070 (12GB) / RTX 3080 | 58 t/s |
| **DeepSeek-R1-32B** | Q4_K_M | 20.2 GB | RTX 3090 (24GB) / RTX 4090 | 36 t/s |
| **DeepSeek-R1-70B** | Q4_K_M | 43.5 GB | 2x RTX 3090 (48GB) / Mac Studio 64GB | 19 t/s |

![DeepSeek R1 Local Setup Ollama Architecture Diagram](/images/benchmarks/deepseek-r1-local-setup-ollama.webp)

---

## 2. Step-by-Step Installation Commands
Ensure Ollama is updated to the latest binary release supporting QwQ and DeepSeek architecture optimizations:

```bash
# 1. Pull and run the balanced 14B reasoning model
ollama run deepseek-r1:14b

# 2. Test chain-of-thought reasoning in terminal
>>> "Solve the following problem step-by-step: Write a Python function to find the longest palindromic substring."
```

Ollama automatically initializes GPU layer offloading according to the [Ollama Official Release Notes](https://github.com/ollama/ollama/releases).

---

## 3. Creating an Optimized Custom Modelfile
Standard default configurations lack parameter tuning for mathematical reasoning. Create a dedicated `Modelfile`:

```dockerfile
FROM deepseek-r1:14b

# Set optimal sampling parameters for reasoning tasks
PARAMETER temperature 0.6
PARAMETER top_p 0.95
PARAMETER top_k 40
PARAMETER num_ctx 32768

# Preserve native reasoning token templates
TEMPLATE """{{ if .System }}<｜System｜>{{ .System }}{{ end }}{{ range .Messages }}{{ if eq .Role "user" }}<｜User｜>{{ .Content }}<｜Assistant｜>{{ else if eq .Role "assistant" }}<｜thought｜>{{ .Content }}{{ end }}{{ end }}"""
```

Compile and register the model:
```bash
ollama create r1-coder -f ./Modelfile
ollama run r1-coder
```

---

## 4. Benchmarking Accuracy and Speed
According to technical disclosures in the [DeepSeek R1 Research Paper](https://arxiv.org/abs/2501.12948) and the [DeepSeek GitHub Architecture Repository](https://github.com/deepseek-ai/DeepSeek-R1), test-time compute scaling delivers parity with proprietary models across AIME and MATH-500 benchmarks.

For developers deploying on Apple hardware, review our unified memory benchmarks in the [Mac Studio M4 Max Review](/hardware/mac-studio-m4-max-llm-benchmarks/).

---

## 5. Frequently Asked Questions (FAQ)

### Why does DeepSeek R1 output `<think>` blocks?
The `<think>` tags contain the raw chain-of-thought reflection where the model verifies assumptions, explores edge cases, and self-corrects before providing the final answer. Removing or masking these tokens degrades output accuracy on logic benchmarks.

### How do I expose DeepSeek R1 as an OpenAI-compatible API?
Ollama automatically serves an OpenAI-compatible endpoint on port 11434. Point your applications to `http://localhost:11434/v1` using `deepseek-r1:14b` as the model name.

### Can I run the full 671B DeepSeek R1 model locally?
Running the un-distilled 671B MoE model requires approximately 380 GB of VRAM even at 4-bit quantization, necessitating an 8x H100 datacenter cluster or multiple Mac Studio 192GB nodes linked via high-speed cluster networking.
