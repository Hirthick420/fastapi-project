Reflection Document – FastAPI Secure User Project
1. Overview

This project involved building a secure FastAPI application with proper user registration, password hashing, database integration, and CI/CD deployment using GitHub Actions and Docker Hub. In addition, automated testing (unit + integration) was implemented to ensure reliability before deployment.

2. Key Experiences
a. Understanding Application Structure

I learned how a production-ready FastAPI project is organized:

app/main.py as the entry point

app/models/ for SQLAlchemy models

app/crud/ for database operations

app/schemas/ for request/response validation

app/core/security.py for hashing and authentication utilities

This structure helped me understand how backend applications scale and stay maintainable.

b. Writing Unit and Integration Tests

Major learning points:

How to mock dependencies and test functions independently

How to test database operations safely using a test database

How fixtures in pytest simplify database setup and teardown

How to differentiate:

Unit tests → small functions

Integration tests → full DB + app components

This improved my confidence in building reliable backend systems.

c. Debugging Import and Module Errors

I faced multiple issues:

ModuleNotFoundError: No module named 'app.…'

Conflicting Python paths

Missing __init__.py files

Incorrect relative imports

I learned how Python resolves packages and why directory structure matters in real projects.

d. Docker & Networking Challenges

Key issues I solved:

Port conflicts (0.0.0.0:8000 already allocated)

Removing old containers that reused the same name

Managing Docker networks

Rebuilding tagged Docker images properly

These helped me understand how containerized apps are deployed in the real world.

e. CI/CD Pipeline Using GitHub Actions

This was the hardest part.
I learned:

How GitHub runners operate

Why Docker Hub authentication failed (fixed using GitHub Secrets)

Why tests must pass before the image builds

How caching improves build speeds

Understanding CI/CD increased my awareness of modern DevOps workflows.

f. Working With Docker Hub

I pushed images using:

docker build

docker push

Automated pushes via GitHub Actions

I also learned why Docker Hub needs login tokens, not passwords.

3. Challenges Faced & How I Solved Them
Challenge 1: Password Hashing Errors

bcrypt error: password too long / backend issue
✔ Switched to bcrypt_sha256
✔ Installed proper dependencies

Challenge 2: Integration Tests → Missing Fixtures

Test DB wouldn’t connect
✔ I created a conftest.py with a db_session fixture
✔ Set TEST_DATABASE_URL correctly

Challenge 3: Docker Container Naming Conflicts

fastapi-secure-user already existed
✔ Removed old containers using
docker rm -f container_name

Challenge 4: CI/CD Build Failures

OAuth token failure when pushing images
✔ Set secrets DOCKERHUB_USERNAME + DOCKERHUB_TOKEN
✔ Ensured YAML workflow syntax was correct

4. Final Outcome

I successfully achieved:

Fully working FastAPI backend

Proper secure password storage

Passing unit + integration tests

Dockerized app

Automated CI/CD pipeline

Deployed to Docker Hub

Clean project documentation

This project gave me end-to-end exposure to backend development, testing, Docker, and DevOps pipelines, all essential for real engineering work.