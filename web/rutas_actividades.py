from flask import request, make_response, jsonify
import json
from __main__ import app
import controlador_actividades
from funciones_auxiliares import Encoder, sanitize_input, validar_session_normal, validar_session_admin
from werkzeug.utils import secure_filename
import os

# Configuración para subir imágenes
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/actividades", methods=["GET"])
def actividades():
    if validar_session_normal():
        actividades, code = controlador_actividades.obtener_actividades()
        return jsonify(actividades), code
    else:
        return jsonify({"status": "Forbidden"}), 403


@app.route("/actividades/<int:id>", methods=["GET"])
def actividad_por_id(id):
    if validar_session_normal():
        respuesta, code = controlador_actividades.obtener_actividad_por_id(id)
    else:
        respuesta = {"status": "Forbidden"}
        code = 403
    return jsonify(respuesta), code

@app.route("/actividades", methods=["POST"])
def guardar_actividad():
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    imagen_file = request.files.get("imagen")
    
    # Guardar imagen
    if imagen_file:
        filename = secure_filename(imagen_file.filename)
        imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        imagen_file.save(imagen_path)
        imagen_url = f"http://localhost:6104/images/{filename}"
    else:
        imagen_url = ""
    
    if validar_session_normal():
        respuesta, code = controlador_actividades.insertar_actividad(nombre, descripcion, imagen_url)
    else:
        respuesta = {"status": "Forbidden"}
        code = 403
    
    return jsonify(respuesta), code

@app.route("/actividades/<int:id>", methods=["PUT"])
def actualizar_actividad(id):
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    imagen_file = request.files.get("imagen")
    
    # Actualizar imagen si se envía
    if imagen_file:
        filename = secure_filename(imagen_file.filename)
        imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        imagen_file.save(imagen_path)
        imagen_url = f"http://localhost:6104/images/{filename}"
    else:
        imagen_url = request.form.get("imagen", "")
    
    if validar_session_normal():
        respuesta, code = controlador_actividades.actualizar_actividad(id, nombre, descripcion, imagen_url)
    else:
        respuesta = {"status": "Forbidden"}
        code = 403
    
    return jsonify(respuesta), code

@app.route("/actividades/<int:id>", methods=["DELETE"])
def eliminar_actividad_delete(id):
    if validar_session_normal():
        respuesta, code = controlador_actividades.eliminar_actividad(id)
    else:
        respuesta = {"status": "Forbidden"}
        code = 403
    return jsonify(respuesta), code