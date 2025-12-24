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
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
    
    driver = None
    try:
        print("🎭 [1/4] Initialisation de la navigation discrète...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # Passage par l'accueil pour chauffer les cookies
        driver.get("https://pixworld.fr/")
        time.sleep(12)

        # Accès au login
        print("🔐 [2/4] Connexion à l'espace membre...")
        driver.get("https://pixworld.fr/login")
        time.sleep(20) 

        # Injection fragmentée (plus humain)
        driver.execute_script(f"document.querySelector('input[type=\"email\"], [name=\"email\"]').value = '{EMAIL}';")
        time.sleep(3)
        driver.execute_script(f"document.querySelector('input[type=\"password\"], [name=\"password\"]').value = '{PASSWORD}';")
        time.sleep(2)
        driver.execute_script("document.querySelector('button[type=\"submit\"]').click();")
        
        print("... Pause d'assimilation session (25s) ...")
        time.sleep(25)

        # Accès au vote
        print("🌍 [3/4] Lancement de la procédure de vote...")
        driver.get("https://pixworld.fr/vote")
        time.sleep(15)
        
        # Clic Site 2
        driver.execute_script(f"""
            var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}'));
            if(a) a.click();
        """)
        
        print("✅ Vote Site 2 envoyé. Longue pause d'assimilation (60s)...")
        time.sleep(60)

        # Le Scanner de Boutons
        print("🎯 [4/4] Recherche de la récompense (Scanner Intelligent)...")
        found = False
        for i in range(30): # 30 tentatives (90 secondes de guet)
            success = driver.execute_script("""
                var targets = Array.from(document.querySelectorAll('button, a.btn, .btn-success, span, div'));
                
                // On cherche Orion OU un bouton de succès/validation qui vient d'apparaître
                var rewardBtn = targets.find(b => 
                    (b.innerText && b.innerText.toUpperCase().includes('ORION')) || 
                    (b.className && b.className.includes('success')) ||
                    (b.innerText && b.innerText.toUpperCase().includes('RÉCOMPENSE')) ||
                    (b.innerText && b.innerText.toUpperCase().includes('VALIDER'))
                );

                if(rewardBtn) {
                    rewardBtn.scrollIntoView({block: 'center'});
                    rewardBtn.click();
                    return true;
                }
                return false;
            """)
            
            if success:
                print(f"✨ VICTOIRE ! Bouton détecté et cliqué à la tentative {i+1}.")
                found = True
                break
            time.sleep(3)

        if not found:
            print("❌ Bouton introuvable après 90s de scan.")
            driver.save_screenshot("debug_final_scanner.png")

        print("Opération terminée. ✅")

    except Exception as e:
        print(f"❌ Erreur système : {e}")
        if driver: driver.save_screenshot("crash_final.png")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
