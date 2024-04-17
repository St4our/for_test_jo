from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash, make_response
import requests
import json
from datetime import datetime, timedelta
import pytz
from dateutil.relativedelta import relativedelta
from time import sleep
import threading
# from functools import update_wrapper
#from api_code_red import *
import telebot
import traceback
import logging

import hashlib

#import requests
import xmltodict

from datetime import datetime, timedelta



class API:
    url: str = 'https://cafe-jojo.iiko.it:443/resto/api'
    token: str = 'e36555f3-5ba3-bc15-cb81-2b27b4de6a37'

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.hash = hashlib.sha1(self.password.encode('utf-8')).hexdigest()

    def logout(self):
        url = f'{self.url}/logout'
        r = requests.get(url=url, params={'key': self.token})
        if r.status_code != 200:
            print(f'{r.status_code}: {r.text}')
            raise
        self.token = r.text

    def auth(self):
        try:
            self.logout()
        except:
            pass
        url = f'{self.url}/auth'
        params = {'login': self.login, 'pass': self.hash}
        r = requests.get(url=url, params=params)
        if r.status_code != 200:
            print(f'{r.status_code}: {r.text}')
            logging.critical(f'{r.status_code}: {r.text}')
            raise
        self.token = r.text
        return self.token
    

    def report_olab(self, date_from: str, date_to: str):
        url = f'{self.url}/reports/olap'
        self.auth()
        params_str = '&'.join([
            f'key={self.token}',
            f'report=SALES',
            f'groupRow=DishCode',
            f'groupRow=DishName',
            f'groupRow=DishFullName',
            f'groupRow=DishCategory',
            f'agr=DishAmountInt',
            f'from={date_from}',
            f'to={date_to}',
        ])
        r = requests.get(url=f'{url}?{params_str}')
        if r.status_code == 401:
            print(f'New token: {self.auth()}')
            return self.report_olab(date_from=date_from, date_to=date_to)
        if r.status_code != 200:
            print(f'{r.status_code}: {r.text}')
            logging.critical(f'{r.status_code}: {r.text}')
            raise
        return xmltodict.parse(r.text)
    
    def report2_olab(self, date_from: str, date_to: str):
        url = f'{self.url}/reports/olap'
        params_str = '&'.join([
            f'key={self.token}',
            f'report=SALES',
            f'groupRow=DishCategory',
            f'agr=DishAmountInt',
            f'from={date_from}',
            f'to={date_to}',
        ])
        r = requests.get(url=f'{url}?{params_str}')
        if r.status_code == 401:
            print(f'New token: {self.auth()}')
            return self.report_olab(date_from=date_from, date_to=date_to)
        if r.status_code != 200:
            print(f'{r.status_code}: {r.text}')
            logging.critical(f'{r.status_code}: {r.text}')
            raise
        return xmltodict.parse(r.text)



plan_info = None
data_prod = {}
plan_save_per = 0


