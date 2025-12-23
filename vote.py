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
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

driver = webdriver.Chrome(options=options)

try:
    # 1. Connexion directe
    print("Tentative de connexion...")
    driver.get("https://pixworld.fr/user/login")
    
    email_field = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "email")))
    email_field.send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    print("Connexion réussie !")
    time.sleep(5)

    # 2. Page de vote
    print("Accès à la page de vote...")
    driver.get("https://pixworld.fr/vote")
    time.sleep(3)

    # 3. Recherche du site de vote (Site 2)
    print(f"Recherche de {SITE_CIBLE}...")
    # On attend que les boutons de vote soient visibles
    vote_links = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-vote-id]"))
    )
    
    found = False
    for link in vote_links:
        if SITE_CIBLE in link.text.lower() or SITE_CIBLE in link.get_attribute("href").lower():
            print("Site trouvé ! Clic envoyé.")
            driver.execute_script("arguments[0].scrollIntoView();", link)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", link)
            found = True
            break
            
    if not found:
        print("Erreur : Le bouton de vote n'est pas encore disponible (chrono en cours ?)")

    # 4. Attente du menu pour Orion
    if found:
        print("Attente du menu de récompense (30s)...")
        time.sleep(30) 
        
        try:
            select_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "site_id"))
            )
            select = Select(select_element)
            
            for option in select.options:
                if "Orion" in option.text:
                    select.select_by_visible_text(option.text)
                    print(f"Serveur {option.text} sélectionné !")
                    time.sleep(2)
                    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
                    print("Récompense validée ! ✅")
                    break
        except:
            print("Menu Orion non détecté. Le vote n'a peut-être pas encore été validé par le site distant.")

finally:
    driver.quit()
    print("Session terminée.")
