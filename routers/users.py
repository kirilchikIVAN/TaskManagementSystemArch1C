from fastapi import APIRouter, Depends

from db.dal.users import Users as UsersDAL
from dependencies.db import get_db_dal_by_type
from schemas.users import User, UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{id}")
async def get_by_id(
    id: int, users_dal: UsersDAL = Depends(get_db_dal_by_type(UsersDAL))
) -> User | None:
    return User.from_orm(await users_dal.get_by_id_with_exception(id))


@router.get("")
async def get_users(
    users_dal: UsersDAL = Depends(get_db_dal_by_type(UsersDAL)),
) -> list[User]:
    return [User.from_orm(user) for user in await users_dal.get_all()]


@router.post("")
async def create_user(
    user: UserCreate,
    users_dal: UsersDAL = Depends(get_db_dal_by_type(UsersDAL)),
) -> User:
    return User.from_orm(await users_dal.create_from_api(user))


@router.delete("/{id}")
async def delete_user(
    id: int,
    users_dal: UsersDAL = Depends(get_db_dal_by_type(UsersDAL)),
) -> None:
    await users_dal.remove_by_id_from_api(id)
