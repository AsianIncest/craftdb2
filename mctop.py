from server_interface import ServerInterface
from bs4 import BeautifulSoup as bs
import lxml
import csv
import os.path
from datetime import datetime as dt

class Agregator_mctop(ServerInterface):
    def __init__(self):
        super().__init__(agregator_main='https://mctop.su/', csv_filename='mctop.csv', csv_header = self.create_dict().keys())
        self.csv_file_exists = os.path.exists(self.csv_filename)

    def get_agrigator_pagination(self):
        links = [self.agregator_main]
        main = self.http_get(self.agregator_main)
        soup = bs(main, "lxml")
        pagination_wrap = soup.find("nav", class_="pagination-wrap")
        pagination_wrap_li = pagination_wrap.findAll("li")
        for i in pagination_wrap_li[2:-1]:
            """мы берём не весь список, а срез, специфика разметки сайта"""
            url = i.find("a").attrs['href']
            links.append(self.agregator_main[:-1] + url)
        return links

    def get_all_servers_url(self, links: list):
        result = []
        for y, i in enumerate(links):
            html = self.http_get(i)
            soup = bs(html, "lxml")
            main_div = soup.find("div", class_="container container-wn")
            servers_div = main_div.find_all("article", class_="col-xs-12 user-pr-card")
            for j in servers_div:
                result.append([y, self.agregator_main[:-1] + j.find("a").attrs['href']])
        return result

    def process_server(self, sertver_url: str, id = 0, server_name='', raiting='', cite='', vk='', votes_m='',
                       votes_d='', players_o='', players_a='', uptime='', admin=''):
        html = self.http_get(sertver_url)
        """
        < header        class ="project-header" >
        div project-body
        tab-content
        """
        html = self.http_get(sertver_url)
        soup = bs(html, 'lxml')
        main = soup.find('section', {'role': 'main'})
        server_name = main.find("header", {"class": "project-header"}).find("h1").text
        raiting = main.find("span", {"class": "project-rating__qty"}).text
        tp = soup.find("div", {"class": "tab-pane active"})
        rows = tp.find("table", {"class": "table table-striped project-info-table"}).findAll("td")
        for x, y in enumerate(rows):

            # print(x,y)
            if 'Сайт проекта' in str(y):
                cite = rows[x + 1].find("a")['href']
            if 'Группа Вконтакте' in str(y):
                vk = rows[x + 1].find("a")['href']
            if 'Голосов' in str(y):
                tmp = rows[x + 1].text
                tmp = tmp.replace('за месяц ', '')
                tmp = tmp.replace(' сегодня ', '')
                tmp = tmp.split(',')
                votes_m = tmp[0].strip()
                votes_d = tmp[1].strip()
            if 'Игроки он-лайн' in str(y):
                tmp = rows[x + 1].text
                players_o = tmp.strip().split("/")[0]
                players_a = tmp.strip().split("/")[1]
            if 'Uptime' in str(y):
                uptime = rows[x + 1].text.strip()

            if 'Администратор' in str(y):
                admin = rows[x + 1].text.strip()
        return(self.create_dict(
            id=id,
            agregator='mctop',
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
        print("Agregator <mctop> started!")
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
                print(f"processing #{i}, <{data['server_name']}>.. OK!")
                data['timestamp'] = current_time
                writer.writerow(data)
                #УБЕРИ ЭТО ДЛЯ ОТЛАДКИ
                if i >= 10:
                    break
                #=====================

