import os
import time
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

def run_bot():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    try:
        print("Démarrage du navigateur furtif...")
        driver = uc.Chrome(
            options=options,
            browser_executable_path='/usr/bin/google-chrome'
        )
        wait = WebDriverWait(driver, 25)

        # 1. Connexion
        print("Accès à la page de connexion...")
        driver.get("https://pixworld.fr/login")
        time.sleep(10)

        print("Saisie des identifiants...")
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_field.send_keys(EMAIL)
        
        pass_field = driver.find_element(By.NAME, "password")
        pass_field.send_keys(PASSWORD)
        
        print("Validation par la touche ENTRÉE...")
        time.sleep(2)
        pass_field.send_keys(Keys.ENTER)
        
        print("Connexion envoyée ! Attente du chargement...")
        time.sleep(12)

        # 2. Page de vote
        print("Navigation vers la page de vote...")
        driver.get("https://pixworld.fr/vote")
        time.sleep(5)

        # 3. Recherche du bouton Orion
        print("Recherche du bouton Orion...")
        try:
            btn_orion = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Orion')]")))
            driver.execute_script("arguments[0].click();", btn_orion)
            print("Bouton Orion cliqué ! ✅")
            time.sleep(5)
            return 
        except:
            print("Orion non trouvé, tentative de clic sur le lien de vote...")

        # 4. Vote classique
        links = driver.find_elements(By.CSS_SELECTOR, "a[data-vote-id]")
        voted = False
        for link in links:
            if SITE_CIBLE in link.get_attribute("href"):
                print(f"Clic sur {SITE_CIBLE}...")
                driver.execute_script("arguments[0].click();", link)
                voted = True
                break
        
        if voted:
            print("Attente de 15s pour le bouton Orion...")
            time.sleep(15)
            btn_orion_final = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Orion')]")))
            driver.execute_script("arguments[0].click();", btn_orion_final)
            print("Bouton Orion cliqué après vote ! ✅")

    except Exception as e:
        print(f"Erreur pendant l'exécution : {e}")
    
    finally:
        if 'driver' in locals():
            driver.quit()
        print("Session terminée.")

if __name__ == "__main__":
    run_bot()
