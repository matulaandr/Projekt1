from typing import List, Tuple, Optional
from db import db_cursor

ALLOWED_STATUSES = ("Nezahájeno", "Probíhá", "Hotovo")

def pridat_ukol(nazev: str, popis: str) -> int:
    """Business logika pro vložení — vyhazuje ValueError při neplatném vstupu. Vrací ID záznamu."""
    if not nazev or not nazev.strip():
        raise ValueError("Název je povinný.")
    if not popis or not popis.strip():
        raise ValueError("Popis je povinný.")
    with db_cursor() as (conn, cursor):
        cursor.execute(
            "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)",
            (nazev.strip(), popis.strip())
        )
        return cursor.lastrowid

def vypsat_ukoly(filter_open_only: bool = True) -> List[Tuple[int, str, str, str]]:
    """Vrátí seznam úkolů: (id, nazev, popis, stav). Pokud filter_open_only=True, vrací jen Nezahájeno/Probíhá."""
    query = "SELECT id, nazev, popis, stav FROM ukoly"
    params: Tuple = tuple()
    if filter_open_only:
        query += " WHERE stav IN ('Nezahájeno', 'Probíhá')"
    with db_cursor() as (conn, cursor):
        cursor.execute(query, params)
        return list(cursor.fetchall())

def zmenit_stav_ukolu(ukol_id: int, novy_stav: str) -> None:
    """Aktualizace stavu. Vyhazuje ValueError pro neplatný stav a LookupError pro neexistující ID."""
    if novy_stav not in ALLOWED_STATUSES:
        raise ValueError("Neplatný stav.")
    with db_cursor() as (conn, cursor):
        cursor.execute("SELECT id FROM ukoly WHERE id = %s", (ukol_id,))
        row = cursor.fetchone()
        if not row:
            raise LookupError("Úkol s tímto ID neexistuje.")
        cursor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (novy_stav, ukol_id))

def odstranit_ukol(ukol_id: int) -> None:
    """Odstranění úkolu. Vyhazuje LookupError pro neexistující ID."""
    with db_cursor() as (conn, cursor):
        cursor.execute("SELECT id FROM ukoly WHERE id = %s", (ukol_id,))
        row = cursor.fetchone()
        if not row:
            raise LookupError("Úkol s tímto ID neexistuje.")
        cursor.execute("DELETE FROM ukoly WHERE id = %s", (ukol_id,))
