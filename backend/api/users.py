from fastapi import APIRouter

from backend.schemas.user import UserCreate, UserResponse
from backend.services.demo_store import store

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("", response_model=UserResponse)
async def create_user(payload: UserCreate) -> UserResponse:
    return store.create_user(payload)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str) -> UserResponse:
    return store.user


@router.put("/{user_id}/profile", response_model=UserResponse)
async def update_profile(user_id: str, payload: UserCreate) -> UserResponse:
    return store.create_user(payload)
