from sqlalchemy import create_engine, MetaData
#Creamos la conexion ala base de datos
engine=create_engine("mariadb+pymysql://root:oomars2401@localhost:3306/pruebagas")
#engine=create_engine("mysql://ladybug:rI8]xG2*sM0[qO4&@yabbering-scarlet-herring-snbwu-mariadb.yabbering-scarlet-herring-snbwu.svc.cluster.local:3306/yabbering-scarlet-herring")
#creamos la metadata para la creacion de los datos
meta=MetaData()
#almacenamos la conexion para utilizarla
conn=engine.connect()
