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
Plotly (interactive visualization)


Infrastructure
Docker
docker-compose


Folder Structure
Root Directory

backend/ – Backend computation and API services

frontend/ – User interface and visualization

docs/ – Project documentation and diagrams

docker-compose.yml – Container orchestration

README.md – Project overview and instructions

.gitignore – Git ignore rules



Backend

main.py – FastAPI application entry point

requirements.txt – Backend dependencies



API Layer

routes.py – REST API endpoints

schemas.py – Request/response schemas



Core Physics Layer

isentropic.py – Isentropic flow equations

normal_shock.py – Normal shock relations

oblique_shock.py – Oblique shock relations

fanno.py – Fanno flow relations

rayleigh.py – Rayleigh flow relations



Solver Layer

root_finding.py – Numerical root-finding utilities

isentropic_solvers.py – Inverse solvers for isentropic flow



Validation and Testing

reference_table.csv – Reference validation cases

validate.py – Validation scripts

test_smoke.py – Automated unit tests



Frontend

App.jsx – Main React application

main.jsx – React entry point

pages/ – UI pages for flow modules

components/ – Reusable UI components

plots/ – Plotly visualization components

api/ – Frontend API calls



Documentation

architecture_diagram.png – High-level system architecture diagram




How to Run (Development)

Backend

cd backend

pip install -r requirements.txt

uvicorn main:app --reload



Frontend

cd frontend

npm install

npm run dev



Key Design Principles

Stateless computation (no database)

Deterministic numerical results

Separation of concerns

Validation-driven development

Modular and extensible architecture
