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
        print("🚀 Mode Contrôle Total (Simulation d'activation forcée)...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # 1. Login (Stable)
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
        
        # --- PHASE D'ACTIVATION FORCÉE ---
        print("Activation de la zone de récompense...")
        # On simule des clics tout autour de la zone centrale pour "réveiller" le script de Pixworld
        driver.execute_script("""
            for(let i=0; i<5; i++) {
                let x = window.innerWidth / 2;
                let y = (window.innerHeight / 2) + (i * 20);
                let el = document.elementFromPoint(x, y);
                if(el) el.click();
            }
        """)
        time.sleep(5)

        # 4. SNIPER PAR CLASSE ET TEXTE
        print("Scan final Orion...")
        # On utilise une boucle qui cherche n'importe quel élément contenant "Orion" 
        # ou ayant une couleur de bouton de succès (souvent 'btn-success' ou 'btn-primary')
        found = False
        for attempt in range(15):
            success = driver.execute_script("""
                function finalShot() {
                    // On cherche par texte exact, puis par partie de texte
                    var targets = Array.from(document.querySelectorAll('button, a, div, span'));
                    var orion = targets.find(e => e.innerText && e.innerText.trim().includes('Orion'));
                    
                    if (orion) {
                        orion.scrollIntoView({block: 'center'});
                        orion.click();
                        // On tente aussi de cliquer sur son parent si c'est un bouton stylisé
                        if (orion.parentElement) orion.parentElement.click();
                        return true;
                    }
                    return false;
                }
                return finalShot();
            """)
            
            if success:
                print(f"🎯 Cible touchée à la tentative {attempt+1} !")
                found = True
                break
            time.sleep(3)

        if not found:
            print("⚠️ Échec de la localisation. Vérification manuelle requise.")

        time.sleep(5)
        print("Opération terminée. ✅")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
