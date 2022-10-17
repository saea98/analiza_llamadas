# analiza_llamadas
Renombra config.ini.ejemplo por config.ini

#para instalar el ambiente de desarrollo puedes usar el archivo 
configura_entorno.sh

# recuerda generar tu venv
python3 -m venv tu_carpeta

#activa ambiente virtual
source tu_carpeta/bin/activate

#para instalar las librerias del proyecto puedes usar 
pip3 install -r requirements.txt

Para ejecutar el analisis se usa el archivo inicia_transcripcion.py

inicia_transcripcion.py /directorio/de/archivos tipo_de_archivo

#ejemplo busca en el directorio ./grabaciones los archivos de tipo .wav

inicia_transcripcion.py  ./grabaciones  .wav
