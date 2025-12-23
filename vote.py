import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION (REMPLIS ICI) ---
EMAIL = os.environ.get('MY_EMAIL')
PASSWORD = os.environ.get('MY_PASSWORD')
PSEUDO = "Calalalopy"
# ----------------------------------

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

driver = webdriver.Chrome(options=options)

try:
    # 1. Connexion au site
    print("Connexion à Pixworld...")
    driver.get("https://pixworld.fr/login")
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    time.sleep(3) # Attendre la connexion
    
    # 2. Aller sur la page de vote
    print("Direction page de vote...")
    driver.get("https://pixworld.fr/vote")
    
    # 3. Saisie du pseudo (si pas automatique)
    print(f"Vérification pseudo : {PSEUDO}")
    input_pseudo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "step-1-user")))
    input_pseudo.clear()
    input_pseudo.send_keys(PSEUDO)
    
    # 4. Bouton Etape Suivante
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)

# 5. Attente du menu de sélection du serveur
    print("Attente du menu de récompense...")
    time.sleep(20) 
    
    try:
        # On cherche le menu de sélection (souvent nommé site_id)
        select_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "site_id"))
        )
        
        from selenium.webdriver.support.ui import Select
        select = Select(select_element)
        
        # On sélectionne Orion
        try:
            select.select_by_visible_text("Orion")
            print("Serveur Orion sélectionné ! ✅")
            
            # Un petit délai pour que la sélection soit prise en compte
            time.sleep(2)
            
            # On clique sur le bouton "Confirmer"
            btn_confirm = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            driver.execute_script("arguments[0].scrollIntoView();", btn_confirm)
            btn_confirm.click()
            print("Récompense réclamée avec succès !")
            
        except:
            print("Impossible de trouver 'Orion' exactement. Tentative de recherche partielle...")
            # Si jamais c'est écrit différemment, on cherche le mot Orion quand même
            for option in select.options:
                if "Orion" in option.text:
                    select.select_by_visible_text(option.text)
                    print(f"Serveur {option.text} sélectionné !")
                    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
                    break
            
    except Exception as e:
        print("Le menu de sélection n'est pas apparu. Le vote a peut-être échoué ou est déjà validé.")
