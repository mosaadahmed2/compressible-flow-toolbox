# backend/main.py
from fastapi import FastAPI
from backend.api.routes import router


app = FastAPI(
    title="Compressible Flow Toolbox API",
    version="0.1.0",
    description="Validated compressible-flow calculations (direct + inverse).",
)

app.include_router(router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}
