import os
import time
import random
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
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
    
    driver = None
    try:
        print("🧘 Mode Pause Totale : On laisse le site assimiler...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        wait = WebDriverWait(driver, 40) # Attente ultra-longue par sécurité

        # 1. CHARGEMENT LOGIN
        driver.get("https://pixworld.fr/login")
        print("... Attente chargement page login (20s) ...")
        time.sleep(20) 

        # 2. SAISIE SÉCURISÉE
        print("Vérification de la présence des champs...")
        # On attend que le champ email soit vraiment visible avant d'injecter
        wait.until(EC.visibility_of_element_located((By.NAME, "email")))
        
        driver.execute_script(f"""
            var mail = document.querySelector('input[name="email"]');
            var pass = document.querySelector('input[name="password"]');
            if(mail) mail.value = '{EMAIL}';
            if(pass) pass.value = '{PASSWORD}';
        """)
        print("... Petite pause post-saisie (5s) ...")
        time.sleep(5)
        
        driver.execute_script("document.querySelector('button[type=\"submit\"]').click();")
        print("... Assimilation de la connexion (25s) ...")
        time.sleep(25)

        # 3. VOTE
        driver.get("https://pixworld.fr/vote")
        print("... Attente chargement page vote (15s) ...")
        time.sleep(15)
        
        driver.execute_script(f"var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}')); if(a) a.click();")
        print("✅ Vote envoyé. On laisse le site valider tranquillement (60s)...")
        time.sleep(60) # Pause maximale pour l'assimilation du vote

        # 4. LE CLIC ORION
        print("🎯 Tentative finale sur Orion...")
        # On ne rafraîchit pas, on cherche juste le bouton qui doit être apparu
        success = driver.execute_script("""
            var el = Array.from(document.querySelectorAll('button, a, div, span'))
                          .find(e => e.innerText && e.innerText.trim().toUpperCase() === 'ORION');
            if(el) {
                el.scrollIntoView();
                el.click();
                return true;
            }
            return false;
        """)

        if success:
            print("✨ VICTOIRE ! Orion cliqué après une pause humaine.")
        else:
            print("❌ Bouton toujours pas là. Capture finale pour voir l'état du site.")
            driver.save_screenshot("pause_totale_result.png")

    except Exception as e:
        print(f"💥 Erreur pendant la pause : {e}")
        if driver: driver.save_screenshot("crash_pause.png")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
