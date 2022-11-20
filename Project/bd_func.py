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

    def _connect_to_db(self):
        self.__client = MongoClient(self.__ip_adr, self.__port)
        self.__db = self.__client[self.__name]
        self.__collection = self.__db.jobs

    def add_vacancy_to_bd(self, *values):
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
            vac_id = str(randint(100, 5000))
            if not self.__collection.find({'_id': vac_id}):
                return vac_id
            else:
                pass

    def __get_all(self):
        self.all_jobs = self.__collection.find()[:]

    def __make_job_data(self, j_id):
        data = self.all_jobs[j_id]
        no_data = "Не указано"
        name = data["name"]
        empl = data["employer"]
        city = data["city"]
        metro = data["metro"] if data["metro"] else no_data
        sal_min = data["salary_min"] if data["salary_min"] else no_data
        sal_max = data["salary_max"] if data["salary_max"] else no_data
        link = data["link"]
        day = data["vac_day"]
        month = data["vac_month"]
        text = (f'Название вакансии: {name}\nРаботодатель: {empl}\nГород: {city}\nМетро: {metro}\n'
                f'Минимальная зарплата: {sal_min}\nМаксимальная зарплата: {sal_max}\nСсылка на вакансию: {link}\n'
                f'Дата размещения: {day}.{month}\n')
        return text

    def show_all(self):
        self.__get_all()
        self.__current_id = 0
        return self.__make_job_data(self.__current_id)

    def search_data(self, search_type: str, data):
        pass

    def __search_by_salary(self, value: str):
        pass

    def __search_by_name(self, value: str):
        pass

    def __search_by_employer(self, value: str):
        pass

    def __search_by_city(self, value: str):
        pass

    def __search_by_metro(self, value: str):
        pass

    def import_db(self, f_name='jobs.json'):
        count = self.__collection.count_documents({})
        if count <= 1:
            with open(f_name) as file:
                file_data = json.load(file)
            if isinstance(file_data, list):
                self.__collection.insert_many(file_data)
            else:
                self.__collection.insert_one(file_data)


if __name__ == '__main__':
    db = DataBase(config.db_ip, config.db_port, config.db_name)
    print(db.show_all())
