from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    async def create_one():
        raise NotImplementedError

    @abstractmethod
    async def get_one():
        raise NotImplementedError

    @abstractmethod
    async def get_all():
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_filter():
        raise NotImplementedError

    @abstractmethod
    async def update_one():
        raise NotImplementedError

    @abstractmethod
    async def delete_one_by_id(id: int):
        raise NotImplementedError
