import hashlib

import requests
import xmltodict

from datetime import datetime, timedelta



class API:
    url: str = 'https://cafe-jojo.iiko.it:443/resto/api'
    token: str = 'b75df82a-0201-0c24-846f-8c425f14f812'

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.hash = hashlib.sha1(self.password.encode('utf-8')).hexdigest()

    def auth(self):
        url = f'{self.url}/auth'
        params = {'login': self.login, 'pass': self.hash}
        r = requests.get(url=url, params=params)
        if r.status_code != 200:
            print(f'{r.status_code}: {r.text}')
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
            raise
        return xmltodict.parse(r.text)


#if __name__ == '__main__':

# api = API(
#     login='API',
#     password='api123',
# )
# api.auth()
# #report = api.report_olab(date_from='12.04.2024', date_to='12.04.2024')
# report_mon = api.report_olab(date_from=formatted_first_day, date_to=formatted_last_day)
# report_day = api.report_olab(date_from=str(now), date_to=str(now))
# #print(report)

# # Извлечение всех DishName и DishAmountInt
# for dish in report_mon['report']['r']:
#     dish_name = dish['DishName']
#     dish_amount_int = str(dish['DishAmountInt'])
#     print(f"Название: {dish_name}, Кол-во: {dish_amount_int.split('.')[0]}")

# for dish in report_day['report']['r']:
#     dish_name = dish['DishName']
#     dish_amount_int = str(dish['DishAmountInt'])
#     print(f"Название: {dish_name}, Кол-во: {dish_amount_int.split('.')[0]}")


        
    
