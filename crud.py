from sqlalchemy.orm import Session

import models,schemas

# 회원 생성 #프로필 추가 필요
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password,
        gender=user.gender,
        birthday=user.birthday,
        nation=user.nation
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_profile = models.Profile(
        user_id = db_user.id
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_user

# 회원 탈퇴
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user

# 회원 정보 수정
def update_user(db: Session, user_id : int, user : schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.name = user.name
    db_user.email = user.email
    db_user.password = user.password
    db_user.gender = user.gender
    db_user.birthday = user.birthday
    db_user.nation=user.nation
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
# 회원 정보 읽기
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# 친구 요청
def call_friend(db : Session, caller_id : int, receiver_id : int):
    db_friend = models.Friend(
        caller_id = caller_id,
        receiver_id = receiver_id,
        state = "요청"
    )
    db.add(db_friend)
    db.commit()
    db.refresh(db_friend)
    return db_friend

# 프로필 보기
# 프로필 수정

# 보낸 요청 목록 보기
def view_call_from_me(db : Session, user_id : int):
    db_call_list = db.query(models.Friend).filter(models.Friend.caller_id == user_id, models.Friend.state == "요청").all()
    return db_call_list

# 친구요청 수락
def accept_call(db : Session, friend_id : int):
    db_friend = db.query(models.Friend).filter(models.Friend.id == friend_id).first()
    db_friend.state = "친구"
    db.add(db_friend)
    db.commit()
    db.refresh(db_friend)
    return db_friend
# 받은 요청 삭제

# 받은 요청 목록보기
def view_call_to_me(db : Session, user_id : int):
    db_call_list = db.query(models.Friend).filter(models.Friend.receiver_id == user_id, models.Friend.state == "요청").all()
    return db_call_list

# 보낸 요청 삭제
# 친구 목록 보기
# 친구 삭제

# 전체유저에서 검색
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# 이메일로 유저 검색
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()




