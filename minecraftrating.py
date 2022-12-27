from server_interface import ServerInterface
from bs4 import BeautifulSoup as bs
import lxml
import csv
import os.path
from datetime import datetime as dt

class Agregator_mctop(ServerInterface):
    def __init__(self):
        self.agregator = "MRATE"
        super().__init__(agregator_main='https://minecraftrating.ru/', csv_filename=f"{self.agregator}.csv", csv_header = self.create_dict().keys())
        self.csv_file_exists = os.path.exists(self.csv_filename)

    def get_agrigator_pagination(self):
        pass

    def get_all_servers_url(self, links: list):

    def process_server(self, sertver_url: str, id=0, server_name='', raiting='', cite='', vk='', votes_m='',
                       votes_d='', players_o='', players_a='', uptime='', admin=''):
        pass


    def start(self):
        current_time = int(round(dt.now().timestamp()))
        print(f"Agregator <{self.agregator}> started!")
        pagination = self.get_agrigator_pagination()
        print("pagination.. OK!")
        links = self.get_all_servers_url(pagination)
        print("server links.. OK!")
        with open(self.csv_filename, 'a', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.csv_header)
            if not self.csv_file_exists:
                writer.writeheader()
            for i, link in enumerate(links):
                data = self.process_server(id=i, sertver_url=link[1])
                print(f"{self.agregator} | processing #{i}, <{data['server_name']}>.. OK!")
                data['timestamp'] = current_time
                writer.writerow(data)
                #УБЕРИ ЭТО ДЛЯ ОТЛАДКИ
                if i >= 10:
                    break
                #=====================