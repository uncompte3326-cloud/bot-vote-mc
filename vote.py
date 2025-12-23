import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# --- CONFIGURATION ---
EMAIL = os.environ.get('MY_EMAIL')
PASSWORD = os.environ.get('MY_PASSWORD')
SITE_CIBLE = "serveur-minecraft.com"
# ---------------------

options = Options()
options.add_argument('--headless=new') # Nouveau mode headless plus discret
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled') # Cache le robot
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

driver = webdriver.Chrome(options=options)

# On retire le flag webdriver pour ne pas être grillé
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

try:
    # 1. Connexion (Lien direct corrigé)
    print("Accès à Pixworld...")
    driver.get("https://pixworld.fr/login") # URL simplifiée
    time.sleep(5)

    try:
        print("Recherche des champs de connexion...")
        email_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        email_field.send_keys(EMAIL)
        driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(PASSWORD)
        
        # Clic sur le bouton de connexion (on cherche par le texte)
        btn_login = driver.find_element(By.XPATH, "//button[contains(text(), 'Connexion')]")
        driver.execute_script("arguments[0].click();", btn_login)
        print("Connexion envoyée !")
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        # Si ça échoue, on prend une capture d'écran "virtuelle" pour comprendre (optionnel)
        driver.save_screenshot("error_login.png")

    time.sleep(5)

    # 2. Page de vote
    print("Navigation vers la page de vote...")
    driver.get("https://pixworld.fr/vote")
    time.sleep(5)

    # 3. Clic sur le Site 2
    print(f"Recherche de {SITE_CIBLE}...")
    try:
        # On cherche tous les liens de vote
        links = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-vote-id]"))
        )
        for link in links:
            if SITE_CIBLE in link.get_attribute("href") or SITE_CIBLE in link.text:
                print("Site de vote trouvé ! Clic...")
                driver.execute_script("arguments[0].click();", link)
                break
    except:
        print("Bouton de vote introuvable. Vérifie si le chrono est bien fini sur le site.")

    # 4. Orion
    print("Attente du menu Orion (40s pour laisser le temps au site distant)...")
    time.sleep(40)
    
    try:
        select_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "site_id"))
        )
        select = Select(select_element)
        select.select_by_visible_text("Orion")
        print("Serveur Orion sélectionné !")
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        print("Récompense validée ! ✅")
    except:
        print("Le menu de sélection n'est pas apparu. Vérifie manuellement si le vote a compté.")

finally:
    driver.quit()
    print("Fin de session.")
