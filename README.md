# FastAPI Calculator – Final Project (IS601)

A full‑stack FastAPI web application implemented as the IS601 Final Project.  
Demonstrates backend API design, database integration, frontend interaction, automated testing (unit, integration, E2E), CI/CD, and containerization.

---

## 📌 Overview

This application allows users to:
- Register and log in securely
- Perform basic and advanced calculations
- View calculation history and summary reports
- Update profile and change passwords

The project is fully tested (pytest + Playwright) and Dockerized for reproducible local/dev environments.

---

## 🚀 Features

- 🔐 User Authentication
  - Register and login with hashed passwords
  - Profile view and password change

- 🧮 Calculations (BREAD)
  - Browse, read, add, edit, and delete calculations
  - Validation via Pydantic + calculation factory pattern

- ➕ Advanced Operations
  - add, sub, mul, div, power, mod, floordiv, sqrt, log, factorial, absdiff

- 📊 Reports & History
  - Summary (total calculations, most used operation, averages, last ID)
  - Recent calculations list (with configurable limit)
  - Endpoints: `GET /reports/summary`, `GET /reports/recent?limit=10`
  - UI page: `/reports-page`

- 🧪 Testing & Automation
  - Unit and integration tests (pytest)
  - End-to-end tests with Playwright (browser automation)
  - CI pipeline runs full test suites and builds Docker images

- 🐳 Containerization & Deployment
  - Dockerfile and docker-compose for app + PostgreSQL
  - GitHub Actions for CI/CD

---

## 🛠 Technology Stack

- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- HTML / JavaScript (static templates)
- Pytest (unit & integration)
- Playwright (E2E)
- Docker & Docker Compose
- GitHub Actions (CI/CD)

---

## 📁 Project Structure (simplified)

```
app/
 ├── core/
 ├── crud/
 ├── db/
 ├── models/
 ├── routers/     # or routes/
 ├── schemas/
 ├── static/
 │    └── html/
 └── main.py
tests/
 ├── unit/
 ├── integration/
 └── e2e/
Dockerfile
docker-compose.yml
requirements.txt
README.md
reflection.md
```

---

## ▶️ Running Locally

1. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
# For Playwright E2E:
playwright install
```

3. Start PostgreSQL (Docker)
```bash
docker compose up -d db
```

4. Run the application
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🌐 Useful URLs (local)

- Home: http://127.0.0.1:8000/
- Register: http://127.0.0.1:8000/register-page
- Login: http://127.0.0.1:8000/login-page
- Calculations (BREAD): http://127.0.0.1:8000/calculations-page
- Reports: http://127.0.0.1:8000/reports-page
- Profile: http://127.0.0.1:8000/profile-page
- API Docs (Swagger): http://127.0.0.1:8000/docs

---

## 🧪 Testing

Run all tests:
```bash
pytest
```

Run suites:
- Unit: `pytest tests/unit`
- Integration: `pytest tests/integration`
- E2E (Playwright):
  1. Start the app: `uvicorn app.main:app --host 127.0.0.1 --port 8000`
  2. Run: `pytest tests/e2e`

> Note: Integration and E2E tests expect a running Postgres instance (start with `docker-compose up -d`).

---

## 🐳 Docker

Build image:
```bash
docker build -t hirthick/fastapi-project:latest .
```

Run container:
```bash
docker run -p 8000:8000 hirthick/fastapi-project:latest
```

Use docker-compose for app + DB:
```bash
docker compose up --build
```

---

## 🔄 CI/CD (GitHub Actions)

The GitHub Actions pipeline:
- Sets up Python environment
- Installs dependencies
- Runs unit, integration, and E2E tests
- Builds the Docker image
- Optionally pushes the image (requires secrets)

Runs automatically on pushes to the main branch.

---

## 📝 Reflection

See `reflection.md` for detailed notes on architecture, testing approach, CI/CD setup, challenges, and lessons learned.

---

## ✅ Project Status

- All required features implemented
- Tests in place (unit, integration, E2E)
- Dockerized application
- CI/CD pipeline configured
- Documentation updated

---

## 🎓 Final Notes

This project demonstrates a complete end‑to‑end web application lifecycle for the IS601 Final Project. Contributions and issues are welcome — please open a GitHub issue or PR.