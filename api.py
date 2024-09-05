import hashlib
import logging

import requests
import xmltodict


class API:
    url: str = 'https://cafe-jojo.iiko.it:443/resto/api'
    token: str

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.token = '563cf669-3f26-a024-a13e-606c8bdf013c'
        self.hash = hashlib.sha1(self.password.encode('utf-8')).hexdigest()

    def logout(self):
        logging.critical(f'logout {self.token}')
        url = f'{self.url}/logout'
        r = requests.get(
            url=url,
            params={'key': self.token},
        )
        if r.status_code != 200:
            print(f'{r.status_code}: {r.text}')
            raise

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
        logging.critical(f'NEW TOKEN: {self.token}')
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
            f'groupRow=DeletedWithWriteoff',
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
        json_data = xmltodict.parse(r.text)
        logging.critical(json_data)
        if json_data['report'] is not None:
            for item in json_data['report']['r']:
                if item['DeletedWithWriteoff'] == 'DELETED_WITHOUT_WRITEOFF':
                    json_data['report']['r'].remove(item)
        return json_data

    def report2_olab(self, date_from: str, date_to: str):
        url = f'{self.url}/reports/olap'
        params_str = '&'.join([
            f'key={self.token}',
            f'report=SALES',
            f'groupRow=DishCategory',
            f'groupRow=DeletedWithWriteoff',
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
        json_data = xmltodict.parse(r.text)
        logging.critical(json_data)
        if json_data['report'] is not None:
            for item in json_data['report']['r']:
                if item['DeletedWithWriteoff'] == 'DELETED_WITHOUT_WRITEOFF':
                    json_data['report']['r'].remove(item)
        return json_data
