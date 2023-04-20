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
        nation=user.nation,
        language = "en"
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
    return {"message" : "삭제성공"}

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

# 언어 변경
def update_language(db : Session, user_id : int, language : str):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.language = language
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
def get_profile(db : Session, user_id : int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    response = {
        "id" : db_user.id,
        "name" : db_user.name,
        "gender" : db_user.gender,
        "hobby" : db_profile.hobby,
        "interest" : db_profile.interest,
        "introduce" : db_profile.introduce
    }
    return response

# 내프로필 수정을 위한 프로필 보기
def get_my_profile(db : Session, user_id : int):
    db_profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    return db_profile

# 프로필 수정
def update_profile(db : Session, user_id :int, profile : schemas.ProfileCreate):
    db_profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    db_profile.location = profile.location
    db_profile.hobby = profile.hobby
    db_profile.interest = profile.interest
    db_profile.introduce = profile.instroduce
    
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

# 보낸 요청 목록 보기
def view_call_from_me(db : Session, user_id : int):
    db_call_list = db.query(models.Friend).filter(models.Friend.caller_id == user_id, models.Friend.state == "요청").all()
    
    response = []
    for receive_column in db_call_list:
        caller_id = receive_column.caller_id
        receiver = db.query(models.User).filter(models.User.id == caller_id).first()
        receiver_profile = db.query(models.Profile).filter(models.Profile.user_id == caller_id)
        response.append({
            "friend_id" : receive_column.id,
            "user_id" : receiver.id,
            "name" : receiver.name,
            "introduce" : receiver_profile.introduce
        })
        
    return response

# 친구요청 수락
def accept_call(db : Session, friend_id : int):
    db_friend = db.query(models.Friend).filter(models.Friend.id == friend_id).first()
    db_friend.state = "친구"
    db.add(db_friend)
    db.commit()
    db.refresh(db_friend)
    return db_friend

# 받은 요청 삭제
def delete_call_to_me(db : Session, friend_id : int, user_id : int):
    db_friend = db.query(models.Friend).filter(models.Friend.id == friend_id, models.Friend.receiver_id == user_id, models.Friend.state == "요청").first()
    db.delete(db_friend)
    db.commit()
    return {"message" : "삭제성공"}

# 받은 요청 목록보기
def view_call_to_me(db : Session, user_id : int):
    db_call_list = db.query(models.Friend).filter(models.Friend.receiver_id == user_id, models.Friend.state == "요청").all()
    
    response = []
    for call_column in db_call_list:
        caller_id = call_column.caller_id
        caller = db.query(models.User).filter(models.User.id == caller_id).first()
        caller_profile = db.query(models.Profile).filter(models.Profile.user_id == caller_id)
        response.append({
            "friend_id" : call_column.id,
            "user_id" : caller.id,
            "name" : caller.name,
            "introduce" : caller_profile.introduce
        })
        
    return response

# 보낸 요청 삭제
def delete_call_from_me(db : Session, friend_id : int, user_id : int):
    db_friend = db.query(models.Friend).filter(models.Friend.id == friend_id, models.Friend.caller_id == user_id, models.Friend.state == "요청").first()
    db.delete(db_friend)
    db.commit()
    return {"message" : "삭제성공"}

# 친구 목록 보기 //list 더해서 반환해야함
def get_friend_list(db : Session, user_id : int):
    response = []
    db_friends1 = db.query(models.Friend).filter(models.Friend.caller_id == user_id, models.Friend.state == "친구").all()
    
    for friend_column in db_friends1:
        friend_id = friend_column.receiver_id
        friend = db.query(models.User).filter(models.User.id == friend_id).first()
        friend_profile = db.query(models.Profile).filter(models.Profile.user_id == friend_id).first()
        response.append({
            "friend_id" : friend_column.id,
            "user_id" : friend.id,
            "name" : friend.name,
            "introduce" : friend_profile.introduce
        })
    
    db_friends2 = db.query(models.Friend).filter(models.Friend.receiver_id == user_id, models.Friend.state == "친구").all()
    
    for friend_column in db_friends2:
        friend_id = friend_column.caller_id
        friend = db.query(models.User).filter(models.User.id == friend_id).first()
        friend_profile = db.query(models.Profile).filter(models.Profile.user_id == friend_id).first()
        response.append({
            "friend_id" : friend_column.id,
            "user_id" : friend.id,
            "name" : friend.name,
            "introduce" : friend_profile.introduce
        })

    return response

# 친구 삭제
def delete_friend(db : Session, friend_id : int, user_id : int):
    db_friend = db.query(models.Friend).filter(models.Friend.id == friend_id, models.Friend.state == "친구").first()
    db.delete(db_friend)
    db.commit()
    return {"message" : "삭제성공"}

# 전체유저 반환
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# 이메일로 유저 검색
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()




