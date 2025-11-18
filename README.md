# FastAPI Secure User Service

This project implements a secure FastAPI-based user registration API with hashed passwords, database storage, unit tests, integration tests, Docker Compose support, and CI/CD deployment to Docker Hub.

Project structure
```
app/
  core/
  crud/
  db/
  models/
  schemas/
  main.py
tests/
  unit/
  integration/
Dockerfile
docker-compose.yml
requirements.txt
.github/workflows/ci-cd.yml
README.md
```

Quickstart — Run locally
1. Create & activate virtualenv
```bash
python3 -m venv .venv
source .venv/bin/activate
# Windows PowerShell:
# python -m venv .venv
# .venv\Scripts\activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run app
```bash
uvicorn app.main:app --reload
```

Open:
- http://localhost:8000/docs
- http://localhost:8000/health

Running tests
- Unit tests:
```bash
pytest tests/unit -q
```
- Integration tests (requires PostgreSQL in Docker):
1. Start DB: `docker compose up -d`
2. Create test DB: `docker exec -it fastapi-db psql -U postgres -c "CREATE DATABASE fastapi_test_db;"`
3. Set env: `export TEST_DATABASE_URL="postgresql://postgres:postgres@localhost:5432/fastapi_test_db"`
4. Run: `pytest tests/integration -q`

Docker
Build:
```bash
docker build -t hirthick/fastapi-secure-user:latest .
```
Run (with PostgreSQL on same Docker network):
```bash
docker run -d --name fastapi-secure-user --network fastapi-project_default -p 8000:8000 \
  -e DATABASE_URL="postgresql://postgres:postgres@fastapi-db:5432/fastapi_db" \
  hirthick/fastapi-secure-user:latest
```

CI/CD
Workflow: `.github/workflows/ci-cd.yml` — runs tests, builds image, pushes to Docker Hub on pushes to `main`.

Notes
- Uses `DATABASE_URL` (defaults to SQLite `./dev.db` if unset).
- Customize models/schemas/core inside `app/`.
