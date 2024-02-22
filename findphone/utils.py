'''
Общемодульные утилиты и базовые классы
'''
from re import findall
from pandas import DataFrame, concat
from phonenumbers import is_valid_number, parse

class PFindPhone():
    '''
    Базовый класс поиска российских номеров форматов: 7KKKXXXXXXX, 8KKKXXXXXXX
    с наличием или без разделяющих знаков " ", "(", ")", "-", "—", "–",
    например +7 (KKK) XXX-XX-XX, 8-KKK-XXX-XX-XX, 8 KKK XXX-XX-XX, т.д.
    '''
    def __init__(self, url: str = None, info: dict = None, content: str | bool = None) -> None:
        self.url = url
        self.info = info
        self.content = content
        self.phones = self.get_phone()

    def get_phone(self) -> set[str] | bool:
        ''' Обобщающий метод парсинга номеров в content '''
        if self.content:
            content = self.delete_symbols(self.content)
            phones = self.find_regular(content)
        else:
            phones = self.content
        return phones

    def delete_symbols(self, content: str) -> str:
        ''' Удаление символов, незначащих при записи номера телефона:
        " ", "(", ")", "-", "—", "–"
        '''
        values_delete = ("(", ")", "-", " ", "—", "–")
        for val in values_delete:
            content = content.replace(val, "")
        return content

    def find_regular(self, content: str) -> set[str]:
        ''' Поиск в content всех вхождений, удовлетворяющих формату номера телефона
        и проверка на его валидацию
        '''
        phones = set()
        for phone in set(findall(r'''\D(7|8)(\d{10})\D''', content)):
            if is_valid_number(parse("+7" + phone[1])):
                phones.add("8" + phone[1])
        return phones

class PrettyDataPhone:
    '''
    Класс хранения экземпляров PFindPhone в виде списка или pandas DataFrame
    '''
    def __init__(self, arr: list[PFindPhone] = None) -> None:
        if arr is None:
            arr = []
        self.data_phones = arr
        self.dataframe_phones = self.dataframe()

    def add(self, arr: list[PFindPhone] | PFindPhone) -> None:
        ''' Добавление нового экземпляра (списка экземпляров) класса PFindPhone
        '''
        if not isinstance(arr, list):
            arr = [arr]
        self.data_phones = self.data_phones + arr
        new_rows = DataFrame([{'URL': a.url, 'INFO': a.info, 'PHONES': a.phones} for a in arr])
        self.dataframe_phones = concat([self.dataframe_phones, new_rows], ignore_index=True)

    def dataframe(self) -> DataFrame:
        ''' Преобразование данных списка экземпляров PFindPhone к pandas DataFrame
        '''
        dataframe = [[fp.url, fp.info, list(fp.phones)] for fp in self.data_phones]
        dataframe = DataFrame(dataframe, columns=["URL", "INFO", "PHONES"])
        return dataframe
