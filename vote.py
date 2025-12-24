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
    # Identité humaine renforcée
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
    
    driver = None
    try:
        print("🎭 Connexion en mode Identité Humaine...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # 1. Login
        driver.get("https://pixworld.fr/login")
        time.sleep(15) # Temps de chargement complet
        
        driver.execute_script(f"""
            var inputs = document.querySelectorAll('input');
            inputs.forEach(i => {{
                if(i.type === 'email' || i.name === 'email') i.value = '{EMAIL}';
                if(i.type === 'password' || i.name === 'password') i.value = '{PASSWORD}';
            }});
            var btn = document.querySelector('button[type="submit"]');
            if(btn) btn.click();
        """)
        print("Identifiants envoyés. Attente de stabilisation de la session...")
        time.sleep(12)

        # 2. Vote
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)
        
        # Clic Site 2
        driver.execute_script(f"var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}')); if(a) a.click();")
        print("Vote Site 2 effectué. Le serveur prépare Orion...")
        time.sleep(25) # On laisse au serveur Minecraft le temps de recevoir l'info de vote

        # 3. Sniper Orion
        print("🎯 Scan final pour Orion...")
        found = False
        for i in range(15):
            success = driver.execute_script("""
                var elements = document.querySelectorAll('*');
                for (var el of elements) {
                    if (el.innerText && el.innerText.trim().toUpperCase() === 'ORION') {
                        el.scrollIntoView({block: "center"});
                        el.click();
                        // On clique aussi sur le parent pour être sûr (si c'est un bouton stylisé)
                        if (el.parentElement) el.parentElement.click();
                        return true;
                    }
                }
                return false;
            """)
            if success:
                print(f"✨ RÉUSSITE : Orion cliqué à la tentative {i+1} !")
                found = True
                break
            time.sleep(2)

        if not found:
            print("❌ Bouton introuvable. On prend une photo pour comprendre.")
            driver.save_screenshot("debug_orion_final.png")

        print("Workflow terminé. ✅")

    except Exception as e:
        print(f"💥 Erreur : {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
