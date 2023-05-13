import typing

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.dal.base import BaseDAL
from db.session import SessionLocal


async def get_db_session() -> typing.AsyncGenerator[AsyncSession, None]:
    db_session: AsyncSession = SessionLocal()
    try:
        yield db_session
    except BaseException:
        await db_session.rollback()
        raise
    else:
        await db_session.commit()
    finally:
        await db_session.close()


DalType = typing.TypeVar("DalType", bound=BaseDAL)


def get_db_dal_by_type(dal_cls: typing.Type[DalType]):
    async def _inner_func(
        db_session: AsyncSession = Depends(get_db_session),
    ) -> DalType:
        return dal_cls(db_session=db_session)

    return _inner_func
