from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import date

from fastapi import FastAPI
import os

app = FastAPI()

# Ruta de ejemplo
@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}

if __name__ == "__main__":
    # Obtener el puerto de la variable de entorno PORT, o usar 8000 por defecto
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    # Escuchar en 0.0.0.0 para aceptar conexiones externas
    uvicorn.run(app, host="0.0.0.0", port=port)

models.Base.metadata.create_all(bind=engine)

class UserBase(BaseModel):
    user_name: str 
    user_last_name: str
    user_mail: str
    user_date: date
    user_password: str
    user_stars: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: int

class MessageBase(BaseModel):
    sms_content: str
    sms_date: str
    sms_sender: int
    sms_recipient: int

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    sms_id: int

class CategorieBase(BaseModel):
    cate_name: str

class CategorieCreate(CategorieBase):
    pass

class Categorie(CategorieBase):
    cate_id: int

class ProductBase(BaseModel):
    prod_name: str
    prod_price: float
    prod_desc: str
    prod_img: bytes
    prod_cate_id: int
    prod_user_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    prod_id: int

class TermsBase(BaseModel):
    term_date: str
    term_content: str

class TermsCreate(TermsBase):
    pass

class Terms(TermsBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Depends(get_db)

# Operaciones CRUD para la tabla de usuarios
@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[User], status_code=status.HTTP_200_OK)
async def read_all_users(db: Session = db_dependency):
    users = db.query(models.User).all()
    # Convertir las fechas a strings antes de devolverlas en la respuesta
    return [{**user.__dict__, "user_date": user.user_date.isoformat()} for user in users]

@app.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: Session = db_dependency):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    # Convertir las fechas a strings antes de devolverlas en la respuesta
    return {**user.__dict__, "user_date": user.user_date.isoformat(), "user_birth_date": user.user_birth_date.isoformat()}

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = db_dependency):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    db.delete(user)
    db.commit()
    return {}

@app.put("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user_update: UserCreate, db: Session = db_dependency):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    for key, value in user_update.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


# Operaciones CRUD para la tabla de mensajes
@app.post("/messages/", response_model=Message, status_code=status.HTTP_201_CREATED)
async def create_message(message: MessageCreate, db: Session = db_dependency):
    db_message = models.Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@app.get("/messages/", response_model=List[Message], status_code=status.HTTP_200_OK)
async def read_all_messages(db: Session = db_dependency):
    return db.query(models.Message).all()

# Operaciones CRUD para la tabla de categorías
@app.post("/categories/", response_model=Categorie, status_code=status.HTTP_201_CREATED)
async def create_categorie(categorie: CategorieCreate, db: Session = db_dependency):
    db_categorie = models.Categorie(**categorie.dict())
    db.add(db_categorie)
    db.commit()
    db.refresh(db_categorie)
    return db_categorie

@app.get("/categories/", response_model=List[Categorie], status_code=status.HTTP_200_OK)
async def read_all_categories(db: Session = db_dependency):
    return db.query(models.Categorie).all()

# Operaciones CRUD para la tabla de productos
@app.post("/products/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: Session = db_dependency):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[Product], status_code=status.HTTP_200_OK)
async def read_all_products(db: Session = db_dependency):
    return db.query(models.Product).all()

@app.get("/products/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
async def read_product(product_id: int, db: Session = db_dependency):
    product = db.query(models.Product).filter(models.Product.prod_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')
    return product

@app.put("/products/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
async def update_product(product_id: int, product_update: ProductCreate, db: Session = db_dependency):
    db_product = db.query(models.Product).filter(models.Product.prod_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail='Product not found')
    for key, value in product_update.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: Session = db_dependency):
    product = db.query(models.Product).filter(models.Product.prod_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')
    db.delete(product)
    db.commit()
    return {}


# Operaciones CRUD para la tabla de términos
@app.post("/terms/", response_model=Terms, status_code=status.HTTP_201_CREATED)
async def create_terms(terms: TermsCreate, db: Session = db_dependency):
    db_terms = models.Terms(**terms.dict())
    db.add(db_terms)
    db.commit()
    db.refresh(db_terms)
    return db_terms

@app.get("/terms/", response_model=List[Terms], status_code=status.HTTP_200_OK)
async def read_all_terms(db: Session = db_dependency):
    return db.query(models.Terms).all()
