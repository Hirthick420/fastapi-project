# Module 13 Reflection – FastAPI Auth, Testing, and CI/CD

## What I implemented

- Added a proper `User` model in SQLAlchemy with a `password_hash` column and uniqueness constraints on `username` and `email`.
- Implemented secure registration and login:
  - `/users/register` API endpoint.
  - `/login` API endpoint returning a JWT access token.
  - HTML pages `/register-page` and `/login-page` that call these APIs via `fetch`.
- Wired in password hashing and verification using `passlib` / bcrypt.
- Fixed database configuration to use environment-based `DATABASE_URL` and updated migrations so tests and Docker use the same schema.
- Added and fixed end-to-end Playwright tests for registration and login, so the browser flow is automatically validated.
- Updated the GitHub Actions CI/CD pipeline to start a PostgreSQL service, run all pytest tests, and then build & push a Docker image to Docker Hub.

## What I learned

- How to connect FastAPI, SQLAlchemy, and PostgreSQL cleanly using a `DATABASE_URL` and shared engine/session configuration.
- The difference between model-level logic (SQLAlchemy), schema-level validation (Pydantic), and UI behavior (the HTML + JavaScript fetch calls).
- How end-to-end tests (Playwright) catch issues that unit tests miss, especially around DOM IDs and error messages.
- How to configure GitHub Actions to spin up a test database service, run tests, and then build/push a Docker image as part of a CI/CD pipeline.

## Challenges and how I solved them

- **Column name mismatch**: I originally used `hashed_password` in the table but `password_hash` in the model, which caused runtime errors and failing tests. I fixed this by updating the model and the actual PostgreSQL schema so they match, then re-running the tests.
- **Login E2E tests failing**: The Playwright tests were failing because the login page was not updating `#message` correctly. I reviewed the test expectations, aligned the DOM IDs and text messages, and verified manually in the browser before re-running Playwright.
- **Postgres DB names and URLs**: There was confusion between different database names (`fastapi_db`, `fastapi_test_db`, etc.). I standardized everything to one DB name in both local Docker Compose and GitHub Actions, and made sure `DATABASE_URL` is passed via environment variables.

## What I would improve next time

- Set up database migrations (e.g., Alembic) earlier so schema changes like renaming `hashed_password` to `password_hash` are more controlled.
- Write the end-to-end tests earlier in the process to catch front-end / back-end integration issues sooner.
- Keep a clearer checklist of environment variables and database names so I don’t waste time debugging simple configuration mismatches.
