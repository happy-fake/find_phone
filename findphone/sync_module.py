'''
Модуль синхронного поиска телефонных номеров в списке URL
'''
from requests import get
from requests.exceptions import RequestException
from .utils import PFindPhone, PrettyDataPhone

class SyncDataPhone(PFindPhone):
    '''
    Класс синхронного парсинга страниц
    '''
    def __init__(self, url: str, timeout: int) -> None:
        info, content = self.content_html(url, timeout)
        super().__init__(url, info, content)

    def content_html(self, url: str, timeout: int) -> tuple[dict, str | bool]:
        ''' Синхронное получение информации с URL-адреса '''
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        try:
            response = get(url, headers=headers, timeout=timeout)
            info = {"status": response.status_code, "reason": response.reason}
            content = str(response.content)
        except RequestException as ex:
            info = {"error": ex}
            content = False
        return info, content

def findphones(urls: list[str], timeout: int = 5) -> PrettyDataPhone:
    '''
    Синхронный парсинг URL-старниц из получаемого списка и оборачивание
    результатов в PrettyDataPhone для лучшего доступа
    '''
    dataphones = PrettyDataPhone()
    for url in urls:
        dataphone = SyncDataPhone(url, timeout)
        dataphones.add(dataphone)
    return dataphones
