import traceback
import requests


class ServerInterface:
    """
        Тут общая структура того что должны переопределить классы потомки
        никакой "бизнесс"-логики
    """
    def __init__(self, agregator_main: str, csv_filename:str, csv_header:str):
        self.agregator_main = agregator_main
        self.csv_filename = csv_filename
        self.csv_header = csv_header

    def err(self, stack):
        """
            Защита, дочерний класс не может вызвать функции из "шагов" напрямую. Он должен их переопределить.
            Выводим сообщение и закрываемся.
        """
        try:
            print(f"Краш! переопредели функцию - {stack[-1].name} \n {stack[-2].line}")
        except Exception as e:
            print(f"Необработанное исключение! \n{e}")
        exit(1)


    def get_agrigator_pagination(self):
        """
            ШАГ 1 - Парсим пагинатор снизу страницы.
            прим.: <1, 2, 3, 4, 5>


            https://mctop.su/page-2/
            https://mctop.su/page-3/
        """
        self.err(traceback.extract_stack())

    def get_all_servers_url(self):
        """
            ШАГ 2 - Пройтись по всем ссылкам из пагинатора и получить список ссылок
            на персональные странички проектов.
            прим.:
            https://mctop.su/servers/1088/
            https://mctop.su/servers/1/
        """
        self.err(traceback.extract_stack())


    def process_server(self, sertver_url: str):
        """
            ШАГ 3 - Распарсить отдельную страничку и вернуть словарь с результатами
        """
        self.err(traceback.extract_stack())

    def start(self):
        """
            ШАГ 4 - Выполнить последовательно предыдущие шаги, получить текущую дату в формате timestamp.
            Результаты записать в файл.
        :return:
        """
        self.err(traceback.extract_stack())
    def create_dict(self, id=0, agregator='', server_name='', raiting='', cite='', vk='', votes_m='', votes_d='', players_o='', players_a='', uptime='', admin='', timestamp=0):
        """
            Утилитка. Создаёт словарик из своих аргументов. Просто для удобства.
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


    def http_get(self, url):
        """
            Утилитка. Делает HTTP запросы на получение страниц.
        """
        try:
            r = requests.get(url)
        except Exception as e:
            print(f"URL={url}")
            print(e)
            exit(1)
        return r.text

