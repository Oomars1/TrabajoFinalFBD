import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine, MetaData

# Crear la conexión a la base de datos
engine = create_engine(
    "mysql://edwin:oomars2401@/pruebagas"
)

# Crear la metadata para la creación de los datos
meta = MetaData()

# Almacenar la conexión para utilizarla
conn = engine.connect()

