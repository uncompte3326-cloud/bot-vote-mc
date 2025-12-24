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
        print("🚀 Mode Sniper de Précision (Force Visuelle)...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # 1. Login (Base stable)
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)
        main_window = driver.current_window_handle
        driver.execute_script(f"document.querySelectorAll('input').forEach(i => {{ if(i.type === 'email') i.value = '{EMAIL}'; if(i.type === 'password') i.value = '{PASSWORD}'; }}); var b = document.querySelector('button[type=\"submit\"]'); if(b) b.click();")
        time.sleep(15)

        # 2. Clic Site 2
        driver.execute_script(f"var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}')); if(a) {{ a.target = '_blank'; a.click(); }}")
        time.sleep(12)

        # 3. Retour Onglet
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(main_window)
        
        # --- LA NOUVEAUTÉ : MISE EN LUMIÈRE ---
        print("Préparation de la zone de clic...")
        found = False
        for attempt in range(15):
            # Script JS qui cherche Orion, le fait clignoter, le centre et clique
            # On cherche dans le document principal ET les iframes via JS direct
            script_force_clic = """
            function findAndClickOrion(root) {
                var els = root.querySelectorAll('button, a, div, span');
                for (var el of els) {
                    if (el.innerText && el.innerText.trim() === 'Orion') {
                        // 1. On le rend visible de force (au cas où il est caché par un overlay)
                        el.style.display = 'block';
                        el.style.visibility = 'visible';
                        el.style.zIndex = '9999';
                        // 2. On le centre dans l'écran
                        el.scrollIntoView({block: "center"});
                        // 3. On clique réellement
                        el.click();
                        return true;
                    }
                }
                // Chercher dans les iframes
                var frames = root.querySelectorAll('iframe');
                for (var f of frames) {
                    try {
                        if (findAndClickOrion(f.contentDocument)) return true;
                    } catch(e) {}
                }
                return false;
            }
            return findAndClickOrion(document);
            """
            
            if driver.execute_script(script_force_clic):
                print(f"🎯 Orion localisé, centré et cliqué à la tentative {attempt+1} !")
                found = True
                break
            
            time.sleep(3)
            if attempt % 3 == 0: print(f"Recherche visuelle... ({attempt*3}s)")

        if not found:
            print("⚠️ Bouton Orion introuvable après scan visuel.")

        print("Opération terminée. ✅")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
