# backend/main.py
from fastapi import FastAPI
from backend.api.routes import router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
    title="Compressible Flow Toolbox API",
    version="0.1.0",
    description="Validated compressible-flow calculations (direct + inverse).",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://compressible-flow-toolbox.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}
