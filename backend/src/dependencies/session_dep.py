from db import db_helper


async def session_dependency():
    async with db_helper.session_factory() as session:
        yield session
        await session.close()
