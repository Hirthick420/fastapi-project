# 🚀 FastAPI Calculator API — Module 11

[![Tests](https://img.shields.io/badge/tests-pytest-green)](#tests) [![Docker](https://img.shields.io/badge/docker-compose-blue)](#docker-usage) [![CI/CD](https://img.shields.io/badge/github%20actions-passed-brightgreen)](#github-actions-cicd)

A FastAPI application that adds a Calculator feature: perform arithmetic operations via API, persist calculations to PostgreSQL, and includes unit & integration tests, Docker support, and a GitHub Actions pipeline.

---

## Table of Contents
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation--setup)
- [Database Setup](#database-setup)
- [Run the App](#run-the-app)
- [API Example](#api-example)
- [Testing](#tests)
- [Docker Usage](#docker-usage)
- [GitHub Actions (CI/CD)](#github-actions-cicd)
- [Reflection](#reflection)
- [Required Screenshots](#required-screenshots)

---

## Project Structure
fastapi-project/
```
app/
├── core/
│   └── calculation_factory.py
├── db/
│   ├── base.py
│   └── session.py
├── models/
│   ├── user.py
│   └── calculation.py
├── schemas/
│   ├── user.py
│   └── calculation.py
├── routers/
│   ├── user.py
│   └── calculation.py
└── main.py

tests/
├── unit/
│   ├── test_calculation_factory.py
│   └── test_calculation_schemas.py
├── integration/
│   ├── test_calculation_model.py
│   └── conftest.py

Dockerfile
docker-compose.yml
requirements.txt
.github/workflows/ci-cd.yml
reflection_md11.md
README.md
```

---

## Features
- Calculator API: add, subtract, multiply, divide
- Persists calculations in PostgreSQL (SQLAlchemy)
- Pydantic schemas and validation
- Unit & integration tests (pytest)
- Docker + docker-compose for local development
- GitHub Actions CI/CD workflow

---

## Installation & Setup

1. Create & activate a virtual environment
   - macOS/Linux:
     python3 -m venv .venv
     source .venv/bin/activate
   - Windows:
     python3 -m venv .venv
     .venv\Scripts\activate

2. Install dependencies
   pip install -r requirements.txt

---

## Database Setup
- By default the app uses PostgreSQL via docker-compose.
- To run without Docker, update DATABASE_URL in `app/db/session.py`.

---

## Run the App

Using Uvicorn (development):
uvicorn app.main:app --reload

App URLs:
- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

---

## API Example

POST /calculator
Request
```json
{
  "operation": "add",
  "a": 10,
  "b": 5
}
```

Response
```json
{
  "id": 1,
  "operation": "add",
  "a": 10,
  "b": 5,
  "result": 15,
  "created_at": "2025-11-24T19:23:00Z"
}
```

Supported operations: `add`, `subtract`, `multiply`, `divide`. Division by zero is validated by Pydantic / application code.

---

## Tests

Run tests:
pytest -q

Expected in your environment for this project:
19 passed, 0 failed

---

## Docker Usage

Build and run with Docker Compose:
docker compose up --build

Services:
- FastAPI app (port 8000)
- PostgreSQL (port 5432)

Images produced:
- fastapi-app
- postgres:15

---

## GitHub Actions (CI/CD)

Workflow: `.github/workflows/ci-cd.yml`

Pipeline tasks:
- Create Python environment
- Install dependencies
- Run pytest
- Build Docker image
- Login & push to Docker Hub

---

## Reflection

See `reflection_md11.md` for a 200–250 word reflection covering:
- hashing passwords
- input validation with Pydantic
- Docker Hub & GitHub Actions challenges
- environment variables
- test-driven development

---

## Required Screenshots to Submit
1. All tests passed (terminal output: `19 passed, 0 failed`)
2. Swagger UI showing calculation route (`/docs`)
3. GitHub Actions page with green checks for build-and-test and docker-build-and-push
4. Docker Desktop showing both containers (app, db)
5. PostgreSQL logs showing INSERTs for calculations

---

If you want additional badges, diagrams, or a short quickstart script added, tell me which items to include.

