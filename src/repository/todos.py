from datetime import datetime, timedelta

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from HW_Web_11.src.schemas.todo import ContactSchema, ContactUpdateSchema
from HW_Web_11.src.entity.models import Todo


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    """Отримати список всіх контактів"""
    stmt = select(Todo).offset(offset).limit(limit)
    todos = await db.execute(stmt)
    return todos.scalars().all()


async def get_contact(todo_id: int, db: AsyncSession):
    """Отримати один контакт за ідентифікатором"""
    stmt = select(Todo).filter_by(id=todo_id)
    todos = await db.execute(stmt)
    return todos.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession):
    """Створити новий контакт"""
    todo = Todo(**body.model_dump(exclude_unset=True))  # (title=body.title, description=body.description)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession):
    """Оновити існуючий контакт"""
    stmt = select(Todo).filter_by(id=contact_id)
    result = await db.execute(stmt)
    todo = result.scalar_one_or_none()

    if todo:
        todo.name = body.name
        todo.firstname = body.firstname
        todo.email = body.email
        todo.number = body.number
        todo.birthday = body.birthday
        todo.completed = body.completed
        await db.commit()
        await db.refresh(todo)
    return todo


async def delete_contact(contact_id: int, db: AsyncSession):
    """Видалити контакт"""
    stmt = select(Todo).filter_by(id=contact_id)
    todo = await db.execute(stmt)
    todo = todo.scalar_one_or_none()
    if todo:
        await db.delete(todo)
        await db.commit()
    return todo


async def get_upcoming_birthdays(db: AsyncSession):  # try
    """Отримати список контактів з найближчими днями народженнями на найближчі 7 днів"""

    current_date = datetime.now().date()
    seven_days_from_now = current_date + timedelta(days=7)

    stmt = select(Todo).where(
        func.date_part('month', Todo.birthday) == current_date.month,
        func.date_part('day', Todo.birthday) >= current_date.day,
        func.date_part('day', Todo.birthday) <= seven_days_from_now.day
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def search_contacts(db: AsyncSession, search_query: str):
    """Пошук контактів за іменем, прізвищем чи адресою електронної пошти"""

    stmt = select(Todo).where(
        (Todo.name.ilike(f'%{search_query}%')) |
        (Todo.firstname.ilike(f'%{search_query}%')) |
        (Todo.email.ilike(f'%{search_query}%'))
    )

    result = await db.execute(stmt)
    return result.scalars().all()