import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
EMAIL = os.environ.get('MY_EMAIL')
PASSWORD = os.environ.get('MY_PASSWORD')
SITE_CIBLE = "serveur-minecraft.com"
# ---------------------

def run_bot():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    try:
        print("Démarrage du mode 'Injection Directe'...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        wait = WebDriverWait(driver, 30)

        # 1. Connexion par injection JavaScript (Indétectable)
        print("Accès à la page de connexion...")
        driver.get("https://pixworld.fr/login")
        time.sleep(10)

        print("Injection des identifiants dans le système...")
        # On remplit les champs directement via le code de la page
        driver.execute_script(f"document.getElementsByName('email')[0].value='{EMAIL}';")
        driver.execute_script(f"document.getElementsByName('password')[0].value='{PASSWORD}';")
        time.sleep(2)
        
        print("Soumission forcée du formulaire...")
        driver.execute_script("document.querySelector('form').submit();")
        
        print("Attente de validation (20s)...")
        time.sleep(20)

        # 2. Saut direct vers la page Orion (pour gagner du temps)
        print("Navigation vers le profil de vote...")
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)

        # 3. Récupération de la récompense
        print("Tentative de clic sur Orion...")
        try:
            # On cherche tous les boutons verts de récompense
            driver.execute_script("document.querySelectorAll('button, a').forEach(el => { if(el.innerText.includes('Orion')) el.click(); });")
            print("Commande de clic Orion envoyée ! ✅")
        except:
            print("Le bouton Orion n'a pas pu être injecté.")

        # 4. Vote de secours
        print("Lancement du vote de secours...")
        driver.execute_script(f"document.querySelectorAll('a').forEach(a => {{ if(a.href.includes('{SITE_CIBLE}')) a.click(); }});")
        time.sleep(15)
        
        # Ultime tentative Orion après vote
        driver.execute_script("document.querySelectorAll('button, a').forEach(el => {{ if(el.innerText.includes('Orion')) el.click(); }});")
        print("Fin de la procédure d'injection.")

    except Exception as e:
        print(f"Erreur : {e}")
    
    finally:
        if 'driver' in locals():
            driver.quit()
        print("Session terminée.")

if __name__ == "__main__":
    run_bot()
