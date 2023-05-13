import datetime
import typing

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import Select

from db.models.base import BaseModel as DBBaseModel
from exceptions.common import ObjectNotFoundError

ModelType = typing.TypeVar("ModelType", bound=DBBaseModel)
CreateSchemaType = typing.TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = typing.TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseDAL(typing.Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model: type[ModelType]
    readable_object_name: str

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    def get_query(self) -> Select:
        return select(self.model)

    def get_exists(self, query: Select | None = None) -> Select:
        query = query if query is not None else self.get_query()
        return select(query.limit(1).exists())

    async def get_all(self, query: Select | None = None) -> typing.Sequence[ModelType]:
        if query is None:
            query = self.get_query()
        return (await self.db_session.execute(query)).scalars().all()

    async def get_first_by_query(self, query: Select) -> ModelType | None:
        return (await self.db_session.execute(query.limit(1))).scalars().first()

    async def get_by_id(self, db_id: int) -> ModelType | None:
        return await self.get_first_by_query(
            self.get_query().where(self.model.id == db_id)
        )

    async def get_by_id_with_exception(self, db_id: int) -> ModelType:
        obj = await self.get_by_id(db_id)
        if obj is None:
            raise ObjectNotFoundError(
                object_name=self.readable_object_name, field="id", value=str(db_id)
            )
        return obj

    async def upsert(self, db_obj: ModelType) -> ModelType:
        self.db_session.add(db_obj)
        await self.db_session.flush()
        await self.db_session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj: ModelType) -> None:
        await self.db_session.delete(db_obj)
        await self.db_session.flush()

    async def create_from_api(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        for field in vars(db_obj).keys():
            if field in obj_in_data:
                if isinstance(
                    getattr(self.model, field).type, sa.String
                ) and isinstance(obj_in_data[field], int):
                    setattr(db_obj, field, str(obj_in_data[field]))
                elif isinstance(
                    getattr(self.model, field).type, sa.String
                ) and isinstance(obj_in_data[field], float):
                    setattr(db_obj, field, str(obj_in_data[field]))
                elif isinstance(
                    getattr(self.model, field).type, sa.DateTime
                ) and isinstance(obj_in_data[field], datetime.datetime):
                    # There is no reason to store TZ info in PG, thus to avoid conflicts in asyncpg, remove it
                    setattr(db_obj, field, obj_in_data[field].replace(tzinfo=None))
        return await self.upsert(db_obj)

    async def update_from_api(
        self, db_obj: ModelType, obj_in: UpdateSchemaType | dict[str, typing.Any]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in vars(db_obj).keys():
            if field in update_data:
                if isinstance(
                    getattr(self.model, field).type, sa.String
                ) and isinstance(update_data[field], int):
                    setattr(db_obj, field, str(update_data[field]))
                elif isinstance(
                    getattr(self.model, field).type, sa.String
                ) and isinstance(update_data[field], float):
                    setattr(db_obj, field, str(update_data[field]))
                elif isinstance(
                    getattr(self.model, field).type, sa.DateTime
                ) and isinstance(update_data[field], datetime.datetime):
                    # There is no reason to store TZ info in PG, thus to avoid conflicts in asyncpg, remove it
                    setattr(db_obj, field, update_data[field].replace(tzinfo=None))
                else:
                    setattr(db_obj, field, update_data[field])
        return await self.upsert(db_obj=db_obj)

    async def update_by_id_from_api(
        self, db_id: int, obj_in: UpdateSchemaType | dict[str, typing.Any]
    ) -> ModelType:
        db_obj = await self.get_by_id_with_exception(db_id=db_id)
        return await self.update_from_api(db_obj=db_obj, obj_in=obj_in)

    async def remove_by_id_from_api(self, db_id: int):
        db_obj = await self.get_by_id_with_exception(db_id=db_id)
        await self.remove(db_obj=db_obj)
