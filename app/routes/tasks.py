
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, status, HTTPException, Query

from app.database import tasks_collection
from app.models.task import TaskDocument
from app.schemas.task import TaskCreate, TaskUpdate
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    task_document = TaskDocument(
        **task.model_dump(),
        owner_id=str(current_user["_id"]),
    )

    result = await tasks_collection.insert_one(
        task_document.model_dump()
    )

    return {
        "id": str(result.inserted_id),
        **task_document.model_dump(mode="json"),
    }


@router.get("/")
async def list_tasks(
    current_user: Annotated[dict, Depends(get_current_user)],
    status_filter: str | None = Query(default=None, alias="status"),
    priority: str | None = Query(default=None),
):
    filters = {
        "owner_id": str(current_user["_id"])
    }

    if status_filter is not None:
        filters["status"] = status_filter

    if priority is not None:
        filters["priority"] = priority

    tasks = await tasks_collection.find(filters).to_list(length=100)

    return [
        {
            "id": str(task["_id"]),
            "title": task["title"],
            "description": task["description"],
            "status": task["status"],
            "priority": task["priority"],
            "due_date": task["due_date"],
            "created_at": task["created_at"],
            "owner_id": task["owner_id"],
        }
        for task in tasks
    ]


@router.get("/{task_id}")
async def get_task(
    task_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid task ID",
        )

    task = await tasks_collection.find_one({
        "_id": ObjectId(task_id),
        "owner_id": str(current_user["_id"]),
    })

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "status": task["status"],
        "priority": task["priority"],
        "due_date": task["due_date"],
        "created_at": task["created_at"],
        "owner_id": task["owner_id"],
    }


@router.patch("/{task_id}")
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid task ID",
        )

    update_data = task_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update",
        )

    result = await tasks_collection.update_one(
        {
            "_id": ObjectId(task_id),
            "owner_id": str(current_user["_id"]),
        },
        {"$set": update_data},
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    updated_task = await tasks_collection.find_one({
        "_id": ObjectId(task_id),
        "owner_id": str(current_user["_id"]),
    })

    return {
        "id": str(updated_task["_id"]),
        "title": updated_task["title"],
        "description": updated_task["description"],
        "status": updated_task["status"],
        "priority": updated_task["priority"],
        "due_date": updated_task["due_date"],
        "created_at": updated_task["created_at"],
        "owner_id": updated_task["owner_id"],
    }


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid task ID",
        )

    result = await tasks_collection.delete_one({
        "_id": ObjectId(task_id),
        "owner_id": str(current_user["_id"]),
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )
