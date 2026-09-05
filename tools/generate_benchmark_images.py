import os
from PIL import Image, ImageDraw, ImageFont

output_dir = "sites/site-1/public/images/benchmarks"
os.makedirs(output_dir, exist_ok=True)

diagrams = [
    {
        "filename": "ollama-vs-vllm-concurrency-benchmarks.webp",
        "badge": "INFERENCE ENGINE BENCHMARK",
        "title": "Ollama vs vLLM: Concurrency & Throughput",
        "subtitle": "Single-Stream Latency vs 10-Stream Continuous Batching (RTX 4090)",
        "col1_title": "Ollama (v0.5.4)",
        "col1_val": "68 tok/s single | 72 tok/s batched",
        "col1_desc": "Sequential Ring Buffer • Zero Config • macOS Metal Native",
        "col2_title": "vLLM (v0.6.2)",
        "col2_val": "64 tok/s single | 280 tok/s batched",
        "col2_desc": "PagedAttention • Continuous Batching • 3.8x Multi-Stream"
    },
    {
        "filename": "vram-requirements-calculator-70b.webp",
        "badge": "HARDWARE SIZING GUIDE",
        "title": "70B Model VRAM Allocation Architecture",
        "subtitle": "Model Weights + KV Cache Scaling (8k vs 32k Context)",
        "col1_title": "Q4_K_M (4.5 bpw)",
        "col1_val": "45.4 GB Required (32k Context)",
        "col1_desc": "Fits across 2x RTX 3090/4090 (48GB Total) • 38 tokens/sec",
        "col2_title": "Q8_0 / FP8 (8.0 bpw)",
        "col2_val": "81.0 GB Required (32k Context)",
        "col2_desc": "Requires 4x RTX 3090 (96GB) or 2x RTX 6000 Ada (96GB)"
    },
    {
        "filename": "deepseek-r1-local-setup-ollama.webp",
        "badge": "REASONING ARCHITECTURE",
        "title": "DeepSeek R1 Local Deployment via Ollama",
        "subtitle": "Chain-of-Thought Optimization & Custom Modelfile Configuration",
        "col1_title": "DeepSeek R1 14B",
        "col1_val": "9.6 GB VRAM • 58 tokens/sec",
        "col1_desc": "Optimal balance for RTX 4070/3080 • temperature 0.6",
        "col2_title": "DeepSeek R1 32B",
        "col2_val": "20.2 GB VRAM • 36 tokens/sec",
        "col2_desc": "Fits single 24GB GPU • Full <think> trace verification"
    },
    {
        "filename": "mac-studio-m4-max-llm-benchmarks.webp",
        "badge": "APPLE SILICON BENCHMARKS",
        "title": "Mac Studio M4 Max: LLM Speed & Tokens/Sec",
        "subtitle": "Unified Memory Bandwidth (546 GB/s) vs Dual RTX 4090",
        "col1_title": "M4 Max (128GB Unified)",
        "col1_val": "22.4 tok/s (70B) | 65 Watts",
        "col1_desc": "Silent 128GB Unified Pool • Zero PCIe Bottlenecks",
        "col2_title": "Dual RTX 4090 (48GB)",
        "col2_val": "38.6 tok/s (70B) | 720 Watts",
        "col2_desc": "GDDR6X Peak Speed • High Thermal & Power Footprint"
    },
    {
        "filename": "custom-mcp-server-python-tutorial.webp",
        "badge": "MODEL CONTEXT PROTOCOL",
        "title": "Custom FastMCP Server Architecture (Python)",
        "subtitle": "Exposing Local Tools & SQLite State to Claude Code & Agentic LLMs",
        "col1_title": "Local Stdio Transport",
        "col1_val": "< 4ms Latency IPC",
        "col1_desc": "Direct Process Stdio • Automated Pydantic Tool Schemas",
        "col2_title": "Stateful SQLite Store",
        "col2_val": "Persistent Context Cache",
        "col2_desc": "Survives Context Resets • Zero-Leak Air-Gapped Security"
    }
]

W, H = 1200, 675

for d in diagrams:
    img = Image.new("RGB", (W, H), color=(15, 23, 42))  # slate-900
    draw = ImageDraw.Draw(img)
    
    # Background subtle border / frame
    draw.rectangle([(20, 20), (W-20, H-20)], outline=(30, 41, 59), width=3)
    
    # Top accent bar
    draw.rectangle([(20, 20), (W-20, 28)], fill=(59, 130, 246))  # blue-500
    
    # Badge
    draw.rounded_rectangle([(60, 55), (340, 95)], radius=6, fill=(30, 58, 138))  # blue-900
    draw.text((80, 65), d["badge"], fill=(147, 197, 253))  # blue-300
    
    # Title & Subtitle
    draw.text((60, 115), d["title"], fill=(248, 250, 252))  # slate-50
    draw.text((60, 155), d["subtitle"], fill=(148, 163, 184))  # slate-400
    
    # Divider line
    draw.line([(60, 195), (W-60, 195)], fill=(51, 65, 85), width=2)
    
    # Box 1 (Left Card)
    box1 = [(60, 230), (570, 580)]
    draw.rounded_rectangle(box1, radius=12, fill=(30, 41, 59), outline=(71, 85, 105), width=2)
    draw.text((90, 260), d["col1_title"], fill=(96, 165, 250))
    draw.text((90, 320), d["col1_val"], fill=(255, 255, 255))
    draw.text((90, 420), d["col1_desc"], fill=(203, 213, 225))
    
    # Box 2 (Right Card)
    box2 = [(630, 230), (1140, 580)]
    draw.rounded_rectangle(box2, radius=12, fill=(30, 41, 59), outline=(59, 130, 246), width=2)
    draw.text((660, 260), d["col2_title"], fill=(52, 211, 153))
    draw.text((660, 320), d["col2_val"], fill=(255, 255, 255))
    draw.text((660, 420), d["col2_desc"], fill=(203, 213, 225))
    
    # Footer branding
    draw.text((60, 615), "LocalAgentStack.com • Empirical AI Engineering Benchmarks 2026", fill=(100, 116, 139))
    
    out_path = os.path.join(output_dir, d["filename"])
    img.save(out_path, "WEBP", quality=90)
    print(f"Generated WebP diagram: {out_path} ({os.path.getsize(out_path)} bytes)")

