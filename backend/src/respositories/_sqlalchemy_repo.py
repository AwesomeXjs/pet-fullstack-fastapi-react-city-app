from sqlalchemy import delete, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from ._abc_repo import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_one(self, item):
        stmt = insert(self.model).values(**item)
        await self.session.execute(stmt)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        result = res.scalar_one_or_none()
        return result

    async def get_all(self):
        query = select(self.model)
        res = await self.session.execute(query)
        result = res.scalars().all()
        return result

    async def get_all_by_filter(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        result = res.scalars().all()
        return result

    async def update_one(self, updated_item, item):
        for name, value in updated_item.model_dump(exclude_unset=True).items():
            setattr(item, name, value)

    async def delete_one_by_id(self, id):
        stmt = delete(self.model).where(self.model.id == id).returning(self.model.title)
        res = await self.session.execute(stmt)
        return res.scalar()
