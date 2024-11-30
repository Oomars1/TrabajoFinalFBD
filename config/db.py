from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

# URL de conexión a PostgreSQL (Render)
DATABASE_URL = "postgresql://pruebagas_zusn_user:HPVUQuzq6DuI1M4PTfSSTMuhanI7Er8M@dpg-ct58d6d6l47c73fdbdag-a.oregon-postgres.render.com/pruebagas_zusn"

# Conexión a la base de datos PostgreSQL
engine = create_engine(DATABASE_URL)

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
