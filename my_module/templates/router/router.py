from fastapi import APIRouter,Depends, Form, HTTPException, status,Path,File, UploadFile
import bcrypt
from models import models
from schemas import schemas
from sqlalchemy.orm import Session
from db import get_db
from sqlalchemy.exc import SQLAlchemyError



from middleware.auth_service import create_access_token,get_current_user,security

auth_router = APIRouter(
    prefix="/auth"
)

user_router = APIRouter(
    prefix="/user"
)

book_router = APIRouter(
    prefix="/book"
)

def check_role(role: str = Path(...), password_admin: str | None = File(None)):
    if role.lower() == "admin" and password_admin != "1010":
        raise HTTPException(status_code=405, detail="Invalid admin password")
    return role

@auth_router.post("/signin/{role}", response_model=schemas.UserResponse,status_code=status.HTTP_201_CREATED)
def signin(user_data: schemas.BaseUser,role: str=Depends(check_role),db: Session = Depends(get_db)):
    try:
        if db.query(models.User).filter(models.User.email==user_data.email).first():
            raise HTTPException(status_code=409,detail="email is already exist")


        new_user = models.User(
            username=user_data.username,
            email=user_data.email,
            role=role
        )
        hash_password = bcrypt.hashpw(password=user_data.password.encode(),salt=bcrypt.gensalt())
        new_user.password=hash_password
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "message": "User created successfully"
        }
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500,detail="server error")
    

@auth_router.post("/login")
def login(user:schemas.login,db:Session=Depends(get_db)):
    user_name = db.query(models.User).filter(models.User.email==user.email).first()

    if not user_name:
        raise HTTPException(status_code=404, detail="User not found")
    if not bcrypt.checkpw(user.password.encode('utf-8'), user_name.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user_id=user_name.user_id, role=user_name.role,username=user.username)
    return {"access_token": token}
   

@user_router.patch(
    path="/update/{user_id}",
    response_model=schemas.Update_Response,
    )
def update_user(This_feature_is_only_for_the_admin_to_choose_which_user_to_edit:int,user_data:schemas.Update,token:str = Depends(security),db:Session=Depends(get_db)):
    try:
        token = get_current_user(token=token)


        if token["role"] == "admin":
            db_user = db.query(models.User).filter(models.User.id==This_feature_is_only_for_the_admin_to_choose_which_user_to_edit).first()
        else:
            db_user = db.query(models.User).filter(models.User.id==token["user_id"]).first()

        db_user.username = user_data.username
        db_user.email = user_data.email
    
        hashed_password = bcrypt.hashpw(user_data.password.encode(), bcrypt.gensalt())
        db_user.password = hashed_password
    
        db.commit()
        return {"message":"seccessful update","username":db_user.username,"email":db_user.email,"password":db_user.password,"id":db_user.id}
    except SQLAlchemyError:
        raise HTTPException(status_code=500,detail="server cant management")
        

@user_router.delete(
    path="/deleted/{user_id}/",
    response_model=schemas.delete
)
def delete(This_feature_is_only_for_the_admin_to_choose_which_user_to_edit:int,token: str = Depends(security),db:Session=Depends(get_db)):
    try:
        token = get_current_user(token=token)
 
        if token["role"] == "admin":
            db_user = db.query(models.User).filter(models.User.id==This_feature_is_only_for_the_admin_to_choose_which_user_to_edit).first()
        else:
            db_user = db.query(models.User).filter(models.User.id==token["user_id"]).first()
        
        db.delete(db_user)
        db.commit()
        return {"message":"user deleted","user_id":db_user.id}
    except SQLAlchemyError:
        raise HTTPException(status_code=500,detail="server cant management")
    

@user_router.get("/search/",response_model=schemas.search)
def search(by_with: str, user: str, db: Session = Depends(get_db)):
    try:


        if by_with.find("email") != -1:
            
            db_user = db.query(models.User).filter(models.User.email == user).first()
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            return db_user

        elif by_with.find("username") != -1:
            
            db_user = db.query(models.User).filter(models.User.username == user).first()
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            return db_user

        else:
            raise HTTPException(status_code=400, detail="Invalid search parameter")

    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")