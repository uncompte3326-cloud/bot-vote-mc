import os
import time
import undetected_chromedriver as uc

# --- CONFIGURATION ---
EMAIL = os.environ.get('MY_EMAIL')
PASSWORD = os.environ.get('MY_PASSWORD')
SITE_CIBLE = "serveur-minecraft.com"

def run_bot():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    # On utilise un User-Agent très spécifique
    options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
    
    driver = None
    try:
        print("🎭 Initialisation de la navigation discrète...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # Étape A : On arrive par l'accueil (plus "humain" qu'un accès direct au login)
        print("Accès à l'accueil...")
        driver.get("https://pixworld.fr/")
        time.sleep(15)

        # Étape B : Navigation vers le login via URL mais avec un délai
        print("Transition vers l'espace membre...")
        driver.get("https://pixworld.fr/login")
        time.sleep(25) # On laisse le temps au serveur de nous "accepter"

        # Étape C : Injection par petits blocs pour éviter les blocages JS
        print("Tentative d'identification...")
        driver.execute_script(f"""
            var inputs = document.getElementsByTagName('input');
            for(var i=0; i<inputs.length; i++){{
                if(inputs[i].type == 'email' || inputs[i].name == 'email') inputs[i].value = '{EMAIL}';
            }}
        """)
        time.sleep(5)
        driver.execute_script(f"""
            var inputs = document.getElementsByTagName('input');
            for(var i=0; i<inputs.length; i++){{
                if(inputs[i].type == 'password' || inputs[i].name == 'password') inputs[i].value = '{PASSWORD}';
            }}
            var btn = document.querySelector('button[type="submit"]');
            if(btn) btn.click();
        """)
        
        print("Connexion envoyée. Longue pause d'assimilation (30s)...")
        time.sleep(30)

        # Étape D : Vote et Orion
        print("Lancement de la procédure de vote...")
        driver.get("https://pixworld.fr/vote")
        time.sleep(15)
        
        # Clic Site 2
        driver.execute_script(f"var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}')); if(a) a.click();")
        
        print("⌛ Vote effectué. Guet final pour Orion (90s)...")
        # On attend 90 secondes sans bouger, en vérifiant Orion
        for i in range(30):
            success = driver.execute_script("""
                var el = Array.from(document.querySelectorAll('*'))
                              .find(e => e.innerText && e.innerText.trim().toUpperCase() === 'ORION');
                if(el) { el.click(); return true; }
                return false;
            """)
            if success:
                print(f"🎯 VICTOIRE ! Orion a été débloqué et cliqué.")
                break
            time.sleep(3)

        driver.save_screenshot("resultat_discret.png")
        print("Opération terminée. ✅")

    except Exception as e:
        print(f"❌ Échec de la navigation : {e}")
        if driver: driver.save_screenshot("debug_discret.png")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
