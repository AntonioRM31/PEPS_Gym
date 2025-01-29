from __future__ import print_function
from __main__ import app
from flask import request,session, render_template
from bd import obtener_conexion
import json
import sys

@app.route("/main",methods=['GET'])
def inicio():
  return render_template('raiz.html')

@app.route("/prelogin",methods=['GET'])
def prelogin():
  return render_template('formulariologin.html')

@app.route("/login", methods=['POST'])
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
                cursor.execute("SELECT perfil FROM usuarios WHERE usuario = %s AND clave = %s", (username, password))
                usuario = cursor.fetchone()
            conexion.close()

            if usuario is None:
                # Usuario no encontrado
                ret = {"status": "ERROR", "mensaje": "Usuario/clave incorrectos"}
                code = 200
                return json.dumps(ret), code
            else:
                # Usuario válido, renderiza la página principal
                session["usuario"] = username
                session["perfil"] = usuario[0]
                return render_template("main.html", username=username, perfil=usuario[0], productos=get_productos())
        except Exception as e:
            print(f"Excepción al validar al usuario: {e}")
            ret = {"status": "ERROR"}
            code = 500
            return json.dumps(ret), code
    else:
        ret = {"status": "Bad request"}
        code = 401
        return json.dumps(ret), code


def get_productos():
    return [
        {
            "nombre": "Bicicleta de montaña",
            "descripcion": "Bicicleta en excelente estado, perfecta para rutas de montaña.",
            "precio": 120.99,
            "imagen": "https://via.placeholder.com/300x200?text=Bicicleta"
        },
        {
            "nombre": "Teléfono móvil",
            "descripcion": "Teléfono con pantalla OLED, 128GB de almacenamiento.",
            "precio": 250.50,
            "imagen": "https://cdn.tmobile.com/content/dam/t-mobile/en-p/cell-phones/apple/Apple-iPhone-16-Pro/Desert-Titanium/Apple-iPhone-16-Pro-Desert-Titanium-thumbnail.png"
        },
        {
            "nombre": "Silla ergonómica",
            "descripcion": "Silla ergonómica para oficina, ideal para largas jornadas.",
            "precio": 85.75,
            "imagen": "https://via.placeholder.com/300x200?text=Silla"
        }
    ]

@app.route("/main", methods=['GET'])
def main():
    if "usuario" in session:
        return render_template("main.html", username=session["usuario"], perfil=session["perfil"], productos=get_productos())
    else:
        return render_template("formulariologin.html", mensaje="Por favor, inicie sesión.")

@app.route("/preregistro",methods=['GET'])
def preregistro():
  return render_template('formularioregistro.html')

@app.route("/registro",methods=['POST'])
def registro():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        juego_json = request.json
        username = juego_json['username']
        password = juego_json['password']
        perfil = juego_json['profile']
    elif content_type == 'application/x-www-form-urlencoded':
        username = request.form['username']
        password = request.form['password']
        perfil = request.form['profile']
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                 #cursor.execute("SELECT perfil FROM usuarios WHERE usuario = %s and clave= %s",(username,password))
                 cursor.execute("SELECT perfil FROM usuarios WHERE usuario = '" + username +"' and clave= '" + password + "'")
                 usuario = cursor.fetchone()
                 if usuario is None:
                     print("INSERT INTO usuarios(usuario,clave,perfil) VALUES('"+ username +"','"+  password+"','"+ perfil+"')") 
                     cursor.execute("INSERT INTO usuarios(usuario,clave,perfil) VALUES('"+ username +"','"+  password+"','"+ perfil+"')")
                     if cursor.rowcount == 1:
                         conexion.commit()
                         ret={"status": "OK" }
                         code=200
                     else:
                         ret={"status": "ERROR" }
                         code=500
                 else:
                   ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo" }
                   code=200
            conexion.close()
        except:
            print("Excepcion al registrar al usuario")   
            ret={"status":"ERROR"}
            code=500
    else:
        ret={"status":"Bad request"}
        code=401
    return json.dumps(ret), code

from flask import redirect, url_for
@app.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for("prelogin"))  # Redirige al formulario de login

