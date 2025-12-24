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
        print("🚀 Mode Héritage & Diagnostic (Lecture du DOM)...")
        driver = uc.Chrome(options=options, browser_executable_path='/usr/bin/google-chrome')
        
        # 1. Login
        driver.get("https://pixworld.fr/vote")
        time.sleep(10)
        main_window = driver.current_window_handle
        driver.execute_script(f"document.querySelectorAll('input').forEach(i => {{ if(i.type === 'email') i.value = '{EMAIL}'; if(i.type === 'password') i.value = '{PASSWORD}'; }}); var b = document.querySelector('button[type=\"submit\"]'); if(b) b.click();")
        time.sleep(15)

        # 2. Vote (Site 2)
        driver.execute_script(f"var a = Array.from(document.querySelectorAll('a')).find(el => el.href.includes('{SITE_CIBLE}')); if(a) {{ a.target = '_blank'; a.click(); }}")
        time.sleep(15)

        # 3. Retour et Scan de Diagnostic
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(main_window)

        # ANALYSE DU CONTENU (Pour comprendre pourquoi il ne trouve pas)
        page_text = driver.execute_script("return document.body.innerText;")
        if "déjà voté" in page_text.lower():
            print("📢 Info : Le site dit que tu as déjà voté.")
        elif "attendez" in page_text.lower() or "secondes" in page_text.lower():
            print("📢 Info : Un compte à rebours est visible.")
        
        # 4. TENTATIVE DE CLIC PAR "SÉLECTEUR UNIVERSEL"
        # On cherche tous les boutons verts (btn-success) même sans texte
        print("Tentative de clic sur tous les boutons de succès...")
        driver.execute_script("""
            var buttons = document.querySelectorAll('.btn-success, .btn-primary, button, .btn');
            buttons.forEach(btn => {
                if(btn.innerText.includes('Orion') || (btn.innerText.length > 0 && btn.innerText.length < 15)) {
                    btn.click();
                }
            });
        """)
        
        time.sleep(5)
        print("Fin du diagnostic. ✅")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
