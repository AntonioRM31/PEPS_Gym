from __future__ import print_function
from __main__ import app
from flask import request,session, render_template, render_template_string, jsonify
from bd import obtener_conexion
import json
import sys
import os
import bcrypt
from controlador_actividades import obtener_actividades
from funciones_auxiliares import sanitize_input
from werkzeug.utils import secure_filename



@app.route("/", methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/x-www-form-urlencoded':
        username = sanitize_input(request.form['username'])
        password = sanitize_input(request.form['password'])
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT usuario, clave FROM usuarios WHERE usuario = %s", (username,))
                usuario = cursor.fetchone()
            conexion.close()
            
            if usuario is None or usuario[1] is None:  # ✅ Verificar hash no nulo
                return json.dumps({"status": "ERROR", "mensaje": "Usuario/clave incorrectos"}), 200
            
            if usuario is not None:
             hashed_password = usuario[1]  # Obtener el hash de la BD
             if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                session["usuario"] = username
                return redirect('/api/menu')
            else:
                return json.dumps({"status": "ERROR", "mensaje": "Usuario/clave incorrectos"}), 200
                
        except Exception as e:
            return json.dumps({"status": "ERROR", "mensaje": f"Excepción: {e}"}), 500
    else:
        return json.dumps({"status": "Bad request"}), 401

@app.route("/registro", methods=['POST'])
def registro():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/x-www-form-urlencoded':
        username = sanitize_input(request.form['username'])
        password = sanitize_input(request.form['password'])
        email = sanitize_input(request.form['email'])
        try:
            # Hashear la contraseña antes de almacenarla
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            conexion = obtener_conexion()
            
            with conexion.cursor() as cursor:
                cursor.execute("SELECT usuario, clave FROM usuarios WHERE usuario = %s", (username,))  
                usuario = cursor.fetchone()
                 
                if usuario is None:
                    cursor.execute("INSERT INTO usuarios(usuario, clave, email) VALUES(%s, %s, %s)", (username, hashed_password, email))

                    if cursor.rowcount == 1:  
                        conexion.commit()
                        # Redirigir a la página de inicio de sesión después del registro exitoso
                        return redirect("../templates/formulariologin.html")
                    else:
                        ret = {"status": "ERROR"}
                        code = 500
                else:
                    ret = {"status": "ERROR", "mensaje": "Usuario ya existe"}
                    code = 200

            conexion.close()
        except Exception as e:
            mensajeerror = (f"Excepción al registrar al usuario: {e}")   
            ret = {"status": "ERROR", "mensaje": f"{mensajeerror}"}
            code = 500
    else:
        ret = {"status": "Bad request"}
        code = 401
    
    return json.dumps(ret), code

@app.route("/menu", methods=['GET'])
def menu():
    if 'usuario' not in session:
        return redirect("../templates/formulariologin.html")
    else:
        username = session['usuario']
        return render_template("main.html", username=username, actividades=obtener_actividades())


@app.route('/eliminar', methods=['POST'])
def eliminar():
    if 'usuario' not in session:
        return redirect("../templates/formulariologin.html")
    else:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/x-www-form-urlencoded':
            id = sanitize_input(request.form['id'])
            try:
                conexion = obtener_conexion()
                with conexion.cursor() as cursor:
                    cursor.execute("DELETE FROM actividades WHERE id = %s", (id,))
                    conexion.commit()
                conexion.close()
                return redirect('/api/menu')

            except Exception as e:
                return json.dumps({"status": "ERROR", "mensaje": f"Excepción: {e}"}), 500
        else:
            return json.dumps({"status": "Bad request"}), 401


@app.route('/editar', methods=['POST'])
def editar():
    if 'usuario' not in session:
        return redirect("../templates/formulariologin.html")
    else:
        content_type = request.headers.get('Content-Type', '')
        if 'application/x-www-form-urlencoded' in content_type or 'multipart/form-data' in content_type:
            id = sanitize_input(request.form.get('id'))
            nuevo_nombre = sanitize_input(request.form.get('nombre'))
            nueva_descripcion = sanitize_input(request.form.get('descripcion'))
            if request.files.get('imagen'):
                imagen = request.files.get('imagen')
            else:
                imagen = "1"
            
            try:
                # Validar imagen
                if imagen != "1" and allowed_file(imagen.filename):
                    tamanio_max = 5 * 1024 * 1024 # 5MB DE LÍMITE
                    tamanio_imagen = len(imagen.read())
                    if tamanio_imagen <= tamanio_max:
                        imagen.seek(0)
                        filename = secure_filename(imagen.filename)
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        imagen.save(filepath)
                        # Guardar en base de datos (solo la ruta)
                        ruta_imagen = f"../images/{filename}"  # Ruta relativa

                        conexion = obtener_conexion()
                        with conexion.cursor() as cursor:
                            cursor.execute("UPDATE actividades SET nombre = %s, descripcion = %s, imagen = %s WHERE id = %s",(nuevo_nombre, nueva_descripcion, ruta_imagen, id,))
                            conexion.commit()
                        conexion.close()
                        return redirect('/api/menu')
                    else:
                        return "La imagen excede el tamaño máximo permitido de 5 MB.", 400
                    
                conexion = obtener_conexion()
                with conexion.cursor() as cursor:
                    cursor.execute("UPDATE actividades SET nombre = %s, descripcion = %s WHERE id = %s",(nuevo_nombre, nueva_descripcion, id,))
                    conexion.commit()
                conexion.close()
                return redirect('/api/menu')
            except Exception as e:
                return json.dumps({"status": "ERROR", "mensaje": f"Excepción: {e}"}), 500
        else:
            return json.dumps({"status": "Bad request"}), 401


# Configuración
UPLOAD_FOLDER = 'apache/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear carpeta si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/insertar_actividad', methods=['POST'])
def insertar_actividad():
    try:
            # Obtener datos del formulario
            nombre = sanitize_input(request.form['nombre'])
            descripcion = sanitize_input(request.form['descripcion'])
            if request.files.get('imagen'):
                imagen = request.files.get('imagen')
            else:
                return "Debes incluir una foto en la actividad.", 500

            # Validar imagen
            if imagen and allowed_file(imagen.filename):
                tamanio_max = 5 * 1024 * 1024 # 5MB DE LÍMITE
                tamanio_imagen = len(imagen.read())
                if tamanio_imagen <= tamanio_max:
                    imagen.seek(0)
                    filename = secure_filename(imagen.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    imagen.save(filepath)
                    # Guardar en base de datos (solo la ruta)
                    ruta_imagen = f"../images/{filename}"  # Ruta relativa

                    conexion = obtener_conexion()
                    with conexion.cursor() as cursor:
                        cursor.execute("INSERT INTO actividades (nombre, descripcion, imagen) VALUES(%s, %s, %s)", (nombre, descripcion, ruta_imagen))
                    conexion.commit()

                    return redirect('/api/menu')  # Redirige a una página de éxito
                else:
                    return "La imagen excede el tamaño máximo permitido de 5 MB.", 400
            else:
                return "Tipo de archivo no permitido", 400

    except Exception as e:
        return f"Error: {str(e)}", 500
    

from flask import redirect, url_for, make_response
@app.route("/logout", methods=['POST'])
def logout():
    session.clear()
    
    response = make_response(redirect("/"))  
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
