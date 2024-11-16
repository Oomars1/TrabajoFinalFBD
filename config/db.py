import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine, MetaData

# Crear la conexión a la base de datos
engine = create_engine(
    "mysql://edwin:oomars2401@pruebagas-ibqod-mariadb.pruebagas-ibqod.svc.cluster.local:3306/pruebagas"
)

# Crear la metadata para la creación de los datos
meta = MetaData()

# Almacenar la conexión para utilizarla
conn = engine.connect()

