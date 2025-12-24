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
    """Simule la frappe d'un humain lettre par lettre"""
    if not text: return
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.4))

def run_bot():
    options = uc.ChromeOptions()
    # On enlève le headless pur pour tester la simulation d'écran
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080') # On force une résolution d'écran réelle
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    try:
        print("Démarrage du navigateur furtif (Écran simule)...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        wait = WebDriverWait(driver, 40) # On augmente l'attente à 40s

        # 1. Connexion
        print("Accès à la page de connexion...")
        driver.get("https://pixworld.fr/login")
        time.sleep(15) # On laisse le temps au site de nous "accepter"

        print("Saisie humaine des identifiants...")
        email_field = wait.until(EC.element_to_be_clickable((By.NAME, "email")))
        email_field.click() # On clique d'abord pour simuler l'humain
        human_type(email_field, EMAIL)
        
        time.sleep(random.uniform(1, 2))
        
        pass_field = driver.find_element(By.NAME, "password")
        pass_field.click()
        human_type(pass_field, PASSWORD)
        
        print("Validation (Entrée)...")
        time.sleep(1)
        pass_field.send_keys(Keys.ENTER)
        
        print("Connexion envoyée ! Attente de la redirection (25s)...")
        time.sleep(25)

        # 2. Page de vote
        print("Tentative d'accès à la page de vote...")
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)

        # 3. Recherche Orion
        print("Recherche du bouton Orion...")
        try:
            # On cherche par texte Orion de manière large
            btn_orion = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Orion')]")))
            driver.execute_script("arguments[0].click();", btn_orion)
            print("Bouton Orion cliqué ! ✅ Victoire !")
            time.sleep(5)
            return
        except:
            print("Orion non trouvé, le site nous a peut-être bloqué à la connexion.")

    except Exception as e:
        print(f"Erreur : {e}")
    
    finally:
        if 'driver' in locals():
            driver.quit()
        print("Session terminée.")

if __name__ == "__main__":
    run_bot()
