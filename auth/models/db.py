from typing import AsyncGenerator

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, JSON, Boolean, DateTime
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

metadata = MetaData()

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("name", String, nullable=False),
    Column("surname", String, nullable=False),
    Column("patronymic", String, nullable=False),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey(role.c.id))
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=False, nullable=False)


engine = create_async_engine("postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres")
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

# class Division(Base):
#     __tablename__ = "division"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     parent_division_id = mapped_column(ForeignKey("division.id"), index=True)
#     unit_head_id = mapped_column(ForeignKey("staff_unit.id"), index=True)
#     status: bool = Column(Boolean, default=False, nullable=False)
#
#
# class Assignment(Base):
#     __tablename__ = "assignment"
#
#     id = Column(Integer, primary_key=True)
#     start_date = Column(DateTime(timezone=True), server_default=func.now())
#     end_date = Column(DateTime(timezone=True), server_default=func.now())
#     user_id = mapped_column(ForeignKey(user.c.id), nullable=False)
#     staff_units_id = mapped_column(ForeignKey("staff_unit.id"), index=True)
#
#
# class StaffUnit(Base):
#     __tablename__ = "staff_unit"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     division_id = mapped_column(ForeignKey("division.id"), index=True)
#
#
# class Acting(Base):
#     __tablename__ = "acting"
#
#     id = Column(Integer, primary_key=True)
#     replacement_id = mapped_column(ForeignKey("user.id"), index=True)
#     substitute_id = mapped_column(ForeignKey("user.id"), index=True)
#     division_id = mapped_column(ForeignKey("division.id"), index=True)
#     start_date = Column(DateTime(timezone=True), server_default=func.now())
#     end_date = Column(DateTime(timezone=True), server_default=func.now())
