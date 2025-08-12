# backend/db_init.py

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """
    Create and return a new PostgreSQL connection.
    Uses DATABASE_URL from environment variables.
    """
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable not set.")
    
    return psycopg2.connect(DATABASE_URL)


def run_migration():
    """
    Run schema.sql to initialize or update the database schema.
    """
    try:
        with open("schema.sql", "r") as f:
            sql_content = f.read()

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql_content)
        conn.commit()
        cur.close()
        conn.close()
        print("✅ schema.sql executed successfully.")
    except Exception as e:
        print("❌ Error running schema.sql:", e)
