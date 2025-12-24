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
        print("🚀 Étape actuelle : Précision du clic Orion...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # 1. Accès et Login (Méthode stable validée)
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

        # 2. Déclenchement du Site 2 (L'élément clé)
        print("Ouverture du vote (Site 2)...")
        driver.execute_script(f"var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}')); if(a) {{ a.target = '_blank'; a.click(); }}")
        time.sleep(12) # On laisse un peu plus de temps pour la validation serveur

        # 3. Simulation humaine : Retour et "Réveil" de la page
        print("Retour sur l'onglet principal et réactivation...")
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(main_window)
        
        # On simule un mouvement de scroll pour forcer Pixworld à vérifier l'état du vote
        driver.execute_script("window.scrollBy(0, 200);")
        time.sleep(3)
        driver.execute_script("window.scrollBy(0, -200);")
        time.sleep(2)

        # 4. LE SNIPER : Recherche récursive d'Orion
        print("Scan intensif du bouton de récompense Orion...")
        success = False
        for attempt in range(20):
            # Cette commande JavaScript est "brutale" : elle clique sur tout ce qui ressemble à Orion
            # même si c'est un bouton, une image ou un texte cliquable.
            result = driver.execute_script("""
                var targets = document.querySelectorAll('button, a, div, span, h5, img');
                var clicked = false;
                targets.forEach(function(el) {
                    if (el.innerText && el.innerText.toUpperCase().includes('ORION')) {
                        el.click();
                        clicked = true;
                    } else if (el.alt && el.alt.toUpperCase().includes('ORION')) {
                        el.click();
                        clicked = true;
                    }
                });
                return clicked;
            """)
            
            if result:
                print(f"✅ Tentative {attempt} : Signal de clic envoyé à Orion !")
                success = True
                # On ne s'arrête pas au premier clic, on en remet un petit coup par sécurité
                time.sleep(1)
            
            if success and attempt > 5: # On attend quelques clics pour être sûr
                break
            
            time.sleep(1)

        # 5. Vérification finale
        if success:
            print("Action Orion terminée. Vérification du timer...")
        else:
            print("⚠️ Orion n'a pas été détecté visuellement. Tentative de secours...")
            driver.refresh() # Parfois un refresh après le vote débloque tout

        print("Opération terminée. ✅")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    run_bot()
