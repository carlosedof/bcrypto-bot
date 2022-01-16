import time

import cv2
import pyautogui
import requests
import platform
import sys
import discord
import win32gui, win32con
from discord.ext import tasks    
import os
from os.path import isfile
from threading import Thread
import config
import uuid
from PySimpleGUI import PySimpleGUI as sg
from multiprocessing import Process
from check_team_viewer import check_team_viewer
from close_list_go_farm import close_list_go_farm
from utils.randomness import add_random
from utils.date import date_formatted


def connect_wallet():
    now = time.time()
    print('::: connecting with wallet :::')
    connect_wallet_img = cv2.imread(r"assets/connectWallet.png")
    time_start = now
    connect_wallet_ref = pyautogui.locateCenterOnScreen(connect_wallet_img, confidence=0.9)
    while not connect_wallet_ref:
        connect_wallet_ref = pyautogui.locateCenterOnScreen(connect_wallet_img, confidence=0.9)
        time.sleep(1)
        if time.time() - time_start > 5 * 60:
            fresh_start()
    if connect_wallet_ref:
        pyautogui.click(connect_wallet_ref.x, connect_wallet_ref.y)
        pyautogui.click(connect_wallet_ref.x, connect_wallet_ref.y)
        time.sleep(0.7)
        pyautogui.click(connect_wallet_ref.x, connect_wallet_ref.y)
    print('::: accepting metamask :::')
    meta_img = cv2.imread(r"assets/acceptMeta.png")
    time_start = now
    authorize = pyautogui.locateCenterOnScreen(meta_img, confidence=0.8)
    while not authorize:
        authorize = pyautogui.locateCenterOnScreen(meta_img, confidence=0.8)
        time.sleep(1)
        if time.time() - time_start > 5 * 60:
            fresh_start()
    if authorize:
        pyautogui.click(authorize.x, authorize.y)
        pyautogui.click(authorize.x, authorize.y)


def change_page(next):
    chartitle_img = cv2.imread(r"assets/chartitle.png")
    x, y = pyautogui.locateCenterOnScreen(chartitle_img, confidence=0.9)
    if x and y:
        pyautogui.click(x, y)
        if next:
            pyautogui.move(0, 410)
            pyautogui.drag(0, -309, 2.3, button='left')
        else:
            pyautogui.move(0, 100)
            pyautogui.drag(0, 325, 2.3, button='left')
        time.sleep(1.6)

def check_network_error():
    print('::: verifying server unstable error... :::')
    errok_img = cv2.imread(r"assets/errorOk.png")
    error_ok = pyautogui.locateCenterOnScreen(errok_img, confidence=0.9)
    time.sleep(0.5)
    if error_ok:
        print('::: server error detected! :::')
        pyautogui.click(error_ok.x, error_ok.y)
        pyautogui.click(error_ok.x, error_ok.y)
        time.sleep(5)
        return True
    print('::: verifying connection error... :::')
    net_img = cv2.imread(r"assets/connectionError.png")
    network_error = pyautogui.locateCenterOnScreen(net_img, confidence=0.9)
    if network_error:
        print('::: connection error detected! :::')
        pyautogui.click(network_error.x, network_error.y)
        pyautogui.click(network_error.x, network_error.y)
        time.sleep(14.2)
        return True
    print('::: verifying multiple servers error... :::')
    mult_serv_img = cv2.imread(r"assets/multipleServer.png")
    multiple_servers = pyautogui.locateCenterOnScreen(mult_serv_img, confidence=0.9)
    if multiple_servers:
        print('::: multiple servers error detected :::')
        pyautogui.click(multiple_servers.x, multiple_servers.y)
        pyautogui.click(multiple_servers.x, multiple_servers.y)
        time.sleep(14.2)
        return True
    
        print('::: verifying problem login error... :::')
    probl_log_img = cv2.imread(r"assets/problemLogging.png")
    probl_log = pyautogui.locateCenterOnScreen(probl_log_img, confidence=0.9)
    if probl_log:
        print('::: login error detected :::')
        probl_logok_img = cv2.imread(r"assets/problemLoggingOk.png")
        probl_logok = pyautogui.locateCenterOnScreen(probl_logok_img, confidence=0.9)
        pyautogui.click(probl_logok.x, probl_logok.y)
        pyautogui.click(probl_logok.x, probl_logok.y)
        time.sleep(14.2)
        return True
    
    print('::: verifying not logged in error... :::')
    not_log_img = cv2.imread(r"assets/connectionError.png")
    not_logged_error = pyautogui.locateCenterOnScreen(not_log_img, confidence=0.9)
    if not_logged_error:
        print('::: not logged error detected :::')
        pyautogui.click(not_logged_error.x, not_logged_error.y)
        pyautogui.click(not_logged_error.x, not_logged_error.y)
        time.sleep(14.2)
        return True

    print('::: verifying if stuck in metamask window... :::')
    accept_img = cv2.imread(r"assets/acceptMeta.png")
    accept_img_ref = pyautogui.locateCenterOnScreen(accept_img, confidence=0.9)
    if accept_img_ref:
        print('::: found open metamask window, proceeding with reload and relogin :::')
        pyautogui.click(accept_img_ref.x, accept_img_ref.y)
        pyautogui.click(accept_img_ref.x, accept_img_ref.y)
        return True

    print('::: verifying if you are in the initial page (connect walled)... :::')
    initial_img = cv2.imread(r"assets/logo.png")
    initial_img_ref = pyautogui.locateCenterOnScreen(initial_img, confidence=0.9)
    if initial_img_ref:
        print('::: found initial page, proceeding with reload and relogin :::')
        pyautogui.click(initial_img_ref.x, initial_img_ref.y)
        pyautogui.click(initial_img_ref.x, initial_img_ref.y)
        return True
    print('::: no errors found! :::')
    return False

