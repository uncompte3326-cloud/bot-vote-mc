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

def human_type(element, text):
    """Tape du texte comme un humain avec des délais entre les lettres."""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))

def run_bot():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
    
    driver = None
    try:
        print("🎭 [1/4] Navigation discrète via l'accueil...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        wait = WebDriverWait(driver, 45)
        
        driver.get("https://pixworld.fr/")
        time.sleep(15)

        print("🔐 [2/4] Accès membre et frappe réelle...")
        driver.get("https://pixworld.fr/login")
        
        # Attente physique du champ email
        email_input = wait.until(EC.element_to_be_clickable((By.NAME, "email")))
        
        # On clique d'abord pour donner le focus (comme un humain)
        email_input.click()
        time.sleep(2)
        human_type(email_input, EMAIL)
        
        time.sleep(2)
        password_input = driver.find_element(By.NAME, "password")
        password_input.click()
        human_type(password_input, PASSWORD)
        
        time.sleep(3)
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
        
        print("... Pause d'assimilation (30s) ...")
        time.sleep(30)

        print("🌍 [3/4] Procédure de vote...")
        driver.get("https://pixworld.fr/vote")
        time.sleep(15)
        
        driver.execute_script(f"var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}')); if(a) a.click();")
        
        print("✅ Vote envoyé. Attente de la récompense (90s)...")
        time.sleep(90)

        print("🎯 [4/4] Scanner final...")
        found = False
        for i in range(30):
            success = driver.execute_script("""
                var targets = Array.from(document.querySelectorAll('button, a.btn, .btn-success, span, div'));
                var reward = targets.find(b => 
                    (b.innerText && b.innerText.toUpperCase().includes('ORION')) || 
                    (b.className && b.className.includes('success'))
                );
                if(reward) { reward.click(); return true; }
                return false;
            """)
            if success:
                print(f"✨ VICTOIRE ! Récompense validée à la tentative {i+1}.")
                found = True
                break
            time.sleep(3)

        if not found:
            driver.save_screenshot("echec_frappe.png")
            print("❌ Bouton introuvable.")

    except Exception as e:
        print(f"❌ Erreur critique : {e}")
        if driver: driver.save_screenshot("crash_frappe.png")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
