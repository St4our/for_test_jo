import datetime
import json
import logging
import threading
import traceback
from time import sleep

import pytz
import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for

from api import API
from config import settings
from db.init import init
from db.models import Plan
from db.repositories.plans import PlanRepository
from db.repositories.plans_histories import PlanHistoryRepository
from db.repositories.tasks import TaskRepository
from logger import config_logger
from utils import get_week_counts

config_logger()
plan_info = None
last_save_day = None
data_prod = {}
plan_save_per = 0

init()


def get_plan_today():
    week_day_count = get_week_counts()
    current_week_day = datetime.date.today().weekday()
    plans = []
    for plan_db in PlanRepository().get_list():
        plan_db: Plan
        plan = round(
            plan_db.plan_month *
            settings.get_percent(weekday=current_week_day) /
            week_day_count[current_week_day]
        )
        fact = plan_db.fact_day
        remainder = round(plan - fact)
        plans.append({
            'name': plan_db.name,
            'plan': plan,
            'fact': fact,
            'remainder': remainder,
        })
    logging.critical(f'plans={plans}')
    return plans


def save_history():
    global last_save_day
    now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
    if now.hour == 4 and last_save_day != now.day:
        logging.critical('ЗАПИСЫВАЮ')
        for plan_db in PlanRepository().get_list():
            PlanRepository().update(plan_db, plan_month=plan_db.plan_month - plan_db.fact_day)
            PlanHistoryRepository().create(name=plan_db.name, fact_day=plan_db.fact_day)
        last_save_day = now.day


def take_info():
    def take():
        global plan_save_per

        time_for_save = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
        time_for_post = time_for_save.strftime("%d.%m.%Y")

        if time_for_save.hour == 23 and time_for_save.minute >= 50 and plan_save_per != 1:
            myfile = open(f"./{time_for_post}.txt", 'wb')
            myfile.write(f"{str(time_for_post)} : {str(plan_info)}".encode('utf-8'))
            myfile.close()
            plan_save_per = 1

        if time_for_save.hour == 1 and time_for_save.minute >= 1 and plan_save_per != 0:
            plan_save_per = 0

        url = "https://cafe-jojo.iikoweb.ru/api/cash/shift/active"

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

        response_cash = requests.get(url, headers=headers)
        data_cash = response_cash.json()
        for shift in data_cash['shifts']:
            if str(shift['sessionStatus']) == "OPEN":
                nal = float(shift['salesCash'])
                bezN = float(shift['salesCard'])
                cash_only = nal + bezN
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

        now = datetime.datetime.now(pytz.timezone('Europe/Moscow'))

        first_day_of_month = now.replace(day=1)

        if now.month == 12:
            last_day_of_month = now.replace(year=now.year + 1, month=1, day=1) - datetime.timedelta(days=1)
        else:
            last_day_of_month = now.replace(month=now.month + 1, day=1) - datetime.timedelta(days=1)

        formatted_first_day = first_day_of_month.strftime("%d.%m.%Y")
        formatted_last_day = last_day_of_month.strftime("%d.%m.%Y")
        now = now.strftime("%d.%m.%Y")

        api = API(login=settings.api_login, password=settings.api_password)

        report_mon = api.report_olab(date_from=formatted_first_day, date_to=formatted_last_day)
        report_day = api.report_olab(date_from=str(now), date_to=str(now))
        report_mon_cat = api.report2_olab(date_from=formatted_first_day, date_to=formatted_last_day)
        report_day_cat = api.report2_olab(date_from=str(now), date_to=str(now))

        if None in [report_day_cat['report'], report_day['report']]:
            api = API(login=settings.api_login, password=settings.api_password)
            previous_day = datetime.datetime.now(pytz.timezone('Europe/Moscow')) - datetime.timedelta(days=1)
            previous_day = previous_day.strftime("%d.%m.%Y")
            report_day = api.report_olab(date_from=str(previous_day), date_to=str(previous_day))
            report_day_cat = api.report2_olab(date_from=str(previous_day), date_to=str(previous_day))

        for dish in report_mon_cat['report']['r']:
            dish_name = dish['DishCategory']
            dish_amount_int = str(dish['DishAmountInt'])
            try:
                data_prod[f'{dish_name}'][0] = f"{dish_amount_int.split('.')[0]}"
            except:
                data_prod[f'{dish_name}'] = []
                data_prod[f'{dish_name}'].append(f"{dish_amount_int.split('.')[0]}")

        for dish in report_day_cat['report']['r']:
            dish_name = dish['DishCategory']
            dish_amount_int = str(dish['DishAmountInt'])
            try:
                try:
                    data_prod[f'{dish_name}'][1] = f"{dish_amount_int.split('.')[0]}"
                except:
                    data_prod[f'{dish_name}'][1] = "0"
            except:
                data_prod[f'{dish_name}'].append(f"{dish_amount_int.split('.')[0]}")

        for dish in report_mon['report']['r']:
            dish_name = dish['DishName']
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
                data_prod[f'{dish_name}'].append(f"{dish_amount_int.split('.')[0]}")

        for i in data_prod:
            if len(data_prod[f'{i}']) < 2:
                data_prod[f'{i}'].append("0")
        data_prod['Соусы'] = [
            sum([
                int(data_prod['Соус барбекю'][0]),
                int(data_prod['Соус кисло-сладкий'][0]),
                int(data_prod['Соус сырный'][0]),
                int(data_prod['Соус Цезарь'][0]),
            ]),
            sum([
                int(data_prod['Соус барбекю'][1]),
                int(data_prod['Соус кисло-сладкий'][1]),
                int(data_prod['Соус сырный'][1]),
                int(data_prod['Соус Цезарь'][1]),
            ]),
        ]
        data_prod['Пиво'] = [
            sum([
                int(data_prod['Bergaer dark'][0]),
                int(data_prod['Bergauer Pilsner'][0]),
                int(data_prod['Bergauer fest'][0]),
                int(data_prod['Bergauer classic'][0]),
                int(data_prod['Bergauer Blanche'][0]),
                int(data_prod['Demidov Б/А'][0]),
            ]),
            sum([
                int(data_prod['Bergaer dark'][1]),
                int(data_prod['Bergauer Pilsner'][1]),
                int(data_prod['Bergauer fest'][1]),
                int(data_prod['Bergauer classic'][1]),
                int(data_prod['Bergauer Blanche'][1]),
                int(data_prod['Demidov Б/А'][1]),
            ]),
        ]
        data_prod['Десерты'] = [
            sum([
                int(data_prod['Чизкейк "Клубничный пломбир"'][0]),
                int(data_prod['Чизкейк "Манго-маракуйя"'][0]),
                int(data_prod['Чизкейк "Сникерс"'][0]),
                int(data_prod['Моти'][0]),
                int(data_prod['Сырники из рикотты'][0]),
            ]),
            sum([
                int(data_prod['Чизкейк "Клубничный пломбир"'][1]),
                int(data_prod['Чизкейк "Манго-маракуйя"'][1]),
                int(data_prod['Чизкейк "Сникерс"'][1]),
                int(data_prod['Моти'][1]),
                int(data_prod['Сырники из рикотты'][1]),
            ]),
        ]

        for pos_prod in data_prod:
            plan_pos: Plan = PlanRepository().get(name=pos_prod)
            if not plan_pos:
                continue
            logging.critical(f'{plan_pos.name} - {data_prod[pos_prod]}')
            fact_month = int(data_prod[pos_prod][0])
            fact_day = int(data_prod[pos_prod][1])
            PlanRepository().update(plan_pos, fact_day=fact_day, fact_month=fact_month)
        #
        # if 'Задача' in str(plan_pos['item']):
        #     plan_pos['factDay'] = str(plan_pos['planDay'])
        #     if data_prod[pos_prod][0] == '':
        #         ops = 0
        #         plan_pos['factMon'] = str(plan_pos['planMonth'])
        #     else:
        #         plan_pos['factMon'] = str(plan_pos['planMonth'])
        save_history()

    try:
        take()
        print("OK")
    except:
        print('NOT OK')
        headers = {
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://cafe-jojo.iikoweb.ru/storeops/index.html',
            'Accept-language': '"ru_RU"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
        }

        response = requests.get('https://cafe-jojo.iikoweb.ru/storeops/common_components/app/page/lock-screen.html',
                                headers=headers)

        cookies = {
            'PHPSESSID': 'jeb6b049ji1v105ud3mabbslu7',
        }

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json;charset=UTF-8',
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

        response = requests.post('https://cafe-jojo.iikoweb.ru/api/auth/login', cookies=cookies, headers=headers,
                                 json=json_data)
        cookies = {
            'PHPSESSID': 'jeb6b049ji1v105ud3mabbslu7',
        }

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': '"ru_RU"',
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
            'referer': 'https://cafe-jojo.iikoweb.ru/storeops/index.html',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }

        response = requests.get('https://cafe-jojo.iikoweb.ru/api/stores/select/102023', cookies=cookies,
                                headers=headers)

        print("переавторизовался1")
        take()
        print("переавторизовался")


