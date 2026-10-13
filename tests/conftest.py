
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.config.settings import settings
from app.database import client as mongo_client


@pytest.fixture(scope="session")
def client():
    if settings.TEST_DATABASE_NAME == settings.DATABASE_NAME:
        pytest.fail(
            "Test database must be different from the application database."
        )

    import app.routes.auth as auth_routes
    import app.routes.tasks as task_routes
    import app.utils.dependencies as dependencies

    test_database = mongo_client[settings.TEST_DATABASE_NAME]
    test_users_collection = test_database["users"]
    test_tasks_collection = test_database["tasks"]

    original_auth_collection = auth_routes.users_collection
    original_task_collection = task_routes.tasks_collection
    original_dependency_collection = dependencies.users_collection

    # Redirect application routes and authentication to the test database.
    auth_routes.users_collection = test_users_collection
    task_routes.tasks_collection = test_tasks_collection
    dependencies.users_collection = test_users_collection

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        # Restore the original collections after testing.
        auth_routes.users_collection = original_auth_collection
        task_routes.tasks_collection = original_task_collection
        dependencies.users_collection = original_dependency_collection
