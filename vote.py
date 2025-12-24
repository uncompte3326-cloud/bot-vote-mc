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
    
    driver = None
    try:
        print("🚀 Lancement du protocole d'injection directe...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # 1. On va sur la page et on attend simplement 15s qu'elle soit là
        driver.get("https://pixworld.fr/login")
        time.sleep(15)
        
        # On injecte et on clique en UNE SEULE FOIS en JavaScript
        # C'est la méthode la plus puissante pour contourner les erreurs de 'null'
        print("Tentative d'injection forcée des identifiants...")
        driver.execute_script(f"""
            var mail = document.querySelector('input[name="email"]') || document.querySelector('input[type="email"]');
            var pass = document.querySelector('input[name="password"]') || document.querySelector('input[type="password"]');
            var btn = document.querySelector('button[type="submit"]') || document.querySelector('.btn-primary');
            
            if(mail && pass && btn) {{
                mail.value = '{EMAIL}';
                pass.value = '{PASSWORD}';
                btn.click();
                return "Injecté";
            }}
            return "Champs introuvables";
        """)
        
        time.sleep(10) # Attente redirection

        # 2. On fonce sur la page de vote
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)
        
        # On clique sur le site de vote
        driver.execute_script(f"var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}')); if(a) a.click();")
        print("Vote Site 2 envoyé...")
        time.sleep(15)

        # 3. On cherche Orion avec un sélecteur très large
        print("Recherche finale du bouton Orion...")
        for i in range(15):
            success = driver.execute_script("""
                var targets = Array.from(document.querySelectorAll('button, a, .btn, span, div, h5'));
                var orion = targets.find(b => b.innerText && b.innerText.trim().toUpperCase() === 'ORION');
                if(orion) {
                    orion.scrollIntoView();
                    orion.click();
                    return true;
                }
                return false;
            """)
            if success:
                print(f"🎯 VICTOIRE ! Orion a été activé à la tentative {i+1}.")
                break
            time.sleep(2)

        driver.save_screenshot("final_attempt.png")
        print("Fin du workflow. ✅")

    except Exception as e:
        print(f"❌ Erreur critique : {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
