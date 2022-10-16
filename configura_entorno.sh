#/bin/sh
pip3 install  git+https://github.com/openai/whisper.git -q
brew  install ffmpeg
pip3 install psycopg2-binary
#genera ambiente virtual
python3 -m venv tu_carpeta

#activa ambiente virtual
source tu_carpeta/bin/activate

pip3 install sentiment-analysis-spanish
pip3 install keras 
python -m pip install tensorflow-macos
pip3 install sklearn

#generar el archivo de requerimientos
pip freeze > requirements.txt
