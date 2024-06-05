import pandas as pd
import adb_scripts
import time
import selenium_instabot as instabot
import random
import settings
import sys
import os
import subprocess


adb_scripts.connect()
adb = adb_scripts.adb

def loop(loop_count):
    alvos = []
    for _ in range(loop_count):    
        alvo = instabot.get_client()
        sys.stdout = open(os.devnull, 'w')
        adb.aa_open_website(rf'https://www.instagram.com/{alvo}/')
        time.sleep(random.uniform(7,12))
        
        df_tmp = adb_scripts.get_uframe()
        try:
            x = list(df_tmp[(df_tmp.bb_area == 18816.0)&(df_tmp.bb_center_x < 300)].bb_center_x)[0]
            y = list(df_tmp[(df_tmp.bb_area == 18816.0)&(df_tmp.bb_center_x < 300)].bb_center_y)[0]
            adb.aa_input_tap(random.uniform((x-150), (x+150)), random.uniform((y-15),(y+15)))
            instabot.df.loc[alvo, 'status_in'] = 'Seguir'
            time.sleep(random.uniform(7,10))
        except:
            pass
        alvos.append(alvo)
        sys.stdout = sys.__stdout__
    return alvos


y0 = 150
x = 150
dy = 90
for _ in range(2):
    for nome in settings.contas_ativas:
        if nome not in settings.ban_list:
            adb.aa_input_tap(90,1500)
            time.sleep(3)
            adb.aa_swipe(810,1494,811,1495,1.1)
            time.sleep(5)
            adb_scripts.take_ss()
            time.sleep(5)
            ordem = adb_scripts.ocr()
            
            time.sleep(3)
            try:
                y = y0 + (dy*int(ordem.index(nome)))
                print(f'{nome}: {x},{y}')
                adb.aa_input_tap(x,y)
                time.sleep(5)
            except:
                with open('arquivo.txt', 'w') as arquivo:
                    arquivo.write(f"{nome}({instabot.hoje})\n")
            loop(25)
            
            instabot.df.to_csv('C:\Projeto Instagram\V3\dataset.csv')

