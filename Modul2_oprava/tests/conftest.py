import os
import pytest
import mysql.connector

TEST_DB_NAME = "task_manager_test"

@pytest.fixture(scope="session", autouse=True)
def configure_test_db_env():
    """
    Přesměruje aplikaci na testovací DB.
    """
    os.environ["TASK_DB_NAME"] = TEST_DB_NAME
    os.environ["TASK_DB_HOST"] = os.getenv("TASK_DB_HOST", "localhost")
    os.environ["TASK_DB_USER"] = os.getenv("TASK_DB_USER", "root")
    os.environ["TASK_DB_PASS"] = os.getenv("TASK_DB_PASS", "martinaandraskova")

@pytest.fixture(scope="session")
def test_db_connection(configure_test_db_env):
    """
    Vytvoří testovací DB a tabulku, pokud neexistují.
    Vrací spojení pro případné přímé dotazy.
    """
    admin_conn = mysql.connector.connect(
        host=os.environ["TASK_DB_HOST"],
        user=os.environ["TASK_DB_USER"],
        password=os.environ["TASK_DB_PASS"]
    )
    admin_cursor = admin_conn.cursor()
    admin_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {TEST_DB_NAME}")
    admin_cursor.close()
    admin_conn.close()

    conn = mysql.connector.connect(
        host=os.environ["TASK_DB_HOST"],
        user=os.environ["TASK_DB_USER"],
        password=os.environ["TASK_DB_PASS"],
        database=TEST_DB_NAME
    )
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
    yield conn
    conn.close()

@pytest.fixture(autouse=True)
def clean_table(test_db_connection):
    """
    Před každým testem vyčistí tabulku ukoly, aby testy byly izolované.
    """
    cursor = test_db_connection.cursor()
    cursor.execute("TRUNCATE TABLE ukoly")
    test_db_connection.commit()
    cursor.close()
