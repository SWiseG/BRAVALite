import psycopg2
import os
from psycopg2 import OperationalError

DB_NAME = str(os.getenv('DB_NAME', 'brava_lite')).strip()
DB_USER = str(os.getenv('DB_USER', 'brava')).strip()
DB_PASSWORD = str(os.getenv('DB_PASSWORD', 'BRV2025DevOPS')).strip()
DB_HOST = str(os.getenv('DB_HOST', 'localhost')).strip()
DB_PORT = str(os.getenv('DB_PORT', '5432')).strip()

def connection_ping():
    try:
        print(f'Database PostegreeSQL connection BRAVA Lite Test Informations')
        print("="*60)
        print(f'DB_NAME {DB_NAME}')
        print(f'DB_USER {DB_USER}')
        print(f'DB_PASSWORD {DB_PASSWORD}')
        print(f'DB_HOST {DB_HOST}')
        print(f'DB_PORT {DB_PORT}')
        print("="*60)
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print("[SUCCESS] Connection is open and avaliable to use!")
        print("[INFO] PostgreSQL version:", db_version[0])
        cursor.close()
        connection.close()
    except OperationalError as e:
        print("[ERROR] Failed to open the current connection:")
        print(e)
    except Exception as e:
        print("[WARN] Failed, error to open connection:")
        print(e)

if __name__ == "__main__":
    connection_ping()
