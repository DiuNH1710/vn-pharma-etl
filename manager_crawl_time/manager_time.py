import psycopg2
from datetime import datetime

def get_last_crawl_time(job_name):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="123456",
        host="host.docker.internal",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("""
           CREATE TABLE IF NOT EXISTS manager_time (
               job_name TEXT PRIMARY KEY,
               last_crawl_time TIMESTAMP
           );
       """)

    cursor.execute("SELECT last_crawl_time FROM manager_time WHERE job_name = %s", (job_name,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0] if result else None


def update_last_crawl_time(job_name):
    now = datetime.now()
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="123456",
        host="host.docker.internal",
        port="5432"
    )
    cursor = conn.cursor()

    cursor.execute("""
           CREATE TABLE IF NOT EXISTS manager_time (
               job_name TEXT PRIMARY KEY,
               last_crawl_time TIMESTAMP
           );
       """)

    cursor.execute("""
        INSERT INTO manager_time (job_name, last_crawl_time)
        VALUES (%s, %s)
        ON CONFLICT (job_name)
        DO UPDATE SET last_crawl_time = EXCLUDED.last_crawl_time
    """, (job_name, now))

    conn.commit()
    cursor.close()
    conn.close()