app = Flask(__name__)

full_position = []


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('login.html')


@app.get('/login')
def login():
    return render_template('login.html')


@app.post('/login')
def login_post():
    login = request.form['log']
    password = request.form['passw']
    if str(login) == settings.admin_login and str(password) == settings.admin_password:
        articles = data_prod
        return render_template(
            'admin.html',
            plans=[
                PlanRepository().generate_dict(plan=plan)
                for plan in PlanRepository().get_list()
            ],
            tasks=[
                TaskRepository().generate_dict(task=task)
                for task in TaskRepository().get_list()
            ],
            articles=articles,
        )
    elif str(login) == settings.user_login and str(password) == settings.user_password:
        return redirect(url_for('user'))
    return render_template('login.html')


@app.post('/admin')
def admin() -> json:
    for plan_db in PlanRepository().get_list():
        PlanRepository().delete(plan_db)
    for task_db in TaskRepository().get_list():
        TaskRepository().delete(task_db)
    for item in request.get_json():
        if 'Задача' in item['name']:
            TaskRepository().create(name=item['name'])
        else:
            PlanRepository().create(
                name=item['name'],
                plan_month_value=item['plan_month_value'],
                plan_month=item['plan_month'],
            )
    return jsonify({
        'status': 'success',
    })


@app.get('/user')
def user():
    return render_template(
        'user.html',
        plans=get_plan_today(),
        tasks=[
            TaskRepository().generate_dict(task=task)
            for task in TaskRepository().get_list()
        ],
    )


def while_obn():
    while True:
        try:
            take_info()
            plans = [
                PlanRepository().generate_dict(plan=plan)
                for plan in PlanRepository().get_list()
            ]
            print("Вот что имеем: ", plans)
            print("Вот что получили: ", data_prod)
            sleep(30)
        except:
            traceback.print_exc()
            sleep(3630)


def start_obn():
    info_take = threading.Thread(target=while_obn)
    info_take.start()


start_obn()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