def get_focus():
    focus_img = cv2.imread(r"assets/coin.png")
    coin = pyautogui.locateCenterOnScreen(focus_img, confidence=0.9)
    if coin:
        pyautogui.click(coin.x, coin.y)
    logo_img = cv2.imread(r"assets/logo.png")
    logo = pyautogui.locateCenterOnScreen(logo_img, confidence=0.9)
    if logo:
        pyautogui.click(logo.x, logo.y)


def refresh_positions():
    print('::: to avoid idle logout...   :::')
    back_img = cv2.imread(r"assets/back.png")
    back = pyautogui.locateCenterOnScreen(back_img, confidence=0.9)
    if back:
        pyautogui.click(back.x, back.y)
        pyautogui.click(back.x, back.y)
    time.sleep(0.1)

def take_screenshot():
    chest_img = cv2.imread(r"assets/chest.png")
    chest = pyautogui.locateCenterOnScreen(chest_img, confidence=0.9)
    if chest:
        pyautogui.click(chest.x, chest.y)
        pyautogui.click(chest.x, chest.y)
    time.sleep(1.5)
    image = pyautogui.screenshot()
    image.save('print.png')
    close_bcoin_img = cv2.imread(r"assets/closeBcoin.png")
    close_bcoin = pyautogui.locateCenterOnScreen(close_bcoin_img, confidence=0.9)
    if close_bcoin:
        pyautogui.click(close_bcoin.x, close_bcoin.y)



def locate_characters(status):
    print('::: locating and moving ' + status + ' characters :::')
    time.sleep(0.5)
    reference_img = None
    if status == 'full':
        reference_img = cv2.imread(r"assets/full.png")
    if status == 'high':
        reference_img = cv2.imread(r"assets/high.png")
    if status == 'low':
        reference_img = cv2.imread(r"assets/low.png")
    locations = pyautogui.locateAllOnScreen(reference_img, confidence=0.9)
    last_item = None
    moved_qt = 0
    for location in locations:
        coords = pyautogui.center(location)
        if last_item is None or coords.y - last_item > 10:
            pyautogui.moveTo(coords.x, coords.y)
            if status == 'high' or status == 'full':
                if status == 'full':
                    pyautogui.move(75, 0)
                    pyautogui.click()
                    config.chars_added_in_cycle = config.chars_added_in_cycle + 1
                else:
                    if config.chars_added_in_cycle < 3:
                        pyautogui.move(140, 0)
                        pyautogui.click()
                        config.chars_added_in_cycle = config.chars_added_in_cycle + 1
            else:
                pyautogui.move(210, 0)
                pyautogui.click()
                moved_qt = moved_qt + 1
            time.sleep(0.5)
        last_item = coords.y
    return moved_qt


