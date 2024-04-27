# chat conversation
import json
import pymysql
import requests
import http.client
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from itertools import cycle

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=["POST"])
@cross_origin()
def function(self):
    load_dotenv()
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_DDBB = os.getenv("DB_DDBB")
    #try:
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_DDBB)
    cursor = connection.cursor()

    print("conexión exitosa")
    id = request.json['id']

    sql = '''
            SELECT
            CONCAT(ua.nombre, ' ', ua.apellido) AS nombre_alumno,
            CONCAT(up.nombre, ' ', up.apellido) AS nombre_profesional,
            e.especialidad AS especialidad_profesional,
            ua.telefono AS telefono_estudiante,
            ua.email AS email_estudiante,
            c.fecha,
            c.hora,
            c.estado,
            c.id AS id_cita,
            up.id id_profesional,
            ua.id id_paciente
        FROM
            citas c
        JOIN
            usuarios up ON c.profesional_id = up.id
        JOIN
            usuarios ua ON c.alumno_id = ua.id
        JOIN
            especialidades e ON up.id = e.usuario_id
        WHERE
            c.profesional_id = '''+str(id)

    cursor.execute(sql)
    resp = cursor.fetchall()
    print(str(resp))

    arrayCitas=[]
    retorno = {
        "citas":{}
    }
    for registro in resp:
        item={
            "nombre_alumno":registro[0],
            "nombre_profesional":registro[1],
            "especialidad_profesional":registro[2],
            "telefono_estudiante":registro[3],
            "email_estudiante":registro[4],
            "fecha":str(registro[5]),
            "hora":str(registro[6]),
            "estado":registro[7],
            "id_cita":registro[8],
            "id_profesional":registro[9],
            "id_paciente":registro[10]
        }
        arrayCitas.append(item)
    retorno['citas'] = arrayCitas
    return retorno

    #except Exception as e:
    #    print('Error: '+ str(e))
    #    retorno = {           
    #        "detalle":"algo falló", 
    #        "validacion":False
    #    }
    #    return retorno

if __name__ == "__main__":
    app.run(debug=True, port=8002, ssl_context='adhoc')