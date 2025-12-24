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
    
    try:
        print("Démarrage du mode 'Injection Synchronisée'...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        wait = WebDriverWait(driver, 40)

        # 1. Connexion
        print("Accès à la page de connexion...")
        driver.get("https://pixworld.fr/login")
        
        # On attend que le champ email soit VRAIMENT là avant d'injecter
        print("Attente de l'apparition des champs...")
        wait.until(EC.presence_of_element_located((By.NAME, "email")))
        time.sleep(5) # Petite pause sécurité pour le chargement des scripts du site

        print("Injection sécurisée des identifiants...")
        # On utilise une méthode plus sûre pour cibler les champs
        js_fill = f"""
            var emailField = document.querySelector('input[name="email"]');
            var passField = document.querySelector('input[name="password"]');
            if(emailField && passField) {{
                emailField.value = '{EMAIL}';
                passField.value = '{PASSWORD}';
                return true;
            }}
            return false;
        """
        success = driver.execute_script(js_fill)
        
        if success:
            print("Champs remplis ! Envoi du formulaire...")
            driver.execute_script("document.querySelector('form').submit();")
        else:
            print("Erreur : Champs introuvables lors de l'injection.")
            return

        print("Connexion envoyée ! Attente de redirection (25s)...")
        time.sleep(25)

        # 2. Passage au vote
        print("Direction la page de vote...")
        driver.get("https://pixworld.fr/vote")
        time.sleep(12)

        # 3. Récupération Orion (Le but final !)
        print("Tentative de clic sur Orion...")
        # On cherche tous les éléments qui contiennent le mot 'Orion' et on clique
        driver.execute_script("""
            var elements = document.querySelectorAll('button, a, span, div');
            elements.forEach(function(el) {
                if(el.innerText.includes('Orion')) {
                    el.click();
                    console.log('Clic Orion effectué');
                }
            });
        """)
        
        # 4. Vote de secours si Orion n'est pas là
        print("Recherche du lien de vote pour le serveur...")
        driver.execute_script(f"""
            document.querySelectorAll('a').forEach(a => {{
                if(a.href.includes('{SITE_CIBLE}')) a.click();
            }});
        """)
        
        print("Attente finale (10s)...")
        time.sleep(10)
        print("Procédure terminée avec succès ! ✅")

    except Exception as e:
        print(f"Erreur pendant l'exécution : {e}")
    
    finally:
        if 'driver' in locals():
            driver.quit()
        print("Session terminée.")

if __name__ == "__main__":
    run_bot()
