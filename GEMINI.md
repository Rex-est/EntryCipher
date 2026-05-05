# SafeTicket - Monorepo Clean Base

This project is a clean, minimal foundation for the SafeTicket secure event ticketing system.

## Project Structure
- `Backend/`: Minimal FastAPI application.
- `Frontend/`: Minimal Angular application (Standalone).
- `.github/workflows/`: Unified CI/CD pipeline for the entire monorepo.

## Backend
- **Framework:** FastAPI
- **Entry Point:** `Backend/main.py`
- **Dependencies:** `Backend/requirements.txt`
- **Run Locally:** `cd Backend && uvicorn main:app --reload`

## Frontend
- **Framework:** Angular 21
- **Architecture:** Standalone Components
- **Test Runner:** Vitest
- **Run Locally:** `cd Frontend && npm start`

## CI/CD Pipeline
The project uses GitHub Actions for continuous integration.
- **Workflow:** `.github/workflows/ci.yml`
- **Jobs:**
  - `Backend CI`: Python setup, dependency installation, and linting.
  - `Frontend CI`: Node.js setup, npm install, build check, and unit testing.

## Development Standards
- Maintain a clean separation between Frontend and Backend.
- Ensure all CI/CD checks pass before merging to `main`.
- Follow the security-first approach as the project evolves.
