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
    # On utilise un User-Agent de Chrome très récent pour éviter le flag "Bot"
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    driver = None
    try:
        print("⚡ [Phase 1] Connexion Flash...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # Accès direct au login
        driver.get("https://pixworld.fr/login")
        time.sleep(7) # Temps minimum pour que les champs existent

        # Injection brutale : on ne cherche pas à imiter l'humain, on remplit et on valide
        driver.execute_script(f"""
            var e = document.querySelector('input[name="email"]');
            var p = document.querySelector('input[name="password"]');
            var b = document.querySelector('button[type="submit"]');
            if(e && p) {{
                e.value = '{EMAIL}';
                p.value = '{PASSWORD}';
                if(b) b.click();
            }}
        """)
        
        print("🚀 [Phase 2] Saut direct vers le vote...")
        time.sleep(8) 
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)
        
        # Déclenchement du vote Site 2
        driver.execute_script(f"var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}')); if(a) a.click();")
        
        print("⌛ [Phase 3] Attente d'assimilation (120s)...")
        # On ne touche plus à rien pendant 2 minutes. On laisse le serveur bosser.
        time.sleep(120)

        # Clic Orion
        print("🎯 Tentative finale sur Orion...")
        success = driver.execute_script("""
            var targets = Array.from(document.querySelectorAll('button, a, span, div, .btn'));
            var orion = targets.find(el => el.innerText && el.innerText.trim().toUpperCase() === 'ORION');
            if(orion) {
                orion.click();
                return true;
            }
            return false;
        """)

        if success:
            print("✨ VICTOIRE : Orion a été cliqué !")
        else:
            driver.save_screenshot("derniere_chance_debug.png")
            print("❌ Orion introuvable. Fin de la tentative.")

    except Exception as e:
        print(f"💥 Erreur : {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
