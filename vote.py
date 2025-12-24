import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        print("🚀 Démarrage du bot (Mode Switch Onglet)...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        wait = WebDriverWait(driver, 20)

        # 1. Connexion
        driver.get("https://pixworld.fr/login")
        time.sleep(5)
        driver.execute_script(f"""
            document.querySelector('input[type="email"]').value = '{EMAIL}';
            document.querySelector('input[type="password"]').value = '{PASSWORD}';
            document.querySelector('form').submit();
        """)
        print("Connexion effectuée...")
        time.sleep(10)

        # 2. Page de vote
        driver.get("https://pixworld.fr/vote")
        time.sleep(5)
        main_window = driver.current_window_handle # On mémorise l'onglet Pixworld

        # 3. Clic sur le Site 2 pour ouvrir l'onglet de vote
        print("Clic sur le Site 2 pour ouvrir le vote...")
        driver.execute_script(f"""
            var links = document.querySelectorAll('a[data-vote-id]');
            links.forEach(a => {{
                if(a.href.includes('{SITE_CIBLE}')) a.click();
            }});
        """)
        
        # On attend qu'un nouvel onglet apparaisse
        time.sleep(5)
        
        # 4. Simulation du retour sur l'onglet principal (Switch)
        print("Retour sur l'onglet Pixworld pour débloquer Orion...")
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                driver.close() # On ferme l'onglet de vote (on s'en fout)
        
        driver.switch_to.window(main_window) # On revient sur Pixworld
        time.sleep(5) # On laisse le temps aux boutons Helios/Orion d'apparaître

        # 5. Clic sur le bouton Orion
        print("Recherche du bouton Orion...")
        # On essaie plusieurs méthodes pour cliquer sur Orion
        try:
            # On attend que le bouton soit cliquable
            orion_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Orion')]")))
            driver.execute_script("arguments[0].click();", orion_btn)
            print("✅ Orion a été cliqué ! Récompense récupérée.")
        except:
            print("⚠️ Bouton Orion non trouvé via XPATH, tentative via script global...")
            driver.execute_script("""
                document.querySelectorAll('button, a, div, span').forEach(el => {
                    if(el.innerText.includes('Orion')) el.click();
                });
            """)

        time.sleep(5)
        print("Opération terminée avec succès. ✅")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
