from abc import ABC, abstractmethod


class IRepository(ABC):
    @classmethod
    @abstractmethod
    async def insert_objects(cls, obj_data: dict):
        """Insert object to DB"""

    @classmethod
    @abstractmethod
    async def update_instance(cls, obj_data: dict):
        """Update object in DB"""

    @classmethod
    @abstractmethod
    async def get_all_items(cls, limit=None, offset=None):
        """Return an item from DB"""
