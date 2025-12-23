import os
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# --- CONFIGURATION ---
EMAIL = os.environ.get('MY_EMAIL')
PASSWORD = os.environ.get('MY_PASSWORD')
SITE_CIBLE = "serveur-minecraft.com"
# ---------------------

def human_type(element, text):
    """Tape du texte lettre par lettre avec des pauses aléatoires"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))

def run_bot():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
    
    try:
        print("Démarrage du navigateur furtif...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        wait = WebDriverWait(driver, 30)

        # 1. Connexion
        print("Accès à la page de connexion...")
        driver.get("https://pixworld.fr/login")
        time.sleep(10)

        print("Saisie humaine des identifiants...")
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        human_type(email_field, EMAIL)
        time.sleep(random.uniform(1, 2))
        
        pass_field = driver.find_element(By.NAME, "password")
        human_type(pass_field, PASSWORD)
        time.sleep(1)
        
        print("Validation (Touche Entrée)...")
        pass_field.send_keys(Keys.ENTER)
        
        print("Connexion envoyée ! Attente de la redirection (20s)...")
        time.sleep(20)

        # 2. Page de vote
        print("Navigation vers la page de vote...")
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)

        # 3. Recherche du bouton Orion
        print("Recherche du bouton Orion...")
        try:
            # On cherche spécifiquement le bouton qui contient Orion
            btn_orion = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Orion')] | //a[contains(., 'Orion')]")))
            driver.execute_script("arguments[0].click();", btn_orion)
            print("Bouton Orion cliqué ! ✅")
            time.sleep(5)
            return 
        except:
            print("Bouton Orion non trouvé immédiatement.")

        # 4. Vote si Orion n'était pas là
        links = driver.find_elements(By.CSS_SELECTOR, "a[data-vote-id]")
        voted = False
        for link in links:
            if SITE_CIBLE in link.get_attribute("href"):
                print(f"Clic sur le lien de vote : {SITE_CIBLE}...")
                driver.execute_script("arguments[0].click();", link)
                voted = True
                break
        
        if voted:
            print("Attente de détection du vote (20s)...")
            time.sleep(20)
            btn_final = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Orion')] | //a[contains(., 'Orion')]")))
            driver.execute_script("arguments[0].click();", btn_final)
            print("Bouton Orion validé après vote ! ✅")

    except Exception as e:
        print(f"Erreur : {e}")
    
    finally:
        if 'driver' in locals():
            driver.quit()
        print("Session terminée.")

if __name__ == "__main__":
    run_bot()
