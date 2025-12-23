import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
EMAIL = os.environ.get('MY_EMAIL')
PASSWORD = os.environ.get('MY_PASSWORD')
SITE_CIBLE = "serveur-minecraft.com"
# ---------------------

options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

try:
    # 1. Connexion
    print("Connexion à Pixworld...")
    driver.get("https://pixworld.fr/login")
    
    email_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    email_field.send_keys(EMAIL)
    driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(PASSWORD)
    
    btn_login = driver.find_element(By.XPATH, "//button[contains(text(), 'Connexion')]")
    driver.execute_script("arguments[0].click();", btn_login)
    print("Connecté !")
    time.sleep(5)

    # 2. Page de vote
    print("Direction la page de vote...")
    driver.get("https://pixworld.fr/vote")
    time.sleep(5)

    # 3. Clic sur le Site 2
    print(f"Recherche du lien {SITE_CIBLE}...")
    links = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-vote-id]"))
    )
    
    voted = False
    for link in links:
        if SITE_CIBLE in link.get_attribute("href") or SITE_CIBLE in link.text:
            print("Site trouvé ! Clic envoyé.")
            driver.execute_script("arguments[0].click();", link)
            voted = True
            break

    if voted:
        # 4. Clic sur le bouton Orion (ton image #8)
        print("Attente de l'apparition du bouton Orion (15s)...")
        time.sleep(15)
        
        try:
            # On cherche spécifiquement le bouton qui contient le texte "Orion"
            btn_orion = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Orion')]"))
            )
            driver.execute_script("arguments[0].click();", btn_orion)
            print("Bouton Orion cliqué ! ✅")
            time.sleep(5)
            print("Récompense validée avec succès.")
        except:
            print("Le bouton Orion n'est pas apparu. Peut-être que le vote n'a pas été détecté.")
    else:
        print("Impossible de trouver le site cible.")

finally:
    driver.quit()
    print("Session terminée.")
