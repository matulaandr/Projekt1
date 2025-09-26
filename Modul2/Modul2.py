import mysql.connector
from mysql.connector import Error

def pripojeni_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="martinaandraskova",
            database="task_manager"
        )
        return conn
    except Error as e:
        print(f"Chyba při připojení k databázi: {e}")
        return None

def vytvoreni_tabulky():
    conn = pripojeni_db()
    if conn:
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
        conn.close()

def pridat_ukol():
    nazev = input("Zadejte název úkolu: ").strip()
    popis = input("Zadejte popis úkolu: ").strip()
    if not nazev or not popis:
        print("Název i popis jsou povinné.")
        return
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", (nazev, popis))
        conn.commit()
        print("Úkol byl přidán.")
        cursor.close()
        conn.close()

def zobrazit_ukoly():
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nazev, popis, stav FROM ukoly WHERE stav IN ('Nezahájeno', 'Probíhá')")
        ukoly = cursor.fetchall()
        if not ukoly:
            print("Seznam úkolů je prázdný.")
        else:
            for u in ukoly:
                print(f"{u[0]}: {u[1]} - {u[2]} [{u[3]}]")
        cursor.close()
        conn.close()

def aktualizovat_ukol():
    zobrazit_ukoly()
    id_ukolu = input("Zadejte ID úkolu pro aktualizaci: ")
    novy_stav = input("Zadejte nový stav (Probíhá/Hotovo): ").strip()
    if novy_stav not in ["Probíhá", "Hotovo"]:
        print("Neplatný stav.")
        return
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ukoly WHERE id = %s", (id_ukolu,))
        if cursor.fetchone():
            cursor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (novy_stav, id_ukolu))
            conn.commit()
            print("Úkol byl aktualizován.")
        else:
            print("Úkol s tímto ID neexistuje.")
        cursor.close()
        conn.close()

def odstranit_ukol():
    zobrazit_ukoly()
    id_ukolu = input("Zadejte ID úkolu pro odstranění: ")
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ukoly WHERE id = %s", (id_ukolu,))
        if cursor.fetchone():
            cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
            conn.commit()
            print("Úkol byl odstraněn.")
        else:
            print("Úkol s tímto ID neexistuje.")
        cursor.close()
        conn.close()

def hlavni_menu():
    vytvoreni_tabulky()
    while True:
        print("\n--- Správce úkolů ---")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit program")
        volba = input("Vyberte možnost (1-5): ")
        if volba == "1":
            pridat_ukol()
        elif volba == "2":
            zobrazit_ukoly()
        elif volba == "3":
            aktualizovat_ukol()
        elif volba == "4":
            odstranit_ukol()
        elif volba == "5":
            print("Konec programu.")
            break
        else:
            print("Neplatná volba.")

# Spuštění programu
if __name__ == "__main__":
    hlavni_menu()
