from db import ensure_schema
from tasks import pridat_ukol, vypsat_ukoly, zmenit_stav_ukolu, odstranit_ukol

def pridat_ukol_ui():
    nazev = input("Zadejte název úkolu: ").strip()
    popis = input("Zadejte popis úkolu: ").strip()
    try:
        new_id = pridat_ukol(nazev, popis)
        print(f"Úkol byl přidán (ID: {new_id}).")
    except ValueError as e:
        print(f"Chyba: {e}")

def zobrazit_ukoly_ui():
    ukoly = vypsat_ukoly(filter_open_only=True)
    if not ukoly:
        print("Seznam úkolů je prázdný.")
        return
    for (id_, naz, pop, stav) in ukoly:
        print(f"{id_}: {naz} - {pop} [{stav}]")

def aktualizovat_ukol_ui():
    zobrazit_ukoly_ui()
    try:
        ukol_id = int(input("Zadejte ID úkolu pro aktualizaci: ").strip())
    except ValueError:
        print("Neplatné ID.")
        return
    novy_stav = input("Zadejte nový stav (Probíhá/Hotovo): ").strip()
    try:
        zmenit_stav_ukolu(ukol_id, novy_stav)
        print("Úkol byl aktualizován.")
    except ValueError as e:
        print(f"Chyba: {e}")
    except LookupError as e:
        print(f"Chyba: {e}")

def odstranit_ukol_ui():
    zobrazit_ukoly_ui()
    try:
        ukol_id = int(input("Zadejte ID úkolu pro odstranění: ").strip())
    except ValueError:
        print("Neplatné ID.")
        return
    try:
        odstranit_ukol(ukol_id)
        print("Úkol byl odstraněn.")
    except LookupError as e:
        print(f"Chyba: {e}")

def hlavni_menu():
    ensure_schema()
    while True:
        print("\n--- Správce úkolů ---")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit program")
        volba = input("Vyberte možnost (1-5): ").strip()
        if volba == "1":
            pridat_ukol_ui()
        elif volba == "2":
            zobrazit_ukoly_ui()
        elif volba == "3":
            aktualizovat_ukol_ui()
        elif volba == "4":
            odstranit_ukol_ui()
        elif volba == "5":
            print("Konec programu.")
            break
        else:
            print("Neplatná volba.")

if __name__ == "__main__":
    hlavni_menu()
