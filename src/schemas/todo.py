from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class ContactSchema(BaseModel):  # TodoSchema
    name: str = Field("default", min_length=3, max_length=15)
    firstname: str = Field(min_length=3, max_length=15)
    email: EmailStr = Field()
    number: int = Field(description="The contact phone number")
    birthday: Optional[date] = Field(None, description="The birthday date Day-Month-Year")
    completed: Optional[bool] = False


class ContactUpdateSchema(ContactSchema):  # TodoUpdateSchema
    completed: bool


class ContactResponse(BaseModel):  # TodoResponse
    id: int = 1
    name: str
    firstname: str
    email: str
    number: int
    birthday: Optional[date]
    completed: bool

    class Config:
        from_attributes: True
