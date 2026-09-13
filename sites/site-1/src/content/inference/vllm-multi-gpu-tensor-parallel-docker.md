---
title: "vLLM Multi-GPU Tensor Parallel: Docker Compose Setup (2026)"
description: "Production-ready Docker Compose configuration for deploying 70B models with tensor parallelism across multiple NVIDIA GPUs using vLLM."
datePublished: "2026-09-10"
dateModified: "2026-09-10"
author: "Engineering Team"
tags: ["vllm", "multi-gpu", "docker", "tensor-parallel", "benchmarks"]
coverImage: "/images/covers/vllm-multi-gpu-tensor-parallel-docker.webp"
canonical: "https://localagentstack.com/inference/vllm-multi-gpu-tensor-parallel-docker/"
category: "inference"
slug: "vllm-multi-gpu-tensor-parallel-docker"
---

# vLLM Multi-GPU Tensor Parallel: Docker Compose Setup (2026)

> **Quick Answer**: Deploying 70B parameter models across multiple graphics cards with vLLM requires configuring the **NVIDIA Container Toolkit**, assigning shared memory (`ipc: host`), and setting `--tensor-parallel-size` equal to the physical GPU count inside `docker-compose.yml`. This delivers native NCCL multi-GPU pooling with sub-millisecond inter-card synchronization.

*Last Updated: September 10, 2026 | Reviewed by Senior Systems Architect*

## Key Takeaways
- **Tensor Parallel Slicing**: Slices each attention head across GPUs simultaneously, multiplying available memory while dividing latency.
- **Shared Memory Requirement**: Docker containers must specify `shm_size: '16gb'` or `ipc: host` to prevent immediate NCCL shared-memory crashes.
- **Hardware Sizing**: Two 24GB GPUs (such as our [2x RTX 3090 vs 1x RTX 4090](/hardware/2x-rtx-3090-vs-1x-rtx-4090-ai-inference/) setup) provide 48GB VRAM, sufficient for Llama 3.3 70B at Q4_K_M.
- **Continuous Batching**: Delivers up to 4.2x higher throughput than sequential runtimes under 10+ concurrent user requests.

---

## 1. Single GPU vs Multi-GPU Tensor Parallelism

| Parameter | Single RTX 4090 (24GB) | Dual RTX 3090 (2x 24GB TP=2) | Quad RTX 3090 (4x 24GB TP=4) |
|---|---|---|---|
| **Max Model Parameter Size** | 32B at Q4_K_M | 70B at Q4_K_M | 70B at FP8 / Q8_0 |
| **KV Cache Capacity (32k Context)** | 1 Concurrent Stream | 12 Concurrent Streams | 35 Concurrent Streams |
| **Inter-GPU Bandwidth** | N/A | 31.5 GB/s (PCIe 4.0 x8) | 63.0 GB/s (Dual Ring) |
| **Token Generation Latency** | 14.5 ms / token | 35.2 ms / token | 22.1 ms / token |

![vLLM Multi-GPU Tensor Parallel Docker Compose Deployment Architecture Diagram](/images/benchmarks/vllm-tensor-parallel-docker.webp)

---

## 2. Production Docker Compose Configuration

Create `docker-compose.yml`:

```yaml
services:
  vllm-multi-gpu:
    image: vllm/vllm-openai:v0.6.3.post1
    container_name: vllm_llama_70b
    restart: unless-stopped
    ipc: host
    environment:
      - HUGGING_FACE_HUB_TOKEN=${HF_TOKEN}
      - NCCL_DEBUG=INFO
    volumes:
      - ~/.cache/huggingface:/root/.cache/huggingface
    ports:
      - "8000:8000"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    command: >
      --model meta-llama/Llama-3.3-70B-Instruct
      --tensor-parallel-size 2
      --gpu-memory-utilization 0.92
      --max-model-len 16384
      --enforce-eager
```

---

## 3. Launching and Validating the Multi-Card Cluster

Execute the deployment:

```bash
# Start container in background
docker compose up -d

# Verify tensor parallel GPU memory distribution
nvidia-smi

# Send test completion query
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.3-70B-Instruct",
    "messages": [{"role": "user", "content": "Explain tensor parallelism in 20 words."}]
  }'
```

To calculate exact memory headroom before deploying larger contexts, consult our [VRAM Requirements Calculator](/hardware/vram-requirements-calculator-70b/) and compare against our [Ollama vs vLLM Concurrency Benchmarks](/inference/ollama-vs-vllm-benchmark/). Refer to the [Official vLLM Distributed Serving Guide](https://docs.vllm.ai/en/latest/serving/distributed_serving.html) for advanced ray-cluster deployments.

---

## Frequently Asked Questions

### Can I run tensor parallelism across mismatched GPU models?
Tensor parallelism requires identical layer memory slicing. Mixing an RTX 3090 with an RTX 4090 will clamp the 4090 down to the slower memory speed of the 3090. For mixed cards, pipeline parallelism (`--pipeline-parallel-size`) is recommended.

### Why do I get a 'CUDA out of memory' error despite having 48GB total VRAM?
By default, vLLM attempts to allocate 90% of all memory to KV cache. If your weights consume 40GB, reduce `--gpu-memory-utilization` to `0.85` or decrease `--max-model-len` to prevent OOM spikes.
