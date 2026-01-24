from fastapi import FastAPI

app = FastAPI(
    title="Compressible Flow Toolbox API",
    description="Backend API for validated compressible flow calculations",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "Compressible Flow Toolbox API running"}

@app.get("/health")
def health():
    return {"status": "ok"}
