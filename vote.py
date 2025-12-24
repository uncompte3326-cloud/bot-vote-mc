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
    
    driver = None
    try:
        print("🚀 Démarrage de l'Infiltration Directe...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # 1. On va directement sur la page de VOTE (parfois ça bypass le login check)
        print("Navigation directe vers la zone de vote...")
        driver.get("https://pixworld.fr/vote")
        time.sleep(15)

        # 2. Si on n'est pas connecté, on injecte les identifiants n'importe où sur la page
        print("Tentative d'injection forcée (Login universel)...")
        # Ce script cherche les champs même s'ils sont cachés ou dans des fenêtres surgissantes
        force_login = f"""
            var inputs = document.querySelectorAll('input');
            if (inputs.length === 0) {{ 
                window.location.href = 'https://pixworld.fr/login'; 
            }} else {{
                inputs.forEach(function(i) {{
                    if(i.type === 'email' || i.name === 'email') i.value = '{EMAIL}';
                    if(i.type === 'password' || i.name === 'password') i.value = '{PASSWORD}';
                }});
                var btn = document.querySelector('button[type="submit"], input[type="submit"]');
                if(btn) btn.click();
                else document.querySelector('form').submit();
            }}
        """
        driver.execute_script(force_login)
        time.sleep(20)

        # 3. On retourne au vote après la tentative de login
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)

        # 4. Clic Orion Ultra-Large
        print("Ciblage du bouton Orion...")
        # On cherche Orion dans TOUT le document, même les textes cachés
        driver.execute_script("""
            var all = document.querySelectorAll('*');
            for (var i = 0; i < all.length; i++) {
                if (all[i].innerText && all[i].innerText.includes('Orion')) {
                    all[i].click();
                    console.log('Orion cliqué');
                }
            }
        """)
        
        # 5. Vote de secours
        print("Finalisation du vote...")
        driver.execute_script(f"document.querySelectorAll('a').forEach(a => {{ if(a.href.includes('{SITE_CIBLE}')) a.click(); }});")
        
        time.sleep(10)
        print("Opération terminée. ✅")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
