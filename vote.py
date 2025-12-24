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
    # On utilise un profil Chrome très standard pour passer inaperçu
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    driver = None
    try:
        print("🎭 [1/4] Connexion furtive...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        wait = WebDriverWait(driver, 60) # On est très patient
        
        # Étape 1 : On va sur le login et on ATTEND que la page soit stable
        driver.get("https://pixworld.fr/login")
        time.sleep(15) 

        # Étape 2 : Saisie caractère par caractère (comme toi au clavier)
        print("⌨️ Simulation de frappe humaine...")
        email_field = wait.until(EC.element_to_be_clickable((By.NAME, "email")))
        email_field.click() # On clique pour activer le champ
        for char in EMAIL:
            email_field.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3)) # Délai aléatoire entre les touches

        time.sleep(2)
        
        pass_field = driver.find_element(By.NAME, "password")
        pass_field.click()
        for char in PASSWORD:
            pass_field.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Étape 3 : On laisse le site "digérer" la connexion
        print("🧘 Assimilation de la session (30s)...")
        time.sleep(30)

        # Étape 4 : Vote et Orion
        print("🌍 Passage au vote...")
        driver.get("https://pixworld.fr/vote")
        time.sleep(20)
        
        # Clic sur le site de vote
        driver.execute_script(f"var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}')); if(a) a.click();")
        
        print("✅ Vote envoyé. Attente finale pour Orion (90s)...")
        time.sleep(90) # Comme tu l'as dit : pause humaine totale

        # Scanner final pour Orion
        success = driver.execute_script("""
            var btn = Array.from(document.querySelectorAll('button, a, .btn, span'))
                           .find(el => el.innerText && el.innerText.trim().toUpperCase() === 'ORION');
            if(btn) { btn.click(); return true; }
            return false;
        """)

        if success:
            print("✨ VICTOIRE ! Orion a été cliqué.")
        else:
            driver.save_screenshot("verif_final.png")
            print("❌ Orion n'est pas apparu. Vérifie 'verif_final.png'.")

    except Exception as e:
        print(f"💥 Erreur : {e}")
        if driver: driver.save_screenshot("crash_debug.png")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
