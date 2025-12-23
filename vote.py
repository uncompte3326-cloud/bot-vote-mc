import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
PSEUDO = "TON_PSEUDO_ICI"  # <--- REMPLACE PAR TON PSEUDO
# ---------------------

options = Options()
options.add_argument('--headless') # Pour que ça tourne en arrière-plan
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

driver = webdriver.Chrome(options=options)

try:
    # 1. Aller sur la page de vote
    print("Ouverture de Pixworld...")
    driver.get("https://pixworld.fr/vote")
    
    # Attendre un peu pour simuler un humain (+ variation 10min gérée par GitHub)
    time.sleep(random.randint(5, 15))

    # 2. Entrer le pseudo
    print(f"Saisie du pseudo : {PSEUDO}")
    input_pseudo = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "step-1-user"))
    )
    input_pseudo.send_keys(PSEUDO)
    
    # 3. Cliquer sur le bouton pour passer à l'étape suivante
    print("Passage à l'étape suivante...")
    btn_next = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    btn_next.click()
    
    time.sleep(3)

    # 4. Cliquer sur le premier site de vote (Top-Serveurs ou autre)
    print("Clic sur le bouton de vote...")
    # Sur Azuriom, c'est souvent le premier lien dans la liste
    vote_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-vote-id]"))
    )
    vote_link.click()
    
    print("Vote initié avec succès !")
    # Note : Le script s'arrête ici car on ne peut pas automatiser 
    # le site externe s'il y a un Captcha. Mais Pixworld validera 
    # souvent le vote après un délai.

finally:
    time.sleep(5)
    driver.quit()
    print("Navigateur fermé.")
