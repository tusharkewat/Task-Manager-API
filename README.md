# Task Manager API

A RESTful Task Management API built with **Python, FastAPI, and MongoDB**. It provides secure user authentication and task management with JWT-based authorization.

## Features

- User registration and login
- Password hashing using Argon2
- JWT access-token authentication
- Create, retrieve, update, and delete tasks
- Filter tasks by status and priority
- Task ownership protection so users can access only their own tasks
- Input validation using Pydantic
- Automated tests with pytest

## Tech Stack

- **Language:** Python
- **Framework:** FastAPI
- **Database:** MongoDB Atlas
- **Database Driver:** PyMongo Async
- **Validation:** Pydantic
- **Authentication:** JWT
- **Password Hashing:** Argon2 via pwdlib
- **Testing:** pytest, FastAPI TestClient, pytest-cov

## Project Structure

```text
task-manager-api/
├── app/
│   ├── config/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── database.py
│   └── main.py
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.13 or a compatible Python version
- MongoDB Atlas account or an accessible MongoDB instance
- Git

### 1. Clone the repository

```bash
git clone https://github.com/tusharkewat/Task-Manager-API.git
cd task-manager-api
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

Configure your MongoDB connection string, database name, JWT secret, and other required settings. Use a separate database for automated tests.

**Never commit your real `.env` file or expose your database credentials or JWT secret.**

### 5. Start the API

```powershell
python -m uvicorn app.main:app --reload
```

The API will be available at:

- API root: `http://127.0.0.1:8000/`
- Health check: `http://127.0.0.1:8000/health`
- Interactive API documentation: `http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Health check |
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | Log in and receive an access token |
| GET | `/auth/me` | Get the authenticated user's profile |
| POST | `/tasks/` | Create a task |
| GET | `/tasks/` | List tasks |
| GET | `/tasks/{task_id}` | Retrieve a task |
| PATCH | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

Task listing supports optional `status` and `priority` query parameters.

Protected endpoints require a valid bearer access token. Use the token returned by login in the `Authorization` header:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Running Tests

Run the complete test suite:

```powershell
python -m pytest tests -v
```

Run tests with code coverage:

```powershell
python -m pytest tests -v --cov=app --cov-report=term-missing
```

The current development test run passed **43 tests with 99% statement coverage**.

## Future Improvements

- Deploy the API to a public hosting platform
- Add pagination and sorting
- Add token refresh and revocation support
- Add CI with GitHub Actions
- Improve API monitoring and logging

## License

No license has been added yet. Choose a license before permitting others to reuse or redistribute this project.
