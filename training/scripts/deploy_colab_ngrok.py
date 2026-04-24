"""
Anti-MathX — Free Deployment via Google Colab + ngrok

This script runs a vLLM server on Google Colab and exposes it to the internet
via ngrok, so your FastAPI backend can connect to it remotely.

Usage (in Google Colab):
  1. Install dependencies:
     !pip install vllm pyngrok

  2. Set your ngrok auth token (free at https://ngrok.com):
     import os
     os.environ["NGROK_AUTH_TOKEN"] = "your_ngrok_token"

  3. Run:
     %run deploy_colab_ngrok.py --model merged-model/

  4. Copy the ngrok URL and set it in your api/.env:
     VLLM_BASE_URL=https://xxxx-xx-xx-xx-xx.ngrok-free.app/v1

Note: Colab sessions are temporary (max ~12 hours). For production,
use RunPod, vast.ai, or HuggingFace Inference Endpoints.
"""

import argparse
import os
import sys
import threading
import time


def parse_args():
    parser = argparse.ArgumentParser(description="Deploy model via Colab + ngrok")
    parser.add_argument("--model", type=str, default="merged-model",
                        help="Path to merged model or HuggingFace model ID")
    parser.add_argument("--model-name", type=str, default="anti-mathx",
                        help="Name to serve the model as")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--ngrok-token", type=str, default="",
                        help="ngrok auth token (or set NGROK_AUTH_TOKEN env var)")
    parser.add_argument("--max-model-len", type=int, default=8192)
    return parser.parse_args()


def start_vllm_server(model: str, model_name: str, port: int, max_model_len: int):
    """Start vLLM server in a background thread."""
    import subprocess
    cmd = [
        sys.executable, "-m", "vllm.entrypoints.openai.api_server",
        "--model", model,
        "--served-model-name", model_name,
        "--host", "0.0.0.0",
        "--port", str(port),
        "--max-model-len", str(max_model_len),
        "--gpu-memory-utilization", "0.90",
        "--dtype", "auto",
        "--trust-remote-code",
    ]
    subprocess.run(cmd)


def wait_for_server(port: int, timeout: int = 300):
    """Wait until the vLLM server is ready."""
    import urllib.request

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            url = f"http://localhost:{port}/v1/models"
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req, timeout=5)
            if response.status == 200:
                return True
        except Exception:
            pass
        time.sleep(5)
        elapsed = int(time.time() - start_time)
        print(f"   ⏳ Waiting for vLLM server... ({elapsed}s)")
    return False


def main():
    args = parse_args()

    ngrok_token = args.ngrok_token or os.environ.get("NGROK_AUTH_TOKEN", "")
    if not ngrok_token:
        print("❌ ngrok auth token required!")
        print("   Set via --ngrok-token or NGROK_AUTH_TOKEN env var")
        print("   Get a free token at: https://dashboard.ngrok.com/get-started/your-authtoken")
        sys.exit(1)

    # Check dependencies
    try:
        from pyngrok import ngrok as ngrok_client
    except ImportError:
        print("❌ pyngrok not installed! Run: pip install pyngrok")
        sys.exit(1)

    try:
        import vllm  # noqa: F401
    except ImportError:
        print("❌ vLLM not installed! Run: pip install vllm")
        sys.exit(1)

    print("\n" + "=" * 55)
    print("  🧮 Anti-MathX — Colab + ngrok Deployment")
    print("=" * 55)
    print(f"  Model:  {args.model}")
    print(f"  Port:   {args.port}")
    print("=" * 55)

    # Start vLLM in background
    print("\n📦 Starting vLLM server in background...")
    server_thread = threading.Thread(
        target=start_vllm_server,
        args=(args.model, args.model_name, args.port, args.max_model_len),
        daemon=True,
    )
    server_thread.start()

    # Wait for server to be ready
    print("⏳ Waiting for model to load (this may take a few minutes)...")
    if not wait_for_server(args.port):
        print("❌ Server did not start within timeout!")
        sys.exit(1)

    print("✅ vLLM server is ready!\n")

    # Start ngrok tunnel
    print("🌐 Starting ngrok tunnel...")
    ngrok_client.set_auth_token(ngrok_token)
    tunnel = ngrok_client.connect(args.port, "http")

    public_url = tunnel.public_url
    api_url = f"{public_url}/v1"

    print("\n" + "=" * 55)
    print("  ✅ Deployment Successful!")
    print("=" * 55)
    print(f"  Public URL:  {public_url}")
    print(f"  API URL:     {api_url}")
    print(f"  Models:      {api_url}/models")
    print()
    print("  📝 Update your api/.env with:")
    print(f"     VLLM_BASE_URL={api_url}")
    print(f"     VLLM_MODEL_NAME={args.model_name}")
    print(f"     MOCK_MODE=false")
    print("=" * 55)
    print("\n  ⚠️  Keep this Colab session running!")
    print("  Press Ctrl+C to stop.\n")

    # Keep alive
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        ngrok_client.disconnect(tunnel.public_url)
        print("✅ Done.")


if __name__ == "__main__":
    main()
