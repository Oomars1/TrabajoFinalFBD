from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime, timezone
from sqlalchemy.orm import Session
import bcrypt
from typing import List
from config.db import get_db
from models.user import users, rol, vehiculos, bitacora, proyecto, gasolineras, log
from schemas.user_schema import User, UserCount, VehiculoCreate, VehiculoResponse, Bitacora, BitacoraResponse
from schemas.user_schema import  Rol, LogCreate, LogResponse, Proyectos, Gasolinera, LoginRequest
from sqlalchemy import func, select, insert, update, delete, join
from utils.auth import verify_password 

user = APIRouter()

# Función para encriptar la contraseña necesario
def encrypt_password(password: str) -> str:
    salt = bcrypt.gensalt()  # Genera un "salt" aleatorio
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  # Hashea la contraseña
    return hashed_password.decode('utf-8')  # Devuelve el hash como string

# Función de login
@user.post("/login", tags=["users"], description="Login user") #okkkk
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        # Realizar la consulta para obtener el usuario
        user = db.query(users).filter(users.username == request.username).first()  # Usamos la sesión de SQLAlchemy
        
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Verificar la contraseña usando la función de hash
        if not verify_password(request.password, user.password):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")
        
        # Si la contraseña es correcta, devuelve el usuario
        return {"id_usuario": user.id_usuario, "username": user.username}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# Obtener el conteo de usuarios