def check_full_heroes():
    count = 0
    while count <= 2:
        if count > 0:
            change_page(True)
        locate_characters('full')
        count = count + 1
    change_page(False)
    change_page(False)


def check_heroes(cycle_count):
    restAll_img = cv2.imread(r"assets/restAll.png")
    rest = pyautogui.locateCenterOnScreen(restAll_img, confidence=0.9)
    time.sleep(0.5)
    print('::: renewing work list  :::')
    if rest:
        pyautogui.click(rest.x, rest.y)
        pyautogui.click(rest.x, rest.y)
        time.sleep(3.5)
    config.chars_added_in_cycle = 0
    check_full_heroes()
    count = 0
    if cycle_count % 2 != 0 and config.chars_added_in_cycle < 3:
        change_page(True)
        change_page(True)
    while count <= 2 and config.chars_added_in_cycle < 3:
        if count > 0:
            if cycle_count % 2 != 0:
                change_page(False)
            else:
                change_page(True)
        locate_characters('high')
        count = count + 1


def fresh_start():
    now = time.time()
    print('::: to ensure our steps, reloading browser page  :::')
    pyautogui.keyDown('ctrl')
    time.sleep(0.3)
    pyautogui.keyDown('shift')
    time.sleep(0.3)
    pyautogui.keyDown('r')
    time.sleep(0.3)
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('shift')
    pyautogui.keyUp('r')
    time.sleep(1)
    pyautogui.press('f5')
    connect_wallet()
    time_start = now
    farm_img = cv2.imread(r"assets/farm.png")
    farm = pyautogui.locateCenterOnScreen(farm_img, confidence=0.9)
    while not authorize:
        farm = pyautogui.locateCenterOnScreen(farm_img, confidence=0.9)
        time.sleep(1)
        if time.time() - time_start > 5 * 60:
            fresh_start()
    print('::: sending to farm  :::')
    if farm:
        pyautogui.click(farm.x, farm.y)
    time.sleep(0.3)


def solve_errors():
    global window
    window.write_event_value('TASK_UPDATE', 'Looking for errors')
    print('::: looking for errors :::')
    check_team_viewer()
    get_focus()
    if check_network_error():
        fresh_start()


def prepare_routing_warning(routine):
    print('A routine is about to start in 3sec ' + routine)
    time.sleep(1)
    print('A routine is about to start in 2sec ' + routine)
    time.sleep(1)
    print('A routine is about to start in 1sec ' + routine)
    time.sleep(1)


def prepare_screen_shot():
    take_screenshot()



last = {
    "heroes": 0,
    "new_map": 0,
    "refresh_heroes": 0,
    "screen_shot": 0,
    "validate_account": 0,
    "cycle_count": 0,
}
validate_fail_attempts = 0

def heroes_cycle():
    global window
    now = time.time()
    prepare_routing_warning('HEROES')
    solve_errors()
    window.write_event_value('TASK_UPDATE', 'Manage heroes')
    go_char_list()
    last["heroes"] = now
    check_heroes(last["cycle_count"])
    last["cycle_count"] = last["cycle_count"] + 1
    close_list_go_farm()
    window.write_event_value('TASK_UPDATE', 'Idle')
    print(date_formatted() + ' - finished managing heroes.')

def refresh_cycle():
    global window
    now = time.time()
    prepare_routing_warning('REFRESH')
    solve_errors()
    window.write_event_value('TASK_UPDATE', 'Refreshing map')
    last["refresh_heroes"] = now
    refresh_positions()
    close_list_go_farm()
    window.write_event_value('TASK_UPDATE', 'Idle')
    print(date_formatted() + ' - finished anti idle.')

async def screenshot_cycle():
    global window
    now = time.time()
    prepare_routing_warning('SCREEN SHOT')
    solve_errors()
    last["screen_shot"] = now
    window.write_event_value('TASK_UPDATE', 'Taking screenshot')
    prepare_screen_shot()
    user = await client.fetch_user(194282818505801730)
    await user.send(file=discord.File('print.png'))
    if isfile('print.png'):
        os.remove('print.png')
    window.write_event_value('TASK_UPDATE', 'Idle')
    print(date_formatted() + ' - took screenshot')

async def validate_account_cycle():
    now = time.time()
    prepare_routing_warning('CHECK ACCOUNT VALIDITY')
    check_account_active()
    # os._exit(1)
    last["validate_account"] = now
    print(date_formatted() + ' - Validated account')


