from fastapi import APIRouter, HTTPException, status
from typing import List
from config.db import conn
from models.user import users, rol, vehiculos, bitacora, proyecto, gasolineras
from schemas.user_schema import User, UserCount, VehiculoCreate, VehiculoResponse, Bitacora, BitacoraResponse
from sqlalchemy import func, select, insert, update, delete, join

user = APIRouter()

# Obtener el conteo de usuarios
@user.get("/users/count", tags=["users"], response_model=UserCount)
def get_users_count():
    try:
        query = select(func.count()).select_from(users)
        result = conn.execute(query).scalar()
        return {"total": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obtener un usuario por su ID
@user.get("/users/{id}", tags=["users"], response_model=User, description="Get a single user by Id")
def get_user(id: int):
    user_record = conn.execute(users.select().where(users.c.id_usuario == id)).first()
    if user_record is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_record

# Obtener todos los usuarios
@user.get("/users", tags=["users"], response_model=List[User], description="Get all users")
def get_all_users():
    return conn.execute(users.select()).fetchall()

# Crear un nuevo usuario
@user.post("/users/", tags=["users"], response_model=User, description="Create a new user")
def create_user(user: User):
    try:
        new_user = {
            "nombre": user.nombre,
            "apellido": user.apellido,
            "password": user.password,  # Asegúrate de cifrar la contraseña
            "id_rol": user.id_rol,
            "username": user.username
        }
        result = conn.execute(users.insert().values(new_user))
        conn.commit()
        return conn.execute(users.select().where(users.c.id_usuario == result.lastrowid)).first()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Actualizar un usuario por su ID
@user.put("/users/{id}", tags=["users"], response_model=User, description="Update a User by Id")
def update_user(id: int, user: User):
    existing_user = conn.execute(users.select().where(users.c.id_usuario == id)).first()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_values = {
        "nombre": user.nombre,
        "apellido": user.apellido,
        "password": user.password,  # Asegúrate de cifrar la contraseña
        "id_rol": user.id_rol,
        "username": user.username
    }
    
    conn.execute(users.update().where(users.c.id_usuario == id).values(updated_values))
    conn.commit()
    return conn.execute(users.select().where(users.c.id_usuario == id)).first()

# Eliminar un usuario por su ID
@user.delete("/users/{id}", tags=["users"], status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    result = conn.execute(users.delete().where(users.c.id_usuario == id))
    conn.commit()
    
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    return {"message": "Se eliminó el usuario", "id": id}

# Crear un nuevo vehículo (si es necesario para tu aplicación)
@user.post("/vehicles/", tags=["vehicles"], description="Create a new vehicle")
def create_vehicle(vehicle: VehiculoCreate):
    try:
        stmt = insert(vehiculos).values(
            modelo=vehicle.modelo,
            marca=vehicle.marca,
            placa=vehicle.placa,
            rendimiento=vehicle.rendimiento,
            galonaje=vehicle.galonaje,
            tipo_combustible=vehicle.tipo_combustible
        )
        conn.execute(stmt)
        conn.commit()

        new_vehicle_id = conn.execute(select(vehiculos.c.id_vehiculo).order_by(vehiculos.c.id_vehiculo.desc()).limit(1)).scalar_one()
        return {"message": "Vehicle created successfully", "vehicle_id": new_vehicle_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Obtener todos los vehículos (si es necesario para tu aplicación)
@user.get("/vehicles/", tags=["vehicles"], response_model=List[VehiculoResponse], description="Get all vehicles")
def get_vehicles():
    try:
        stmt = select(
            vehiculos.c.id_vehiculo,
            vehiculos.c.modelo,
            vehiculos.c.marca,
            vehiculos.c.placa,
            vehiculos.c.tipo_combustible
        )
        
        result = conn.execute(stmt).fetchall()
        vehicles = []
        for row in result:
            vehicle_data = {
                "id": row.id_vehiculo,
                "modelo": row.modelo,
                "marca": row.marca,
                "placa": row.placa,
                "tipo_combustible": row.tipo_combustible
            }
            vehicles.append(vehicle_data)

        return vehicles
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Crear un nuevo registro en la bitácora
@user.post("/bitacora/", tags=["bitacora"], description="Create a new record in the bitacora")
def create_bitacora(record: Bitacora):
    try:
        stmt = insert(bitacora).values(
            km_inicial=record.km_inicial,
            km_final=record.km_final,
            num_galones=record.num_galones,
            costo=record.costo,
            tipo_gasolina=record.tipo_gasolina,
            id_usuario=record.id_usuario,
            id_vehiculo=record.id_vehiculo,
            id_gasolinera=record.id_gasolinera,
            id_proyecto=record.id_proyecto
        )
        conn.execute(stmt)
        conn.commit()

        new_record_id = conn.execute(select(bitacora.c.id_bitacora).order_by(bitacora.c.id_bitacora.desc()).limit(1)).scalar_one()
        return {"message": "Bitacora record created successfully", "record_id": new_record_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Obtener todas las bitácoras
@user.get("/bitacora/", tags=["bitacora"], response_model=List[BitacoraResponse], description="Get all bitacora records")
def get_bitacora():
    try:
        stmt = select(
            bitacora.c.id_bitacora,
            bitacora.c.km_inicial,
            bitacora.c.km_final,
            bitacora.c.num_galones,
            bitacora.c.costo,
            bitacora.c.tipo_gasolina,
            users.c.nombre,
            vehiculos.c.modelo,
            gasolineras.c.nombre.label("gasolinera"),
            proyecto.c.nombre.label("proyecto")
        ).join(users, bitacora.c.id_usuario == users.c.id_usuario) \
         .join(vehiculos, bitacora.c.id_vehiculo == vehiculos.c.id_vehiculo) \
         .join(gasolineras, bitacora.c.id_gasolinera == gasolineras.c.id_gasolinera) \
         .join(proyecto, bitacora.c.id_proyecto == proyecto.c.id_proyecto)
        
        result = conn.execute(stmt).fetchall()
        records = []
        for row in result:
            record_data = {
                "id": row.id_bitacora,
                "km_inicial": row.km_inicial,
                "km_final": row.km_final,
                "num_galones": row.num_galones,
                "costo": row.costo,
                "tipo_gasolina": row.tipo_gasolina,
                "usuario": row.nombre,
                "vehiculo": row.modelo,
                "gasolinera": row.gasolineras,
                "proyecto": row.proyecto
            }
            records.append(record_data)

        return records
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
