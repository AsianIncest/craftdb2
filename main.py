import traceback
import requests
from bs4 import BeautifulSoup as bs
import lxml
import csv
import os.path

class ServerInterface:
    """
    Тут общая структура того что должны переопределить классы потомки
    никакой "бизнесс"-логики
    """
    def __init__(self, agregator_main: str, csv_filename:str, csv_header:str):
        self.agregator_main = agregator_main
        #self.pagination = []
        self.csv_filename = csv_filename
        self.csv_header = csv_header

    def err(self, stack):
        """
        Защита от дурака)), если попытаться вызвать не переопределённую функцию!
        :param stack:
        traceback.extract_stack()
        :return:
        Закрывает прогу при вызове и выводит имя функции
        """
        try:
            print(f"Краш переопредели функцию - {stack[-1].name} \n {stack[-2].line}")
        except Exception as e:
            print(f"Необработанное исключение! \n{e}")
        exit(1)


    def get_agrigator_pagination(self):
        """
            ШАГ 1 - получает ссылки на все страницы серверов агрегатора, пример:
            https://mctop.su/page-2/
            https://mctop.su/page-3/

            Специфичная тема для каждого агрегатора
        """
        self.err(traceback.extract_stack())

    def get_all_servers_url(self):
        """
            ШАГ 2 - получить ссылки на сервера, пример
            https://mctop.su/servers/1088/
            https://mctop.su/servers/1/
        """
        self.err(traceback.extract_stack())


    def process_server(self, sertver_url: str):
        """
            Парсит страничку отдельного сервера
        :param sertver_url:
            прим.: https://mctop.su/servers/1088/
        :return:
            возвратит словарик с данными
        """
        self.err(traceback.extract_stack())

    def create_dict(self, id=0, agregator='', server_name='', raiting='', cite='', vk='', votes_m='', votes_d='', players_o='', players_a='', uptime='', admin=''):
        """
            Генерируем словарик, ПОКА ЧЕРНОВИК
        :return:
        """
        return {'id': id,
        'agregator': agregator,
        'server_name': server_name,
        'raiting': raiting,
        'cite': cite,
        'vk': vk,
        'votes_mounth': votes_m,
        'votes_day': votes_d,
        'players_online': players_o,
        'players_all': players_a,
        'uptime': uptime,
        'admin': admin}


    def print_data(self):
        """
            Выводим данные в словарике
        :return:
        """
        self.err(traceback.extract_stack())

    def save_data(self, file : str):
        """
            Сохраним куда-нибудь, пример в файл, потом перикручу БД
        :param file:
            путь к файлу, полный
        :return:
        """
        self.err(traceback.extract_stack())

    def http_get(self, url):
        try:
            r = requests.get(url)
        except Exception as e:
            print(f"URL={url}")
            print(e)
            exit(1)
        return r.text


class Agregator_mctop(ServerInterface):
    def __init__(self):
        super().__init__(agregator_main='https://mctop.su/', csv_filename='mctop.csv',
                         csv_header = "id, agregator, server_name, raiting, cite, vk, votes_mounth, votes_day, players_online, players_all, uptime, admin")
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
                pass
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
        print("Agregator <mctop> started!")
        pagination = self.get_agrigator_pagination()
        print("pagination.. OK!")
        links = mctop.get_all_servers_url(pagination)
        print("server links.. OK!")
        with open(self.csv_filename, 'a', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.csv_header.split(", "))
            if not self.csv_file_exists:
                writer.writeheader()
            for i, link in enumerate(links):
                data = self.process_server(id=i, sertver_url=link[1])
                print(f"processing #{i}, <{data['server_name']}>.. OK!")
                writer.writerow(data)



if __name__ == "__main__":
    mctop = Agregator_mctop()
    mctop.start()


