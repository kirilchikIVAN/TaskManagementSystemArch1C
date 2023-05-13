from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    boss_id: int | None = None

    class Config:
        orm_mode = True


class User(UserCreate):
    id: int
