Compressible Flow Toolbox (RES Cycle II)
Overview

The Compressible Flow Toolbox is a web-based engineering application for solving compressible gas dynamics problems. The system allows users to select a flow model, provide known physical parameters, and compute all related flow properties using validated analytical relations and numerical methods.

The application is designed as a stateless scientific computation tool, focusing on numerical correctness, reproducibility, and clear separation of concerns.

Supported Flow Models

The toolbox supports the following compressible flow models:

Isentropic Flow

Normal Shock

Oblique Shock

Fanno Flow (flow with friction)

Rayleigh Flow (flow with heat addition)

Each module supports both direct and inverse problem solving.

System Architecture

The system follows a layered architecture:

Frontend: React (JavaScript) for user interaction and visualization

API Layer: FastAPI (Python) for request handling and validation

Solver Layer: Numerical root-finding and inversion logic

Core Physics Layer: Analytical gas dynamics equations

Validation Layer: Reference data and automated verification

All components are containerized using Docker for reproducible deployment.

Tech Stack
Backend

Python

FastAPI

NumPy

SciPy

Pydantic

Pytest

Frontend

React (JavaScript)

Plotly (for visualization)

Infrastructure

Docker

docker-compose

Folder Structure
backend/
  core/        # Physics equations
  solvers/     # Numerical methods
  api/         # REST API endpoints
  validation/  # Golden cases and validation scripts
  tests/       # Automated tests

frontend/
  src/
    pages/
    components/
    plots/
    api/

docs/
  architecture.md
  architecture_diagram.png

How to Run (Development)
Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

Frontend
cd frontend
npm install
npm run dev