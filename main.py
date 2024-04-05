from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash, make_response
import requests
import json
from datetime import datetime, timedelta
import pytz
from dateutil.relativedelta import relativedelta
from time import sleep
import threading
# from functools import update_wrapper




plan_info = {}
data_prod = {}


def take_info():
    def take():
        # URL запроса на зал и доставку
        url = "https://cafe-jojo.iikoweb.ru/api/cash/shift/active"

        # Заголовки запроса
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ru_RU",
            "Cookie": "PHPSESSID=lbgoou322ps9hj4rm1urausa04",
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

        #----------------------------------------------
        
        # Получаем текущую дату и время по московскому времени
        now_moscow = datetime.now(pytz.timezone('Europe/Moscow'))

        # Форматируем дату в нужный формат
        formatted_date = now_moscow.strftime('%a %b %d %Y')


        cookies = {
            'PHPSESSID': '8833g5d95hiaidp8dbebo5j1sr',
        }

        headers = {
            'authority': 'cafe-jojo.iikoweb.ru',
            'accept': 'application/json, text/plain, */*',
            'accept-language': '"ru_RU"',
            'content-type': 'application/json;charset=UTF-8',
            # 'cookie': 'PHPSESSID=8833g5d95hiaidp8dbebo5j1sr',
            'origin': 'https://cafe-jojo.iikoweb.ru',
            'referer': 'https://cafe-jojo.iikoweb.ru/storeops/index.html',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }

        json_data = {
            'dateFrom': f'{formatted_date}',
            'dateTo': f'{formatted_date}',
            'mode': 'TOTAL_BY_PERIODS',
            'storeIds': [],
        }

        r_mes = []

        # Определяем первый день месяца
        first_day_of_month = now_moscow.replace(day=1)

        # Определяем последний день месяца
        last_day_of_month = first_day_of_month + relativedelta(months=1) - timedelta(days=1)

        # Находим понедельник первой недели месяца
        current_week_monday = first_day_of_month - timedelta(days=first_day_of_month.weekday())

        # Выводим даты понедельников и воскресенья для всех недель месяца
        while current_week_monday <= last_day_of_month:
            sleep(0.5)
            # Находим воскресенье текущей недели
            current_week_sunday = current_week_monday + timedelta(days=6)
            
            # Выводим даты понедельника и воскресенья
            mon = current_week_monday.strftime('%a %b %d %Y')
            sun = current_week_sunday.strftime('%a %b %d %Y')
            #print(mon)
            #print(sun)
            
            # Переходим к следующей неделе
            current_week_monday += timedelta(days=7)

            json_data_mes = {
                'dateFrom': f"{mon}",
                'dateTo': f"{sun}",
                'mode': 'TOTAL_BY_PERIODS',
                'storeIds': [],
            }
            r_r = requests.post('https://cafe-jojo.iikoweb.ru/api/report/product-mix', cookies=cookies, headers=headers, json=json_data_mes)
            data_mes = json.loads(r_r.text)
            prodali_mes = (data_mes['data']['totalByCategory'])
            r_mes.append(prodali_mes)

        r = requests.post('https://cafe-jojo.iikoweb.ru/api/report/product-mix', cookies=cookies, headers=headers, json=json_data)
        data = json.loads(r.text)

        prodali = (data['data']['totalByCategory'])
        #print(prodali)

        for i in prodali:
            j = i
            if i == '' or i == "Не кальян":
                pass #i = 'Без категории'
            else:
                #print("Позиция ",i,prodali[j]['forecast'])
                k = f"{i}-{prodali[j]['forecast']}"
                try:
                    data_prod[f'{i}'][0] = f"{prodali[j]['forecast']}"
                except:
                    data_prod[f'{i}'] = []
                    data_prod[f'{i}'].append(f"{prodali[j]['forecast']}")
                    #print("Записали ",k)
        
        data_mes_per = {}
        #print(r_mes)

        for p in r_mes:
            for i in p:
                # print(i)
                j = i
                if i == '' or i == "Не кальян":
                    pass #i = 'Без категории'
                else:
                    try:
                        #print("Позиция mes ",i,p[j]['actual'])
                        k = f"{i}-{p[j]['actual']}"
                        #data_prod.append(k)
                        # data_prod[f'{i}'] = []
                        try:
                            data_mes_per[f'{i}'].append(f"{p[j]['actual']}")
                        except:
                            data_mes_per[f'{i}'] = []
                            data_mes_per[f'{i}'].append(f"{p[j]['actual']}")
                        # data_prod[f'{i}'].append(f"{prodali[j]['actual']}")
                        # data_prod[f'{i}'] = f"{prodali[j]['actual']}"
                       
                    except:
                        pass

        for i in data_mes_per:
            # try:
            per = 0
            for j in data_mes_per[f'{i}']:
                #print(i,' : ', j)
                per += float(j)
            try:
                data_prod[f'{i}'][1] = f"{per}"
            except:    
                data_prod[f'{i}'].append(f"{per}")

        # Работа с данными по залу и доставке
        for shift in data_cash['shifts']:
            nal = float(shift['salesCash'])
            bezN = float(shift['salesCard'])
            cash_only = nal+bezN
            menedz = shift['manager']['name']
            if menedz != "Доставка":
                menedz = 'Зал'
            try:
                data_prod[f'{menedz}'][0] = f"{cash_only}"
            except:    
                data_prod[f'{menedz}'] = []
                data_prod[f'{menedz}'].append(f"{cash_only}")
                data_prod[f'{menedz}'].append(f"0")
            print(f"{menedz}: {cash_only}")

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
            'PHPSESSID': '8833g5d95hiaidp8dbebo5j1sr',
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
            'PHPSESSID': '8833g5d95hiaidp8dbebo5j1sr',
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
            'PHPSESSID': '8833g5d95hiaidp8dbebo5j1sr',
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
            print("Пришло: ",articles)
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
def admin():
    global data_prod
    global plan_info

    if request.method == "POST":
        for el in data_prod:
            try:
                del data_prod[f'{el}'][2]
                plan_info = {}
                data_prod = {}
                # take_info()
            except:
                pass
            j = data_prod.get(f'{el}')
            a = request.form[f"p_day{el}"]
            b = request.form[f"p_mes{el}"]
            try:
                data_prod[f'{el}'].append(a)
                data_prod[f'{el}'].append(b)
            except:
                sleep(6)
                data_prod[f'{el}'].append(a)
                data_prod[f'{el}'].append(b)

        print(plan_info)
        print(data_prod)
        return redirect(url_for('user'))
        #return render_template('user.html', data_prod=data_prod)

def while_obn():
    while True:
        print(plan_info)
        print(data_prod)
        sleep(5)
        take_info()
        print(plan_info)
        print(data_prod)
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
        return render_template('user.html', data_prod=data_prod)
        
start_obn()  

#     if str(login) == '1' and str(password) == '2':
#         return render_template('user.html')
#     else:
#         return render_template('login.html')
    

if __name__ == '__main__':
   app.run(host="0.0.0.0", debug=True)
