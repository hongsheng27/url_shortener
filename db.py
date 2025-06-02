import os
import psycopg2
from datetime import datetime

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "shorturl"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        host=os.getenv("DB_HOST", "localhost"), 
        port=os.getenv("DB_PORT", 5432)
    )

def insert_url(long_url:str, short_code: str):
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute("""
        INSERT INTO urls (long_url, short_code, created_at)
        VALUES (%s, %s, %s)
      """, (long_url, short_code, datetime.now()))
      conn.commit()
      cursor.close()
      
def get_url_by_code(code: str) -> str | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT long_url FROM urls WHERE short_code = %s", (code,))
    result = cursor.fetchone()
    print(result)
    conn.close()
    return result[0] if result else None

def get_code_by_long_url(long_url: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT short_code FROM urls WHERE long_url = %s", (long_url,))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None