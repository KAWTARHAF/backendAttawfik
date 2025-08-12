# backend/db_init.py

import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def _read_schema_file(schema_path: Path) -> str:
    # Try a few encodings; fall back to ignoring undecodable bytes to avoid startup crashes
    candidate_encodings = ("utf-8", "utf-8-sig", "cp1252", "latin-1")
    for encoding in candidate_encodings:
        try:
            with open(schema_path, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    # Final attempt: read bytes and decode with utf-8 replacing invalid bytes
    with open(schema_path, "rb") as f:
        return f.read().decode("utf-8", errors="replace")


def run_migration():
    try:
        schema_path = Path(__file__).with_name("schema.sql")
        if not schema_path.exists():
            print(f"⚠️ schema.sql not found at {schema_path}")
            return

        sql = _read_schema_file(schema_path)

        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("⚠️ DATABASE_URL is not set. Skipping migration.")
            return

        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        print("✅ schema.sql executed successfully.")
    except Exception as e:
        print("❌ Error running schema.sql:", e)
