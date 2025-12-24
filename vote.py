import os
import time
import random
import undetected_chromedriver as uc

# --- CONFIGURATION ---
EMAIL = os.environ.get('MY_EMAIL')
PASSWORD = os.environ.get('MY_PASSWORD')
SITE_CIBLE = "serveur-minecraft.com"

def human_pause(min_s=5, max_s=10):
    """Fait une pause aléatoire pour imiter un humain."""
    pause = random.uniform(min_s, max_s)
    print(f"⏳ Pause humaine de {pause:.1f}s...")
    time.sleep(pause)

def run_bot():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
    
    driver = None
    try:
        print("👤 Lancement du bot avec pauses humaines...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # 1. CONNEXION
        driver.get("https://pixworld.fr/login")
        human_pause(8, 12) # Laisse le temps aux scripts de tracking de charger
        
        print("Saisie des identifiants...")
        driver.execute_script(f"""
            document.querySelector('input[name="email"]').value = '{EMAIL}';
            document.querySelector('input[name="password"]').value = '{PASSWORD}';
        """)
        human_pause(2, 4) # Pause entre saisie et clic
        driver.execute_script("document.querySelector('button[type=\"submit\"]').click();")
        
        print("Attente post-connexion (assimilation session)...")
        human_pause(15, 20) # Très important pour que le cookie de session soit "digéré"

        # 2. VOTE
        driver.get("https://pixworld.fr/vote")
        human_pause(10, 15)
        
        print("Clic sur le Site 2...")
        driver.execute_script(f"var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}')); if(a) a.click();")
        
        print("Attente critique : Le site de vote communique avec Pixworld...")
        human_pause(40, 50) # On laisse presque une minute pour que l'API de vote valide l'IP

        # 3. RÉCUPÉRATION ORION (Sans rafraîchir)
        print("Recherche du bouton Orion...")
        # On tente de le trouver sans rafraîchir pendant encore 1 minute
        found = False
        for _ in range(20):
            success = driver.execute_script("""
                var el = Array.from(document.querySelectorAll('button, a, div, span'))
                              .find(e => e.innerText && e.innerText.trim().toUpperCase() === 'ORION');
                if(el) {
                    el.click();
                    return true;
                }
                return false;
            """)
            if success:
                print("🎯 Orion trouvé et cliqué !")
                found = True
                break
            time.sleep(5) # Petite pause entre chaque vérification visuelle

        if not found:
            print("❌ Toujours pas d'Orion après les pauses. Diagnostic final...")
            driver.save_screenshot("human_pause_debug.png")

        print("Opération terminée. ✅")

    except Exception as e:
        print(f"💥 Erreur : {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
