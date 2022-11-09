import torch
import whisper
import psycopg2
import tensorflow as tf
#import sys
import configparser 
from sentiment_analysis_spanish import sentiment_analysis

#archivo=sys.argv[1]
#config = configparser.ConfigParser()
#config.read("config.ini")
def transcribe(path, nom_archivo, fecha_grabacion):
    #model = whisper.load_model("large", device = "cpu")
    physical_devices = tf.config.experimental.list_physical_devices('GPU')
    for i in physical_devices:
        tf.config.experimental.set_memory_growth(i, True)
    print(f"PyTorch version: {torch.__version__}")
    # Check PyTorch has access to MPS (Metal Performance Shader, Apple's GPU architecture)
    print(f"Is MPS (Metal Performance Shader) built? {torch.backends.mps.is_built()}")
    print(f"Is MPS available? {torch.backends.mps.is_available()}")
    device_torch = torch.device('cuda')
    print(device_torch)
    # Set the device      
    device1 = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device1}")
    x = torch.rand(size=(5, 6)).to(device1)
    x
    model = whisper.load_model("large",device = "cpu")
    result = model.transcribe(path+"/"+nom_archivo, fp16=False)
    print(result["text"])
    print(fecha_grabacion)
    sentiment = sentiment_analysis.SentimentAnalysisSpanish()
    sentimiento=sentiment.sentiment(result["text"])
    print(sentimiento)
    guarda_log(nom_archivo, result["text"], sentimiento, fecha_grabacion)
def guarda_log(nom_archivo, transcripcion, tipo, fecha_grabacion):
    config = configparser.ConfigParser()
    config.read("config.ini")
    try:
        connection = psycopg2.connect(user=config["DEFAULT"]["DB_USER"],
                                  password=config["DEFAULT"]["DB_PASSWORD"],
                                  host=config["DEFAULT"]["DB_HOST"],
                                  port=config["DEFAULT"]["DB_PORT"],
                                  database=config["DEFAULT"]["DB_NAME"])
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO texto_analizado (archivo, contenido, tipo_comentario, fecha_grabacion) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (nom_archivo, transcripcion, tipo, fecha_grabacion)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)

    finally:
        # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
