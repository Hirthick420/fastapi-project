🚀 FastAPI Calculator API – Module 11 (Calculations, Testing & Docker CI/CD)

This project extends the previous FastAPI application by adding a full Calculator feature, including:

New Calculation model

New Calculation factory

New Calculation Pydantic schemas

Complete unit & integration tests

Updated database models

Updated routers

Docker support + GitHub Actions CI/CD pipeline

Reflection document

This README explains how to run, test, and build the project.

📁 Project Structure
fastapi-project/
│── app/
│   ├── core/
│   │    └── calculation_factory.py
│   ├── db/
│   │    ├── base.py
│   │    ├── session.py
│   ├── models/
│   │    ├── user.py
│   │    └── calculation.py
│   ├── schemas/
│   │    ├── user.py
│   │    └── calculation.py
│   ├── routers/
│   │    ├── user.py
│   │    └── calculation.py
│   └── main.py
│
│── tests/
│   ├── unit/
│   │    ├── test_calculation_factory.py
│   │    └── test_calculation_schemas.py
│   ├── integration/
│   │    ├── test_calculation_model.py
│   │    └── conftest.py
│
│── Dockerfile
│── docker-compose.yml
│── requirements.txt
│── ci-cd.yml
│── reflection_md11.md
│── README.md  ← (this file)

📦 Installation & Setup
1. Create & activate virtual environment
python3 -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows

2. Install dependencies
pip install -r requirements.txt

🗄️ Database Setup

The database is automatically created when running the FastAPI app using:

SQLAlchemy ORM

PostgreSQL through docker-compose

To run locally without Docker, update DATABASE_URL in:

app/db/session.py

▶️ Running the FastAPI Application
Using Uvicorn:
uvicorn app.main:app --reload


App runs at:

👉 http://127.0.0.1:8000

Swagger docs:

👉 http://127.0.0.1:8000/docs

🧮 Calculation Feature

The new feature includes:

API route for performing calculations

Stores operations in PostgreSQL

Supports:

addition

subtraction

multiplication

division

Example POST request
POST /calculator
{
  "operation": "add",
  "a": 10,
  "b": 5
}

Example response
{
  "id": 1,
  "operation": "add",
  "a": 10,
  "b": 5,
  "result": 15,
  "created_at": "2025-11-24T19:23:00Z"
}

🧪 Running Tests

The project includes unit + integration tests.

Run:

pytest -q


Expected (you achieved this):

19 passed, 0 failed

🐳 Docker Usage
Build and run locally:
docker compose up --build


Services started:

FastAPI app (port 8000)

PostgreSQL (port 5432)

Images created:

fastapi-app

postgres:15

🔄 GitHub Actions CI/CD Pipeline

Workflow located at:

.github/workflows/ci-cd.yml


Pipeline performs:

✔️ Create Python environment
✔️ Install dependencies
✔️ Run pytest
✔️ Build Docker image
✔️ Login to Docker Hub
✔️ Push final image to Docker Hub

You successfully ran:

build-and-test

docker-build-and-push

Both jobs show green ✔ success.

📄 Reflection Document

File: reflection_md11.md
Contains 200–250 word reflection on:

hashing passwords

validating input with Pydantic

Docker Hub & GitHub Actions hurdles

environment variables

test-driven development

📷 Required Screenshots to Submit

Submit these 5 screenshots:

✅ 1. All tests passed

From terminal:

19 passed, 0 failed

✅ 2. Swagger UI showing calculation route

/docs page

✅ 3. GitHub Actions page showing success

The page with build-and-test and docker-build-and-push green check marks.

✅ 4. Docker Desktop showing both containers running

app

db

✅ 5. PostgreSQL logs showing INSERTs for calculations

Your screenshot of duplicate users is OK.

