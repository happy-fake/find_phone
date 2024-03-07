# FindPhone
Парсер российских телефонных номеров с web-страниц.

## Форматы номеров
* Искомые форматы номеров:
    <br>7KKKXXXXXXX, 8KKKXXXXXXX с наличием или без разделяющих знаков " ", "(", ")", "-", "—", "–", например +7 (KKK) XXX-XX-XX, 8-KKK-XXX-XX-XX, 8 KKK XXX-XX-XX, т.д.
* Возвращаемые форматы номеров:
    <br>8KKKXXXXXXX

## Импорт и вызов функций
```python
from findphone.sync_module import findphones   # импорт синхронного парсера
from findphone.async_module import afindphones # импорт асинхронного парсера

urls = ["https://hands.ru/company/about/", "https://repetitors.info/",
        "https://twitter.com/", "https://mysmsbox.ru/mobile-handbook"]

data = findphones(urls=urls)  # запуск синхронного парсера
data = afindphones(urls=urls) # запуск асинхронного парсера
```

## Таймаут соединения
По умолчанию значение таймаута равно 5, однако его можно задать самостоятельно:
```python
data = findphones(urls=urls, timeout=10)
data = afindphones(urls=urls, timeout=10)
```

## Интерпретация результатов
Возможные получаемые данные:
 * URL: str - адрес web-страницы;
 * CONTENT: str (удачное соединение) или False (неудачное) - контент web-страницы;
    > Внимание! Соединение со статусом 4XX и 5XX считается удачным - контент данных web-страниц также подлежит парсингу!
 * INFO: {"status": ..., "reason": ...} или {"error": ...} - информация о подключении;
 * PHONES: set() (удачное соединение) или False (неудачное) - множество распознанных телефонных номеров.

### Пример 1
Интерпретация через массив:
```python
print(data.data_phones) # результат в виде списка экземпляров класса SyncDataPhone

for sync_data in data.data_phones:
    print(sync_data.url)     # URL
    print(sync_data.content) # CONTENT
    print(sync_data.info)    # INFO
    print(sync_data.phones)  # PHONES
```

### Пример 2
Интерпретация через DataFrame:
```python
print(data.dataframe_phones) # результат в виде pandas DataFrame со столбцами: URL, INFO, PHONES
```
