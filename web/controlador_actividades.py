# controlador_actividades.py
from bd import obtener_conexion
from __main__ import app
from funciones_auxiliares import sanitize_input

def insertar_actividad(nombre, descripcion, imagen):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO actividades(nombre, descripcion, imagen) VALUES (%s, %s, %s)",
                           (nombre, descripcion, imagen))
            ret = {"status": "OK"} if cursor.rowcount == 1 else {"status": "Failure"}
        conexion.commit()
        conexion.close()
        code = 200
    except Exception as e:
        app.logger.info("Excepción al insertar una actividad: %s", e)
        ret = {"status": "Failure"}
        code = 500
    return ret, code

def convertir_actividad_a_json(actividad):
    return {
        'id': actividad[0],
        'nombre': sanitize_input(actividad[1]),
        'descripcion': sanitize_input(actividad[2]),
        'imagen': sanitize_input(actividad[3])
    }

def obtener_actividades():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, imagen FROM actividades")
            actividades = cursor.fetchall()
            actividadesjson = []
            if actividades:
                for actividad in actividades:
                    actividadesjson.append(convertir_actividad_a_json(actividad))
        conexion.close()
        code=200
    except:
        app.logger.info("Excepcion al obtener las actividades")
        actividadesjson=[]
    return actividadesjson


def obtener_actividad_por_id(id):
    actividadjson = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, imagen FROM actividades WHERE id = %s LIMIT 1", (id,))
            actividad = cursor.fetchone()
            if actividad:
                actividadjson = convertir_actividad_a_json(actividad)
        conexion.close()
        code = 200
    except Exception as e:
        app.logger.info("Excepción al consultar una actividad: %s", e)
        code = 500
    return actividadjson, code

def actualizar_actividad(id, nombre, descripcion, imagen):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE actividades SET nombre = %s, descripcion = %s, imagen = %s WHERE id = %s",
                           (nombre, descripcion, imagen, id))
            ret = {"status": "OK"} if cursor.rowcount == 1 else {"status": "Failure"}
        conexion.commit()
        conexion.close()
        code = 200
    except Exception as e:
        app.logger.info("Excepción al actualizar una actividad: %s", e)
        ret = {"status": "Failure"}
        code = 500
    return ret, code

def eliminar_actividad(id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM actividades WHERE id = %s", (id,))
            ret = {"status": "OK"} if cursor.rowcount == 1 else {"status": "Failure"}
        conexion.commit()
        conexion.close()
        code = 200
    except Exception as e:
        app.logger.info("Excepción al eliminar una actividad: %s", e)
        ret = {"status": "Failure"}
        code = 500
    return ret, code
