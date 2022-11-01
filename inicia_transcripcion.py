import sys
import os
from trancribe2 import *
#recibe el directorio a analizar y el tipo de archivo que buscara
dir_path = sys.argv[1]
ext_buscada = sys.argv[2]
fecha_grabacion = sys.argv[3]
#guarda los archivos que analizara 
res = []

for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        root, extension = os.path.splitext(path)
        #valida que el tipo de archivo sea el buscado
        if extension==ext_buscada:
            res.append(path)
            # llama a la transcripción y almacenamiento en la base de datos
            transcribe(dir_path, path, fecha_grabacion)

#print(res)
