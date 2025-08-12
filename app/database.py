import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/ai_project"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Migration ----------
def _read_sql_with_fallback(sql_path: Path) -> str:
    # essaie UTF-8, puis UTF-8-SIG, puis CP1252 (Windows)
    for enc in ("utf-8", "utf-8-sig", "cp1252"):
        try:
            return sql_path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    # dernier recours : remplacements permissifs
    return sql_path.read_bytes().decode("utf-8", errors="replace")

def run_migration():
    """Applique schema.sql s'il existe, sinon crée les tables ORM."""
    try:
        # Test de connexion d'abord
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("✅ Connexion à la base de données réussie.")
        
        sql_path = Path(__file__).resolve().parent.parent / "schema.sql"
        if sql_path.exists():
            sql = _read_sql_with_fallback(sql_path)
            # découpe simple sur ';' (OK pour un schéma basique)
            statements = [s.strip() for s in sql.split(';') if s.strip()]
            with engine.begin() as conn:
                for stmt in statements:
                    if stmt.strip():  # Ignore les lignes vides
                        conn.exec_driver_sql(stmt)
            print("✅ schema.sql appliqué.")
        else:
            # fallback ORM
            Base.metadata.create_all(bind=engine)
            print("✅ ORM create_all appliqué (pas de schema.sql).")
    except Exception as e:
        print(f"❌ Error running migration: {e}")
        print("⚠️ Le serveur continuera sans base de données.")
