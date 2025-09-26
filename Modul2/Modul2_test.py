import pytest
import mysql.connector
from datetime import datetime

# Pomocná funkce pro připojení k testovací DB
def pripojeni_test_db():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="martinaandraskova",
        database="task_manager"
    )

# Testy pro pridat_ukol()
def test_pridat_ukol_pozitivni():
    conn = pripojeni_test_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ("Testovací úkol", "Popis"))
    conn.commit()
    cursor.execute("SELECT * FROM ukoly WHERE nazev = %s", ("Testovací úkol",))
    result = cursor.fetchone()
    assert result is not None
    cursor.execute("DELETE FROM ukoly WHERE nazev = %s", ("Testovací úkol",))
    conn.commit()
    cursor.close()
    conn.close()

def test_pridat_ukol_negativni():
    conn = pripojeni_test_db()
    cursor = conn.cursor()
    with pytest.raises(mysql.connector.errors.DataError):
        cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ("", ""))
        conn.commit()
    cursor.close()
    conn.close()

# Testy pro aktualizovat_ukol()
def test_aktualizovat_ukol_pozitivni():
    conn = pripojeni_test_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ("Aktualizace", "Test"))
    conn.commit()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Aktualizace",))
    id_ukolu = cursor.fetchone()[0]
    cursor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", ("Hotovo", id_ukolu))
    conn.commit()
    cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (id_ukolu,))
    stav = cursor.fetchone()[0]
    assert stav == "Hotovo"
    cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
    conn.commit()
    cursor.close()
    conn.close()

def test_aktualizovat_ukol_negativni():
    conn = pripojeni_test_db()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM ukoly")
    max_id = cursor.fetchone()[0] or 0
    neexistujici_id = max_id + 100
    cursor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", ("Hotovo", neexistujici_id))
    conn.commit()
    cursor.execute("SELECT * FROM ukoly WHERE id = %s", (neexistujici_id,))
    result = cursor.fetchone()
    assert result is None
    cursor.close()
    conn.close()

# Testy pro odstranit_ukol()
def test_odstranit_ukol_pozitivni():
    conn = pripojeni_test_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ("Odstranit", "Test"))
    conn.commit()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Odstranit",))
    id_ukolu = cursor.fetchone()[0]
    cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
    conn