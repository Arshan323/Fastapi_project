

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
# user_register
class BaseUser(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    message: str

    class Config:
        from_attributes = True

# login

class login(BaseModel):
    username: str
    email:EmailStr
    password: str

# update_user

class Update(BaseModel):
    username: str
    email: EmailStr
    password: str
    
class Update_Response(BaseModel):
    username: str
    email: EmailStr
    password: str
    message: str

    class Config:
        from_attributes = True


# delete

class delete(BaseModel):
    message:str
    user_id:int
    
# search
class search(BaseModel):
    	
    id:int
    email: EmailStr
    phone_number: Optional[str]
    update_at: datetime
    username: str
    created_at: datetime
   