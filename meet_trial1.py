import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  
from datetime import datetime , date
import time 
from time import sleep as wait , localtime
import sys, os
import requests
import base64
import json
from playsound import playsound
from win10toast import ToastNotifier


driver, people_view, chatbox, panel_dismiss, you = 0, 0, 0, 0, 0

def desktop_notification(not_tit="You were been called in the meeting",msg='Google meet alert!'):
    from win10toast import ToastNotifier
    toaster = ToastNotifier()
    icon = 'icons\\roasted_nuts.ico'
    stay_time = 5
    toaster.show_toast(not_tit, icon_path=icon, duration=stay_time, msg=msg)

def audio_alert(path='alertcall/alert_5_sec.mp3'):  
    from playsound import playsound
    
    playsound(path)
    

def alert():
    desktop_notification()
    audio_alert()


#sign_in(password='incorrect') for getting correct id / pw
def sign_in(password='correct'):
    import os
    from getpass import getpass as pw
    try:
        path = os.getcwd()+'\\'
        if password=='incorrect':
            desktop_notification(not_tit='Warning! Login failed',msg = 'Enter proper login credentials.')
            print("Warning! Enter proper login credentials\n\n")
            with open(path+'login_credentials.txt','w') as login_inp:
                username = input("Enter google meet official user ID: ").strip()
                while '@svce.ac.in' not in username :
                    print("Enter valid google id for joining the class")
                    username = input("Enter official google account user ID: ").strip()
                password = pw("Enter google password: ")
                login_inp.write(username+'\n'+password)
            return username, password  
        if os.path.isfile(path+'login_credentials.txt'):
            with open(path+'login_credentials.txt','r') as login:
                username,password = login.read().split('\n')
        else: 
            with open(path+'login_credentials.txt','w') as login_inp:
                desktop_notification(not_tit='Required Google Sign In',msg = 'Google meet Assistance')
                username = input("Enter google meet official user ID: ").strip()
                while '@svce.ac.in' not in username :
                    print("Enter valid google id for joining the class")
                    username = input("Enter official google account user ID: ").strip()
                password = pw("Enter google password: ")
                login_inp.write(username+'\n'+password)
        if password=='incorrect':
            desktop_notification(not_tit='Warning! Login failed',msg = 'Enter proper login credentials.')
            print("Warning! Enter proper login credentials.\n\n")
            with open(path+'login_credentials.txt','w') as login_inp:
                username = input("Enter google meet official user ID: ").strip()
                while '@svce.ac.in' not in username :
                    print("Enter valid google id for joining the class")
                    username = input("Enter official google account user ID: ").strip()
                password = input("Enter google password: ").strip()
                login_inp.write(username+'\n'+password)
        return username, password       
    except:
        os.remove(path+'login_credentials.txt')


#returns driver or action if only action=True
def get_driver():
    import selenium
    from selenium import webdriver

    chromedriver = "chromedriver.exe"

    #ssl_handshake_alert
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(chromedriver, options=chrome_options)
    return driver

#returns action
def get_action():
    global driver
    return selenium.webdriver.ActionChains(driver)

def media(camera=False,mic=False):
    action = get_action()
    action.key_down(Keys.CONTROL).send_keys('d').pause(2).send_keys('e').key_up(Keys.CONTROL).perform()
    driver.implicitly_wait(50)
    
def read_with_timeout( caption, default, default_prompt = "You did not respond!", timeout = 10):
    import sys, time, msvcrt
    start_time = time.time()
    sys.stdout.write('%s(%s):'%(caption, default))
    sys.stdout.flush()
    input = ''
    while True:
        if msvcrt.kbhit():
            byte_arr = msvcrt.getche()
            if ord(byte_arr) == 13: # enter_key
                break
            elif ord(byte_arr) >= 32: #space_char
                input += "".join(map(chr,byte_arr))
        if len(input) == 0 and (time.time() - start_time) > timeout:
            desktop_notification(not_tit="You did not respond!",msg='Joining Automatically.')
            print(default_prompt)
            break

    print('')  # needed to move to next line
    if len(input) > 0:
        return input
    else:
        return default

