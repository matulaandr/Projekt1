import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://www.engeto.cz"


#  Fixture – otevře web a akceptuje cookies
@pytest.fixture
def accepted_page(page: Page):
    """Otevře hlavní stránku a potvrdí cookies banner, pokud je viditelný."""
    page.goto(BASE_URL)
    page.wait_for_load_state("domcontentloaded")

    cookie_btn = page.get_by_role("button", name="Chápu a přijímám")
    if cookie_btn.is_visible():
        cookie_btn.click()

    return page

# Test: Objednávka kurzu Tester s Pythonem
def test_order_python_tester_course(accepted_page: Page):
    page = accepted_page

    # otevře stránku s přehledem IT kurzů
    page.get_by_role("link", name="Přehled IT kurzů").click()
    # počká, až se objeví odkaz na kurz "Tester s Pythonem"
    page.get_by_role("link", name="Tester s Pythonem", exact=True).wait_for(state="visible", timeout=10000)

    # klikne na kurz "Tester s Pythonem"
    page.get_by_role("link", name="Tester s Pythonem", exact=True).click()
 
    # zobrazí termíny kurzu
    page.get_by_role("link", name="Zobrazit termíny kurzu").click()
    page.locator("text=Detail termínu").first.wait_for(state="visible", timeout=10000)

    # klikne na první dostupný termín kurzu
    page.locator("text=Detail termínu").first.click()
   
    # přidá kurz do košíku
    page.get_by_role("link", name="Objednat kurz").click()

    # nastaví množství kurzů na jednu jednotku
    quantity_input = page.get_by_role("spinbutton", name="Množství")
    quantity_input.fill("1")

    # pokračuje do objednávky
    page.get_by_role("link", name="Pokračovat v objednávce").click()

    # ověří, že se zobrazily fakturační údaje
    expect(page.locator("h3:has-text('Fakturační údaje')")).to_be_visible(timeout=10000)

# Test: Přihlášení do výukového portálu
def test_login_to_learning_portal(accepted_page: Page):
    page = accepted_page

    # otevře stránku výukového portálu
    page.get_by_role("link", name="Výukový portál").click()
    page.wait_for_load_state("networkidle")  # počká, až se načtou všechny zdroje

    # klikne na tlačítko pro přihlášení e-mailem a heslem
    page.get_by_role("button", name="Přihlásit se pomoci e-mailu a hesla").click()

    # najde pole pro e-mail podle id a vyplní ho
    email_input = page.locator("#username")
    email_input.fill("martina.andraskova@icloud.com")

    # ověří, že se hodnota skutečně vyplnila správně
    expect(email_input).to_have_value("martina.andraskova@icloud.com")



# Test: Ověření hlavní stránky a potvrzení cookies
def test_homepage_cookie_acceptance(page: Page):
    # otevře hlavní stránku
    page.goto(BASE_URL)
    page.wait_for_load_state("domcontentloaded")  # počká, až se načte DOM

    # najde tlačítko pro cookies
    cookie_btn = page.get_by_role("button", name="Chápu a přijímám")
    
    # pokud je tlačítko vidět, klikne na něj
    if cookie_btn.is_visible():
        cookie_btn.click()

    # ověří, že tlačítko cookies už není vidět
    expect(cookie_btn).not_to_be_visible()

    # ověří, že hlavní text na stránce je vidět
    expect(page.get_by_text("Staň se novým IT talentem")).to_be_visible()
