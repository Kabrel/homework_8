from random import randint
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import *


class DataBase:
    def __init__(self, ip, port, name, **kwargs):
        self.__ip_adr = ip
        self.__port = port
        self.__name = name
        self._connect_to_db()

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

    def delete_vacancy_from_bd(self):
        pass

    def change_vacancy_in_bd(self):
        pass

    def __create_id(self) -> str:
        while True:
            j_id = str(randint(100, 5000))
            if not self.__collection.find({'_id': j_id}):
                return j_id
            else:
                pass
