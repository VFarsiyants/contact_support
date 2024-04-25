from typing import List

from sqlalchemy import select
from pydantic import BaseModel

from src.db.models import Contact, Base, Action
from src.repositories.entries import ContactEntry, ActionEntry
from src.db.session import async_session
from src.repositories.alchemy.base_repository import IRepository


class BaseRepository(IRepository):
    db_model = Base
    entry_model = BaseModel

    @classmethod
    async def insert_objects(cls, obj_data: dict):
        async with async_session() as session:
            async with session.begin():
                session.add(cls.db_model(**obj_data))
                await session.commit()

    @classmethod
    async def update_instance(cls, obj_data: dict):
        async with async_session() as session:
            async with session.begin():
                session.add(cls.db_model(**obj_data))
                await session.commit()

    @classmethod
    async def get_all_items(cls, limit=None, offset=None) -> List[entry_model]:
        # TODO pagination
        async with async_session() as session:
            async with session.begin():
                stmt = select(cls.db_model)
                result = await session.scalars(stmt)
        return [cls.entry_model.model_validate(obj) for obj in result]

    @classmethod
    async def update(cls, obj_data: dict) -> entry_model:
        instance_id = obj_data.pop('id')
        async with async_session() as session:
            async with session.begin():
                instance = await session.get(cls.db_model, instance_id) 
                for key, value in obj_data.items():
                    setattr(instance, key, value)       
                await session.commit()

        return cls.entry_model.model_validate(instance)


class ContactRepository(BaseRepository):
    db_model = Contact
    entry_model = ContactEntry


class ActionRepository(BaseRepository):
    db_model = Action
    entry_model = ActionEntry
