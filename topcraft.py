from server_interface import ServerInterface
from bs4 import BeautifulSoup as bs
import lxml
import csv
import os.path
from datetime import datetime as dt

class Agregator_topcraft(ServerInterface):
    def __init__(self):
        self.agregator = "TOPCRAFT"
        super().__init__(agregator_main='https://topcraft.ru/', csv_filename=f"{self.agregator}.csv",
                         csv_header=self.create_dict().keys())
        self.csv_file_exists = os.path.exists(self.csv_filename)

    def get_agrigator_pagination(self):
        links = [self.agregator_main]
        main = self.http_get(self.agregator_main)
        soup = bs(main, "lxml")
        pagination_main = soup.find("ul", {"class": "pagination"})
        lis = pagination_main.findAll('li')
        for i in lis[2:-1]:
            href = i.find('a')['href']
            links.append(self.agregator_main + href[1:])
        return links


    def get_all_servers_url(self, links: list):
        result = []
        for y, i in enumerate(links):
            html = self.http_get(i)
            soup = bs(html, "lxml")
            main_div = soup.find("section", class_="server-rt-cards")
            servers_div = main_div.find_all("article", class_="col-xs-12 user-pr-card")
            for j in servers_div:
                result.append([y, self.agregator_main[:-1] + j.find("a").attrs['href']])
                y += 1
            #####################################
            if y>5:
                break##########УБЕРИ КОСТЫЛЬ
            ######################################
        return result

    def process_server(self, sertver_url: str, id=0, server_name='', raiting='', cite='', vk='', votes_m='',
                       votes_d='', players_o='', players_a='', uptime='', admin=''):
        html = self.http_get(sertver_url)
        soup = bs(html, 'lxml')
        header = soup.find('header', {'class': 'project-header'})
        server_name = header.find('h1').text
        raiting = header.find('span', {'class': 'project-rating__qty'}).text
        main_table = soup.find('table', {'class': 'table project-info-table'})
        rows = main_table.find_all('td')
        for x, i in enumerate(rows):
            if "Сайт" in str(i):
                cite = rows[x+1].text

            if "Вконтакте" in str(i):
                vk = rows[x+1].text

            if "Голосов" in str(i):
                v = rows[x+1].text.split(',')
                votes_m = v[0].replace('за месяц ', '').strip()
                votes_d = v[1].replace(' сегодня ','').strip()

            if "Игроки" in str(i):
                g = rows[x+1].text.split('/')
                players_o = g[0].strip()
                players_a = g[1].strip()

            if "Uptime" in str(i):
                uptime = rows[x+1].text

            if "Администратор" in str(i):
                admin = rows[x+1].text

        return(self.create_dict(
            id=id,
            agregator=self.agregator,
            server_name=server_name,
            raiting=raiting,
            cite=cite,
            vk=vk,
            votes_m=votes_m,
            votes_d=votes_d,
            players_o=players_o,
            players_a=players_a,
            uptime=uptime,
            admin=admin
        ))

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

