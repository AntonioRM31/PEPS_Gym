from __future__ import print_function
from __main__ import app
from flask import request, jsonify, session
import os
import json
import sys
from werkzeug.utils import secure_filename

# Configuración: tamaño máximo permitido (5 MB)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Obtener el archivo subido
        f = request.files['fichero']

        # Verificar que el archivo exista y sea una imagen por extensión
        if not (f and f.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))):
            return json.dumps({"status": "ERROR", "mensaje": "El archivo debe ser una imagen."}), 400

        # Verificar el tamaño del archivo
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        f.seek(0)  # Volver al inicio del archivo
        if file_size > MAX_FILE_SIZE:
            return json.dumps({"status": "ERROR", "mensaje": "El archivo es demasiado grande."}), 400

        # Definir la carpeta para guardar imágenes: static/uploads
        basepath = os.path.dirname(__file__)  # Ruta del archivo actual
        upload_folder = os.path.join(basepath, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)  # Crear carpeta si no existe

        # Borrar la imagen anterior si existe (almacenada en session['profile_image'])
        if 'profile_image' in session:
            old_image_url = session['profile_image']  # Ejemplo: "/static/uploads/Foto_Perfil2.jpg"
            # Convertir la URL en ruta absoluta
            old_image_path = os.path.join(basepath, old_image_url.lstrip("/"))
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
                print("Imagen anterior borrada: " + old_image_path, file=sys.stdout)

        # Contar cuántos archivos hay actualmente para generar un nombre nuevo
        files = os.listdir(upload_folder)
        n = len(files) + 1

        # Obtener la extensión del archivo original (incluye el punto)
        extension = os.path.splitext(f.filename)[1]

        # Generar el nombre automático, por ejemplo: "Foto_Perfil3.jpg"
        new_filename = f"Foto_Perfil{n}{extension}"
        new_filename = secure_filename(new_filename)

        # Ruta completa donde se guardará la imagen
        upload_path = os.path.join(upload_folder, new_filename)
        print('Guardando en: ' + upload_path, file=sys.stdout)

        # Guardar la imagen
        f.save(upload_path)

        # Generar la URL relativa (para mostrarla en el frontend)
        image_url = f"/apache/static/uploads/{new_filename}"

        # Guardar la URL de la imagen en la sesión para poder borrar la anterior en futuras subidas
        session['profile_image'] = image_url

        return json.dumps({"status": "OK", "image_url": image_url}), 200
    except Exception as e:
        print(f"Error al subir la imagen: {e}", file=sys.stdout)
        return json.dumps({"status": "ERROR"}), 500
