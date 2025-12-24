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
    # Identité Chrome Windows standard pour éviter le flag GitHub
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    driver = None
    try:
        print("⚡ [1/3] Connexion Flash (Injection Instantanée)...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # On fonce direct sur le login
        driver.get("https://pixworld.fr/login")
        time.sleep(8) 

        # Injection JS brutale pour éviter d'être repéré par le clavier
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
        
        print("🚀 [2/3] Saut direct vers la zone de vote...")
        time.sleep(10) 
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)
        
        # On déclenche le vote sur le Site 2
        driver.execute_script(f"var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}')); if(a) a.click();")
        
        print("⌛ [3/3] Phase d'assimilation critique (120 secondes)...")
        # On ne touche plus à rien, on laisse le serveur Minecraft et Pixworld se synchroniser
        time.sleep(120)

        # Tentative finale sur Orion
        print("🎯 Scan final pour le bouton Orion...")
        success = driver.execute_script("""
            var elements = Array.from(document.querySelectorAll('button, a, span, div, .btn'));
            var target = elements.find(el => el.innerText && el.innerText.trim().toUpperCase() === 'ORION');
            if(target) {
                target.scrollIntoView({block: 'center'});
                target.click();
                return true;
            }
            return false;
        """)

        if success:
            print("✨ VICTOIRE : Le bouton Orion a été activé !")
        else:
            driver.save_screenshot("ultimate_check.png")
            print("❌ Orion est resté introuvable. Vérifie 'ultimate_check.png'.")

    except Exception as e:
        print(f"💥 Erreur fatale : {e}")
    finally:
        if driver: driver.quit()
        print("Fin du workflow. ✅")

if __name__ == "__main__":
    run_bot()
