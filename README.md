# 🚀 FastAPI Calculator API — Module 11

<div align="center">

[![Tests](https://img.shields.io/badge/tests-pytest-green)](#-tests) 
[![Docker](https://img.shields.io/badge/docker-compose-blue)](#-docker-usage) 
[![CI/CD](https://img.shields.io/badge/github%20actions-passed-brightgreen)](#-github-actions-cicd)

A production-ready FastAPI application with user authentication, calculator operations, PostgreSQL persistence, comprehensive testing, Docker support, and GitHub Actions CI/CD pipeline.

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation--setup)
- [Database Setup](#-database-setup)
- [Running the App](#-running-the-app)
- [API Examples](#-api-examples)
- [Testing](#-testing)
- [Docker](#-docker-usage)
- [CI/CD Pipeline](#-github-actions-cicd)
- [Reflection](#-reflection)
- [Screenshots](#-screenshots)

---

## ✨ Features

### 👤 User Management
- Register new users with validation
- Login with secure password hashing
- Pydantic-based request validation

### 🧮 Calculator System
- **Operations**: Addition, subtraction, multiplication, division
- **Safety**: Division-by-zero protection
- **Persistence**: SQLAlchemy with PostgreSQL
- **API Endpoints**:
  - `GET /calculations` — List all calculations
  - `GET /calculations/{id}` — Get single calculation
  - `POST /calculations` — Create new calculation
  - `PUT /calculations/{id}` — Update calculation
  - `DELETE /calculations/{id}` — Delete calculation

### 🧪 Testing & Quality
- Unit tests for schemas, factory patterns, security
- Integration tests for database + API routes
- 100% test coverage with pytest

### 🐳 Docker & Deployment
- Containerized app + PostgreSQL
- Consistent local & production environments
- Docker Compose orchestration

### ⚙️ CI/CD Pipeline
- Automated testing on every push
- Docker image building & registry push
- GitHub Actions workflow

---

## 📁 Project Structure

```
fastapi-project/
│
├── app/
│   ├── core/
│   │   ├── calculation_factory.py
│   │   └── security.py
│   ├── db/
│   │   ├── base.py
│   │   ├── init_db.py
│   │   └── session.py
│   ├── models/
│   │   ├── user.py
│   │   └── calculation.py
│   ├── schemas/
│   │   ├── user.py
│   │   └── calculation.py
│   ├── crud/
│   │   ├── user.py
│   │   └── calculation.py
│   ├── dependencies.py
│   └── main.py
│
├── tests/
│   ├── unit/
│   │   ├── test_calculation_factory.py
│   │   ├── test_security.py
│   │   ├── test_calculation_schemas.py
│   │   └── test_schemas.py
│   └── integration/
│       ├── test_user_model.py
│       ├── test_user_routes.py
│       ├── test_calculation_model.py
│       └── test_calculation_routes.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── reflection_md12.md
└── README.md
```

---

## 🛠 Installation & Setup

### 1️⃣ Clone & Navigate

```bash
cd fastapi-project
```

### 2️⃣ Create Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄 Database Setup

Start PostgreSQL using Docker Compose:

```bash
docker-compose up -d
```

| Service | Port | Purpose |
|---------|------|---------|
| `postgres` | 5432 | Main database |
| `fastapi-app` | 8000 | API server (optional) |

The app automatically connects using `DATABASE_URL` from environment variables.

---

## ▶ Running the App

Start the development server:

```bash
uvicorn app.main:app --reload
```

**Access the application:**
- 🌐 API Root: http://127.0.0.1:8000
- 📚 Swagger UI: http://127.0.0.1:8000/docs
- 📖 ReDoc: http://127.0.0.1:8000/redoc

---

## 📌 API Examples

### 👤 Register User

```http
POST /users/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "strongpass123"
}
```

### 🔑 Login User

```http
POST /users/login
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "strongpass123"
}
```

### ➕ Create Calculation

```http
POST /calculations
Content-Type: application/json

{
  "a": 10,
  "b": 5,
  "type": "add"
}
```

**Response:**
```json
{
  "id": 1,
  "a": 10,
  "b": 5,
  "type": "add",
  "result": 15,
  "user_id": null
}
```

### 📊 Retrieve Calculations

```http
GET /calculations
```

### 🔍 Get Single Calculation

```http
GET /calculations/1
```

### ✏️ Update Calculation

```http
PUT /calculations/1
Content-Type: application/json

{
  "a": 15,
  "b": 3,
  "type": "subtract"
}
```

### 🗑 Delete Calculation

```http
DELETE /calculations/1
```

---

## 🧪 Testing

Run all tests:

```bash
pytest -q
```

Run with verbose output:

```bash
pytest -v
```

Run specific test file:

```bash
pytest tests/unit/test_calculation_factory.py -v
```

**Expected output:**
```
====================== all tests passed ======================
```

> ⚠️ **Note**: Integration tests require PostgreSQL running (`docker-compose up -d`)

---

## 🐳 Docker Usage

### Build & Run with Docker Compose

```bash
docker-compose up --build
```

This starts both the FastAPI app and PostgreSQL database.

### Manual Docker Build & Push

```bash
docker build -t yourname/fastapi-project:latest .
docker push yourname/fastapi-project:latest
```

### Stop Containers

```bash
docker-compose down
```

---

## 🤖 GitHub Actions (CI/CD)

**Pipeline Location:** `.github/workflows/ci-cd.yml`

### Pipeline Steps:
1. ✅ Python environment setup
2. 📦 Install dependencies
3. 🧪 Run unit & integration tests
4. 🐳 Build Docker image
5. 📤 Push to Docker Hub (requires secrets)

### Required Secrets in GitHub:
- `DOCKER_USERNAME` — Docker Hub username
- `DOCKER_PASSWORD` — Docker Hub access token

---

## 📝 Reflection

Detailed reflection on the project is available in [`reflection_md12.md`](./reflection_md12.md).

**Topics covered:**
- Secure API route design
- SQLAlchemy + Pydantic integration
- Integration test debugging strategies
- Docker networking & multi-container setups
- CI/CD pipeline learnings

---

## 📸 Screenshots

Please include the following screenshots in your submission:

1. ✅ **Pytest Output** — All tests passed
2. 🎨 **Swagger UI** — User & calculator endpoints
3. 🚀 **GitHub Actions** — Successful CI/CD pipeline
4. 🐳 **Docker Desktop** — Running containers
5. 📊 **Sample Calculation** — Created via Swagger UI

---

## 📄 License

This project is part of IS601 coursework at NJIT.

---

<div align="center">

**Made with ❤️ for NJIT IS601**

</div>