@user.get("/users/count", tags=["users"], response_model=UserCount)
def get_users_count(db: Session = Depends(get_db)):
    try:
        # Obtener el conteo de usuarios utilizando la sesión
        result = db.query(func.count()).select_from(users).scalar()
        return {"total": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obtener un usuario por su ID
@user.get("/users/{id}", tags=["users"], response_model=User, description="Get a single user by Id")
def get_user(id: int, db: Session = Depends(get_db)):
    user_record = db.query(users).filter(users.c.id_usuario == id).first()  # Usamos la sesión
    if user_record is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user_record

# Obtener todos los usuarios
@user.get("/users/", tags=["users"], response_model=List[User], description="Get all users")
def get_all_users(db: Session = Depends(get_db)):
    # Obtener todos los usuarios utilizando la sesión
    return db.query(users).all()  # Usamos la sesión para obtener todos los usuarios



# Crear un nuevo usuario
@user.post("/users/", tags=["users"], response_model=User, description="Create a new user") #okkk
def create_user(user: User, db: Session = Depends(get_db)):
    try:
        hashed_password = encrypt_password(user.password)
        
        new_user = users(
            nombre=user.nombre,
            apellido=user.apellido,
            password=hashed_password,
            id_rol=user.id_rol,
            username=user.username,
            created_at=datetime.now()
        )
        
        db.add(new_user)  # Agregar el nuevo usuario a la sesión
        db.commit()  # Confirmar la transacción
        db.refresh(new_user)  # Refrescar el objeto con los datos de la base de datos
        
        return new_user
    
    except Exception as e:
        db.rollback()  # Revertir los cambios si ocurre un error
        raise HTTPException(status_code=400, detail=str(e))


# Actualizar un usuario por su ID
@user.put("/users/{id}", tags=["users"], response_model=User, description="Update a User by Id") #okkkkkkkkk
def update_user(id: int, user: User, db: Session = Depends(get_db)):
    # Consultar el usuario existente en la base de datos
    existing_user = db.query(users).filter(users.id_usuario == id).first()  # Usamos la sesión

    if existing_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Preparar los valores para la actualización
    updated_values = {
        "nombre": user.nombre,
        "apellido": user.apellido,
        "id_rol": user.id_rol,
        "username": user.username
    }

    # Encriptar solo la contraseña si ha sido proporcionada en la solicitud
    if user.password:
        updated_values["password"] = encrypt_password(user.password)

    # Actualizar el usuario en la base de datos
    db.query(users).filter(users.id_usuario == id).update(updated_values)
    db.commit()  # Confirmar los cambios

    # Sincronizar los cambios con la base de datos
    db.refresh(existing_user) 

    return existing_user



# Eliminar un usuario por su ID
@user.delete("/users/{id}", tags=["users"], status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    try:
        user_to_delete = db.query(users).filter(users.id_usuario == id).first()  # Usamos la sesión
        if user_to_delete is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        db.delete(user_to_delete)
        db.commit()  # Confirmar la eliminación
        return {"message": "Se eliminó el usuario", "id": id}
    
    except Exception as e:
        db.rollback()  # Revertir si ocurre un error
        raise HTTPException(status_code=400, detail=str(e))


##################################################################################################################
# Crear un nuevo vehículo (si es necesario para tu aplicación)
@user.post("/vehiculos/", tags=["vehiculos"], description="Create a new vehicle") #okk
def create_vehicle(vehicle: VehiculoCreate, db: Session = Depends(get_db)):
    try:
        new_vehicle = vehiculos(
            modelo=vehicle.modelo,
            marca=vehicle.marca,
            placa=vehicle.placa,
            rendimiento=vehicle.rendimiento,
            galonaje=vehicle.galonaje,
            tipo_combustible=vehicle.tipo_combustible
        )
        
        db.add(new_vehicle)  # Agregar el nuevo vehículo a la sesión
        db.commit()  # Confirmar la transacción
        db.refresh(new_vehicle)  # Sincronizar el objeto con la base de datos
        
        return {"message": "Vehículo creado exitosamente", "vehicle_id": new_vehicle.id_vehiculo}
    
    except Exception as e:
        db.rollback()  # Revertir si ocurre un error
        raise HTTPException(status_code=400, detail=str(e))


# Obtener todos los vehículos (si es necesario para tu aplicación)
@user.get("/vehiculos/", tags=["vehiculos"], response_model=List[VehiculoResponse], description="Get all vehicles") #okk
def get_vehicles(db: Session = Depends(get_db)):
    try:
        result = db.query(vehiculos).all()  # Obtener todos los vehículos usando la sesión
        vehicles = []
        
        for row in result:
            vehicle_data = {
                "id_vehiculo": row.id_vehiculo,
                "modelo": row.modelo,
                "marca": row.marca,
                "placa": row.placa,
                "rendimiento": row.rendimiento,
                "galonaje": row.galonaje,
                "tipo_combustible": row.tipo_combustible
            }
            vehicles.append(vehicle_data)
        
        return vehicles
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Eliminar un vehículo por su ID #okk
@user.delete("/vehiculos/{id}", tags=["vehiculos"], status_code=status.HTTP_204_NO_CONTENT, description="Delete a vehicle by ID") #okkkk
def delete_vehicle(id: int, db: Session = Depends(get_db)):
    try:
        vehicle_to_delete = db.query(vehiculos).filter(vehiculos.id_vehiculo == id).first()  # Usamos la sesión
        if vehicle_to_delete is None:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        
        db.delete(vehicle_to_delete)
        db.commit()  # Confirmar la eliminación
        return {"message": "Vehículo eliminado exitosamente", "vehicle_id": id}
    
    except Exception as e:
        db.rollback()  # Revertir si ocurre un error
        raise HTTPException(status_code=400, detail=f"Error eliminando el vehículo: {str(e)}")



# Actualizar un vehículo por su ID
@user.put("/vehiculos/{id}", tags=["vehiculos"], description="Update a vehicle by ID") #okkk
def update_vehicle(id: int, vehicle: VehiculoCreate, db: Session = Depends(get_db)):
    try:
        vehicle_to_update = db.query(vehiculos).filter(vehiculos.id_vehiculo == id).first()
        if vehicle_to_update is None:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        
        # Actualizar los valores del vehículo
        vehicle_to_update.modelo = vehicle.modelo
        vehicle_to_update.marca = vehicle.marca
        vehicle_to_update.placa = vehicle.placa
        vehicle_to_update.rendimiento = vehicle.rendimiento
        vehicle_to_update.galonaje = vehicle.galonaje
        vehicle_to_update.tipo_combustible = vehicle.tipo_combustible

        db.commit()  # Confirmar los cambios
        db.refresh(vehicle_to_update)  # Sincronizar con la base de datos

        return {"message": "Vehículo actualizado exitosamente", "vehicle_id": id}
    
    except Exception as e:
        db.rollback()  # Revertir si ocurre un error
        raise HTTPException(status_code=400, detail=f"Error actualizando el vehículo: {str(e)}")



##################################################################################################################
# Crear un nuevo registro en la bitácora  -------------- probada y pasada
@user.post("/bitacora/", tags=["bitacora"], description="Create a new record in the bitacora") #okkk
def create_bitacora(record: Bitacora, db: Session = Depends(get_db)):
    try:
        new_record = bitacora(
            created_at=datetime.now(),
            comentario=record.comentario,
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
        
        db.add(new_record)  # Agregar el nuevo registro a la sesión
        db.commit()  # Confirmar la transacción
        db.refresh(new_record)  # Sincronizar el objeto con la base de datos
        
        return {"message": "Registro de bitácora creado exitosamente", "record_id": new_record.id_bitacora}
    
    except Exception as e:
        db.rollback()  # Revertir si ocurre un error
        raise HTTPException(status_code=400, detail=str(e))


#okokokokok
@user.get("/bitacora/", tags=["bitacora"], response_model=List[BitacoraResponse], description="Get all bitacora records with related data") #ok
def get_bitacora(db: Session = Depends(get_db)):
    try:
        # Realiza la consulta uniendo las tablas necesarias
        result = db.query(
            bitacora.id_bitacora,
            bitacora.created_at,
            bitacora.comentario,
            bitacora.km_inicial,
            bitacora.km_final,
            bitacora.num_galones,
            bitacora.costo,
            bitacora.tipo_gasolina,
            users.nombre.label("usuario"),   # Alias correcto para 'nombre' de 'users'
            vehiculos.modelo.label("vehiculo"),  # Alias correcto para 'modelo' de 'vehiculos'
            gasolineras.nombre.label("gasolineras"),  # Alias correcto para 'nombre' de 'gasolineras'
            proyecto.nombre.label("proyecto")   # Alias correcto para 'nombre' de 'proyecto'
        ).join(users, bitacora.id_usuario == users.id_usuario) \
         .join(vehiculos, bitacora.id_vehiculo == vehiculos.id_vehiculo) \
         .join(gasolineras, bitacora.id_gasolinera == gasolineras.id_gasolinera) \
         .join(proyecto, bitacora.id_proyecto == proyecto.id_proyecto).all()

        # Preparar los registros con los datos obtenidos
        records = []
        for row in result:
            # Asegúrate de que cada `row` tiene los campos correctos
            record_data = {
                "id_bitacora": row[0],   # Accede a la columna 'id_bitacora'
                "created_at": row[1],    # Accede a la columna 'created_at'
                "comentario": row[2],    # Accede a la columna 'comentario'
                "km_inicial": row[3],   # Accede a la columna 'km_inicial'
                "km_final": row[4],     # Accede a la columna 'km_final'
                "num_galones": row[5],  # Accede a la columna 'num_galones'
                "costo": row[6],        # Accede a la columna 'costo'
                "tipo_gasolina": row[7],# Accede a la columna 'tipo_gasolina'
                "usuario": row[8],      # Accede al alias 'usuario'
                "vehiculo": row[9],     # Accede al alias 'vehiculo'
                "gasolineras": row[10], # Accede al alias 'gasolineras'
                "proyecto": row[11],    # Accede al alias 'proyecto'
            }
            records.append(record_data)

        return records
    
    except Exception as e:
        # Si ocurre un error, devolver el mensaje
        raise HTTPException(status_code=400, detail=f"Error retrieving bitacora records: {str(e)}")


# Eliminar un registro de la bitácora por su ID
@user.delete("/bitacora/{id}", tags=["bitacora"], status_code=status.HTTP_204_NO_CONTENT, description="Delete a record from the bitacora by ID") #okkkk
def delete_bitacora(id: int, db: Session = Depends(get_db)):
    try:
        record_to_delete = db.query(bitacora).filter(bitacora.id_bitacora == id).first()  # Usamos la sesión
        if record_to_delete is None:
            raise HTTPException(status_code=404, detail="Registro de bitácora no encontrado")
        
        db.delete(record_to_delete)
        db.commit()  # Confirmar la eliminación
        return {"message": "Registro de bitácora eliminado exitosamente", "id": id}
    
    except Exception as e:
        db.rollback()  # Revertir si ocurre un error
        raise HTTPException(status_code=400, detail=f"Error eliminando el registro de bitácora: {str(e)}")


# Actualizar un registro en la bitácora -------------- Adaptado y funcional OK
@user.put("/bitacora/{id}", tags=["bitacora"], description="Update an existing record in the bitacora") #okkk
def update_bitacora(id: int, record: Bitacora, db: Session = Depends(get_db)):
    try:
        stmt = (
            db.query(bitacora)
            .filter(bitacora.id_bitacora == id)
            .update({
                "comentario": record.comentario,
                "km_inicial": record.km_inicial,
                "km_final": record.km_final,
                "num_galones": record.num_galones,
                "costo": record.costo,
                "tipo_gasolina": record.tipo_gasolina,
                "id_usuario": record.id_usuario,
                "id_vehiculo": record.id_vehiculo,
                "id_gasolinera": record.id_gasolinera,
                "id_proyecto": record.id_proyecto
            })
        )
        db.commit()  # Confirmar los cambios
        updated_record = db.query(bitacora).filter(bitacora.id_bitacora == id).first()  # Obtener el registro actualizado
        
        if not updated_record:
            raise HTTPException(status_code=404, detail="Registro de bitácora no encontrado.")
        
        return {"message": "Registro de bitácora actualizado exitosamente", "record_id": id}
    
    except Exception as e:
        db.rollback()  # Revertir si ocurre un error
        raise HTTPException(status_code=400, detail=f"Error actualizando el registro de bitácora: {str(e)}")


##################################################################################################################
# Crear un rol  okkkkk
@user.post("/roles/", tags=["roles"], response_model=Rol, status_code=status.HTTP_201_CREATED) #okkkk
def create_role(role: Rol, db: Session = Depends(get_db)):
    try:
        new_role = rol(descripcion=role.descripcion)
        
        db.add(new_role)  # Agregar el nuevo rol a la sesión
        db.commit()  # Confirmar la transacción
        db.refresh(new_role)  # Sincronizar el objeto con la base de datos
        
        return new_role
    
    except Exception as e:
        db.rollback()  # Revertir los cambios si ocurre un error
        raise HTTPException(status_code=400, detail=f"Error creando el rol: {str(e)}")



# Leer todos los roles
@user.get("/roles/", tags=["roles"], response_model=list[Rol]) #okkkk
def get_roles(db: Session = Depends(get_db)):
    try:
        result = db.query(rol).all()  # Obtener todos los roles usando la sesión
        return [Rol(id_rol=row.id_rol, descripcion=row.descripcion) for row in result]
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener los roles: {str(e)}")


# Leer un rol por ID
@user.get("/roles/{id_rol}", tags=["roles"], response_model=Rol) #okkkk
def get_role_by_id(id_rol: int, db: Session = Depends(get_db)):
    try:
        result = db.query(rol).filter(rol.id_rol == id_rol).first()  # Usamos la sesión para buscar el rol
        if not result:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        
        return Rol(id_rol=result.id_rol, descripcion=result.descripcion)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener el rol: {str(e)}")



# Actualizar un rol
@user.put("/roles/{id_rol}", tags=["roles"], response_model=Rol) #okkk
def update_role(id_rol: int, role: Rol, db: Session = Depends(get_db)):
    try:
        # Realizar la actualización del rol
        result = db.query(rol).filter(rol.id_rol == id_rol).update({
            "descripcion": role.descripcion
        })
        db.commit()  # Confirmar los cambios

        if result == 0:  # Si no se actualizó ningún rol, lanzamos un error
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        
        updated_role = db.query(rol).filter(rol.id_rol == id_rol).first()
        return updated_role
    
    except Exception as e:
        db.rollback()  # Revertir los cambios si ocurre un error
        raise HTTPException(status_code=400, detail=f"Error actualizando el rol: {str(e)}")


# Eliminar un rol
@user.delete("/roles/{id_rol}", tags=["roles"], status_code=status.HTTP_204_NO_CONTENT) #okkk
def delete_role(id_rol: int, db: Session = Depends(get_db)):
    try:
        # Buscar el rol que se va a eliminar
        role_to_delete = db.query(rol).filter(rol.id_rol == id_rol).first()
        if role_to_delete is None:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        
        db.delete(role_to_delete)  # Eliminar el rol
        db.commit()  # Confirmar la transacción
        
        return {"message": f"Rol con id {id_rol} eliminado exitosamente"}
    
    except Exception as e:
        db.rollback()  # Revertir si ocurre un error
        raise HTTPException(status_code=400, detail=f"Error eliminando el rol: {str(e)}")


    
##################################################################################################################
# Crear un registro de log
#ojo en este tenemos que ver el disparador para cuando se haga lo del login
@user.post("/logs/", tags=["logs"], response_model=LogResponse, status_code=status.HTTP_201_CREATED) #okkkk
def create_log(log_entry: LogCreate, db: Session = Depends(get_db)):
    try:
        new_log = log(
            descripcion=log_entry.descripcion,
            id_usuario=log_entry.id_usuario,
            created_at=datetime.now()  # Se establece el timestamp actual
        )
        
        db.add(new_log)  # Agregar el nuevo log a la sesión
        db.commit()  # Confirmar la transacción
        db.refresh(new_log)  # Sincronizar el objeto con la base de datos
        
        return LogResponse(
            id_log=new_log.id_log,
            created_at=new_log.created_at,
            descripcion=new_log.descripcion,
            id_usuario=new_log.id_usuario
        )
    
    except Exception as e:
        db.rollback()  # Revertir si ocurre un error
        raise HTTPException(status_code=400, detail=f"Error creando el log: {str(e)}")


# Leer todos los registros de log
@user.get("/logs/", tags=["logs"], response_model=list[LogResponse]) #okkk
def get_logs(db: Session = Depends(get_db)):
    try:
        result = db.query(log).all()  # Obtener todos los logs usando la sesión
        return [
            LogResponse(
                id_log=row.id_log,
                created_at=row.created_at,
                descripcion=row.descripcion,
                id_usuario=row.id_usuario
            ) for row in result
        ]
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener los logs: {str(e)}")



# Leer un log por ID
@user.get("/logs/{id_log}", tags=["logs"], response_model=LogResponse) #okk
def get_log_by_id(id_log: int, db: Session = Depends(get_db)):
    try:
        result = db.query(log).filter(log.id_log == id_log).first()  # Usamos la sesión para buscar el log
        if not result:
            raise HTTPException(status_code=404, detail="Log no encontrado")
        
        return LogResponse(
            id_log=result.id_log,
            created_at=result.created_at,
            descripcion=result.descripcion,
            id_usuario=result.id_usuario
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener el log: {str(e)}")


# Actualizar un log
@user.put("/logs/{id_log}", tags=["logs"], response_model=LogResponse) #okkk
def update_log(id_log: int, log_entry: LogCreate, db: Session = Depends(get_db)):
    try:
        stmt = db.query(log).filter(log.id_log == id_log).update({
            "descripcion": log_entry.descripcion,
            "id_usuario": log_entry.id_usuario
        })
        db.commit()  # Confirmar los cambios

        if stmt == 0:  # Si no se actualizó ningún log, lanzamos un error
            raise HTTPException(status_code=404, detail="Log no encontrado")
        
        updated_log = db.query(log).filter(log.id_log == id_log).first()
        return LogResponse(
            id_log=updated_log.id_log,
            created_at=updated_log.created_at,
            descripcion=updated_log.descripcion,
            id_usuario=updated_log.id_usuario
        )
    
    except Exception as e:
        db.rollback()  # Revertir si ocurre un error
        raise HTTPException(status_code=400, detail=f"Error actualizando el log: {str(e)}")

@user.post("/login", tags=["users"], description="Login user")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(users).filter(users.c.username == request.username).first()  # Usamos la sesión de SQLAlchemy
        
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        if not verify_password(request.password, user.password):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")
        
        # Crear un log de inicio de sesión
        log_entry = LogCreate(
            descripcion=f"Usuario {user.username} inició sesión",
            id_usuario=user.id_usuario
        )
        create_log(log_entry, db)  # Llamada al método para crear el log
        
        return {"id_usuario": user.id_usuario, "username": user.username}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# Eliminar un log
@user.delete("/logs/{id_log}", tags=["logs"], status_code=status.HTTP_204_NO_CONTENT) #okkk
def delete_log(id_log: int, db: Session = Depends(get_db)):
    try:
        log_to_delete = db.query(log).filter(log.id_log == id_log).first()  # Buscar el log a eliminar
        if log_to_delete is None:
            raise HTTPException(status_code=404, detail="Log no encontrado")
        
        db.delete(log_to_delete)  # Eliminar el log
        db.commit()  # Confirmar la eliminación
        return {"message": f"Log con id {id_log} eliminado exitosamente"}
    
    except Exception as e:
        db.rollback()  # Revertir si ocurre un error
        raise HTTPException(status_code=400, detail=f"Error eliminando el log: {str(e)}")

    
##################################################################################################################
#agg proyecto
@user.post("/proyectos/", tags=["proyectos"], response_model=Proyectos, description="Create a new project") #okk
def create_proyecto(proyecto_data: Proyectos, db: Session = Depends(get_db)):
    try:
        # Crear el nuevo proyecto
        new_proyecto = proyecto(
            nombre=proyecto_data.nombre,
            direccion=proyecto_data.direccion,
            activo=proyecto_data.activo,
            created_at=datetime.now()
        )

        db.add(new_proyecto)  # Agregar el nuevo proyecto a la sesión
        db.commit()  # Confirmar la transacción
        db.refresh(new_proyecto)  # Sincronizar el objeto con la base de datos

        return new_proyecto

    except Exception as e:
        db.rollback()  # Revertir si ocurre un error
        raise HTTPException(status_code=400, detail=f"Error creando el proyecto: {str(e)}")
    
#por id
@user.get("/proyectos/{id_proyecto}", response_model=Proyectos, tags=["proyectos"]) #okkk
def get_proyecto(id_proyecto: int, db: Session = Depends(get_db)):
    try:
        proyecto_data = db.query(proyecto).filter(proyecto.id_proyecto == id_proyecto).first()

        if not proyecto_data:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")

        return proyecto_data

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener el proyecto: {str(e)}")


#all proyectos
@user.get("/proyectos/", response_model=List[Proyectos], tags=["proyectos"]) #okkk
def get_all_proyectos(db: Session = Depends(get_db)):
    try:
        proyectos = db.query(proyecto).all()  # Obtener todos los proyectos usando la sesión
        return proyectos

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener los proyectos: {str(e)}")

#actualizar 
@user.put("/proyectos/{id_proyecto}", response_model=Proyectos, tags=["proyectos"]) #okkk
def update_proyecto(id_proyecto: int, proyecto_update: Proyectos, db: Session = Depends(get_db)):
    try:
        # Realizar la actualización del proyecto
        stmt = db.query(proyecto).filter(proyecto.id_proyecto == id_proyecto).update({
            "nombre": proyecto_update.nombre,
            "direccion": proyecto_update.direccion,
            "activo": proyecto_update.activo
        })
        db.commit()  # Confirmar los cambios

        if stmt == 0:  # Si no se actualizó ningún proyecto, lanzamos un error
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")

        updated_proyecto = db.query(proyecto).filter(proyecto.id_proyecto == id_proyecto).first()
        return updated_proyecto

    except Exception as e:
        db.rollback()  # Revertir si ocurre un error
        raise HTTPException(status_code=400, detail=f"Error actualizando el proyecto: {str(e)}")


#delete
@user.delete("/proyectos/{id_proyecto}", tags=["proyectos"]) #okkk
def delete_proyecto(id_proyecto: int, db: Session = Depends(get_db)):
    try:
        proyecto_to_delete = db.query(proyecto).filter(proyecto.id_proyecto == id_proyecto).first()  # Buscar el proyecto a eliminar
        if proyecto_to_delete is None:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")
        
        db.delete(proyecto_to_delete)  # Eliminar el proyecto
        db.commit()  # Confirmar la transacción
        
        return {"message": f"Proyecto con id {id_proyecto} eliminado exitosamente"}

    except Exception as e:
        db.rollback()  # Revertir si ocurre un error
        raise HTTPException(status_code=400, detail=f"Error eliminando el proyecto: {str(e)}")


##################################################################################################################
#post gasolinera
#ok
@user.post("/gasolineras/", tags=["gasolineras"], response_model=Gasolinera, description="Create a new gas station") #okkk
def create_gasolinera(gasolinera_data: Gasolinera, db: Session = Depends(get_db)):
    try:
        # Crear la nueva gasolinera
        new_gasolinera = gasolineras(
            nombre=gasolinera_data.nombre,
            direccion=gasolinera_data.direccion,
            created_at=datetime.now()
        )
        
        db.add(new_gasolinera)  # Agregar la gasolinera a la sesión
        db.commit()  # Confirmar la transacción
        db.refresh(new_gasolinera)  # Sincronizar el objeto con la base de datos
        
        return new_gasolinera
    
    except Exception as e:
        db.rollback()  # Revertir si ocurre un error
        raise HTTPException(status_code=400, detail=str(e))
    
#leer gas
@user.get("/gasolineras/", response_model=List[Gasolinera], tags=["gasolineras"], description="Get all gas stations") #okkk
def get_all_gasolineras(db: Session = Depends(get_db)):
    try:
        result = db.query(gasolineras).all()  # Obtener todas las gasolineras usando la sesión
        return result
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
#gas por id
#okkkkkkk
@user.get("/gasolineras/{id_gasolinera}", response_model=Gasolinera, tags=["gasolineras"], description="Get a gas station by ID")
def get_gasolinera(id_gasolinera: int, db: Session = Depends(get_db)):
    try:
        gasolinera = db.query(gasolineras).filter(gasolineras.id_gasolinera == id_gasolinera).first()

        if not gasolinera:
            raise HTTPException(status_code=404, detail="Gasolinera not found")

        return gasolinera
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


#actualizar datos de gas
#ok
@user.put("/gasolineras/{id_gasolinera}", response_model=Gasolinera, tags=["gasolineras"], description="Update a gas station")
def update_gasolinera(id_gasolinera: int, gasolinera_data: Gasolinera, db: Session = Depends(get_db)):
    try:
        # Actualizar los datos de la gasolinera
        stmt = db.query(gasolineras).filter(gasolineras.id_gasolinera == id_gasolinera).update({
            "nombre": gasolinera_data.nombre,
            "direccion": gasolinera_data.direccion
        })
        db.commit()  # Confirmar los cambios

        if stmt == 0:  # Si no se actualizó ninguna gasolinera, lanzamos un error
            raise HTTPException(status_code=404, detail="Gasolinera not found")

        updated_gasolinera = db.query(gasolineras).filter(gasolineras.id_gasolinera == id_gasolinera).first()
        return updated_gasolinera

    except Exception as e:
        db.rollback()  # Revertir si ocurre un error
        raise HTTPException(status_code=400, detail=f"Error actualizando la gasolinera: {str(e)}")


#eliminar esta gas:
#ok
@user.delete("/gasolineras/{id_gasolinera}", tags=["gasolineras"], description="Delete a gas station")
def delete_gasolinera(id_gasolinera: int, db: Session = Depends(get_db)):
    try:
        gasolinera_to_delete = db.query(gasolineras).filter(gasolineras.id_gasolinera == id_gasolinera).first()  # Buscar la gasolinera a eliminar
        if gasolinera_to_delete is None:
            raise HTTPException(status_code=404, detail="Gasolinera no encontrada")
        
        db.delete(gasolinera_to_delete)  # Eliminar la gasolinera
        db.commit()  # Confirmar la transacción
        return {"message": "Gasolinera eliminada exitosamente"}
    
    except Exception as e:
        db.rollback()  # Revertir si ocurre un error
        raise HTTPException(status_code=400, detail=f"Error eliminando la gasolinera: {str(e)}")

