# Task Manager API

A secure RESTful Task Management API built with **Python, FastAPI, and MongoDB Atlas**. The API supports user authentication, personal task management, filtering, and access control using JSON Web Tokens (JWT).

<p align="center">
  <a href="https://task-manager-api-q787.onrender.com/">Live API</a> ·
  <a href="https://task-manager-api-q787.onrender.com/docs">Swagger Documentation</a> ·
  <a href="https://github.com/tusharkewat/Task-Manager-API">GitHub Repository</a>
</p>

## Features

- **User Authentication:** Register and log in securely.
- **Password Security:** Hash passwords using Argon2 through `pwdlib`.
- **JWT Authorization:** Protect endpoints using bearer access tokens.
- **Task Management:** Create, retrieve, update, and delete tasks.
- **Task Filtering:** Filter tasks by status and priority.
- **Ownership Protection:** Users can access and manage only their own tasks.
- **Input Validation:** Validate request data using Pydantic.
- **Database Integration:** Store user and task data in MongoDB Atlas.
- **Automated Testing:** Test API functionality using pytest and FastAPI TestClient.

## Live Demo

| Resource | Link |
|---|---|
| Live API | https://task-manager-api-q787.onrender.com/ |
| Interactive API Documentation | https://task-manager-api-q787.onrender.com/docs |
| Health Check | https://task-manager-api-q787.onrender.com/health |
| GitHub Repository | https://github.com/tusharkewat/Task-Manager-API |

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | REST API framework |
| MongoDB Atlas | Cloud database |
| PyMongo Async | Asynchronous database operations |
| Pydantic | Request validation and data schemas |
| PyJWT | JWT creation and verification |
| pwdlib with Argon2 | Password hashing |
| pytest | Automated testing |
| pytest-cov | Test coverage reporting |
| Uvicorn | ASGI application server |
| Render | API hosting |

## Project Structure

```text
Task-Manager-API/
├── app/
│   ├── config/
│   │   └── settings.py
│   ├── models/
│   │   ├── task.py
│   │   └── user.py
│   ├── routes/
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── schemas/
│   │   ├── task.py
│   │   └── user.py
│   ├── services/
│   ├── utils/
│   │   ├── dependencies.py
│   │   ├── jwt.py
│   │   └── security.py
│   ├── database.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_auth_flow.py
│   ├── test_dependencies.py
│   ├── test_main.py
│   ├── test_task_schemas.py
│   └── test_tasks.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.13 or a compatible Python version
- A MongoDB Atlas account or another accessible MongoDB instance
- Git

### 1. Clone the repository

```bash
git clone https://github.com/tusharkewat/Task-Manager-API.git
cd Task-Manager-API
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root, using `.env.example` as a reference.

Configure the required variables:

```dotenv
APP_NAME=Task Manager API
ENVIRONMENT=development
MONGODB_URL=your_mongodb_connection_string
DATABASE_NAME=task_manager
TEST_DATABASE_NAME=task_manager_test
JWT_SECRET_KEY=your_secure_random_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace the example values with your own configuration. Generate a strong, random JWT secret.

**Security notes:**

- Never commit your real `.env` file.
- Never publish your MongoDB credentials or JWT secret.
- Use a separate database for automated tests.
- Configure MongoDB Atlas network access and database permissions carefully.

### 5. Start the API locally

```powershell
python -m uvicorn app.main:app --reload
```

The local API will be available at:

- API root: http://127.0.0.1:8000/
- Health check: http://127.0.0.1:8000/health
- Interactive documentation: http://127.0.0.1:8000/docs

## API Endpoints

### General

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Health check |

### Authentication

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | Not required |
| POST | `/auth/login` | Log in and receive an access token | Not required |
| GET | `/auth/me` | Retrieve the authenticated user's profile | Required |

### Tasks

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/tasks/` | Create a task | Required |
| GET | `/tasks/` | List the user's tasks | Required |
| GET | `/tasks/{task_id}` | Retrieve a task | Required |
| PATCH | `/tasks/{task_id}` | Update a task | Required |
| DELETE | `/tasks/{task_id}` | Delete a task | Required |

### Task Filtering

The task listing endpoint supports optional `status` and `priority` query parameters.

Examples:

```http
GET /tasks/?status=pending
GET /tasks/?priority=high
GET /tasks/?status=completed&priority=medium
```

Supported task statuses:

- `pending`
- `in_progress`
- `completed`

Supported priorities:

- `low`
- `medium`
- `high`

## Authentication

The login endpoint returns a JWT access token.

For protected endpoints, provide the token in the `Authorization` header:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

In Swagger UI:

1. Open the [API documentation](https://task-manager-api-q787.onrender.com/docs).
2. Register a user using `POST /auth/register`.
3. Log in using `POST /auth/login`.
4. Copy the returned `access_token`.
5. Click **Authorize** and enter the bearer token as requested by the interface.
6. Test the protected endpoints.

The API validates authentication and restricts task operations to the authenticated user's own tasks.

## Running Tests

Run the complete automated test suite:

```powershell
python -m pytest tests -v
```

Run tests with a coverage report:

```powershell
python -m pytest tests -v --cov=app --cov-report=term-missing
```

### Test Results

The current recorded test run achieved:

- **43 tests passed**
- **99% statement coverage**
- **0 failed tests**

These results reflect the development test run and may change as the project evolves.

## Deployment

The API is deployed on Render and uses MongoDB Atlas for database storage.

- **Live API:** https://task-manager-api-q787.onrender.com/
- **Swagger UI:** https://task-manager-api-q787.onrender.com/docs

The hosting platform requires the appropriate environment variables to be configured in its dashboard. Do not upload your local `.env` file.

## Future Improvements

- Add pagination and sorting for task listings.
- Add token refresh and revocation support.
- Introduce GitHub Actions for continuous integration.
- Improve structured logging and error monitoring.
- Add rate limiting and additional security controls.
- Expand API documentation with more request and response examples.

## License

No license has been added to this repository yet. Add a license if you want to explicitly define how others may use, modify, and distribute the project.
