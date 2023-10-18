# from fastapi import Depends
# from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
# from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
# from sqlalchemy.orm import DeclarativeBase
#
# from auth.models.db import User
#
# engine = create_async_engine("postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres")
# async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
#
#
# class Base(DeclarativeBase):
#     pass
#
#
# async def get_async_session():
#     async with async_session_maker() as session:
#         yield session
#
#
# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabase(session, User)
