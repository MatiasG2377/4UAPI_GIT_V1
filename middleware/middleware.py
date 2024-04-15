from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from functions_jwt import write_token, validate_token
from fastapi.responses import JSONResponse

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes (debes restringirlo en producción)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Permitir estos métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Resto del código...
