"""
db_connection.py — חיבור SQLAlchemy ל-SQL Server
"""
import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from models.models import Base

logger = logging.getLogger(__name__)

# ── הרכבת Connection String ──────────────────────────────────
_SERVER   = os.getenv('DB_SERVER',   r'localhost\SQLEXPRESS')
_DATABASE = os.getenv('DB_NAME',     'CleverCheckDB')
_DRIVER   = os.getenv('DB_DRIVER',   'ODBC+Driver+17+for+SQL+Server')

DATABASE_URL = (
    f"mssql+pyodbc://@{_SERVER}/{_DATABASE}"
    f"?driver={_DRIVER}&Trusted_Connection=yes"
)

# ── Engine ───────────────────────────────────────────────────
engine = create_engine(
    DATABASE_URL,
    echo=False,              # True → הדפסת SQL לדיבוג
    pool_pre_ping=True,      # בדיקת חיות חיבור לפני שימוש
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db() -> None:
    """יצירת טבלאות אם לא קיימות (Dev/Test בלבד — בפרודקשן: Alembic)."""
    logger.info("Initializing database schema...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database ready.")


def get_db() -> Session:
    """
    Generator לשימוש עם Dependency Injection (Flask / pytest).
    סוגר את ה-session בסיום הבקשה.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def health_check() -> bool:
    """בדיקת תקינות חיבור — משמש ב-/health endpoint."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        logger.error(f"DB health check failed: {exc}")
        return False



