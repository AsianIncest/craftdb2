import traceback

import requests


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

    def create_dict(self, id=0, agregator='', server_name='', raiting='', cite='', vk='', votes_m='', votes_d='', players_o='', players_a='', uptime='', admin='', timestamp=0):
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
        'admin': admin,
        'timestamp': timestamp
        }


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

