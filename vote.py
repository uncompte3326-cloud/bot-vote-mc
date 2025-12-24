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
        print("🚀 Mode Sniper de Flux (Attente dynamique d'Orion)...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # 1. Connexion stable
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)
        main_window = driver.current_window_handle
        driver.execute_script(f"""
            document.querySelectorAll('input').forEach(i => {{
                if(i.type === 'email' || i.name === 'email') i.value = '{EMAIL}';
                if(i.type === 'password' || i.name === 'password') i.value = '{PASSWORD}';
            }});
            var btn = document.querySelector('button[type="submit"], input[type="submit"]');
            if(btn) btn.click();
        """)
        time.sleep(15)

        # 2. Clic sur le Site 2 pour déclencher le processus
        print("Clic sur le Site 2...")
        driver.execute_script(f"""
            var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}'));
            if(a) {{
                a.target = '_blank';
                a.click();
            }}
        """)
        
        # 3. Gestion de l'onglet (On l'ouvre et on le referme vite pour simuler ton geste)
        time.sleep(5)
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(main_window)
        print("Retour sur Pixworld, en attente de l'injection d'Orion...")

        # 4. LE SNIPER : On scanne la page sans bouger
        found = False
        for i in range(30): # On surveille pendant 60 secondes (2s x 30)
            # On cherche spécifiquement le bouton vert Orion
            clicked = driver.execute_script("""
                var els = document.querySelectorAll('button, a, div, span');
                for (var el of els) {
                    if (el.innerText && el.innerText.trim() === 'Orion') {
                        el.click();
                        return true;
                    }
                }
                return false;
            """)
            
            if clicked:
                print(f"🎯 Orion détecté et cliqué à la seconde {i*2} !")
                found = True
                break
            
            if i % 5 == 0:
                print(f"Toujours en attente... ({i*2}s)")
            time.sleep(2)

        if not found:
            print("⚠️ Orion n'est pas apparu dynamiquement.")
        
        time.sleep(5)
        print("Fin de session. ✅")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
