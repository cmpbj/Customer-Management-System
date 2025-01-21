from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CustomerUpdate(CustomerBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None