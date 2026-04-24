# Anti-MathX 🧮

AI-powered Turkish university math problem solver. Covers Abstract Mathematics, Linear Algebra, Graph Theory, and Topology with step-by-step Chain of Thought solutions.

## Architecture

```
┌─────────────────┐     SSE Stream     ┌──────────────────┐     OpenAI API     ┌──────────────────┐
│   SolidJS App   │ ◄──────────────── │   FastAPI Server  │ ◄──────────────── │   vLLM Server    │
│   TailwindCSS   │                    │   Middleware      │                    │  Qwen2.5-Math    │
│   KaTeX         │                    │   CORS            │                    │  + LoRA Adapters  │
└─────────────────┘                    └──────────────────┘                    └──────────────────┘
```

## Quick Start

### Frontend (SolidJS)

```bash
cd client
npm install
npm run dev        # → http://localhost:5173
```

### Backend (FastAPI)

```bash
cd api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py     # → http://localhost:8080
```

> **Note:** The backend starts in **mock mode** by default (`MOCK_MODE=true`), returning pre-written solutions without GPU access.

### Environment Variables

Create `api/.env`:

```env
VLLM_BASE_URL=http://localhost:8000/v1
VLLM_API_KEY=sk-no-key-required
VLLM_MODEL_NAME=Qwen/Qwen2.5-Math-7B-Instruct
API_PORT=8080
CORS_ORIGINS=http://localhost:5173
MOCK_MODE=true
```

## Topics Covered

| Category | Subcategories |
|---|---|
| 🔮 Soyut Matematik | Denklik Bağıntısı, Kısmi Sıralama, İkili İşlemler, Gruplar, Halkalar |
| 📐 Lineer Cebir | Vektör Uzay, Alt Vektör Uzay, Determinant, Lineer Dönüşümler, Lineer Birleşim |
| 🔗 Çizge Teorisi | General coverage |
| 🍩 Topoloji | General coverage |

## Tech Stack

- **Frontend:** SolidJS, TailwindCSS v4, KaTeX, solid-markdown
- **Backend:** Python, FastAPI, SSE streaming
- **AI Engine:** Qwen2.5-Math-7B, Unsloth (LoRA fine-tuning), vLLM
- **Training:** JSONL dataset, Chain of Thought prompts in Turkish

## License

MIT