def fetch_links(day, check=False, d_count=False):
    import requests
    import base64
    import json

    user='rohitnavaneethakrishnan'
    repo_name = 'aut_sem7_tt'
    path_to_file = 'tt_october_revised'
    json_url =f'https://api.github.com/repos/{user}/{repo_name}/contents/{path_to_file}'

    try :
        response = requests.get(json_url)
        jsonResponse = response.json()  
        content = base64.b64decode(jsonResponse['content'])
        tt_json = content.decode('utf-8')
        tt_sch = json.loads(tt_json)
        with open('tt_data.txt','w') as tt_file:
            tt_file.write(tt_json)

    except :
        with open('tt_data.txt','r') as tt_file:
            tt_json = tt_file.read()
            tt_sch = json.loads(tt_json)
            
    g_d = tt_sch['g_d']
    time_table = tt_sch['time_table']
    subjects = tt_sch['subjects']
    
    if d_count: return len(time_table)
    if check : 
        return [ time_table[day][hour]['close_time'] for hour in time_table[day] ]  
    else:
        t_sub = {}
        sub_codes = [time_table[day][hour]['SUB CODE'] for hour in time_table[day].keys() ]
        for sub_code in sub_codes :
            t_sub[sub_code] = subjects[sub_code]
        return {'gen_details':g_d, 'today_tt':time_table[day], 'today_sub' : t_sub}

def time_dif(work_time):
    c_day, c_month, c_year, c_hour, c_minute, c_second = list(map(int,datetime.now().strftime("%d %m %Y %H %M %S").split()))
    w_hour, w_minute, w_second = list(map(int,work_time.split(':')))
    c_time = datetime(day=c_day , month = c_month, year =c_year,  hour = c_hour, minute = c_minute, second = c_second)
    w_time = datetime(day=c_day , month = c_month, year =c_year,  hour = w_hour, minute = w_minute, second = w_second)
    return (w_time - c_time).total_seconds()

def day_confirmation():
    week = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday']
    c_d = time.localtime().tm_wday              
    add_wait_time = 0  
    days_count =  fetch_links(week[c_d], d_count = True )
    if c_d == (days_count-1): 
        print('came in d equality check')
        same=False
        for i in fetch_links(week[c_d], check = True ) : 
            if time_dif(i) > 0: 
                same=True
                break
        if same: return [week[c_d], 0]
        else: return [week[0], (6 - c_d)*86400] 

    elif c_d > (days_count-1) : 
        add_wait_time = (6 - c_d)*86400 
        return [week[0] , add_wait_time]                     
    close_time = fetch_links(week[c_d], check=True)    
    for i in close_time :
        if time_dif(i) > 0: 
            day = True
            break
        else: day = week[c_d + 1]
    print(week[c_d] if day else week[c_d + 1])
    return [week[c_d] if day else week[c_d + 1], add_wait_time]

