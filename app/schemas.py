from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    phone: str = Field(..., example="+79991234567")
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str

class LoginSchema(BaseModel):
    phone: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ProfileCreate(BaseModel):
    first_name: str
    last_name: str
    additional_info: Optional[str] = None

class NewsCreate(BaseModel):
    title: str
    content: str
    news_type: Optional[str] = None
