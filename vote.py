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
        print("🚀 Démarrage du bot (Synchronisation Orion)...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        wait = WebDriverWait(driver, 30)

        # 1. Connexion avec vérification de présence
        print("Accès à la page de connexion...")
        driver.get("https://pixworld.fr/login")
        
        # On attend que l'input email soit présent avant d'injecter quoi que ce soit
        email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[name='email']")))
        print("Champs détectés, connexion en cours...")
        
        driver.execute_script(f"""
            document.querySelector('input[type="email"], input[name="email"]').value = '{EMAIL}';
            document.querySelector('input[type="password"], input[name="password"]').value = '{PASSWORD}';
            document.querySelector('form').submit();
        """)
        time.sleep(15) # On laisse le temps de se connecter

        # 2. Navigation vers la page de vote
        print("Direction la page de vote...")
        driver.get("https://pixworld.fr/vote")
        main_window = driver.current_window_handle

        # 3. Clic sur le Site 2 pour débloquer Orion
        print("Déclenchement du Site 2 (ouverture onglet)...")
        # On cherche le lien qui contient le site de vote
        driver.execute_script(f"""
            var links = document.querySelectorAll('a');
            links.forEach(a => {{
                if(a.href.includes('{SITE_CIBLE}')) {{
                    a.target = '_blank'; // On force l'ouverture dans un nouvel onglet
                    a.click();
                }}
            }});
        """)
        
        time.sleep(8) # On attend que l'onglet de vote charge un peu

        # 4. Retour sur l'onglet principal et fermeture des autres
        print("Retour sur Pixworld pour valider Orion...")
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                driver.close()
        
        driver.switch_to.window(main_window)
        time.sleep(5) # Temps pour que le script de Pixworld affiche Orion/Helios

        # 5. Clic sur le bouton Orion
        print("Ciblage du bouton Orion...")
        # On utilise un script pour cliquer sur Orion peu importe sa forme (bouton ou lien)
        orion_found = driver.execute_script("""
            var elements = document.querySelectorAll('button, a, span, div');
            for (var el of elements) {
                if(el.innerText && el.innerText.includes('Orion')) {
                    el.click();
                    return true;
                }
            }
            return false;
        """)

        if orion_found:
            print("✅ Orion a été cliqué ! Vote validé.")
        else:
            print("⚠️ Bouton Orion non trouvé. Tentative de rafraîchissement...")
            driver.refresh()
            time.sleep(5)
            driver.execute_script("document.querySelectorAll('*').forEach(el => { if(el.innerText && el.innerText.includes('Orion')) el.click(); });")

        print("Fin de la session. ✅")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    run_bot()
