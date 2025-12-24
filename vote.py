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
        print("🚀 Mode Infiltration + Déblocage Onglet...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # 1. Page de vote directe
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)
        main_window = driver.current_window_handle

        # 2. Login universel (Base fonctionnelle)
        driver.execute_script(f"""
            document.querySelectorAll('input').forEach(i => {{
                if(i.type === 'email' || i.name === 'email') i.value = '{EMAIL}';
                if(i.type === 'password' || i.name === 'password') i.value = '{PASSWORD}';
            }});
            var btn = document.querySelector('button[type="submit"], input[type="submit"]');
            if(btn) btn.click();
        """)
        time.sleep(15)

        # 3. CLIC SITE 2 (Ouverture d'onglet réelle)
        print("Ouverture du Site 2 dans un nouvel onglet...")
        driver.execute_script(f"""
            var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}'));
            if(a) {{
                a.target = '_blank';
                a.click();
            }}
        """)
        time.sleep(10) # On laisse l'onglet de vote ouvert 10s

        # 4. RETOUR ET FERMETURE (Simule le comportement humain)
        print("Fermeture de l'onglet de vote et retour sur Pixworld...")
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                driver.close()
        
        driver.switch_to.window(main_window)
        time.sleep(5) # Pause pour laisser le script de Pixworld s'actualiser

        # 5. SNIPER ORION
        print("Scan intensif du bouton Orion...")
        for i in range(20):
            clicked = driver.execute_script("""
                var elements = document.querySelectorAll('button, a, span, div, h5');
                for (var el of elements) {
                    if (el.innerText && el.innerText.includes('Orion')) {
                        el.click();
                        return true;
                    }
                }
                return false;
            """)
            if clicked:
                print(f"🎯 Orion trouvé et cliqué à la tentative {i} !")
                break
            time.sleep(1)

        print("Opération terminée. ✅")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
