import whisper
import psycopg2
import sys
import configparser 
from sentiment_analysis_spanish import sentiment_analysis

archivo=sys.argv[1]
config = configparser.ConfigParser()
config.read("config.ini")
#model = whisper.load_model("large", device = "gpu")
model = whisper.load_model("large")
result = model.transcribe(archivo, fp16=False)
print(result["text"])
sentiment = sentiment_analysis.SentimentAnalysisSpanish()
sentimiento=sentiment.sentiment(result["text"])
print(sentimiento)

try:
    connection = psycopg2.connect(user=config["DEFAULT"]["DB_USER"],
                                  password=config["DEFAULT"]["DB_PASSWORD"],
                                  host=config["DEFAULT"]["DB_HOST"],
                                  port=config["DEFAULT"]["DB_PORT"],
                                  database=config["DEFAULT"]["DB_NAME"])
    cursor = connection.cursor()

    postgres_insert_query = """ INSERT INTO texto_analizado ( archivo, contenido,tipo_comentario) VALUES (%s,%s,%s)"""
    record_to_insert = (archivo, result["text"],sentimiento)
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