def today_class():
    from time import sleep as wait
    from datetime import datetime
    [day, add_wait_time] = day_confirmation()
    today_details = fetch_links(day)
    general_details = today_details['gen_details']
    tt = today_details['today_tt']
    subject = today_details['today_sub']

    c_a = 0   
    if (not  add_wait_time) and day != datetime.now().strftime("%A") :
        print('Your NEXT class is scheduled for tomorrow (Monday).')
        desktop_notification(not_tit="You are Free today", msg='Your NEXT class is scheduled for tomorrow (Monday)')

    elif add_wait_time:
        desktop_notification(not_tit="You are Free today", msg='Your NEXT class is scheduled for Monday') 
        print('Your NEXT class is scheduled for Monday.')
        wait(add_wait_time)
        add_wait_time=0

    for i,hour in enumerate(tt.keys()):
        class_url, meet_url = subject[tt[hour]['SUB CODE']]['classroom_link'], subject[tt[hour]['SUB CODE']]['meet_link']
        till_join = time_dif(tt[hour]['start_time'])  
        till_leave = time_dif(tt[hour]['close_time'])
        if day != datetime.now().strftime("%A"):
            till_join += 86400 
            till_leave += 86400

        if till_join > 0:
            c_m = i-c_a
            if c_m: 
                desktop_notification(not_tit='Warning!',msg=('You have missed '+str(c_m)+(' class' if c_m<2 else 'classes')))
                print('\n\nWarning! You have missed',c_m,'class' if c_m<2 else 'classes')
            c_a += 1
            new = True if c_a==1 else False

            if new : desktop_notification(not_tit=("Upcoming class - " + subject[tt[hour]["SUB CODE"]]["SUB CODE"]+ ' at '+tt[hour]['start_time']), msg=subject[tt[hour]["SUB CODE"]]["SUBJECT NAME"])
            else: desktop_notification(not_tit=("Next class - " + subject[tt[hour]["SUB CODE"]]["SUB CODE"]+ ' at '+tt[hour]['start_time']), msg=subject[tt[hour]["SUB CODE"]]["SUBJECT NAME"])
            wait(till_join)
            print('\n\n', (general_details),end='\n\n\n\t\t')
            print(f'\n\n\t\t{hour} CLASS :\n\t\t',f'SUB CODE     : {subject[tt[hour]["SUB CODE"]]["SUB CODE"]}', f'SUBJECT NAME : {subject[tt[hour]["SUB CODE"]]["SUBJECT NAME"]}', f'FACULTY      : {subject[tt[hour]["SUB CODE"]]["FACULTY"]}\n\n',sep='\n\n\t\t')
            print('\n\n')
            
            join_meeting(meet_url, class_url,tt[hour]['close_time'],new)
            continue
        elif till_leave > 0:
            c_m = i-c_a
            if c_m:
                desktop_notification(not_tit='Warning!',msg=('You have missed '+str(c_m)+(' class' if c_m<2 else 'classes')))
                print('\n\nWarning! You have missed',c_m,'class' if c_m<2 else 'classes')
            c_a += 1
            print('\n\n', (general_details),end='\n\n\n\t\t')
            print(f'\t\t{hour} CLASS\n\t\t',f'SUB CODE     : {subject[tt[hour]["SUB CODE"]]["SUB CODE"]}', f'SUBJECT NAME : {subject[tt[hour]["SUB CODE"]]["SUBJECT NAME"]}', f'FACULTY      : {subject[tt[hour]["SUB CODE"]]["FACULTY"]}\n\n',sep='\n\n\t\t')
            print('\n\n')

            new = True if c_a==1 else False
            
            delay = abs(int(till_join))
            
            if delay:
                delay_msg_not =  ('You are delayed by ' + str(delay//60) + (' minute,' if delay<120 else 'minutes, ')+str(delay%60)+(' second' if (delay%60)<2 else ' seconds'))
                
                desktop_notification(not_tit='Warning! Delay Join',msg= delay_msg_not )
                wait(2)
                print(f'\n\nWarning!'+delay_msg_not)
            desktop_notification(not_tit=("Current session, " + subject[tt[hour]["SUB CODE"]]["SUB CODE"]), msg=subject[tt[hour]["SUB CODE"]]["SUBJECT NAME"])
            join_meeting(meet_url, class_url,tt[hour]['close_time'],new)
        



def chat(send_msg = False,read=True):
    chats_tab_list = driver.find_elements_by_class_name("GDhqjd")
    driver.implicitly_wait(50)
    sender_timestamps = [i.get_attribute('data-formatted-timestamp') for i in chats_tab_list] 
    #sender_names = [i.get_attribute('data-sender-name') for i in chats_ele_list]  
    senders_ele_li = driver.find_elements_by_class_name("YTbUzc")
    driver.implicitly_wait(50)
    sender_names = [i.get_attribute('innerHTML') for i in senders_ele_li]

    s_time_ele_li = driver.find_elements_by_class_name("MuzmKe")
    driver.implicitly_wait(50)
    sender_time = [i.get_attribute('innerHTML') for i in s_time_ele_li]
    chats_ele = driver.find_elements_by_xpath('//div[@class="Zmm6We"]')
    driver.implicitly_wait(50)
    chats = [i.text for i in chats_ele]
    print(sender_time, sender_names, chats)
    chat_content =  [i.text for i in chats_tab_list]
    driver.implicitly_wait(50)
    print(chat_content,sender_timestamps)
    wait(300)

    if send_msg:
        try:
            textbox = driver.find_elements_by_xpath('//textarea[@class="KHxj8b tL9Q4c"]')
        except:
            textbox = driver.find_elements_by_class_name("KHxj8b tL9Q4c")
        msg_text(textbox)
        try:
            send = driver.find_elements_by_class_name("uArJ5e Y5FYJe cjq2Db HZJnJ Cs0vCd M9Bg4d")
        except:
            send = driver.find_elements_by_xpath('//*[@id="ow3"]/div[1]/div/div[4]/div[3]/div[3]/div/div[2]/div[2]/div[2]/span[2]/div/div[3]/div[2]')


def meet_set_up(captions=True,video = True,chatbox=False):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from time import sleep as wait
    action = get_action()
    global driver
    
    if captions:
        action.key_down(Keys.SHIFT).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).key_up(Keys.SHIFT).send_keys(Keys.ENTER).perform()
        driver.implicitly_wait(40)
        wait(1) 
        desktop_notification(not_tit='Captions Turned on', msg='Google meet assistance')
        print('\n\nCaptions Turned on')
    if not(video):
        wait(1)
        
        action.send_keys(Keys.UP).pause(0.75).send_keys(Keys.ENTER).pause(5).send_keys(Keys.TAB).pause(0.75).send_keys(Keys.TAB).pause(0.75).send_keys(Keys.ENTER).pause(0.75).send_keys(Keys.TAB).send_keys(Keys.TAB).pause(0.75).send_keys(Keys.TAB).send_keys(Keys.TAB).pause(2).send_keys(Keys.DOWN).send_keys(Keys.DOWN).send_keys(Keys.DOWN).pause(1).send_keys(Keys.ENTER).pause(1).send_keys(Keys.TAB).pause(0.5).send_keys(Keys.ENTER).perform()
        driver.implicitly_wait(50)
        desktop_notification(not_tit='Audio only mode enabled', msg='Click Settings to enable Video mode')
        print('\n\nAudio only mode selected\n')
        wait(0.5)
    if chatbox:
        action.key_down(Keys.CONTROL).pause(1).key_down(Keys.ALT).pause(2).send_keys('c').pause(0.7).key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
        driver.implicitly_wait(50)
        wait(1)
    
def self_monitor(closetime, people=True, chats=False, close_panel=False, new=False):
    global people_view 
    global chatbox
    global panel_dismiss
    if new:
        try:
            driver.execute_script('''window.wiz_progress&&window.wiz_progress();''')
            driver.implicitly_wait(20)
            people_view = driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[4]/div[3]/div[3]/div/div[2]/div[2]/div[1]/div[1]')
            driver.implicitly_wait(100)
        except:
            pass
        try:
            chatbox = driver.find_element_by_xpath('//div[@class="uArJ5e UQuaGc kCyAyd QU4Gid foXzLb M9Bg4d"]')
            driver.implicitly_wait(100)  
        except:
            pass
    if people:
        driver.execute_script('arguments[0].click()' , people_view)
        driver.implicitly_wait(23)
        wait(0.8)
        attendance()
    if chats:  
        try:  
            driver.execute_script('arguments[0].click()', chatbox)
            driver.implicitly_wait(50)
            print('chat clicked')
        except:
            action = get_action()
            action.key_down(Keys.CONTROL).pause(1.5).key_down(Keys.ALT).pause(2).send_keys('c').key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
            wait(1)
        chat()

    if close_panel:
        panel_dismiss = driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[4]/div[3]/div[3]/div/div[2]/div[1]/div[2]/div/button')
        driver.implicitly_wait(50)
        driver.execute_script('arguments[0].click()' , panel_dismiss)
        driver.implicitly_wait(50)
        wait(0.8)



def new_login():
    global driver, you
    username, password = sign_in()
    driver = get_driver()
    driver.maximize_window()
    driver.implicitly_wait(10)
    sign_url = "https://accounts.google.com/signin"
    desktop_notification(not_tit='Google Sign In', msg='Two-step verification - Get access to mobile device, if required.')
    driver.get(sign_url)
    driver.set_page_load_timeout(200)
    
    while True:        
        try:
            driver.find_element_by_id("identifierId").send_keys(username)
            driver.implicitly_wait(50)
            driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button').click()
            driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
            driver.implicitly_wait(20)
            driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button').click()
            driver.implicitly_wait(20)
            wait(2)
            you = driver.find_element_by_class_name("x7WrMb").text
            driver.implicitly_wait(100)
            desktop_notification(not_tit=you, msg='Sign in successful')
            print('\n\n'+you)    
            wait(2)                                                                                         #######
            driver.minimize_window()
            break
        except:
            driver.execute_script('''window.open(arguments[0],"_self");''',sign_url)
            driver.implicitly_wait(100)


def leave_meeting(end,manual=False):
    
    desktop_notification(not_tit='Its time to Leave meeting.', msg='Google meet Assistance')
    end_meet = driver.find_element_by_xpath(end)
    driver.implicitly_wait(100) 
    #end_meet.click()
    driver.execute_script('arguments[0].click()',end_meet)      
    driver.implicitly_wait(20)
                           



def join_meeting(meet, classroom, close_time, new=False):
    import requests
    import base64
    import json

    user='rohitnavaneethakrishnan'
    repo_name = 'aut_sem7_tt'
    path_to_file = 'xpaths'
    json_url =f'https://api.github.com/repos/{user}/{repo_name}/contents/{path_to_file}'

    try:
        response = requests.get(json_url)
        jsonResponse = response.json()  
        content = base64.b64decode(jsonResponse['content'])
        xpath_ = content.decode('utf-8')
        xpath = json.loads(xpath_)
        with open('xpaths.txt','w') as xpath_txt:
            xpath_txt.write(xpath_)

    except:
        with open('xpaths.txt','r') as xpath_txt:
            xpath = xpath_txt.read()
    join_xpath = xpath['join']
    captions_xpath = xpath['caption']
    end_xpath = xpath['end']
    menu_button= xpath['menu']


    from time import  sleep as wait
    import os
    path = os.getcwd()
    if new:
        desktop_notification(not_tit="Ready to join?",msg='We are getting into the meet in few seconds!')
        print('joining meeting...')
    else: desktop_notification(not_tit="Unfortunately you left the meeting",msg='Check your internet connection')
    global driver, you
    driver.maximize_window()
    driver.implicitly_wait(30)
    wait(1)
    try:
        reload_meet = False
        classroom = 'https://classroom.google.com/u/4/c/MTY2OTMzMzcxODQ2'
        meet = 'https://meet.google.com/lookup/bl5xrcfrph'
        driver.execute_script('''window.open(arguments[0],"_self");''',classroom)
        driver.set_page_load_timeout(200)
        driver.save_screenshot(path +'login_check.png')
        wait(3)
        driver.execute_script('''window.open(arguments[0],"_self");''',meet)
        driver.set_page_load_timeout(200)
        wait(1.5)
        driver.execute_script('''window.wiz_progress&&window.wiz_progress();''')
        driver.implicitly_wait(50)
        wait(5)
        join = driver.find_element_by_xpath(join_xpath)
        driver.implicitly_wait(300)
        wait(1)
    except selenium.common.exceptions.NoSuchElementException:
        reload_meet = True
    while reload_meet:
        driver.execute_script('''window.open(arguments[0],"_self");''',classroom)
        driver.set_page_load_timeout(100)
        # driver.save_screenshot(path +'login_check.png')
        wait(2)
        try:
            meet = driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[2]/div/div[1]/div/div[2]/div[2]/span/a').get_attribute('href')
            driver.implicitly_wait(50)
        except :
            meet = driver.find_element_by_xpath('//a[@class="tnRfhc etFl5b"]').get_attribute('href')
            driver.implicitly_wait(30)
        driver.execute_script('''window.open(arguments[0],"_self");''',meet)
        driver.set_page_load_timeout(200)
        wait(5)
        try:
            driver.execute_script('''window.wiz_progress&&window.wiz_progress();''')
            driver.implicitly_wait(20)
            wait(2)                               
            join = driver.find_element_by_xpath(join_xpath)
            driver.implicitly_wait(500)
            wait(1)
            reload_meet = False
        except :
            reload_meet = True
        
    if new: response = read_with_timeout('If you want to join this class manually, PRESS ENTER or type "M" to avoid techincal errors.', 'Automatic',default_prompt='\tYou did not respond! Joining Automatically.',timeout=9) 
    else: response ='Automatic'
    will = 'will' if response is 'Automatic' else 'will not'
    print( 'The google meet mode is %s and you %s receive  Alerts.' % (response, will ))

    if will == 'will not':
        media()
        wait(time_dif(close_time))
        leave_meeting(end_xpath, manual=True)
    else:
        media()
        try:
            driver.find_element_by_tag_name('body').click()
            driver.implicitly_wait(100)
            join = driver.find_element_by_xpath(join_xpath)
            driver.implicitly_wait(300)
            driver.execute_script('arguments[0].click()' , join)
            driver.implicitly_wait(100)
            wait(2)
        except selenium.common.exceptions.StaleElementReferenceException:
            join = driver.find_element_by_xpath(join_xpath)
            driver.implicitly_wait(100)
            driver.execute_script('arguments[0].click()' , join)
            driver.implicitly_wait(30)
            wait(2)
        except:
            join = driver.find_element_by_xpath(join_xpath)
            driver.implicitly_wait(100)
            driver.execute_script('arguments[0].click()' , join)
            driver.implicitly_wait(20)
            wait(2)
            print('some technical error occured, please wait or close the application and Try again.')
            
        driver.execute_script('''window.wiz_progress&&window.wiz_progress();''')
        driver.implicitly_wait(100)
        wait(2)  

        #adding others button pops up if only you are the one in the meeting , so closing it by dismiss button else passing too next clicks
        try:
            add_others_dismiss_button = driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[3]/div/div[2]/div[2]/div[3]/div')
            driver.implicitly_wait(10)
            add_others_dismiss_button.click()
            driver.implicitly_wait(10)
        except :pass
            
        driver.execute_script('''window.wiz_progress&&window.wiz_progress(); window.stopScanForCss&&window.stopScanForCss(); ccTick('bl');''')
        driver.implicitly_wait(10)
        wait(1)
        driver.execute_script('''window.wiz_progress&&window.wiz_progress();''')
        driver.implicitly_wait(10)
        wait(3)
        #turning on captions with button click
        try:                                         
            captions = driver.find_element_by_xpath(captions_xpath)
            driver.implicitly_wait(100)
            captions.click()
            driver.implicitly_wait(20)
            captions.click()
            driver.implicitly_wait(20)
            print('captions Turned on!')
        except:
            meet_set_up()   
            #for captions turning on using shortcut keys 
        wait(1)
        try:                                                                    
            menu = driver.find_element_by_xpath(menu_button)
            driver.implicitly_wait(100)
            wait(1)
            menu.click()
            driver.implicitly_wait(30)
            wait(2)
        except:               
            menu = driver.find_element_by_xpath(menu_button)
            driver.implicitly_wait(100)
            wait(1)
            menu.click()
            driver.implicitly_wait(30)
            wait(2)
        wait(2)
        meet_set_up(captions=False, video=False)


        while time_dif(close_time)>0:
            wait(15)
            try:
                driver.find_element_by_xpath(end_xpath)
                driver.implicitly_wait(100)
            except:
                join_meeting(meet, classroom, close_time, new=False)
            continue
        leave_meeting(end_xpath)
        desktop_notification(not_tit='You left the meeting.', msg='Google meet Assistance')  






def app_entry(access=True):
    if access:
        print('Signing into Google account.\n\n')
        desktop_notification(not_tit='Signing into Google account',msg = 'Google meet Assistance')
        new_login()
        wait(1)
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print('Its',current_time,'now\n\n',flush=True)
        wait(1)
        while True:
            today_class()
            #wait(3600)
    else:
        print('Access denied! Your free subcription has ended.\n\nContact developer')
        audio_alert(path='alertcall/Alert_20_sec.mp3')

def app_verification():
    import requests
    import base64
    import json
    user='rohitnavaneethakrishnan'
    repo_name = 'aut_sem7_tt'
    path_to_file = 'verification'
    json_url =f'https://api.github.com/repos/{user}/{repo_name}/contents/{path_to_file}'  
    try:
        response = requests.get(json_url)
        jsonResponse = response.json() 
        content = base64.b64decode(jsonResponse['content'])
        ver_json = content.decode('utf-8')
        ver_dict = json.loads(ver_json)
        ver_count = int(ver_dict['usage_limit'])
    except: ver_count = 20
    with open('admin_file.txt','r+') as ver_file:
        limit = ver_file.read()
        ver_dict = json.loads(limit)
        user_count = int(ver_dict['usage_limit'])
        if user_count>ver_count:
            app_entry(access=False)
        else:
            with open('admin_file.txt','r+') as ver_json:
                ver_json.write('{"usage_limit":"'+str(user_count+1)+'"}')
            app_entry()


