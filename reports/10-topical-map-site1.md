# Topical Authority Architecture & Internal Linking Map: Site 1 (LocalAgentStack)

This document establishes the hierarchical topical authority blueprint and internal linking matrix for **Site 1**. Every URL serves a distinct search intent, preventing keyword cannibalization.

---

## 1. Topical Architecture Hierarchy

```
LocalAgentStack (Root)
│
├── 1.0 /inference/ (Pillar: Local Inference Runtimes)
│   ├── 1.1 /inference/ollama/ (Cluster Hub)
│   │   ├── 1.1.1 /inference/ollama/install-gpu-acceleration (Child Guide)
│   │   ├── 1.1.2 /inference/ollama/concurrency-speed-benchmark (Child Benchmark)
│   │   └── 1.1.3 /inference/ollama/context-window-expansion (Child Tutorial)
│   ├── 1.2 /inference/vllm/ (Cluster Hub)
│   │   ├── 1.2.1 /inference/vllm/multi-gpu-tensor-parallel (Child Guide)
│   │   └── 1.2.2 /inference/vllm/paged-attention-memory (Child Deep-Dive)
│   └── 1.3 /inference/llama-cpp/ (Cluster Hub)
│       └── 1.3.1 /inference/llama-cpp/q4-vs-q8-quantization (Child Benchmark)
│
├── 2.0 /agents/ (Pillar: Autonomous Agent Architectures)
│   ├── 2.1 /agents/claude-code/ (Cluster Hub)
│   │   ├── 2.1.1 /agents/claude-code/mcp-setup-guide (Child Tutorial)
│   │   └── 2.1.2 /agents/claude-code/automated-scheduled-tasks (Child Workflow)
│   ├── 2.2 /agents/langgraph/ (Cluster Hub)
│   └── 2.3 /agents/mcp-servers/ (Cluster Hub & Directory)
│
├── 3.0 /hardware/ (Pillar: Hardware Sizing & VRAM Engineering)
│   ├── 3.1 /hardware/vram-calculator/ (Interactive Tool)
│   ├── 3.2 /hardware/mac-studio-ai-benchmarks/ (Pillar Evaluation)
│   └── 3.3 /hardware/multi-gpu-workstation-builds/ (Hardware Guide)
│
├── 4.0 /models/ (Pillar: Open-Weight Models & Benchmarks)
│   ├── 4.1 /models/deepseek-r1-local-guide/ (Deep Guide)
│   └── 4.2 /models/llama-3-3-vs-qwen-coder/ (Comparison Matrix)
│
└── 5.0 /rag/ (Pillar: Local RAG & Privacy Stacks)
    ├── 5.1 /rag/chromadb-ollama-tutorial/ (Step-by-Step Guide)
    └── 5.2 /rag/air-gapped-enterprise-compliance/ (Whitepaper Guide)
```

---

## 2. Internal Linking Rules & Authority Flow
1. **Vertical Authority Flow (Up & Down)**:
   - Every child article MUST link up to its parent Cluster Hub using descriptive category anchors (e.g. `explore our full [vLLM multi-GPU serving guide]`).
   - Every Cluster Hub MUST link down to all child articles in its sub-cluster via an index grid.
2. **Horizontal Silo Linking (Sibling to Sibling)**:
   - Child articles within the same cluster MUST cross-link to adjacent steps in the workflow (e.g., the *Ollama Install* guide links directly to the *Ollama Concurrency Benchmark*).
3. **Cross-Silo Contextual Bridges**:
   - Cross-silo links are permitted ONLY when technically necessary (e.g. an article on *DeepSeek R1* linking to the *VRAM Requirements Calculator*).
4. **Anchor Text Diversity Policy**:
   - 60% Natural descriptive partial-match phrases.
   - 25% Technical entity names.
   - 15% Branded / Navigational anchors.
   - 0% Exact-match repetitive spam.
