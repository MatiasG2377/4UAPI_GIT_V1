from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_USER = 'uwkroqoqou2ieroj'
DB_PASSWORD = '6MVRtb8rvM3HQ9NMPJ47'
DB_HOST = 'b38upoqwbjpslbwjl572-mysql.services.clever-cloud.com'
DB_PORT = '3306'
DB_NAME = 'b38upoqwbjpslbwjl572'

# URL de conexión a la base de datos en la nube
URL_DATABASE = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(URL_DATABASE)

# Creamos la sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declaramos la clase base para el mapeo ORM
Base = declarative_base()
