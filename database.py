from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_USER = 'uglippajbziyfn7z'
DB_PASSWORD = 'tz9BH7MNWU84RsGME1px'
DB_HOST = 'bdcdv72tkuakz9qbnlc3-mysql.services.clever-cloud.com'
DB_PORT = '3306'
DB_NAME = 'bdcdv72tkuakz9qbnlc3'

# URL de conexión a la base de datos en la nube
URL_DATABASE = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(URL_DATABASE)

# Creamos la sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declaramos la clase base para el mapeo ORM
Base = declarative_base()
