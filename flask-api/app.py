import os
import psycopg2
import rapidjson
import cachetools
from flask import Flask, request, Response
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
CREATE_MASTER_TABLE = (
    "CREATE TABLE IF NOT EXISTS master (id SERIAL PRIMARY KEY, title TEXT, company TEXT, industry TEXT, location TEXT, date TIMESTAMP, link TEXT);" 
)
INSERT_JOB_MASTER = (
    "INSERT INTO master (title, company, industry, location, date, link) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"
)

app = Flask(__name__)

master_cache = cachetools.TTLCache(maxsize=7, ttl=604800)


def connect_to_db():
    connection = psycopg2.connect(DATABASE_URL)
    return connection

@app.route("/api/master", methods=["POST"])
def add_job_master():
    connection = connect_to_db()
    data = request.get_json()
    for row in data:
        title = row["title"]
        company = row["company"]
        industry = row["industry"]
        location = row["location"]
        date = row["date"]
        link = row["link"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_MASTER_TABLE)
                cursor.execute(INSERT_JOB_MASTER, (title, company, industry, location, date, link))
        cursor.close()
    connection.close()
    return Response("Job added successfully", status=200)


@app.route("/api/master", methods=["GET"])
def get_jobs_master():
    connection = connect_to_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM master")  # TODO: Optimize this to only select the newly added jobs and also reflect this optimization in the React
            rows = cursor.fetchall()
    connection.close()
    cursor.close()

    jobs_list = []
    for row in rows:
        jobs_list.append({
            "id": row[0],
            "title": row[1],
            "company": row[2],
            "industry": row[3],
            "location": row[4],
            "date": row[5].strftime('%m/%d/%Y'),
            "link": row[6]
        })
    return rapidjson.dumps(jobs_list)

@app.route("/api/master/cache", methods=["GET"])
def get_jobs_master_cache():
    cache_key = datetime.now().strftime('%m/%d/%Y')

    if cache_key in master_cache:
        return master_cache[cache_key]
    else:
        jobs_data = get_jobs_master()
        master_cache[cache_key] = jobs_data
        return jobs_data

if __name__ == '__main__':
    app.run(debug=True)
