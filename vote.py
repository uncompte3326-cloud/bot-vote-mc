import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION (REMPLIS ICI) ---
EMAIL = "uncompte.3326@gmail.com" 
PASSWORD = "Aug896//"
PSEUDO = "Calalalopy"
# ----------------------------------

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

driver = webdriver.Chrome(options=options)

try:
    # 1. Connexion au site
    print("Connexion à Pixworld...")
    driver.get("https://pixworld.fr/login")
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    time.sleep(3) # Attendre la connexion
    
    # 2. Aller sur la page de vote
    print("Direction page de vote...")
    driver.get("https://pixworld.fr/vote")
    
    # 3. Saisie du pseudo (si pas automatique)
    print(f"Vérification pseudo : {PSEUDO}")
    input_pseudo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "step-1-user")))
    input_pseudo.clear()
    input_pseudo.send_keys(PSEUDO)
    
    # 4. Bouton Etape Suivante
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)

    # 5. Clic sur le site de vote
    print("Clic sur le lien de vote...")
    vote_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-vote-id]")))
    vote_link.click()
    
    print("Robot a terminé son travail !")

finally:
    driver.quit()