# locates game window - back btn and opens char list
def go_char_list():
    now = time.time()
    print(' ')
    print('::: moving to char list... :::')
    print(' ')
    back_img = cv2.imread(r"assets/back.png")
    back = pyautogui.locateCenterOnScreen(back_img, confidence=0.9)
    time.sleep(0.1)
    if back:
        pyautogui.click(back.x, back.y)
        pyautogui.click(back.x, back.y)
    time.sleep(0.1)
    heroes_img = cv2.imread(r"assets/heroes.png")
    time_start = now
    heroes = pyautogui.locateCenterOnScreen(heroes_img, confidence=0.9)
    while not heroes:
        heroes = pyautogui.locateCenterOnScreen(heroes_img, confidence=0.9)
        time.sleep(1)
        if time.time() - time_start > 5 * 60:
            fresh_start()
    if heroes:
        pyautogui.click(heroes.x, heroes.y)

async def manage_open_windows(cycle):
    bomb_open_windows = []
    try:
        def winEnumHandler( hwnd, ctx ):
            if win32gui.IsWindowVisible( hwnd ):
                print(win32gui.GetWindowText( hwnd ));
                if "Bombcrypto - Google Chrome" == win32gui.GetWindowText( hwnd ) or "Bombcrypto - Mozilla Firefox" == win32gui.GetWindowText( hwnd ) or "Bombcrypto - Opera" == win32gui.GetWindowText( hwnd ):
                    bomb_open_windows.append(hwnd)
        win32gui.EnumWindows( winEnumHandler, None )
    except:
        print('It was not possible to gather multiple Bombcrypto client windows. Bot will continue working but only for single client version. Verify if you are using Windows Operating System and if there are bombcrypto browser windows opened.')
    global window
    window.write_event_value('WINDOWS_DETECTED', len(bomb_open_windows))  # put a message into queue for GUI
    # SW_MINIMIZE
    for window_id in bomb_open_windows:
        win32gui.ShowWindow(window_id, win32con.SW_MINIMIZE)
    for window_id in bomb_open_windows:
        win32gui.SetForegroundWindow(window_id)
        # win32gui.ShowWindow(window_id, win32con.SW_MAXIMIZE)
        win32gui.ShowWindow(window_id, win32con.SW_RESTORE)
        time.sleep(0.5)
        if cycle == 'HEROES':
            heroes_cycle()
        elif cycle == 'REFRESH':
            refresh_cycle()
        elif cycle == 'SCREEN_SHOT':
            await screenshot_cycle()
        time.sleep(5)
        win32gui.ShowWindow(window_id, win32con.SW_MINIMIZE)
        time.sleep(1)
    for window_id in bomb_open_windows:
        win32gui.ShowWindow(window_id, win32con.SW_RESTORE)
    if len(bomb_open_windows) == 0:
        time.sleep(0.5)
        if cycle == 'HEROES':
            heroes_cycle()
        elif cycle == 'REFRESH':
            refresh_cycle()
        elif cycle == 'SCREEN_SHOT':
            await screenshot_cycle()


    
async def main():        
    now = time.time()
    global window
    try:
        global t
        if now - last["heroes"] > add_random(int(t['send_heroes_for_work']) * 60):
            await manage_open_windows('HEROES')
        should_refresh = now - last["refresh_heroes"] > add_random(int(t['refresh_heroes_positions']) * 60)
        should_refresh_after_heroes = now - last["heroes"] > add_random(int(t['refresh_heroes_positions']) * 60)
        if should_refresh and should_refresh_after_heroes:
            await manage_open_windows('REFRESH')

        if now - last["screen_shot"] > add_random(int(t['screen_shot']) * 60):
            await manage_open_windows('SCREEN_SHOT')

        if now - last["validate_account"] > add_random(int(t['validate_account']) * 60):
            window.write_event_value('TASK_UPDATE', 'Validating account key')
            await validate_account_cycle()
            window.write_event_value('TASK_UPDATE', 'Idle')

    except Exception as e:
        print(e)
        fresh_start()


