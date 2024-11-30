from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

# Conexión a la base de datos PostgreSQL
engine = create_engine("postgresql://postgres:tXebTxHkwclkDkEoKAPWvzbuNJkYpGES@autorack.proxy.rlwy.net:23141/railway")

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
