import whisper
import psycopg2
#import sys
import configparser 
from sentiment_analysis_spanish import sentiment_analysis

#archivo=sys.argv[1]
#config = configparser.ConfigParser()
#config.read("config.ini")
def transcribe(path, nom_archivo, fecha_grabacion):
    model = whisper.load_model("large", device = "cpu")
    #model = whisper.load_model("large")
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
