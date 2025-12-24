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
    
    driver = None
    try:
        print("Démarrage du mode 'Sélecteur Universel'...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        wait = WebDriverWait(driver, 40)

        # 1. Connexion
        print("Accès à la page de connexion...")
        driver.get("https://pixworld.fr/login")
        time.sleep(10)

        print("Recherche des champs par type...")
        # On cherche par type d'input au lieu du nom 'email'
        try:
            email_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[name*='mail']")))
            pass_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            
            print("Champs trouvés ! Injection...")
            driver.execute_script(f"arguments[0].value='{EMAIL}';", email_field)
            driver.execute_script(f"arguments[0].value='{PASSWORD}';", pass_field)
            
            time.sleep(2)
            print("Soumission du formulaire...")
            # On cherche le bouton submit ou on valide le formulaire
            driver.execute_script("document.querySelector('form').submit();")
        except Exception as e:
            print(f"Échec de localisation des champs : {e}")
            driver.save_screenshot("debug_login.png")
            return

        print("Attente de redirection après login (25s)...")
        time.sleep(25)

        # 2. Page de vote
        print("Accès à la page de vote...")
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)

        # 3. Clic Orion
        print("Tentative de clic Orion...")
        driver.execute_script("""
            var found = false;
            document.querySelectorAll('button, a, span').forEach(el => {
                if(el.innerText.includes('Orion')) {
                    el.click();
                    found = true;
                }
            });
            return found;
        """)
        
        # 4. Vote de secours
        print("Lancement du vote secondaire...")
        driver.execute_script(f"""
            document.querySelectorAll('a').forEach(a => {{
                if(a.href.includes('{SITE_CIBLE}')) a.click();
            }});
        """)
        
        time.sleep(10)
        print("Procédure terminée. ✅")

    except Exception as e:
        print(f"Erreur globale : {e}")
        if driver: driver.save_screenshot("error_final.png")
    
    finally:
        if driver:
            driver.quit()
        print("Session terminée.")

if __name__ == "__main__":
    run_bot()
