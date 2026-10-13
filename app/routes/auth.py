from typing import Annotated
from fastapi import Depends
from app.utils.dependencies import get_current_user

from fastapi import APIRouter, HTTPException, status
from pymongo.errors import DuplicateKeyError

from app.database import users_collection
from app.models.user import UserDocument
from app.schemas.user import UserRegister
from app.utils.security import hash_password, verify_password

from app.schemas.user import UserLogin
from app.utils.security import verify_password
from app.utils.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserRegister):
    existing_user = await users_collection.find_one(
        {"email": user.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    user_document = UserDocument(
        name=user.name,
        email=str(user.email),
        hashed_password=hash_password(user.password),
    )

    try:
        result = await users_collection.insert_one(
            user_document.model_dump()
        )
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id),
        "name": user_document.name,
        "email": user_document.email,
    }
    
    

@router.post("/login")
async def login_user(user: UserLogin):
    existing_user = await users_collection.find_one(
        {"email": str(user.email)}
    )

    if not existing_user or not verify_password(
        user.password,
        existing_user["hashed_password"],
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(str(existing_user["_id"]))

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me")
async def get_my_profile(
    current_user: Annotated[dict, Depends(get_current_user)],
):
    return {
        "user_id": str(current_user["_id"]),
        "name": current_user["name"],
        "email": current_user["email"],
        "created_at": current_user["created_at"],
    }

