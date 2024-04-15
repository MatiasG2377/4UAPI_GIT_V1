from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, EmailStr
from functions_jwt import validate_token, write_token
from fastapi.responses import JSONResponse

from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User as DBUser
from database import SessionLocal, engine

auth_routes = APIRouter()

class User(BaseModel):
    username: EmailStr
    password: str

@auth_routes.post("/login")
def login(user: User):
    print(user.dict())
    if user.username == "123@hotmail.com" and user.password == "123":
        return write_token(user.dict())
    else:
        return JSONResponse(content={"message": "User not found"}, status_code=404)


@auth_routes.post("/verify/token")
def verify_token(Authorization: str = Header(None)):
    if Authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    parts = Authorization.split(" ")
    if len(parts) != 2:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    token = parts[1]
    print(token)
    return validate_token(token, output=True)



# @auth_routes.post("/verify/token")
# def verify_token(Authorization: str = Header(None)):
#     token = Authorization.split(" ")[1]
#     print(token)
#     return validate_token(token, output=True)
    
