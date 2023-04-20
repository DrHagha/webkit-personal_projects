from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    gender = Column(String, index=True)
    birthday = Column(String)
    nation = Column(String, index=True)
    password = Column(String)

    my_profile = relationship("Profile")
    call_from_me = relationship("Friend", foreign_keys="[Friend.caller_id]", 
                                primaryjoin="User.id==Friend.caller_id")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    location = Column(String, index=True)
    hobby = Column(String, index=True)
    interest = Column(String, index=True)
    introduce = Column(String)

    owner = relationship("User")


class Friend(Base):
    __tablename__ = "friends"
    id = Column(Integer, primary_key=True)
    caller_id = Column(Integer, ForeignKey("users.id"), index=True)  # 발신자
    receiver_id = Column(Integer, ForeignKey("users.id"), index=True)  # 수신자
    state = Column(String, index=True)

    ForeignKeyConstraint(['caller_id', 'receiver_id'], ['users.id', 'users.id'])

    call1 = relationship("User", foreign_keys=[caller_id])
    call2 = relationship("User", foreign_keys=[receiver_id])