from __future__ import print_function
from __main__ import app
from flask import request,session, render_template
from bd import obtener_conexion
import json
import sys
import bcrypt


@app.route("/",methods=['GET'])
def inicio():
  return render_template('raiz.html')

@app.route("/login",methods=['GET'])
def prelogin():
  return render_template('formulariologin.html')

@app.route("/main", methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        juego_json = request.json
        username = juego_json['username']
        password = juego_json['password']
    elif content_type == 'application/x-www-form-urlencoded':
        username = request.form['username']
        password = request.form['password']
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                # Consulta segura usando parámetros
                cursor.execute("SELECT clave FROM usuarios WHERE usuario = %s", (username,))
                usuario = cursor.fetchone()
            conexion.close()

            if usuario is None:
                # Usuario no encontrado
                ret = {"status": "ERROR", "mensaje": "Usuario/clave incorrectos"}
                code = 200
                return json.dumps(ret), code
            else:
                # Verificar si la contraseña coincide con el hash
                hashed_password = usuario[1]  # La contraseña está en la segunda columna
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    # Si la contraseña es correcta, renderiza la página principal
                    session["usuario"] = username
                    return render_template("main.html", username=username, actividades=get_actividades())
                else:
                    # Si la contraseña no coincide
                    ret = {"status": "ERROR", "mensaje": "Usuario/clave incorrectos"}
                    code = 200
                    return json.dumps(ret), code
        except Exception as e:
            print(f"Excepción al validar al usuario: {e}")
            ret = {"status": "ERROR"}
            code = 500
            return json.dumps(ret), code
    else:
        ret = {"status": "Bad request"}
        code = 401
        return json.dumps(ret), code


def get_actividades():
    return [
        {
            "nombre": "Levantamiento de peso muerto",
            "descripcion": "Ejercicio esencial para fuerza y estabilidad.",
            "imagen": "static/images/peso_muerto.jpg"
        },
        {
            "nombre": "Remo para espalda",
            "descripcion": "Fortalece la espalda y mejora la resistencia.",
            "imagen": "static/images/remo_espalda.jpeg"
        },
        {
            "nombre": "Clase de CrossFit",
            "descripcion": "Rutinas intensas para mejorar el acondicionamiento físico.",
            "imagen": "static/images/crossfit.jpeg"
        }
    ]

@app.route("/login", methods=['GET'])
def main():
    if "usuario" in session:
        return render_template("main.html", username=session["usuario"], actividades=get_actividades())
    else:
        return render_template("formulariologin.html", mensaje="Por favor, inicie sesión.")

@app.route("/preregistro",methods=['GET'])
def preregistro():
  return render_template('formularioregistro.html')


@app.route("/registro", methods=['POST'])
def registro():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        juego_json = request.json
        username = juego_json['username']
        password = juego_json['password']
        email = juego_json['email']
    elif content_type == 'application/x-www-form-urlencoded':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        try:
            # Hashear la contraseña antes de almacenarla
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            conexion = obtener_conexion()
            
            with conexion.cursor() as cursor:
                cursor.execute("SELECT usuario FROM usuarios WHERE usuario = %s", (username,))
                usuario = cursor.fetchone()
                 
                if usuario is None:
                    cursor.execute("INSERT INTO usuarios(usuario, clave, email) VALUES(%s, %s, %s)", (username, hashed_password, email))

                    if cursor.rowcount == 1:  
                        conexion.commit()
                        # Redirigir a la página de inicio de sesión después del registro exitoso
                        return redirect(url_for('prelogin'))  # Aquí redirige a /login
                    else:
                        ret = {"status": "ERROR"}
                        code = 500
                else:
                    ret = {"status": "ERROR", "mensaje": "Usuario ya existe"}
                    code = 200

            conexion.close()
        except Exception as e:
            print(f"Excepción al registrar al usuario: {e}")   
            ret = {"status": "ERROR"}
            code = 500
    else:
        ret = {"status": "Bad request"}
        code = 401
    
    return json.dumps(ret), code

from flask import redirect, url_for, make_response
@app.route("/logout", methods=['GET'])
def logout():
    session.clear()
    
    response = make_response(redirect(url_for("inicio")))  
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    
    return response

