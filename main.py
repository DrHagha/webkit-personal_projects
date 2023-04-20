from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models,schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#회원 생성
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

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