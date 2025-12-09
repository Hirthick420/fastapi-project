# Module 14 Reflection – BREAD Endpoints, Front-End Integration, and E2E Testing

## Overview
Module 14 focused on extending the FastAPI calculator application by implementing complete BREAD (Browse, Read, Edit, Add, Delete) functionality for the `calculations` resource. This module combined backend development, HTML/JavaScript front-end integration, Playwright E2E testing, and CI/CD verification. It was the most “full-stack” module so far, requiring the calculations feature to work across the API, user interface, automated tests, and GitHub Actions.

This reflection summarizes what I implemented, what challenges I faced, and what I learned while completing Module 14.

---

## Backend Implementation
The backend already had a `Calculation` model and Pydantic schemas from earlier modules. In Module 14, I ensured the following BREAD endpoints were correct and fully functional:

- **GET /calculations** – Browse all calculations  
- **GET /calculations/{id}** – Read a single calculation  
- **POST /calculations** – Add a new calculation  
- **PUT /calculations/{id}** – Edit/update an existing calculation  
- **DELETE /calculations/{id}** – Delete a calculation  

These endpoints live in `app/main.py` and use SQLAlchemy for persistence. I also used a helper function `_compute_result()` to correctly compute arithmetic operations and safely handle division by zero. Pydantic validators in `CalculationCreate` ensure that invalid payloads (e.g., division by zero) are rejected before reaching the database.

---

## Front-End: calculations-page UI
Module 14 required the backend to be usable from a real front-end interface. I created:

- **`app/static/html/calculations.html`**
- A new route **`/calculations-page`**

This page includes:

- A clean form for adding new calculations  
- Fields for `a`, `b`, and operation type  
- A dynamic table showing all calculations  
- JS functions to:
  - Fetch all calculations from the API  
  - Submit new calculations  
  - Edit existing ones using prompts  
  - Delete calculations with a confirmation dialog  
  - Display success/error messages in a `<p id="message">` element  

The page communicates with the FastAPI backend using `fetch()` for all BREAD operations. Client-side validation ensures `a` and `b` must be valid numbers before submission.

This gave the project a more complete “web app” feel rather than just a set of API endpoints.

---

## End-to-End Testing with Playwright
Module 14 required extending E2E tests. I created a new file:

- **`tests/e2e/test_calculations_e2e.py`**

The tests cover:

### ✔ Positive Cases
- Creating a calculation from the UI  
- Editing a calculation through the “Edit” button  
- Deleting a calculation  
- Verifying UI success messages for each action  

### ✔ Negative Cases
- Invalid numeric inputs  
- Blank fields  
- Division by zero attempting to create a calculation  
- Ensuring the page still loads and the system recovers gracefully  

The tests run in Chromium and interact with the actual HTML and JavaScript components. Handling browser dialogs (prompts and confirms) was initially tricky, but Playwright’s `page.on("dialog", …)` solved it. All E2E tests passed successfully locally and in GitHub Actions.

---

## CI/CD Integration
The GitHub CI pipeline was already set up in earlier modules. For Module 14:

- The workflow installs Playwright browsers  
- Spins up a Postgres service  
- Runs all unit, integration, and E2E tests  
- Verifies the project builds successfully  

After committing the Module 14 changes, I pushed to GitHub and ensured CI passed. A screenshot of the green workflow run was included as part of the submission.

---