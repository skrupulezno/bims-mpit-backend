from pydantic import BaseModel

class UserCreate(BaseModel):
    phone: str
    password: str
    first_name: str
    last_name: str

class ProfileCreate(BaseModel):
    first_name: str
    last_name: str
    additional_info: str = None
