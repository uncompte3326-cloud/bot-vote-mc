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
    options.add_argument('--window-size=1920,1080')
    driver = uc.Chrome(options=options)
    
    try:
        # 1. CONNEXION FORCÉE
        print("🔐 Phase 1 : Connexion à Pixworld...")
        driver.get("https://pixworld.fr/login") # On va direct sur la page login
        time.sleep(5)
        
        # On remplit les champs un par un avec vérification
        driver.execute_script(f"""
            var inputs = document.querySelectorAll('input');
            inputs.forEach(i => {{
                if(i.type === 'email' || i.name === 'email') i.value = '{EMAIL}';
                if(i.type === 'password' || i.name === 'password') i.value = '{PASSWORD}';
            }});
            document.querySelector('button[type="submit"]').click();
        """)
        print("Attente de validation du compte (10s)...")
        time.sleep(10)

        # 2. ALLER SUR LA PAGE DE VOTE
        print("🌍 Phase 2 : Accès à la page de vote...")
        driver.get("https://pixworld.fr/vote")
        time.sleep(5)

        # 3. CLIQUER SUR LE SITE 2
        print("🖱️ Phase 3 : Clic sur le Site 2...")
        driver.execute_script(f"var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}')); if(a) a.click();")
        time.sleep(15) # On attend que le vote soit validé par le serveur

        # 4. LE CLIC FINAL SUR ORION
        print("🎯 Phase 4 : Sniper Orion...")
        found = False
        for i in range(10):
            # On cherche Orion partout (même dans les recoins du site connecté)
            clicked = driver.execute_script("""
                var btn = Array.from(document.querySelectorAll('button, a, .btn')).find(el => el.innerText.includes('Orion'));
                if(btn) { btn.click(); return true; }
                return false;
            """)
            if clicked:
                print("✅ Orion cliqué ! Récompense envoyée.")
                found = True
                break
            print(f"Attente apparition bouton... ({i*2}s)")
            time.sleep(2)

        driver.save_screenshot("final_check.png")
        print("🏁 Workflow terminé.")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
