import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

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
    # Simulation d'un agent utilisateur humain pour éviter les blocages passifs
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
    
    driver = None
    try:
        print("🚀 Lancement du Bot Diagnostic (Cible: Orion)...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # 1. CONNEXION
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)
        main_window = driver.current_window_handle
        
        print("Tentative de login...")
        driver.execute_script(f"""
            document.querySelectorAll('input').forEach(i => {{
                if(i.type === 'email' || i.name === 'email') i.value = '{EMAIL}';
                if(i.type === 'password' || i.name === 'password') i.value = '{PASSWORD}';
            }});
            var btn = document.querySelector('button[type="submit"], input[type="submit"]');
            if(btn) btn.click();
        """)
        time.sleep(15)

        # 2. DÉCLENCHEMENT VOTE (SITE 2)
        print("Déclenchement du vote sur le Site 2...")
        driver.execute_script(f"""
            var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}'));
            if(a) {{
                a.target = '_blank';
                a.click();
            }}
        """)
        time.sleep(15) # Temps de validation serveur

        # 3. GESTION DES ONGLETS
        print("Retour sur l'onglet Pixworld...")
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(main_window)
        time.sleep(5)
