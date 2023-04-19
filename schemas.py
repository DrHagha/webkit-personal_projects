from typing import Union
from pydantic import BaseModel

class ItemBase(BaseModel):
    title : str
    description : Union[str, None] = None
    
class ItemsCreate(ItemBase):
    pass

class Item(ItemsCreate):
    id : int
    owner_id : int
    
    class Config:
        orm_mode = True
        
class UserBase(BaseModel):
    email : str
    
class UserCreate(UserBase):
    password : str
    
class User(UserBase):
    id : int
    id_active : bool
    items : list[Item] = []
    
    class Config:
        orm_mode = True