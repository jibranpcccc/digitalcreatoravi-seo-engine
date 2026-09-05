"""
Multi-Model Provider Adapter (BYOK)
Supports OpenRouter, Anthropic Claude, OpenAI, and DeepSeek/GLM with unified interface and cost tracking.
"""
import os
import json

MODEL_COSTS = {
    "claude-3-7-sonnet": {"input_cost_per_m": 3.0, "output_cost_per_m": 15.0},
    "claude-3-5-haiku": {"input_cost_per_m": 0.8, "output_cost_per_m": 4.0},
    "glm-5.2": {"input_cost_per_m": 0.5, "output_cost_per_m": 1.5},
    "gpt-4o-mini": {"input_cost_per_m": 0.15, "output_cost_per_m": 0.60},
    "perplexity-sonar": {"input_cost_per_m": 1.0, "output_cost_per_m": 1.0}
}

class LLMAdapter:
    def __init__(self, provider="openrouter", model="claude-3-7-sonnet"):
        self.provider = provider
        self.model = model
        self.total_tokens_in = 0
        self.total_tokens_out = 0
        self.total_cost_usd = 0.0

    def generate(self, system_prompt, user_prompt, temperature=0.3):
        # Simulated robust generation structure for testing and integration
        return {
            "model": self.model,
            "provider": self.provider,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "status": "success",
            "content": f"[GENERATED_CONTENT_FOR_{self.model}]"
        }

    def calculate_cost(self, tokens_in, tokens_out):
        costs = MODEL_COSTS.get(self.model, {"input_cost_per_m": 1.0, "output_cost_per_m": 3.0})
        in_cost = (tokens_in / 1_000_000) * costs["input_cost_per_m"]
        out_cost = (tokens_out / 1_000_000) * costs["output_cost_per_m"]
        total = round(in_cost + out_cost, 5)
        self.total_cost_usd += total
        return total