def take_info():
    def take():
        global plan_save_per

        time_for_save = datetime.now(pytz.timezone('Europe/Moscow'))
        time_for_post = time_for_save.strftime("%d.%m.%Y")

        if time_for_save.hour == 23 and time_for_save.minute >= 50 and plan_save_per != 1:
            myfile = open(f"./{time_for_post}.txt", 'wb')
            myfile.write (f"{str(time_for_post)} : {str(plan_info)}".encode('utf-8'))
            myfile.close()
            plan_save_per = 1

        if time_for_save.hour == 1 and time_for_save.minute >= 1 and plan_save_per != 0:
            plan_save_per = 0

        # URL запроса на зал и доставку
        url = "https://cafe-jojo.iikoweb.ru/api/cash/shift/active"

        # Заголовки запроса
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ru_RU",
            "Cookie": "PHPSESSID=jeb6b049ji1v105ud3mabbslu7",
            "Referer": "https://cafe-jojo.iikoweb.ru/till-shifts/ru-RU/index.html",
            "Sec-Ch-Ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Windows",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }

        # Выполнение GET-запроса по залу и доставке
        response_cash = requests.get(url, headers=headers)
        data_cash = response_cash.json()
        #print(data_cash)
        # Работа с данными по залу и доставке
        for shift in data_cash['shifts']:
            if str(shift['sessionStatus']) == "OPEN":
                nal = float(shift['salesCash'])
                bezN = float(shift['salesCard'])
                cash_only = nal+bezN
                menedz = shift['manager']['name']
                if menedz != "Доставка":
                    menedz = 'Для зала'
                if menedz == "Доставка":
                    menedz = 'Для доставки'
                try:
                    data_prod[f'{menedz}'][1] = f"{cash_only}"
                except:    
                    data_prod[f'{menedz}'] = []
                    data_prod[f'{menedz}'].append(f"0")
                    data_prod[f'{menedz}'].append(f"{cash_only}") 
                #print(f"{menedz}: {cash_only}")

        #----------------------------------------------
        # Получаем текущую дату
        #now = datetime.now()
        now = datetime.now(pytz.timezone('Europe/Moscow'))

        # Получаем первый день месяца
        first_day_of_month = now.replace(day=1)

        # Получаем последний день месяца
        if now.month == 12:
            # Если текущий месяц - декабрь, последний день - 31 декабря следующего года
            last_day_of_month = now.replace(year=now.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            # Для остальных месяцев последний день - последний день текущего месяца
            last_day_of_month = now.replace(month=now.month + 1, day=1) - timedelta(days=1)

        # Форматируем даты в формат DD.MM.YYYY
        formatted_first_day = first_day_of_month.strftime("%d.%m.%Y")
        formatted_last_day = last_day_of_month.strftime("%d.%m.%Y")
        now = now.strftime("%d.%m.%Y")
        print(now)

        #print(f"Первый день месяца: {formatted_first_day}")
        #print(f"Последний день месяца: {formatted_last_day}")

        api = API(
            login='API',
            password='api123',
        )
        #api.auth()

        report_mon = api.report_olab(date_from=formatted_first_day, date_to=formatted_last_day)
        report_day = api.report_olab(date_from=str(now), date_to=str(now))
        #sleep(2)
        report_mon_cat = api.report2_olab(date_from=formatted_first_day, date_to=formatted_last_day)
        report_day_cat = api.report2_olab(date_from=str(now), date_to=str(now))

        if report_day_cat['report'] == None or report_day['report']== None:
            api = API(
                login='API',
                password='api123',
            )
            now_p = datetime.now(pytz.timezone('Europe/Moscow'))
            previous_day = now_p - timedelta(days=1)
            previous_day = previous_day.strftime("%d.%m.%Y")
            print("previous_day: ", previous_day)
            report_day = api.report_olab(date_from=str(previous_day), date_to=str(previous_day))
            report_day_cat = api.report2_olab(date_from=str(previous_day), date_to=str(previous_day))
        #report_day = api.report_olab(date_from='11.04.2024', date_to='11.04.2024')

        #print("report_mon_cat: ", report_mon_cat)
        for dish in report_mon_cat['report']['r']:
            dish_name = dish['DishCategory']
            #print(dish_name)
            dish_amount_int = str(dish['DishAmountInt'])
            try:
                data_prod[f'{dish_name}'][0] = f"{dish_amount_int.split('.')[0]}"
            except:    
                data_prod[f'{dish_name}'] = [] 
                data_prod[f'{dish_name}'].append(f"{dish_amount_int.split('.')[0]}")

        #print("report_day_cat: ", report_day_cat)
        for dish in report_day_cat['report']['r']:
            dish_name = dish['DishCategory']
            dish_amount_int = str(dish['DishAmountInt'])
            try:
                try:
                    data_prod[f'{dish_name}'][1] = f"{dish_amount_int.split('.')[0]}"
                except:
                    data_prod[f'{dish_name}'][1] = "0"
            except:   
                #data_prod[f'{dish_name}'] = [] 
                data_prod[f'{dish_name}'].append(f"{dish_amount_int.split('.')[0]}")

        # Извлечение всех DishName и DishAmountInt
        for dish in report_mon['report']['r']:
            dish_name = dish['DishName']
            #print(dish_name)
            dish_amount_int = str(dish['DishAmountInt'])
            try:
                data_prod[f'{dish_name}'][0] = f"{dish_amount_int.split('.')[0]}"
            except:    
                data_prod[f'{dish_name}'] = [] 
                data_prod[f'{dish_name}'].append(f"{dish_amount_int.split('.')[0]}")

        for dish in report_day['report']['r']:
            dish_name = dish['DishName']
            dish_amount_int = str(dish['DishAmountInt'])
            try:
                try:
                    data_prod[f'{dish_name}'][1] = f"{dish_amount_int.split('.')[0]}"
                except:
                    data_prod[f'{dish_name}'][1] = "0"
            except:   
                #data_prod[f'{dish_name}'] = [] 
                data_prod[f'{dish_name}'].append(f"{dish_amount_int.split('.')[0]}")

                    
        for i in data_prod:
            # Проверяем, есть ли ключ в словаре и длина соответствующего массива
            #print(i, len(data_prod[f'{i}']))
            if len(data_prod[f'{i}']) < 2:
                data_prod[f'{i}'].append("0")

        
        
        #[{'item': 'Вок с курицей персонал', 'planDay': '1', 'planMonth': '2'}, {'item': 'По деревенски персонал', 'planDay': '3', 'planMonth': '4'}]
        if plan_info != None:
            for pos_prod in data_prod:
                #if str(pos_prod) in plan_info:
                for plan_pos in plan_info:
                    if str(plan_pos['item']) == str(pos_prod):
                        plan_pos['factDay'] = float(plan_pos['planDay'])-float(data_prod[pos_prod][1])
                        plan_pos['factMon'] = float(plan_pos['planMonth'])-float(data_prod[pos_prod][0])

    try:
        take()
        print("OK")
    except:
        headers = {
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://cafe-jojo.iikoweb.ru/storeops/index.html',
            'Accept-language': '"ru_RU"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
        }

        response = requests.get('https://cafe-jojo.iikoweb.ru/storeops/common_components/app/page/lock-screen.html', headers=headers)


        cookies = {
            'PHPSESSID': 'jeb6b049ji1v105ud3mabbslu7',
        }

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json;charset=UTF-8',
            # 'cookie': 'PHPSESSID=8833g5d95hiaidp8dbebo5j1sr',
            'origin': 'https://cafe-jojo.iikoweb.ru',
            'referer': 'https://cafe-jojo.iikoweb.ru/storeops/index.html',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }

        json_data = {
            'login': 'prodaji',
            'password': 'prodaji333',
        }

        response = requests.post('https://cafe-jojo.iikoweb.ru/api/auth/login', cookies=cookies, headers=headers, json=json_data)
        cookies = {
            'PHPSESSID': 'jeb6b049ji1v105ud3mabbslu7',
        }

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': '"ru_RU"',
            # 'cookie': 'PHPSESSID=8833g5d95hiaidp8dbebo5j1sr',
            'referer': 'https://cafe-jojo.iikoweb.ru/storeops/index.html',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }

        response = requests.get('https://cafe-jojo.iikoweb.ru/api/config/get', cookies=cookies, headers=headers)


        cookies = {
            'PHPSESSID': 'jeb6b049ji1v105ud3mabbslu7',
        }

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': '"ru_RU"',
            # 'cookie': 'PHPSESSID=8833g5d95hiaidp8dbebo5j1sr',
            'referer': 'https://cafe-jojo.iikoweb.ru/storeops/index.html',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }

        response = requests.get('https://cafe-jojo.iikoweb.ru/api/stores/select/102023', cookies=cookies, headers=headers)
        
        print("переавторизовался1")
        take()
        print("переавторизовался")

    # return info_prod 


