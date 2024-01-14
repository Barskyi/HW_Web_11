from sqlalchemy import String, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Todo(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    firstname: Mapped[str] = mapped_column(String(50), index=True)
    email: Mapped[str] = mapped_column(String(50), index=True)
    number: Mapped[int] = mapped_column(Integer(), index=True)  # int
    birthday: Mapped[Date] = mapped_column(Date, index=True)
    completed: Mapped[bool] = mapped_column(default=False)
