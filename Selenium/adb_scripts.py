from adbkit import ADBTools
import time
import subprocess
import requests
import settings

def connect():
    ADBTools.aa_kill_all_running_adb_instances()
    global adb
    adb_path = r"C:\platform-tools\adb.exe"
    deviceserial = f'{settings.connect}'
    adb = ADBTools(adb_path=adb_path,
                deviceserial=deviceserial)

    adb.aa_start_server()
    time.sleep(3)
    adb.aa_connect_to_device()

    #Screenshots
def take_ss():
    try:
        subprocess.run([r'C:\platform-tools\adb.exe', 'shell', 'screencap', '/sdcard/screenshot.png'])

        subprocess.run([r'C:\platform-tools\adb.exe', 'pull', '/sdcard/screenshot.png', 'screenshot.png'])

        print("Captura de tela salva como 'screenshot.png'")
    except Exception as e:
        print(f"Erro ao capturar a tela: {e}")

#Read img's words
def ocr():
    #OCR.space API
    api_key = settings.api_key

    # URL API OCR.space
    api_url = 'https://api.ocr.space/parse/image'

    # Output img
    image_path = 'screenshot.png'

    # Request Settings
    payload = {
        'apikey': api_key,
        'language': 'por',  # Language
    }

    # Load and send image
    with open(image_path, 'rb') as image_file:
        result = requests.post(api_url, files={'image': image_file}, data=payload)    
    
    # Parse JSON
    if result.status_code == 200:
        json_result = result.json()
        lista = []
        saida = []
        if 'ParsedResults' in json_result:
            
            for item in json_result['ParsedResults']:
                text = item['ParsedText']
                lista.append(text.lower().split('\r\n'))
            for item in lista[0]:
                if item in settings.contas_ativas:
                    saida.append(item)
            return saida
        else:
            print('Nenhum texto foi encontrado na imagem.')
    else:
        print(f'Erro na solicitação: {result.status_code}')

def get_uframe(screenshotfolder="c:\\ttscreenshots"):
    adb.aa_update_screenshot()
    return adb.aa_get_all_displayed_items_from_uiautomator(
        screenshotfolder=screenshotfolder,  # screenshots will be saved here
        max_variation_percent_x=10,
        # used for one of the click functions, to not click exactly in the center - more information below
        max_variation_percent_y=10,  # used for one of the click functions, to not click exactly in the center
        loung_touch_delay=(
            1000,
            1500,
        ),  # with this settings longtouch will take somewhere between 1 and 1,5 seconds
        swipe_variation_startx=10,  # swipe coordinate variations in percent
        swipe_variation_endx=10,
        swipe_variation_starty=10,
        swipe_variation_endy=10,
        sdcard="/storage/emulated/0/",
        # sdcard will be used if you use the sendevent methods, don't pass a symlink - more information below
        tmp_folder_on_sd_card="AUTOMAT",  # this folder will be created in the sdcard folder for using sendevent actions
        bluestacks_divider=32767,
    )