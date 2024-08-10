import os
import psycopg2
import rapidjson
from flask import Flask, request, Response
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
CREATE_MASTER_TABLE = (
    "CREATE TABLE IF NOT EXISTS master (id SERIAL PRIMARY KEY, title TEXT, company TEXT, location TEXT, date TIMESTAMP, link TEXT);" 
)
INSERT_JOB_MASTER = (
    "INSERT INTO master (title, company, location, date, link) VALUES (%s, %s, %s, %s, %s) RETURNING id;"
)

app = Flask(__name__)

def connect_to_db():
    connection = psycopg2.connect(DATABASE_URL)
    return connection

@app.route("/api/master", methods=["POST"])
def add_job_master():
    data = request.get_json()
    title = data["title"]
    company = data["company"]
    location = data["location"]
    date = data["date"]
    link = data["link"]
    connection = connect_to_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MASTER_TABLE)
            cursor.execute(INSERT_JOB_MASTER, (title, company, location, date, link))
    connection.close()
    cursor.close()
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
            "location": row[3],
            "date": row[4].strftime("%Y-%m-%d %H:%M:%S"),
            "link": row[5]
        })
    
    jobs_data = rapidjson.dumps(jobs_list)
    return jobs_data

if __name__ == '__main__':
    app.run(debug=True)
