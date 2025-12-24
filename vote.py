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
        print("🚀 Phase Finale : Sniper JavaScript sur Orion...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # 1. Navigation et Login (Stable)
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)
        main_window = driver.current_window_handle
        driver.execute_script(f"document.querySelectorAll('input').forEach(i => {{ if(i.type === 'email') i.value = '{EMAIL}'; if(i.type === 'password') i.value = '{PASSWORD}'; }}); var b = document.querySelector('button[type=\"submit\"]'); if(b) b.click();")
        time.sleep(15)

        # 2. Déclenchement du Site 2
        print("Ouverture du vote...")
        driver.execute_script(f"var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}')); if(a) {{ a.target = '_blank'; a.click(); }}")
        time.sleep(12)

        # 3. Retour Onglet et "Réveil" Forcé
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(main_window)
        
        # On force un petit scroll et un refresh de la détection
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(5)

        # 4. L'ATTAQUE SNIPER (Injection JS Directe)
        print("Exécution du clic forcé sur Orion...")
        script_sniper = """
            function sniper() {
                // On cherche tous les éléments qui contiennent 'Orion'
                var elements = document.querySelectorAll('button, a, div, span, h5');
                var found = false;
                elements.forEach(el => {
                    if(el.innerText && el.innerText.trim() === 'Orion') {
                        console.log('Cible verrouillée : Orion');
                        // On simule TOUS les types de clics possibles
                        el.click();
                        el.dispatchEvent(new MouseEvent('mousedown'));
                        el.dispatchEvent(new MouseEvent('mouseup'));
                        el.dispatchEvent(new MouseEvent('click', {bubbles: true}));
                        found = true;
                    }
                });
                return found;
            }
            return sniper();
        """
        
        # On essaie de sniper toutes les 2 secondes
        for i in range(10):
            if driver.execute_script(script_sniper):
                print(f"🎯 Orion cliqué avec succès à la tentative {i+1} !")
                break
            else:
                print(f"Attente apparition Orion... ({i+1}/10)")
                time.sleep(2)

        time.sleep(5)
        print("Opération terminée. ✅")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