def check_account_active_outside(code):
    print('Please wait. Validating your registration key...')
    data = {'pcUnique': uuid.UUID(int=uuid.getnode()), 
    'environmentInfo': platform.uname().system + 
        platform.uname().release + 
        platform.uname().node + 
        platform.uname().machine}
    r = requests.put('http://18.231.92.140/api/registrationKey/' + code, data =data)
    response = requests.get("http://18.231.92.140/api/registrationKey/isValid/" + code, params=data)
    global window2
    try:
        if r.status_code == 200 and response.json() == True:
            window2.write_event_value('KEY_VALIDATED', True)
        else:
            window2.write_event_value('KEY_VALIDATED', False)
    except:
        window2.write_event_value('KEY_VALIDATED', False)
    return response

def check_account_active():
    global window
    window.write_event_value('TASK_UPDATE', 'Validating account key')
    print('Please wait. Validating your registration key...')
    data = {'pcUnique': uuid.UUID(int=uuid.getnode()), 
    'environmentInfo': platform.uname().system + 
        platform.uname().release + 
        platform.uname().node + 
        platform.uname().machine}
    global ALREADY_INFORMED_KEY
    r = None
    response = None
    global validate_fail_attempts
    try:
        r = requests.put('http://18.231.92.140/api/registrationKey/' + ALREADY_INFORMED_KEY, data =data)
        response = requests.get("http://18.231.92.140/api/registrationKey/isValid/" + ALREADY_INFORMED_KEY, params=data)
    except:
        print('Error validating key, if there is 2 more subsequent unsuccessful attempts will close bot')
        validate_fail_attempts = validate_fail_attempts + 1
        if validate_fail_attempts > 2:
            window.write_event_value('ACTIVATION_STATUS', False)
            return False
    
    try:
        if r.status_code == 200 and response.json() == True:
            window.write_event_value('ACTIVATION_STATUS', True)
            validate_fail_attempts = 0
            return True
        else:
            validate_fail_attempts = validate_fail_attempts + 1
            if validate_fail_attempts > 2:
                window.write_event_value('ACTIVATION_STATUS', False)
                return False
            elif response.json() == True:
                window.write_event_value('ACTIVATION_STATUS', True)
                return True
            else:
                window.write_event_value('ACTIVATION_STATUS', False)
                return False
    except:
        window.write_event_value('ACTIVATION_STATUS', False)
        return False


client = discord.Client()


valid_account = True
@tasks.loop(seconds=2)
async def check_send_print():
    global valid_account
    global window
    window.write_event_value('TASK_UPDATE', 'Idle')
    global t
    t = {
        "send_heroes_for_work": get_config_value_by_property('MANAGE_HEROES'),
        "refresh_heroes_positions": get_config_value_by_property('ANTI_IDLE'),
        "screen_shot": get_config_value_by_property('SCREENSHOT'),
        "validate_account": 60
    }
    if valid_account:
        await main()




@client.event
async def on_message(message):
    if message.content.startswith('print'):
        image = pyautogui.screenshot()
        image.save('printA.png')
        user = await client.fetch_user(194282818505801730)
        await user.send(file=discord.File('printA.png'))
        if isfile('printA.png'):
            os.remove('printA.png')

    

def get_config_value_by_property(prop):
    my_file = open("configs.txt")
    content = my_file.read()
    key_values = content.splitlines()
    for k_val in key_values:
        if prop in k_val.split('=')[0]:
            return k_val.split('=')[1]



def edit_config_value_by_property(prop, new_val):
    my_file = open("configs.txt")
    content = my_file.read()
    key_values = content.splitlines()
    new_list = []
    to_edit = None
    for k_val in key_values:
        if prop in k_val.split('=')[0]:
            to_edit = k_val.split('=')[0]
        else:
            new_list = [*new_list, k_val]
    my_file_write = open("configs.txt", "w")
    new_str = prop + '=' + new_val + '\n'
    for n_list in new_list:
        new_str = new_str + n_list + '\n'
    my_file_write.write(new_str)


@client.event
async def on_ready():
    global window
    response = check_account_active()
    if response:
        check_send_print.start()
    else:
        print('Your registration key is not valid for this computer. It may be expired, not existent or has already been used in another computer. Please contact administration.');
        # os._exit(1)

    

def long_operation_thread(window):
    client.run('OTI4ODQ2OTA1MDY3MzMxNjM0.YdeuFw.selHKD1N56Tzo8-1JKUf757cjEo')


