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
    # On ajoute une identité de navigateur réelle
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
    
    try:
        print("Démarrage du navigateur furtif...")
        driver = uc.Chrome(
            options=options,
            browser_executable_path='/usr/bin/google-chrome'
        )
        wait = WebDriverWait(driver, 30)

        # 1. Connexion
        print("Accès à la page de connexion...")
        driver.get("https://pixworld.fr/login")
        time.sleep(12)

        print("Saisie des identifiants...")
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_field.send_keys(EMAIL)
        time.sleep(1)
        
        pass_field = driver.find_element(By.NAME, "password")
        pass_field.send_keys(PASSWORD)
        time.sleep(1)
        
        print("Tentative de connexion (Entrée + Clic)...")
        pass_field.send_keys(Keys.ENTER)
        
        # On tente quand même de cliquer sur le bouton si Entrée n'a pas suffi
        try:
            btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            driver.execute_script("arguments[0].click();", btn)
        except:
            pass

        print("Connexion envoyée ! Attente de redirection (15s)...")
        time.sleep(15)

        # 2. Page de vote
        print("Navigation forcée vers la page de vote...")
        driver.get("https://pixworld.fr/vote")
        time.sleep(8)

        # 3. Recherche du bouton Orion
        print("Recherche du bouton Orion...")
        # On cherche par texte ou par classe pour être sûr
        try:
            btn_orion = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Orion')]")))
            driver.execute_script("arguments[0].click();", btn_orion)
            print("Bouton Orion cliqué ! ✅")
            time.sleep(5)
            return 
        except:
            print("Orion non trouvé, vérification du lien de vote...")

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
            print("Attente de 20s pour l'apparition d'Orion...")
            time.sleep(20)
            btn_orion_final = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Orion')]")))
            driver.execute_script("arguments[0].click();", btn_orion_final)
            print("Bouton Orion cliqué après vote ! ✅")

    except Exception as e:
        print(f"Erreur : {e}")
        # On prend une capture d'écran pour voir ce qui bloque (invisible mais utile)
        try: driver.save_screenshot("error.png")
        except: pass
    
    finally:
        if 'driver' in locals():
            driver.quit()
        print("Session terminée.")

if __name__ == "__main__":
    run_bot()
