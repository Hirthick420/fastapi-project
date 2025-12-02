# Module 12 – User & Calculation Routes + Integration Testing

## What I implemented

In this module I completed the back-end logic of my FastAPI calculator API by adding
real HTTP routes on top of the models and schemas from earlier modules.

**User routes**

- `POST /users/register`  
  - Accepts a `UserCreate` Pydantic schema (username, email, password).
  - Hashes the password using the existing security helper.
  - Stores the new user in the PostgreSQL database using SQLAlchemy.
  - Returns a `UserRead` schema (no password hash in the response).

- `POST /users/login`  
  - Looks up the user by username.
  - Verifies the password against the stored hash.
  - Returns the same `UserRead` schema on success.
  - Returns an HTTP error if the credentials are invalid.

**Calculation routes (BREAD)**

- `GET /calculations` – browse all stored calculations.
- `GET /calculations/{id}` – read a single calculation by id.
- `POST /calculations` – create a new calculation using `CalculationCreate`.
  - Uses the calculation factory to compute the result based on the `type`
    ("add", "sub", "mul", "div").
  - Saves the calculation with SQLAlchemy.
- (Optional future work: add PUT/PATCH/DELETE endpoints for full BREAD support.)

All routes use the Pydantic schemas (`UserCreate`, `UserRead`, `CalculationCreate`,
`CalculationRead`) so request/response bodies are validated and documented automatically
in the OpenAPI docs.

## How I tested it

- I ran the API locally via:

  ```bash
  uvicorn app.main:app --reload
I used Swagger UI at /docs to manually test:

registering a user

logging in with the same credentials

creating a calculation

browsing and reading calculations by id

I wrote integration tests in tests/integration/test_user_routes.py and
tests/integration/test_calculation_routes.py (or similar names) using TestClient:

Register + login round-trip for a user.

Duplicate registration returns an error instead of creating a new user.

Create a calculation, read it back, and verify the result.

Check that invalid input returns the correct HTTP status codes.

I ran all tests with:

docker-compose up -d   # start Postgres
pytest -q


All tests (unit + integration) pass.

CI/CD and Docker

My existing GitHub Actions workflow still runs pytest on each push.

The tests now include the new user and calculation routes.

The application can be built into a Docker image and run together with
PostgreSQL via docker-compose.yml.

A successful CI run indicates that the image is buildable and the tests pass,
which is the basis for continuous deployment to Docker Hub.

What I learned / challenges

I saw how everything from previous modules fits together:

FastAPI routes (endpoints)

SQLAlchemy models for persistence

Pydantic schemas for validation and serialization

Docker + PostgreSQL for a real database

pytest integration tests for end-to-end behaviour

I understood why integration tests need a real database running (via Docker)
and why tests were failing when Postgres was not started.

I practiced using Swagger UI (/docs) to manually verify my API, which is
helpful both for debugging and for demonstrating the project.