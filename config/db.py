from sqlalchemy import create_engine, MetaData
#Creamos la conexion ala base de datos
#engine=create_engine("mariadb+pymysql://root:oomars2401@localhost:3306/pruebagas")
engine=create_engine("mariadb+pymysql://root:oomars2401@localhost:3306/pruebagas")
#creamos la metadata para la creacion de los datos
meta=MetaData()
#almacenamos la conexion para utilizarla
conn=engine.connect()
