import psycopg2, os
from movie_utils import extract_name, extract_year, extract_languages, extract_quality, extract_file_size, extract_mini_languages, determine_resolution
import json


#port = 15672

#Establish a connection
try:
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    print("Connection established successfully")
    # Create a cursor
    cur = conn.cursor()

    # do something here
    cur.execute("""CREATE TABLE IF NOT EXISTS movie (
                id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                name VARCHAR(255),
                year INT,
                languages TEXT[],
                quality TEXT,
                file_size TEXT,
                magnet_link TEXT
                )"""
    )

    BASE = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE, "../crawler/tamilblasters_home_page.jsonl")

    with open(file_path, "r") as f:
        for line in f:
            #make the line a json object
            line = json.loads(line)
            #extract the data from the json object
            name = extract_name(line["title"])
            year = extract_year(line["title"])
            languages = extract_languages(line["title"])
            quality = extract_quality(line["title"])
            file_size = extract_file_size(line["title"])
            if file_size == None:
                file_size = "0"
            if quality == None:
                quality = determine_resolution(file_size)

            mini_languages = extract_mini_languages(line["title"])
            if mini_languages.__len__() > languages.__len__():
                languages = mini_languages
            #insert the data into the database
            cur.execute("INSERT INTO movie (name, year, languages, quality, file_size, magnet_link) VALUES ( %s, %s, %s, %s, %s, %s)", ( name, year, languages, quality, file_size, line["magnet_link"]))
            conn.commit()

    # close the cursor
    cur.close()
    print("Changes committed successfully")
    # close the connection
    conn.close()

except psycopg2.Error as e:
    print("Error connecting to PostgreSQL database:", e)
