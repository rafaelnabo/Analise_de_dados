from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from webdriver_manager.chrome import ChromeDriverManager
import time
#from bs4 import BeautifulSoup
import json
import random
import datetime
import pandas as pd
import sys
from selenium.webdriver.firefox.options import Options

hoje = datetime.datetime.today().strftime('%d-%m-%Y')
df = pd.read_csv('C:\Projeto Instagram\V3\dataset.csv')
df.set_index('username', inplace=True)

def get_client():       
    calvo = df[(df.status_in != 'Commit') & (df.status_in != 'Venda') & (df.status_in != 'SOLICITADO') & (df.status_in != 'Ocupado') & (df.status_in != 'Seguir')].sample(1)
    df.loc[calvo.index[0], 'status_in'] = 'Ocupado'
    #df.loc[calvo.index[0], 'last_interactive'] = hoje
    return calvo.index[0]

def load_accounts(arquivo):
    try:
        with open(arquivo, "r") as file:
            accounts = json.load(file)
            
    except FileNotFoundError:
        accounts = []
    return accounts

dados = load_accounts('accounts.json')[0]


#Codigo do bot
class Instabot:

    def __init__(self, dados = dados):
        self.firefox_options = Options()
        #self.browser = webdriver.Chrome(ChromeDriverManager().install())
        #self.firefox_options.add_argument('-headless')
        #self.chrome_options.add_argument(f'--proxy-server={proxy}')
        self.email = dados.get('username', None)
        self.passw = dados.get('password', None)
        self.repre = dados.get('repre', None)
        self.browser = webdriver.Firefox(options=self.firefox_options)
        self.wait =  WebDriverWait(self.browser, 5)
    
    def login(self):
        self.browser.get("https://www.instagram.com/")
        usuario = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        senha = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
        usuario.send_keys(self.email)
        time.sleep(0.5)
        senha.send_keys(self.passw)
        time.sleep(1)
        senha.send_keys(Keys.ENTER)
        time.sleep(6)

        self.check = self.browser.find_elements(By.CSS_SELECTOR, "input[name='username']")
        if self.check:
            return 0
        else:
            return 1
    #validar login _ac8f

    def logar(self):
        logar = 0
        while not logar:
            try:
                self.login()
            except:
                pass
            if self.browser.find_elements(By.CSS_SELECTOR, "input[name='username']"):
                logar = 0
            else:
                logar = 1
    def skip_ban(self):
            try:
                self.browser.find_elements(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/section/main/div[2]/div/div/div[2]/div/div[1]')[0].click()
            except:
                pass
            try:
                self.browser.find_elements(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/section/main/div[2]/div/div/div[2]/div/div[1]/div')[0].click()
            except:
                pass 

    def seguir(self):
        if self.browser.find_elements(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div/button/div')[0].text == 'Seguir':
            try:
                self.browser.find_elements(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div/button/div')[0].click()
                time.sleep(3)
                return 1
            except:
                return 0
        else:
            return 0
    

           

def bot(contas):
    return [Instabot(conta) for conta in contas]

def cliente_valido(navegador):
        client_valido = 0
        
        while client_valido == 0:
            alvo = get_client()
            try:
                navegador.browser.get(f'https://instagram.com/{alvo}')
            except:
                pass
            time.sleep(4)
            try:
                Ban = navegador.browser.find_elements(By.CLASS_NAME, '_abya')
                pag_n_carrega = navegador.browser.find_elements(By.CLASS_NAME, 'xw7yly9')
            except:
                Ban = 0
                pag_n_carrega = 0
            if (Ban) or (pag_n_carrega):
                client_valido = 1
                navegador.skip_ban()
                time.sleep(5)
            else:
                try:
                    publi = int(navegador.browser.find_elements(By.CLASS_NAME, '_ac2a')[0].text)
                except:
                    publi = 0
                try:
                    if publi >6:
                        client_valido = 1
                        check_pv = navegador.browser.find_elements(By.CLASS_NAME, '_aa_u')
                        for item in check_pv:
                            if item.text == 'Esta conta é privada':
                                #return alvo
                                client_valido = 0
                                
                except:
                    pass
        return alvo