from pydantic import BaseModel, Field


class SolveRequest(BaseModel):
    """Request payload for the /api/solve endpoint."""

    category: str = Field(
        ...,
        description="Main category, e.g. 'Soyut Matematik', 'Lineer Cebir'",
        examples=["Soyut Matematik", "Lineer Cebir"],
    )
    subcategory: str = Field(
        ...,
        description="Subcategory within the main category",
        examples=["Denklik Bağıntısı", "Determinant"],
    )
    question: str = Field(
        ...,
        min_length=5,
        max_length=5000,
        description="The mathematical question to solve",
    )


class SolveResponse(BaseModel):
    """Non-streaming response (for testing)."""

    solution: str
    category: str
    subcategory: str


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    model_available: bool
