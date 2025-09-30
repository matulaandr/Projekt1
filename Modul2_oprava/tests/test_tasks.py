import pytest
from Modul2_oprava.tasks import pridat_ukol, vypsat_ukoly, zmenit_stav_ukolu, odstranit_ukol

# Přidání úkolu
def test_pridat_ukol_pozitivni():
    new_id = pridat_ukol("Testovací úkol", "Popis testu")
    assert isinstance(new_id, int)
    ukoly = vypsat_ukoly(filter_open_only=False)
    assert any(u[0] == new_id and u[1] == "Testovací úkol" for u in ukoly)

def test_pridat_ukol_negativni():
    with pytest.raises(ValueError):
        pridat_ukol("", "Popis")
    with pytest.raises(ValueError):
        pridat_ukol("Název", "   ")

# Aktualizace úkolu
def test_aktualizovat_ukol_pozitivni():
    new_id = pridat_ukol("Aktualizovat", "Změna stavu")
    zmenit_stav_ukolu(new_id, "Hotovo")
    ukoly = vypsat_ukoly(filter_open_only=False)
    # najdi náš úkol
    target = [u for u in ukoly if u[0] == new_id][0]
    assert target[3] == "Hotovo"

def test_aktualizovat_ukol_negativni():
    # neplatný stav
    new_id = pridat_ukol("Aktualizovat neplatně", "Změna stavu")
    with pytest.raises(ValueError):
        zmenit_stav_ukolu(new_id, "Dokončeno")  # mimo povolené ENUM

    # neexistující ID
    with pytest.raises(LookupError):
        zmenit_stav_ukolu(99999, "Hotovo")

# Odstranění úkolu
def test_odstranit_ukol_pozitivni():
    new_id = pridat_ukol("Smazat", "Odstranit")
    odstranit_ukol(new_id)
    ukoly = vypsat_ukoly(filter_open_only=False)
    assert all(u[0] != new_id for u in ukoly)

def test_odstranit_ukol_negativni():
    with pytest.raises(LookupError):
        odstranit_ukol(123456)