def bot_loop():
    global window
    first_run = True
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event.startswith('Start bot'):
            # window.Element('Start bot').update(disabled=True)
            window.Element('CURRENT_STATUS').update('Running')
            global bot_running
            if bot_running is False:
                print('Starting...')
                Thread(target=long_operation_thread, args=(window,), daemon=True).start()
            else:
                print('Bot is already running')
            bot_running = True
        elif event == 'WINDOWS_DETECTED':
            window.Element('WINDOWS_DETECTED').update(values[event])
        elif event == 'ACTIVATION_STATUS':
                if values[event] == True:
                    print('Account validated!')
                    window.Element('ACTIVATION_STATUS_VAL').update('VALID',text_color='lime', font=('Arial', 10, 'bold'))
                else:
                    global valid_account
                    valid_account = False
                    window.Element('ACTIVATION_STATUS_VAL').update('INVALID/EXPIRED',text_color='red', font=('Arial', 10, 'bold'))
                    window.Element('CURRENT_STATUS').update('Stopped')
                    window.Element('Start bot').update(disabled=True)
        elif event == 'ANTIIDLE_BTN':
            edit_config_value_by_property('ANTI_IDLE', values['ANTIIDLE'])
            window.Element('ANTIIDLE_LABEL').update(values['ANTIIDLE'] + 'm')
            window.Element('ANTIIDLE').update('')
        elif event == 'SCREENSHOT_BTN':
            edit_config_value_by_property('SCREENSHOT', values['SCREENSHOT'])
            window.Element('SCREENSHOT_LABEL').update(values['SCREENSHOT'] + 'm')
            window.Element('SCREENSHOT').update('')
        elif event == 'MANAGE_HEROES_BTN':
            edit_config_value_by_property('MANAGE_HEROES', values['MANAGE_HEROES'])
            window.Element('MANAGE_HEROES_LABEL').update(values['MANAGE_HEROES'] + 'm')
            window.Element('MANAGE_HEROES').update('')
        elif event == 'TASK_UPDATE':
            window.Element('TASK').update(values['TASK_UPDATE'])
    window.close()

