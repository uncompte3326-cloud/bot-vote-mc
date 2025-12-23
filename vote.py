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
    options.add_argument('--headless')  # Indispensable sur GitHub
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # On initialise le driver indétectable
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 25)

    try:
        # 1. Connexion
        print("Accès à la page de connexion...")
        driver.get("https://pixworld.fr/login")
        time.sleep(8) # On laisse le temps au camouflage de s'activer

        print("Remplissage des identifiants...")
        # On utilise les noms exacts des champs
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_field.send_keys(EMAIL)
        
        pass_field = driver.find_element(By.NAME, "password")
        pass_field.send_keys(PASSWORD)
        
        btn_login = driver.find_element(By.XPATH, "//button[contains(text(), 'Connexion')]")
        driver.execute_script("arguments[0].click();", btn_login)
        print("Formulaire envoyé !")
        time.sleep(5)

        # 2. Page de vote
        print("Navigation vers /vote...")
        driver.get("https://pixworld.fr/vote")
        time.sleep(5)

        # 3. Vérification du bouton Orion (ton cas actuel)
        print("Vérification si Orion est déjà prêt...")
        try:
            # On cherche le bouton vert Orion de ton image #8
            btn_orion = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Orion')]")))
            driver.execute_script("arguments[0].click();", btn_orion)
            print("Bouton Orion cliqué ! ✅")
            time.sleep(5)
            print("Récompense validée !")
            return # On s'arrête là si ça a marché
        except:
            print("Orion n'est pas apparu direct, on tente de cliquer sur le site de vote...")

        # 4. Si Orion n'était pas là, on clique sur le site de vote
        links = driver.find_elements(By.CSS_SELECTOR, "a[data-vote-id]")
        for link in links:
            if SITE_CIBLE in link.get_attribute("href"):
                driver.execute_script("arguments[0].click();", link)
                print("Lien vers serveur-minecraft cliqué !")
                break
        
        # On attend que Pixworld détecte le clic et affiche Orion
        time.sleep(15)
        btn_orion_final = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Orion')]")))
        driver.execute_script("arguments[0].click();", btn_orion_final)
        print("Bouton Orion cliqué après vote ! ✅")

    except Exception as e:
        print(f"Erreur pendant l'exécution : {e}")
        # En cas d'erreur, on enregistre une capture d'écran pour voir le blocage
        driver.save_screenshot
