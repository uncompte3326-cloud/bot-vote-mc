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
        print("🔐 Étape 1 : Connexion à Pixworld...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        wait = WebDriverWait(driver, 30) # On laisse 30s max pour charger
        
        # 1. Page de Login
        driver.get("https://pixworld.fr/login")
        
        # Attente visuelle du champ email
        wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
        
        # Connexion via JS pour éviter les erreurs de focus
        driver.execute_script(f"""
            document.querySelector('input[name="email"]').value = '{EMAIL}';
            document.querySelector('input[name="password"]').value = '{PASSWORD}';
            document.querySelector('button[type="submit"]').click();
        """)
        
        print("Login envoyé, attente de redirection (10s)...")
        time.sleep(10)

        # 2. Page de Vote
        print("🌍 Étape 2 : Lancement du vote...")
        driver.get("https://pixworld.fr/vote")
        time.sleep(5)
        
        # On déclenche le Site 2
        driver.execute_script(f"""
            var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}'));
            if(a) a.click();
        """)
        print("Vote Site 2 déclenché, attente de validation (15s)...")
        time.sleep(15)

        # 3. Orion Sniper
        print("🎯 Étape 3 : Clic sur le bouton Orion...")
        found = False
        for i in range(10):
            # On cherche par texte exact "Orion"
            success = driver.execute_script("""
                var buttons = Array.from(document.querySelectorAll('button, a, .btn, span, div'));
                var orion = buttons.find(b => b.innerText && b.innerText.trim() === 'Orion');
                if(orion) {
                    orion.click();
                    return true;
                }
                return false;
            """)
            if success:
                print(f"✅ VICTOIRE : Orion cliqué à la tentative {i+1} !")
                found = True
                break
            time.sleep(2)

        if not found:
            print("⚠️ Orion non trouvé. Capture de debug générée.")
            driver.save_screenshot("debug_final.png")

        print("Opération terminée. ✅")

    except Exception as e:
        print(f"❌ Erreur : {e}")
        if driver: driver.save_screenshot("crash_debug.png")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
