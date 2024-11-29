from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

# Conexión a la base de datos (asegúrate de que la URL de conexión es correcta)
engine = create_engine("mariadb+pymysql://root:oomars2401@localhost:3306/pruebagas")

# Crea la metadata para la creación de los datos
meta = MetaData()

# Configura el sessionmaker para crear sesiones de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener la sesión de la base de datos (para usar en los endpoints)
def get_db():
    db = SessionLocal()  # Crea una nueva sesión
    try:
        yield db  # Devuelve la sesión para usarla en los endpoints
    finally:
        db.close()  # Asegura que la sesión se cierre después de su uso
