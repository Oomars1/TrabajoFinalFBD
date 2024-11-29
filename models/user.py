from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

# Definir el objeto Base para la aplicación
Base = declarative_base()

# Tabla de roles (rol)
class rol(Base):
    __tablename__ = "rol"

    id_rol = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(Text, nullable=False)

    # Relación inversa con los usuarios
    users = relationship("users", back_populates="rol")

# Tabla de usuarios (usuarios) UserDB
class users(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    id_rol = Column(Integer, ForeignKey("rol.id_rol"))
    activo = Column(Boolean, default=False)
    username = Column(String(30), unique=True, nullable=False)

    # Relación con el rol
    rol = relationship("rol", back_populates="users")

# Tabla de vehículos (vehiculos)
class vehiculos(Base):
    __tablename__ = "vehiculos"

    id_vehiculo = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    modelo = Column(String(50), nullable=False)
    marca = Column(String(50), nullable=False)
    placa = Column(String(30), unique=True, nullable=False)
    rendimiento = Column(String(30))
    galonaje = Column(Float)
    tipo_combustible = Column(String(25), nullable=False)

# Tabla de logs (log)
class log(Base):
    __tablename__ = "log"

    id_log = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    descripcion = Column(Text, nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))

# Tabla de proyectos (proyecto)
class proyecto(Base):
    __tablename__ = "proyecto"

    id_proyecto = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    nombre = Column(String(50), nullable=False)
    direccion = Column(String(60), nullable=False)
    activo = Column(Boolean, default=False)

# Tabla de gasolineras (gasolineras)
class gasolineras(Base):
    __tablename__ = "gasolineras"

    id_gasolinera = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    nombre = Column(String(50), nullable=False)
    direccion = Column(String(60), nullable=False)

# Tabla de bitácoras (bitacora)
class bitacora(Base):
    __tablename__ = "bitacora"

    id_bitacora = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    comentario = Column(Text)
    km_inicial = Column(Integer, nullable=False)
    km_final = Column(Integer, nullable=False)
    num_galones = Column(Float, nullable=False)
    costo = Column(Float, nullable=False)
    tipo_gasolina = Column(String(30), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_vehiculo = Column(Integer, ForeignKey("vehiculos.id_vehiculo"))
    id_gasolinera = Column(Integer, ForeignKey("gasolineras.id_gasolinera"))
    id_proyecto = Column(Integer, ForeignKey("proyecto.id_proyecto"))