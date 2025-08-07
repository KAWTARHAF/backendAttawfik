# backend/db_init.py

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def run_migration():
    try:
        with open("schema.sql", "r") as f:
            sql = f.read()

        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        print("✅ schema.sql executed successfully.")
    except Exception as e:
        print("❌ Error running schema.sql:", e)
