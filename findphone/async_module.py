'''
Модуль асинхронного поиска телефонных номеров в списке URL
'''
from asyncio import as_completed
from asyncio.exceptions import TimeoutError as aTimeoutError
from aiohttp import ClientSession, ClientError, ClientTimeout
from .utils import PFindPhone as AsyncDataPhone, PrettyDataPhone

async def _prepare_dataphone(url: str, session: ClientSession, timeout: int) -> AsyncDataPhone:
    ''' Асинхронное получение информации с URL-адреса '''
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
               AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    try:
        async with session.get(url, headers=headers, timeout=ClientTimeout(total=timeout)) as response:
            content = await response.text()
            info = {"status": response.status, "reason": response.reason}
    except ClientError as ex:
        info = {"error": ex}
        content = False
    except aTimeoutError:
        info = {"error": "TimeoutError: The waiting time has been exceeded"}
        content = False
    dataphone = AsyncDataPhone(url, info, content)
    return dataphone

async def afindphones(urls: list[str], timeout: int = 5) -> PrettyDataPhone:
    '''
    Асинхронный парсинг URL-старниц из получаемого списка и оборачивание
    результатов в PrettyDataPhone для лучшего доступа
    '''
    dataphones = PrettyDataPhone()
    async with ClientSession() as session:
        for dataphone in as_completed([_prepare_dataphone(url, session, timeout) for url in urls]):
            dataphones.add(await dataphone)
    return dataphones
