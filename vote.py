import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

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
        print("🚀 Mode Infiltration Finale + Force Orion...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # 1. Page de vote
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)
        main_window = driver.current_window_handle

        # 2. Login (Méthode validée)
        driver.execute_script(f"""
            document.querySelectorAll('input').forEach(i => {{
                if(i.type === 'email' || i.name === 'email') i.value = '{EMAIL}';
                if(i.type === 'password' || i.name === 'password') i.value = '{PASSWORD}';
            }});
            var btn = document.querySelector('button[type="submit"], input[type="submit"]');
            if(btn) btn.click();
        """)
        time.sleep(15)

        # 3. CLIC SITE 2
        print("Déclenchement du Site 2...")
        driver.execute_script(f"var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}')); if(a) {{ a.target = '_blank'; a.click(); }}")
        time.sleep(10)

        # 4. RETOUR ET FOCUS
        print("Retour sur l'onglet principal...")
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(main_window)
        
        # PETITE ASTUCE : On fait défiler la page pour simuler une activité
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(5)

        # 5. SCAN ET CLIC PHYSIQUE
        print("Recherche chirurgicale d'Orion...")
        # On tente de trouver l'élément et de cliquer dessus via ActionChains (clic simulé)
        found = False
        for i in range(15):
            # Script pour trouver le centre du bouton Orion
            coords = driver.execute_script("""
                var el = Array.from(document.querySelectorAll('button, a, span, div, h5')).find(e => e.innerText && e.innerText.includes('Orion'));
                if (el) {
                    el.scrollIntoView();
                    var rect = el.getBoundingClientRect();
                    return {x: rect.left + rect.width/2, y: rect.top + rect.height/2};
                }
                return null;
            """)
            
            if coords:
                print(f"🎯 Bouton Orion détecté aux coordonnées : {coords}")
                # On utilise ActionChains pour un vrai clic
                actions = ActionChains(driver)
                # Note: en headless, on utilise plutôt le clic JS car ActionChains peut être capricieux
                driver.execute_script("""
                    var el = Array.from(document.querySelectorAll('*')).find(e => e.innerText && e.innerText.includes('Orion'));
                    el.style.border = '5px solid red'; // Debug visuel interne
                    el.click();
                """)
                found = True
                break
            time.sleep(2)

        if found:
            print("✅ Clic Orion envoyé avec succès.")
        else:
            print("⚠️ Bouton non détecté. Tentative de 'Force Refresh' de la zone...")
            driver.execute_script("location.reload();")
            time.sleep(5)

        print("Opération terminée. ✅")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
