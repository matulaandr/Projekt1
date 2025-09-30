import os
import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager

# Načtení konfigurace z prostředí (umožní přepínat produkční/testovací DB)
DB_HOST = os.getenv("TASK_DB_HOST", "localhost")
DB_USER = os.getenv("TASK_DB_USER", "root")
DB_PASS = os.getenv("TASK_DB_PASS", "martinaandraskova")
DB_NAME = os.getenv("TASK_DB_NAME", "task_manager")

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

def ensure_schema():
    """Vytvoří tabulku ukoly, pokud neexistuje."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(255) NOT NULL,
                popis TEXT NOT NULL,
                stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
                datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
    except Error as e:
        print(f"Chyba při zajištění schématu: {e}")
    finally:
        if conn:
            conn.close()

@contextmanager
def db_cursor():
    """
    Kontextový manager: vrátí (conn, cursor) a zajistí commit/uzavření.
    Použití:
        with db_cursor() as (conn, cursor):
            cursor.execute(...)
            conn.commit()  # commit lze vynechat, proběhne i v finally
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield conn, cursor
        conn.commit()
    finally:
        cursor.close()
        conn.close()
