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
        print("Démarrage du mode 'Scan Total'...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # 1. Connexion
        print("Accès à la page de connexion...")
        driver.get("https://pixworld.fr/login")
        time.sleep(15) # On laisse un temps de chargement massif

        print("Tentative d'auto-remplissage via JavaScript global...")
        # Ce script cherche tous les inputs et remplit intelligemment
        injection_script = f"""
            var inputs = document.querySelectorAll('input');
            var filled = 0;
            inputs.forEach(function(i) {{
                if(i.type === 'email' || i.name.includes('mail') || i.placeholder.toLowerCase().includes('email')) {{
                    i.value = '{EMAIL}';
                    filled++;
                }}
                if(i.type === 'password' || i.name.includes('pass') || i.placeholder.toLowerCase().includes('mot de passe')) {{
                    i.value = '{PASSWORD}';
                    filled++;
                }}
            }});
            if(filled >= 2) {{
                var form = document.querySelector('form');
                if(form) form.submit();
                return "OK";
            }}
            return "NOT_FOUND";
        """
        
        result = driver.execute_script(injection_script)
        print(f"Résultat de l'injection : {result}")

        if result == "NOT_FOUND":
            print("Échec du scan. Tentative de secours via navigation directe...")
        
        print("Attente de redirection (25s)...")
        time.sleep(25)

        # 2. Page de vote
        print("Navigation vers la page de vote...")
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)

        # 3. Récupération Orion
        print("Scan du bouton Orion...")
        driver.execute_script("""
            var btns = document.querySelectorAll('button, a, span, div');
            btns.forEach(function(b) {
                if(b.innerText && b.innerText.includes('Orion')) b.click();
            });
        """)
        
        # 4. Vote de secours
        print("Scan des liens de vote...")
        driver.execute_script(f"""
            document.querySelectorAll('a').forEach(a => {{
                if(a.href && a.href.includes('{SITE_CIBLE}')) a.click();
            }});
        """)
        
        time.sleep(10)
        print("Fin de session. ✅")

    except Exception as e:
        print(f"Erreur : {e}")
    
    finally:
        if driver:
            driver.quit()
        print("Navigateur fermé.")

if __name__ == "__main__":
    run_bot()
