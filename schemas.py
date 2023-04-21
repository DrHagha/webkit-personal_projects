from typing import Union
import datetime

from pydantic import BaseModel


class UserBase(BaseModel):

    name: str
    email: str
    gender: str
    birthday: str
    nation: str
    password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserDelete(UserBase):
    id: int


class ProfileBase(BaseModel):
    
    location: str
    hobby: str
    interest: str
    instroduce: str


class ProfileCreate(ProfileBase):
    pass


class Profile(ProfileBase):

    class Config:
        orm_mode = True


class FriendBase(BaseModel):
    caller_id: int
    receiver_id: int
    state: str


class FriendCreate(FriendBase):
    pass


class Friend(FriendBase):
    state: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str