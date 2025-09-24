ukoly = []

def hlavni_menu():
    while True:
        print("\nSprávce úkolů - Hlavní menu")
        print("1. Přidat nový úkol")
        print("2. Zobrazit všechny úkoly")
        print("3. Odstranit úkol")
        print("4. Konec programu")
        volba = input("Vyberte možnost (1-4): ")

        if volba == "1":
            pridat_ukol()
        elif volba == "2":
            zobrazit_ukoly()
        elif volba == "3":
            odstranit_ukol()
        elif volba == "4":
            print("Konec programu.")
            break
        else:
            print("Neplatná volba. Zkuste to znovu.")

def pridat_ukol():
    while True:
        nazev = input("Zadejte název úkolu: ").strip()
        if not nazev:
            print("Název úkolu nesmí být prázdný.")
            continue
        popis = input("Zadejte popis úkolu: ").strip()
        if not popis:
            print("Popis úkolu nesmí být prázdný.")
            continue
        ukoly.append({"nazev": nazev, "popis": popis})
        print(f"Úkol '{nazev}' byl přidán.")
        break

def zobrazit_ukoly():
    print("\nSeznam úkolů:")
    if not ukoly:
        print("Žádné úkoly nejsou k dispozici.")
    else:
        for i, u in enumerate(ukoly, start=1):
            print(f"{i}. {u['nazev']} - {u['popis']}")

def odstranit_ukol():
    zobrazit_ukoly()
    if not ukoly:
        return
    try:
        cislo = int(input("Zadejte číslo úkolu, který chcete odstranit: "))
        if 1 <= cislo <= len(ukoly):
            odebrany = ukoly.pop(cislo - 1)
            print(f"Úkol '{odebrany['nazev']}' byl odstraněn.")
        else:
            print("Neplatné číslo úkolu.")
    except ValueError:
        print("Zadejte prosím platné číslo.")

# Spuštění programu
hlavni_menu()
