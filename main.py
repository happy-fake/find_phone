'''
Примеры вызовов асинхронной (afindphones) и синхронной (findphones)
функций парсинга web-страницы на наличие телефонных номеров российского формата,
например +7 (KKK) XXX-XX-XX, 8-KKK-XXX-XX-XX, 8 KKK XXX-XX-XX, т.д.
'''
from asyncio import run
from findphone.async_module import afindphones
from findphone.sync_module import findphones

if __name__ == "__main__":
    urls = ["https://hands.ru/company/about/", "https://repetitors.info/",
            "https://twitter.com/", "https://mysmsbox.ru/mobile-handbook"]

    print("синхронный парсинг:")
    data = findphones(urls=urls)
    print(data.dataframe_phones)

    print("\nасинхронный парсинг:")
    data = run(afindphones(urls=urls))
    print(data.dataframe_phones)