app = Flask(__name__)

full_position = []



@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        login = request.form['log']
        password = request.form['passw'] 
        print(login,password)
        if str(login) == 'admin@jojo' and str(password) == 'admin_jojo321':
            #articles = ['Kal', 'Kal2', 'Kal3']
            # take_info()
            articles = data_prod
            #print("Пришло: ",articles)
            return render_template('admin.html', articles=articles)
            # return render_template('index.html')
        
        if str(login) == 'user@jojo' and str(password) == '111user_jojo':
            return redirect(url_for('user'))
            #return render_template('user.html', data_prod=data_prod)

        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/admin', methods=['POST', 'GET'])
def admin()-> json:
    global data_prod
    global plan_info

    if request.method == "POST":
        data = request.get_json()
        print(data)
        plan_info = data
        #[{'item': 'Вок с курицей персонал', 'planDay': '1', 'planMonth': '2'}, {'item': 'По деревенски персонал', 'planDay': '3', 'planMonth': '4'}]
        return jsonify({'status': 'success'})

    #     for el in data_prod:
    #         try:
    #             del data_prod[f'{el}'][2]
    #             plan_info = {}
    #             data_prod = {}
    #             # take_info()
    #         except:
    #             pass
    #         j = data_prod.get(f'{el}')
    #         a = request.form[f"p_day{el}"]
    #         b = request.form[f"p_mes{el}"]
    #         try:
    #             data_prod[f'{el}'].append(a)
    #             data_prod[f'{el}'].append(b)
    #         except:
    #             sleep(6)
    #             data_prod[f'{el}'].append(a)
    #             data_prod[f'{el}'].append(b)

    #     print(plan_info)
    #     print(data_prod)
    #     return redirect(url_for('user'))


def while_obn():
    while True:
        try:
            #print(plan_info)
            #print(data_prod)
            take_info()         
            print("Вот что имеем: ", plan_info)
            print("Вот что получили: ", data_prod)
            sleep(30)
            #print(data_prod)
        except:
            traceback.print_exc()
            sleep(3630)

def start_obn():
    info_take = threading.Thread(target=while_obn)
    info_take.start()

# def nocache(f):
#     def new_func(*args, **kwargs):
#         resp = make_response(f(*args, **kwargs))
#         resp.cache_control.no_cache = True
#         return resp
#     return update_wrapper(new_func, f)

# @nocache  
@app.route('/user', methods=['POST', 'GET'])
def user():
    if request.method == "GET":
        return render_template('user.html', data_prod=plan_info)
        
start_obn()  

#     if str(login) == '1' and str(password) == '2':
#         return render_template('user.html')
#     else:
#         return render_template('login.html')
    

if __name__ == '__main__':
   app.run(host="0.0.0.0", debug=True)