def the_gui():
    """
    Starts and executes the GUI
    Reads data from a Queue and displays the data to the window
    Returns when the user exits / closes the window
    """
    sg.theme('Dark Blue 14')
    layout_header = [
        [sg.Text('Task: '), sg.Text('-',key='TASK')],
        [sg.Text('Game windows opened: ',justification='left'), sg.Text('-',key='WINDOWS_DETECTED',justification='left')],
    ]
    top_img_col = [
        [sg.Image("assets/bcoinIcon.png", size=(52, 52), key='-IMAGE_BCOIN-')]
    ]

    layout_footer = [
        [sg.Button('Exit', size=(15,1))]
    ]
    bot_img_col = [
        [sg.Image("assets/chest.png", size=(52, 52), key='-IMAGE_CHEST-')]
    ]

    configs_col_l1 = [
        [
            sg.Text('Anti idle refresh:', size=(13, 1)),
            sg.Text(get_config_value_by_property('ANTI_IDLE') + 'm', key='ANTIIDLE_LABEL'),
        ]
    ]
    configs_col_r1 = [
        [
            sg.Input(key='ANTIIDLE', size=(5, 1)),
            sg.Button('Change', key='ANTIIDLE_BTN')
        ]
    ]

    configs_col_l2 = [
        [
            sg.Text('Manage heroes:', size=(13, 1)),
            sg.Text(get_config_value_by_property('MANAGE_HEROES') + 'm', key='MANAGE_HEROES_LABEL'),
        ]
    ]
    configs_col_r2 = [
        [
            sg.Input(key='MANAGE_HEROES', size=(5, 1)),
            sg.Button('Change', key='MANAGE_HEROES_BTN')
        ]
    ]

    configs_col_l3 = [
        [
            sg.Text('Take screenshot:', size=(13, 1)),
            sg.Text(get_config_value_by_property('SCREENSHOT') + 'm', key='SCREENSHOT'),
        ]
    ]
    configs_col_r3 = [
        [
            sg.Input(key='SCREENSHOT', size=(5, 1)),
            sg.Button('Change', key='SCREENSHOT_BTN')
        ]
    ]
    activation_status_col = [
        [
            sg.Text('Activation status:'),
            sg.Text('-', key='ACTIVATION_STATUS_VAL',size=(15, 1), justification='center')
        ]
    ]



    layout = [
        [
            sg.Column(layout_header, element_justification='left',expand_x=True),
            sg.Column(top_img_col, element_justification='right')
        ],
        [
            sg.Text('Timers: ', font=('Arial', 10, 'bold'))
        ],
        [
            sg.Column(configs_col_l1, element_justification='left',expand_x=True),
            sg.Column(configs_col_r1, element_justification='right')
        ],
        [
            sg.Column(configs_col_l2, element_justification='left',expand_x=True),
            sg.Column(configs_col_r2, element_justification='right')
        ],
        [
            sg.Column(configs_col_l3, element_justification='left',expand_x=True),
            sg.Column(configs_col_r3, element_justification='right')
        ],
        [
            sg.Button('Start bot', bind_return_key=True, size=(15,1)),
            sg.Text('Stopped', size=(22, 1),key='CURRENT_STATUS'),
        ],
        [
            sg.Text('Logs:', font=('Arial', 10, 'bold'))],
        [
            # sg.Output(size=(45, 5))
        ],
        [
            sg.Column(bot_img_col, element_justification='left',expand_x=True),
            sg.Column(layout_footer, element_justification='right')
        ],
        [
            sg.Column(activation_status_col, element_justification='right',expand_x=True)
        ],
    ]

    global window
    window = sg.Window('Bombcrypto bot', layout)


    layout2 = [
        [
            sg.Text('Activation', font=('Arial', 10, 'bold'))
        ],
        [sg.Text('Please inform your registration key:',key='ACTIVATION_LABEL')],
        [
            sg.Column(
                [[sg.Input(key='KEY_INPUT')]], 
                element_justification='center',expand_x=True)
        ],
        [
            sg.Column(
                [
                    [
                        sg.Button('Submit', key='VALIDATE_KEY', size=(35, 1)),
                        sg.Button('Retry', key='REVALIDATE_KEY', size=(35, 1), visible=False)
                    ]
                ], 
                element_justification='center',expand_x=True)
        ],
        [
            sg.Column(
                [[sg.Button('Close', key='CLOSE_ACTIVATION', size=(35, 1))]], 
                element_justification='center',expand_x=True)
        ],
        
    ]
    global bot_running
    bot_running = False
    global window2
    window2 = sg.Window('Activate Bombcrypto bot', layout2,size=(450, 180))
    global ALREADY_INFORMED_KEY
    if get_config_value_by_property('KEY') is not None:
        ALREADY_INFORMED_KEY = get_config_value_by_property('KEY')
    else:
        ALREADY_INFORMED_KEY = None

    # --------------------- EVENT LOOP ---------------------
    while True:
        if ALREADY_INFORMED_KEY is None:
            event2, values2 = window2.read()
            if event2 == 'VALIDATE_KEY':
                window2['KEY_INPUT'].Update(visible = False)
                window2['VALIDATE_KEY'].Update(visible = False)
                window2['REVALIDATE_KEY'].Update(visible = False)
                window2.Element('ACTIVATION_LABEL').update('Please wait...')
                check_account_active_outside(values2['KEY_INPUT'])
            elif event2 == 'REVALIDATE_KEY':
                window2['KEY_INPUT'].Update(visible = True)
                window2['VALIDATE_KEY'].Update(visible = True)
                window2['REVALIDATE_KEY'].Update(visible = False)
                window2.Element('ACTIVATION_LABEL').update('Please inform your registration key:')
            elif event2 in (sg.WIN_CLOSED, 'Exit'):
                break
            elif event2 == 'CLOSE_ACTIVATION':
                break
            elif event2 == 'KEY_VALIDATED':
                if values2['KEY_VALIDATED']:
                    window2.close()
                    edit_config_value_by_property('KEY', values2['KEY_INPUT'])
                    ALREADY_INFORMED_KEY = values2['KEY_INPUT']
                else:
                    window2['KEY_INPUT'].Update(visible = False)
                    window2['VALIDATE_KEY'].Update(visible = False)
                    window2['REVALIDATE_KEY'].Update(visible = True)
                    window2.Element('ACTIVATION_LABEL').update('The activation key is not valid.')
                first_run = True
                if values2['KEY_VALIDATED']:
                    bot_loop()
        else:
            bot_loop()
            break
        

    # if user exits the window, then close the window and exit the GUI func
    window.close()


if __name__ == '__main__':
    the_gui()
