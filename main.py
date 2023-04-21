from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session
from datetime import timedelta, datetime

import crud, models,schemas
from database import SessionLocal, engine

from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from secret import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM 
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

# CORS 미들웨어를 설정합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#로그인
@app.post("/login", response_model=schemas.User)
def login_for_access_token(email : str, password : str, db: Session = Depends(get_db)):
    print(email)
    print(password)
    login_user = crud.login(email=email, password= password, db=db)
    print(login_user)
    return login_user

#회원 생성
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

#언어변경
@app.put("/setting/language/{user_id}")
def update_language(user_id : int, language : str, db : Session = Depends(get_db)):
    db_user = crud.update_language(user_id=user_id, language=language, db=db)
    return db_user

#유저 목록 호출
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

#유저 아이디로 가져오기
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#수정을 위한 프로필 조회
@app.get("/profile/me/{user_id}")
def get_my_profile(user_id : int, db : Session = Depends(get_db)):
    db_profile = crud.get_my_profile(user_id=user_id ,db=db)
    print(db_profile)
    return db_profile

#유저 프로필 조회
@app.get("/profile/{user_id}")
def get_profile(user_id : int, db : Session = Depends(get_db)):
    db_profile = crud.get_profile(user_id=user_id ,db=db)
    return db_profile

#유저 프로필 수정
@app.put("/profile/{user_id}")
def get_profile(user_id : int, profile : schemas.Profile, db : Session = Depends(get_db)):
    db_profile = crud.update_profile(user_id=user_id, profile=profile, db=db)
    return db_profile

#회원 탈퇴
@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id : int, db : Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id = user_id)
    return db_user
    
#회원 수정
@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id : int , user : schemas.UserCreate ,db : Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, user=user)
    return db_user

#친구요청
@app.post("/friend/", response_model=schemas.Friend)
def create_friend(caller_id : int, receiver_id : int, db : Session = Depends(get_db)):
    db_friend = crud.call_friend(db = db, caller_id = caller_id, receiver_id=receiver_id)
    return db_friend

#받은 요청 조회
@app.get("/friend/to_me/")
def view_call_to_me(user_id : int, db : Session = Depends(get_db)):
    db_friends = crud.view_call_to_me(db = db, user_id=user_id)
    return db_friends

#받은 요청 거부(삭제)
@app.delete("/friend/to_me/")
def delete_call_to_me(user_id : int, friend_id : int, db : Session = Depends(get_db)):
    db_friend = crud.delete_call_to_me(db = db, friend_id = friend_id, user_id= user_id)
    return db_friend

#보낸요청 조회
@app.get("/friend/from_me/")
def view_call_to_me(user_id : int, db : Session = Depends(get_db)):
    db_friends = crud.view_call_from_me(db = db, user_id=user_id)
    return db_friends

#보낸 요청 거부(삭제)
@app.delete("/friend/from_me/")
def delete_call_to_me(user_id : int, friend_id : int, db : Session = Depends(get_db)):
    db_friend = crud.delete_call_from_me(db = db, friend_id = friend_id, user_id= user_id)
    return db_friend

#받은 요청 수락
@app.put("/friend/accept/")
def accept_call(friend_id : int, db : Session = Depends(get_db)):
    db_friend = crud.accept_call(db = db, friend_id=friend_id)
    return db_friend

#친구 삭제
@app.delete("/friend/")
def delete_friend(friend_id : int, user_id : int, db : Session = Depends(get_db)):
    db_friend = crud.delete_friend(friend_id = friend_id, user_id= user_id, db=db)
    return db_friend

#친구 목록보기
@app.get("/freind/{user_id}")
def get_friends(user_id : int, db : Session = Depends(get_db)):
    db_friends = crud.get_friend_list(user_id= user_id, db=db)
    print(db_friends)
    return db_friends