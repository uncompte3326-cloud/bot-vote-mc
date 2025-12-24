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

def run_bot():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    driver = None
    try:
        print("🔐 Étape 1 : Connexion sécurisée...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        wait = WebDriverWait(driver, 20)
        
        # Aller sur la page de login directe
        driver.get("https://pixworld.fr/login")
        
        # Attendre que le champ email soit réellement présent dans le code
        email_field = wait.until(EC.presence_of_element_property((By.NAME, 'email'), 'type', 'email'))
        
        # Injection des identifiants
        driver.execute_script(f"""
            document.querySelector('input[name="email"]').value = '{EMAIL}';
            document.querySelector('input[name="password"]').value = '{PASSWORD}';
            document.querySelector('button[type="submit"]').click();
        """)
        
        print("Connexion en cours, attente de redirection...")
        time.sleep(10)

        # Étape 2 : Vote
        print("🌍 Étape 2 : Page de vote...")
        driver.get("https://pixworld.fr/vote")
        time.sleep(5)
        
        # Clic Site 2
        driver.execute_script(f"var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}')); if(a) a.click();")
        print("Vote effectué, attente de 15s pour le serveur...")
        time.sleep(15)

        # Étape 3 : Orion
        print("🎯 Étape 3 : Sniper Orion...")
        # On tente de trouver le bouton Orion par tous les moyens possibles
        for i in range(10):
            success = driver.execute_script("""
                var buttons = Array.from(document.querySelectorAll('button, a, .btn, span'));
                var orion = buttons.find(b => b.innerText && b.innerText.trim() === 'Orion');
                if(orion) {
                    orion.click();
                    return true;
                }
                return false;
            """)
            if success:
                print("✅ RÉUSSITE : Orion a été cliqué !")
                break
            print(f"Recherche Orion... ({i+1}/10)")
            time.sleep(2)

        driver.save_screenshot("proof_of_success.png")
        print("Opération terminée. ✅")

    except Exception as e:
        print(f"❌ Erreur : {e}")
        if driver:
            driver.save_screenshot("error_debug.png")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    run_bot()
