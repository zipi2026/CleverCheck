# db_connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

#from models.book import Base

# ← החלף את הפרמטרים לפי הגדרות SQL Server בבית הספר
SERVER   = 'D403-003'                  # שם השרת
DATABASE = 'CleverCheckDB'       # ← שם ה-DB שייצרי
DRIVER   = 'SQL Server'                 # Driver מהרשימה למטה

# SERVER   = 'localhost'
# DATABASE = 'CleverCheck_YourName'
# DRIVER   = 'SQL Server'

# יצירת connection string ל-SQL Server עם SQLAlchemy
engine = create_engine(
    f'mssql+pyodbc://{SERVER}/{DATABASE}'
    f'?driver={DRIVER.replace(" ", "+")}'
    f'&Trusted_Connection=yes'           # Windows auth, ללא סיסמה
)

# יצירת הטבלאות אוטומטית אם לא קיימות
#Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()

def health_check() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"DB connection failed: {e}")
        return False
# from sqlalchemy import create_engine, text
#
# engine = create_engine(
#     "mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
# )
#
# try:
#     with engine.connect() as conn:
#         conn.execute(text("SELECT 1"))
#     print("DB connected ✅")
# except Exception as e:
#     print("DB connection failed ❌", e)