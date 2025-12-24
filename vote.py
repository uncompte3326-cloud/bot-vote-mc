import os
import time
import undetected_chromedriver as uc

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
        print("🚀 Mode Brise-Mur (Scan des IFrames pour Orion)...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # 1. Login (Base stable)
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)
        main_window = driver.current_window_handle
        driver.execute_script(f"document.querySelectorAll('input').forEach(i => {{ if(i.type === 'email') i.value = '{EMAIL}'; if(i.type === 'password') i.value = '{PASSWORD}'; }}); var b = document.querySelector('button[type=\"submit\"]'); if(b) b.click();")
        time.sleep(15)

        # 2. Clic Site 2
        print("Clic sur le Site 2...")
        driver.execute_script(f"var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}')); if(a) {{ a.target = '_blank'; a.click(); }}")
        time.sleep(10)

        # 3. Retour Onglet
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(main_window)
        print("Retour sur Pixworld. Début du scan multidimensionnel...")

        # 4. LE SNIPER MULTI-CADRES
        found = False
        for attempt in range(20):
            # A. On cherche d'abord sur la page principale
            clicked = driver.execute_script("""
                var el = Array.from(document.querySelectorAll('button, a, div')).find(e => e.innerText && e.innerText.trim() === 'Orion');
                if(el) { el.click(); return true; }
                return false;
            """)
            
            # B. Si pas trouvé, on scanne TOUTES les Iframes
            if not clicked:
                iframes = driver.find_elements(By.TAG_NAME, "iframe")
                for index, frame in enumerate(iframes):
                    try:
                        driver.switch_to.frame(frame)
                        clicked = driver.execute_script("""
                            var el = Array.from(document.querySelectorAll('button, a, div')).find(e => e.innerText && e.innerText.trim() === 'Orion');
                            if(el) { el.click(); return true; }
                            return false;
                        """)
                        driver.switch_to.default_content() # On ressort de l'iframe
                        if clicked: 
                            print(f"🎯 Orion trouvé dans l'Iframe #{index} !")
                            break
                    except:
                        driver.switch_to.default_content()
                        continue

            if clicked:
                print(f"✅ Clic effectué à la tentative {attempt+1} !")
                found = True
                break
            
            time.sleep(3)
            if attempt % 3 == 0: print(f"Scan en cours... ({attempt*3}s)")

        print("Opération terminée. ✅")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
