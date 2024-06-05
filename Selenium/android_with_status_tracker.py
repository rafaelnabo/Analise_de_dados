import time
import random
import selenium_instabot as instabot
import adb_scripts
from settings import contas_ativas
#Kill and start adb
adb_scripts.connect(50462)


def seguir_alvo(alvo):
    adb_scripts.adb.aa_open_website(rf'https://www.instagram.com/{alvo}/')
    time.sleep(random.uniform(4, 6))
    #First photo in second line (1,2)
    adb_scripts.adb.aa_input_tap(int(random.uniform(70, 445)), int(random.uniform(1050, 1100)))
    time.sleep(random.uniform(3, 5))
    #Follow Buttom
    adb_scripts.adb.aa_input_tap(random.uniform(800, 850), random.uniform(65, 80))
    #Save
    instabot.df.loc[alvo, 'status_in'] = 'Seguido'
    instabot.df.to_csv('C:\Projeto Instagram\V3\dataset.csv')

tracker = instabot.Instabot()
tracker.logar()


#Initial Y
dy = 90
y0 = 240
for conta in contas_ativas:
    #Change acc
    adb_scripts.adb.aa_swipe(804,1484,806,1487,1.5)
    time.sleep(5)
    adb_scripts.take_ss()
    ocr = adb_scripts.ocr()
    y = y0 + dy*ocr.index(conta)
    #click x,y
    print(f'{conta}(500, {y})')
    adb_scripts.adb.aa_input_tap(random.uniform(150, 350), y)
    time.sleep(random.uniform(5,6))
    for _ in range(100):
        #Check client status
        alvo = instabot.cliente_valido(tracker)
        seguir_alvo(alvo)
    time.sleep(random.uniform(5,7))