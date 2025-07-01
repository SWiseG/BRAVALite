import psycopg2
from psycopg2 import sql
import os

DB_NAME = str(os.getenv('DB_NAME', 'brava_lite')).strip()
DB_USER = str(os.getenv('DB_USER', 'brava')).strip()
DB_PASSWORD = str(os.getenv('DB_PASSWORD', 'BRV2025DevOPS')).strip()
DB_HOST = str(os.getenv('DB_HOST', 'localhost')).strip()
DB_PORT = str(os.getenv('DB_PORT', '5432')).strip()

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

def connection_clear():
    cur = conn.cursor()
    cur.execute("""
        SELECT table_schema, table_name, column_name
        FROM information_schema.columns
        WHERE data_type IN ('text', 'character varying')
        AND table_schema NOT IN ('information_schema', 'pg_catalog');
    """)

    colunas = cur.fetchall()

    print(f"🔍 Verify {len(colunas)} columns...")

    for schema, tabela, coluna in colunas:
        query = sql.SQL("SELECT {coluna} FROM {schema}.{tabela} LIMIT 1000").format(
            coluna=sql.Identifier(coluna),
            schema=sql.Identifier(schema),
            tabela=sql.Identifier(tabela)
        )

        try:
            cur.execute(query)
            for linha in cur.fetchall():
                valor = linha[0]
                if valor is not None:
                    try:
                        valor.encode('utf-8').decode('utf-8')
                    except UnicodeDecodeError:
                        print(f"[ERROR] Error encoding: {schema}.{tabela}.{coluna} ➜ Value with problemn: {repr(valor)}")
        except Exception as e:
            print(f"[WARN] Error to verify {schema}.{tabela}.{coluna}: {e}")

    cur.close()

if __name__ == "__main__":
    try:
        connection_clear()
    finally:
        conn.close()
