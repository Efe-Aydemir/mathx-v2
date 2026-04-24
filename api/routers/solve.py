"""
Solve endpoint with SSE streaming support.
"""

import json
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from models.schemas import SolveRequest
from services.inference import stream_inference, stream_mock_inference
from config import settings

router = APIRouter(prefix="/api", tags=["solver"])


@router.post("/solve")
async def solve(request: SolveRequest):
    """
    Solve a math problem with streaming SSE response.

    The response streams token-by-token as Server-Sent Events.
    Each event contains a JSON payload: {"token": "..."}.
    The stream ends with a "data: [DONE]" event.
    """

    async def event_generator():
        # Choose between real and mock inference
        if settings.MOCK_MODE:
            stream = stream_mock_inference(
                request.category, request.subcategory, request.question
            )
        else:
            stream = stream_inference(
                request.category, request.subcategory, request.question
            )

        async for token in stream:
            data = json.dumps({"token": token}, ensure_ascii=False)
            yield f"data: {data}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "mock_mode": settings.MOCK_MODE,
        "model": settings.VLLM_MODEL_NAME if not settings.MOCK_MODE else "mock",
    }
