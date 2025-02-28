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

class ProfileUpdate(BaseModel):
    photo_url: Optional[str] = None
    additional_info: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str

class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    business_role: Optional[str] = None
    corporate_email: Optional[str] = None
    photo_url: Optional[str] = None
    additional_info: Optional[str] = None

class DepartmentResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class NewsResponse(BaseModel):
    id: int
    title: str
    content: str
    news_type: Optional[str] = None
    is_approved: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    author_id: int
    department_id: Optional[int] = None

class DocumentResponse(BaseModel):
    id: int
    title: str
    file_path: str
    doc_type: str
    description: Optional[str] = None
    uploaded_at: datetime
    uploaded_by: int

class SmartSearchResponse(BaseModel):
    query: str
    department: Optional[DepartmentResponse] = None
    employees: List[EmployeeResponse]
    news: List[NewsResponse]
    documents: List[DocumentResponse]
