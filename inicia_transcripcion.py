import sys
import os
import psycopg2
from trancribe2 import *
#recibe el directorio a analizar y el tipo de archivo que buscara
dir_path = sys.argv[1]
ext_buscada = sys.argv[2]
fecha_grabacion = sys.argv[3]
#guarda los archivos que analizara 
res = []

config = configparser.ConfigParser()
config.read("config.ini")

for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        root, extension = os.path.splitext(path)
        #valida que el tipo de archivo sea el buscado
        if extension==ext_buscada:
            res.append(path)
            # llama a la transcripción y almacenamiento en la base de datos

            try:
                connection = psycopg2.connect(user=config["DEFAULT"]["DB_USER"],
                                  password=config["DEFAULT"]["DB_PASSWORD"],
                                  host=config["DEFAULT"]["DB_HOST"],
                                  port=config["DEFAULT"]["DB_PORT"],
                                  database=config["DEFAULT"]["DB_NAME"])
                cursor = connection.cursor()

                query=""" select count(1) from texto_analizado where archivo= '%s' ;"""
                #existe_registro = (path)
                query_comp= (query % path)
                cursor.execute(query_comp)
                connection.commit()
                cuantos=cursor.fetchone()[0]
                print(cuantos)
                if cuantos==0:
                    transcribe(dir_path, path, fecha_grabacion)
                else:
                    print('Ya fue procesado')

            except (Exception, psycopg2.Error) as error:
                print("Error al buscar el registro", error, path)
            finally:
                # closing database connection.
                if connection:
                    cursor.close()
                    connection.close()
                    print("Conexion cerrada")
#print(res)
