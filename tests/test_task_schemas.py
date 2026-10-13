
import pytest
from pydantic import ValidationError

from app.schemas.task import TaskCreate, TaskUpdate


def test_task_create_rejects_blank_title():
    with pytest.raises(ValidationError):
        TaskCreate(title="   ")


def test_task_update_rejects_blank_title():
    with pytest.raises(ValidationError):
        TaskUpdate(title="   ")


def test_task_create_strips_title_whitespace():
    task = TaskCreate(title="  Learn Python  ")

    assert task.title == "Learn Python"


def test_task_update_strips_title_whitespace():
    task = TaskUpdate(title="  Updated Title  ")

    assert task.title == "Updated Title"


def test_task_update_rejects_invalid_status():
    with pytest.raises(ValidationError):
        TaskUpdate(status="invalid_status")


def test_task_update_rejects_invalid_priority():
    with pytest.raises(ValidationError):
        TaskUpdate(priority="urgent")
