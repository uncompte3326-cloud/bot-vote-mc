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
        print("🚀 Reprise du code fonctionnel (Mode Infiltration + Surveillance)...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # 1. On va sur la page de vote (directement là où ça avait marché)
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)

        # 2. On injecte le login au cas où (Universal Login)
        print("Vérification de la connexion...")
        driver.execute_script(f"""
            var inputs = document.querySelectorAll('input');
            inputs.forEach(function(i) {{
                if(i.type === 'email' || i.name === 'email') i.value = '{EMAIL}';
                if(i.type === 'password' || i.name === 'password') i.value = '{PASSWORD}';
            }});
            var btn = document.querySelector('button[type="submit"], input[type="submit"]');
            if(btn) btn.click();
        """)
        time.sleep(15)

        # 3. Étape CRITIQUE : Clic sur le Site 2 pour débloquer le choix
        print("Déclenchement du Site 2...")
        driver.execute_script(f"""
            document.querySelectorAll('a').forEach(a => {{
                if(a.href.includes('{SITE_CIBLE}')) {{
                    a.target = '_self'; // On évite d'ouvrir un nouvel onglet pour rester focus
                    a.click();
                }}
            }});
        """)
        
        # 4. BOUCLE DE SURVEILLANCE : On attend que le bouton Orion apparaisse
        print("Surveillance de l'apparition du bouton Orion (pendant 30s)...")
        found = False
        for i in range(30): # On essaie pendant 30 secondes
            # On cherche Orion dans TOUTE la page (bouton, texte, lien)
            check_orion = driver.execute_script("""
                var elements = document.querySelectorAll('button, a, span, div, h5');
                for (var el of elements) {
                    if (el.innerText && el.innerText.includes('Orion')) {
                        el.click();
                        return true;
                    }
                }
                return false;
            """)
            
            if check_orion:
                print(f"✅ SUCCÈS : Bouton Orion trouvé et cliqué à la seconde {i} !")
                found = True
                break
            
            time.sleep(1) # On attend 1 sec avant de re-scanner
            if i % 5 == 0: print(f"En attente... ({i}s)")

        if not found:
            print("⚠️ Orion n'est pas apparu. Tentative de rafraîchissement final...")
            driver.refresh()
            time.sleep(5)
            driver.execute_script("document.querySelectorAll('*').forEach(el => { if(el.innerText && el.innerText.includes('Orion')) el.click(); });")

        print("Opération terminée. ✅")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
