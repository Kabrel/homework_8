# -*- coding: utf-8 -*-

from random import randint
from datetime import datetime
import json
from pymongo import MongoClient
from pymongo.errors import *

import config


class DataBase:
    def __init__(self, ip, port, name, **kwargs):
        self.__ip_adr = ip
        self.__port = port
        self.__name = name
        self._connect_to_db()
        self.import_db()
        self.__current_id = 0
        self.__count = 0

    def _connect_to_db(self):
        self.__client = MongoClient(self.__ip_adr, self.__port)
        self.__db = self.__client[self.__name]
        self.__collection = self.__db.jobs

    def test(self, data):
        return self.__collection.find_one({'_id': data})

    def add_vacancy_to_bd(self, values):
        c_date = datetime.now()
        job_data = {'_id': self.__create_id(),
                    'name': values[0],
                    'employer': values[1],
                    'city': values[2],
                    'metro': values[3],
                    'salary_min': values[4],
                    'salary_max': values[5],
                    'vac_day': str(c_date.day),
                    'vac_month': str(c_date.month)}
        try:
            self.__collection.insert_one(job_data)
            return True
        except DuplicateKeyError:
            return False

    def delete_vacancy_from_bd(self, vac_id):
        try:
            self.__collection.delete_one({'_id': vac_id})
            return True
        except OperationFailure:
            return False

    def change_vacancy_in_bd(self, vac_id, value: dict):
        s_filter = {'_id': vac_id}
        new_val = {"$set": value}
        self.__collection.update_one(s_filter, new_val)
        return True

    def __create_id(self) -> str:
        while True:
            vac_id = str(randint(1, 500000))
            if not self.__collection.find_one({'_id': vac_id}):
                return vac_id
            else:
                pass

    def __get_all(self):
        self.all_jobs = self.__collection.find()[:]
        self.__count = self.__collection.count_documents({})

    def __make_job_data(self, j_id):
        data = self.all_jobs[j_id]
        no_data = "Не указано"
        job_id = data["_id"]
        name = data["name"]
        empl = data["employer"]
        city = data["city"]
        metro = data["metro"] if data["metro"] else no_data
        if data['salary_max'] is not None and data['salary_min'] is not None:
            salary = f"от {data['salary_min']} до {data['salary_max']} руб."
        elif data['salary_min'] is not None:
            salary = f"от {data['salary_min']} руб."
        elif data['salary_max'] is not None:
            salary = f"до {data['salary_max']} руб."
        else:
            salary = no_data
        link = data["link"]
        day = data["vac_day"] if data["vac_day"] else 'Не известно'
        month = data["vac_month"] if data["vac_month"] else 'Не известно'
        text = (f'Название вакансии: {name}\nРаботодатель: {empl}\nГород: {city}\nМетро: {metro}\n'
                f'Зарплата: {salary}\nСсылка на вакансию: {link}\nДата размещения: {day}.{month}\nid:{job_id}')
        return text

    def show_all(self):
        self.__get_all()
        self.__current_id = 0
        return self.__make_job_data(self.__current_id)

    def show_next(self):
        if self.__current_id < (self.__count - 1):
            self.__current_id += 1
        else:
            self.__current_id = 0
        return self.__make_job_data(self.__current_id)

    def show_prev(self):
        if self.__current_id > 0:
            self.__current_id -= 1
        else:
            self.__current_id = self.__count - 1
        return self.__make_job_data(self.__current_id)

    def search_data(self, search_type: str, data: str):
        match search_type:
            case 'by_salary':
                return self.__search_by_salary(data)
            case 'by_name':
                return self.__search_by_names(data)
            case 'by_employer':
                return self.__search_by_employer(data)
            case 'by_city':
                return self.__search_by_city(data)
            case 'by_metro':
                return self.__search_by_metro(data)

    def __search_by_salary(self, value: str):
        val = int(value)
        search = {'$or': [{'salary_min': {'$gte': val}}, {'salary_max': {'$gte': val}}]}
        self.all_jobs = self.__collection.find(search)[:]
        self.__count = self.__collection.count_documents(search)
        self.__current_id = 0
        return self.__make_job_data(self.__current_id)

    def __search_by_names(self, value: str):
        val = value
        search = {'name': {'$regex': val, '$options': 'i'}}
        self.all_jobs = self.__collection.find(search)[:]
        self.__count = self.__collection.count_documents(search)
        self.__current_id = 0
        return self.__make_job_data(self.__current_id)

    def __search_by_employer(self, value: str):
        val = value
        search = {'employer': {'$regex': val, '$options': 'i'}}
        self.all_jobs = self.__collection.find(search)[:]
        self.__count = self.__collection.count_documents(search)
        self.__current_id = 0
        return self.__make_job_data(self.__current_id)

    def __search_by_city(self, value: str):
        val = value
        search = {'city': {'$regex': val, '$options': 'i'}}
        self.all_jobs = self.__collection.find(search)[:]
        self.__count = self.__collection.count_documents(search)
        self.__current_id = 0
        return self.__make_job_data(self.__current_id)

    def __search_by_metro(self, value: str):
        val = value
        search = {'metro': {'$regex': val, '$options': 'i'}}
        self.all_jobs = self.__collection.find(search)[:]
        self.__count = self.__collection.count_documents(search)
        self.__current_id = 0
        return self.__make_job_data(self.__current_id)

    def import_db(self, f_name='jobs.json'):
        count = self.__collection.count_documents({})
        if count <= 1:
            with open(f_name, encoding='utf-8') as file:
                file_data = json.load(file)
            if isinstance(file_data, list):
                self.__collection.insert_many(file_data)
            else:
                self.__collection.insert_one(file_data)


if __name__ == '__main__':  # debug
    db = DataBase(config.db_ip, config.db_port, config.db_name)
    #print(db.test('5000'))
    #print(db.add_vacancy_to_bd(['test', 'test_empl', 'spb', 'metro1', '25000', '50000']))
    #print(db.change_vacancy_in_bd('100587', {'name': 'test_edited',
                                            # 'employer': 'emplo_edit',
                                            # 'metro': 'metr'}))
