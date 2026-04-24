#!/bin/bash
# ====================================================================
# Anti-MathX — vLLM Server Deployment Script
#
# This script starts a vLLM-powered OpenAI-compatible API server
# for serving the fine-tuned Qwen2.5-Math model.
#
# Usage:
#   bash deploy_vllm.sh                         # Use default merged-model/
#   bash deploy_vllm.sh /path/to/merged-model    # Specify model path
#   bash deploy_vllm.sh username/model-name      # Use HuggingFace Hub model
#
# Requirements:
#   pip install vllm
# ====================================================================

set -e

# ── Configuration ──
MODEL_PATH="${1:-merged-model}"
MODEL_NAME="${2:-anti-mathx}"
PORT="${3:-8000}"
HOST="0.0.0.0"
MAX_MODEL_LEN=8192
GPU_MEMORY_UTILIZATION=0.90
DTYPE="auto"

echo "============================================"
echo "  🧮 Anti-MathX — vLLM Server"
echo "============================================"
echo "  Model:     ${MODEL_PATH}"
echo "  Served as: ${MODEL_NAME}"
echo "  Endpoint:  http://${HOST}:${PORT}/v1"
echo "  Max Len:   ${MAX_MODEL_LEN}"
echo "============================================"
echo ""

# ── Check vLLM installation ──
if ! python -c "import vllm" 2>/dev/null; then
    echo "❌ vLLM is not installed!"
    echo "   Install with: pip install vllm"
    exit 1
fi

# ── Check GPU availability ──
if python -c "import torch; assert torch.cuda.is_available()" 2>/dev/null; then
    GPU_NAME=$(python -c "import torch; print(torch.cuda.get_device_name(0))")
    GPU_MEM=$(python -c "import torch; print(f'{torch.cuda.get_device_properties(0).total_mem/1024**3:.1f}')")
    echo "✅ GPU detected: ${GPU_NAME} (${GPU_MEM} GB VRAM)"
else
    echo "⚠️  No GPU detected! vLLM requires a CUDA-capable GPU."
    echo "   If running on CPU, consider using llama.cpp or Ollama instead."
    exit 1
fi

echo ""
echo "🚀 Starting vLLM server..."
echo "   Press Ctrl+C to stop"
echo ""

# ── Start vLLM ──
python -m vllm.entrypoints.openai.api_server \
    --model "${MODEL_PATH}" \
    --served-model-name "${MODEL_NAME}" \
    --host "${HOST}" \
    --port "${PORT}" \
    --max-model-len "${MAX_MODEL_LEN}" \
    --gpu-memory-utilization "${GPU_MEMORY_UTILIZATION}" \
    --dtype "${DTYPE}" \
    --trust-remote-code \
    --disable-log-requests
