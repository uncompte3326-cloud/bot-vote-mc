import os
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# --- CONFIGURATION ---
EMAIL = os.environ.get('MY_EMAIL')
PASSWORD = os.environ.get('MY_PASSWORD')
# ---------------------

def run_bot():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    driver = None
    try:
        print("🚀 Lancement de la Phase Finale (Simulation Humaine)...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        actions = ActionChains(driver)

        # 1. Connexion forcée
        driver.get("https://pixworld.fr/login")
        time.sleep(10)
        
        print("Injection des identifiants...")
        driver.execute_script(f"""
            document.querySelector('input[type="email"]').value = '{EMAIL}';
            document.querySelector('input[type="password"]').value = '{PASSWORD}';
            document.querySelector('form').submit();
        """)
        time.sleep(15)

        # 2. Zone de vote avec simulation de mouvement
        print("Accès à la zone de vote...")
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)

        # 3. Simulation de mouvement de souris sur le bouton Orion
        print("Tentative de déclenchement du timer...")
        script_final = """
            var target = document.evaluate("//button[contains(., 'Orion')] | //a[contains(., 'Orion')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if(target) {
                target.scrollIntoView();
                // On simule un vrai événement de souris
                var ev = new MouseEvent('click', { 'view': window, 'bubbles': True, 'cancelable': True });
                target.dispatchEvent(ev);
                return "CLIC_OK";
            }
            return "NON_TROUVE";
        """
        result = driver.execute_script(script_final)
        print(f"Action sur Orion : {result}")

        # 4. Forçage du lien de vote (Site 2)
        print("Déclenchement du Site 2...")
        driver.execute_script("""
            var links = document.querySelectorAll('a[data-vote-id]');
            links.forEach(a => {
                if(a.href.includes('serveur-minecraft.com')) {
                    a.click();
                }
            });
        """)
        
        print("Attente de validation serveur (30s)...")
        time.sleep(30)
        print("Procédure terminée. ✅")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
