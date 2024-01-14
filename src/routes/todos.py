from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from HW_Web_11.src.schemas.todo import ContactSchema, ContactUpdateSchema, ContactResponse
from HW_Web_11.src.database.db import get_db
from HW_Web_11.src.repository import todos as repository_contacts

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get('/', response_model=list[ContactResponse])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(get_db)):
    """Отримати список всіх контактів"""
    todos = await repository_contacts.get_contacts(limit, offset, db)
    return todos


@router.get('/{contact_id}', response_model=ContactResponse)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    """Отримати один контакт за ідентифікатором"""
    todo = await repository_contacts.get_contact(contact_id, db)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return todo


@router.post('/{contact_id}', response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db)):
    """Створити новий контакт"""
    todo = await repository_contacts.create_contact(body, db)
    return todo


@router.put('/{contact_id}')
async def update_contact(body: ContactUpdateSchema, contact_id: int, db: AsyncSession = Depends(get_db)):
    """Оновити існуючий контакт"""
    todo = await repository_contacts.update_contact(contact_id, body, db)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return todo


@router.delete('/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    """Видалити контакт"""
    todo = await repository_contacts.delete_contact(contact_id, db)
    return todo


@router.get('/birthday-upcoming/')
async def get_upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    """Отримати список контактів з найближчими днями народженнями на найближчі 7 днів"""
    upcoming_birthdays = await repository_contacts.get_upcoming_birthdays(db)
    return {"upcoming_birthdays": upcoming_birthdays}


@router.get('/search-contacts/')
async def search_contacts_route(db: AsyncSession = Depends(get_db), search_query: str = Query(..., min_length=1)):
    """Пошук контактів за іменем, прізвищем чи адресою електронної пошти"""
    contacts = await repository_contacts.search_contacts(db, search_query)
    return {"contacts": contacts}
