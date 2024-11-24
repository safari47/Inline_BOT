import json
from urllib import parse, request
import asyncio
from config.config import settings
from example.example import contact_list
import requests


# Асинхронная функция для работы с Giphy API
async def search_gifs(query: str, offset=0, limit=10):
    """
    Поиск GIF через Giphy API
    :param query: строка запроса
    :param offset: смещение для пагинации
    :param limit: количество гифок на страницу
    :return: список гифок
    """
    url = "http://api.giphy.com/v1/gifs/search"

    # Формируем параметры запроса с учетом оффсета и лимита
    params = parse.urlencode(
        {"q": query, "api_key": settings.API_KEY, "limit": limit, "offset": offset}
    )

    # Выполняем запрос к Giphy API
    with request.urlopen("".join((url, "?", params))) as response:
        data = json.loads(response.read())

    # Достаём данные о гифках
    gif_data = data.get("data")
    return gif_data


async def search_contact(query: str) -> list:
    """
    Асинхронная функция для поиска контактов в списке `contact_list`.

    Аргументы:
        query (str): Строка для поиска (может быть частью имени или фамилии).

    Возвращает:
        list: Список контактов, которые соответствуют запросу (по имени или фамилии).
              Возвращается пустой список, если соответствий нет.

    Особенности:
        - Поиск нечувствителен к регистру (обрабатывается методом `.lower()`).
        - Проверяются имена (first_name) и фамилии (last_name) контактов в `contact_list`.

    Исключения:
        Предполагается, что `contact_list` определён ранее и имеет структуру объектов с атрибутами `first_name` и `last_name`.
    """
    result = []
    for contact in contact_list:
        if (
            query.lower() in contact.first_name.lower()
            or query in contact.last_name.lower()
        ):
            result.append(contact)
    return result


async def search_organization(query: str, latitude: str, longitude: str):
    """
    Асинхронная функция для поиска организаций через API 2GIS.

    Аргументы:
        query (str): Строка для поиска (например, название организации).
        latitude (str): Широта центральной точки поиска.
        longitude (str): Долгота центральной точки поиска.

    Возвращает:
        list: Список организаций, содержащий данные о местоположении, адресе и другой информации, 
              либо пустой список [] в случае ошибок или отсутствия данных.

    Исключения:
        Обрабатываются ошибки HTTP-запросов (requests.exceptions.RequestException) и другие неожиданные исключения, 
        возвращается пустой список.
    """
    # Формируем параметры запроса
    attr = "items.point,items.full_address_name,items.external_content"
    url = f"https://catalog.api.2gis.com/3.0/items?q={query}&point=20.568384,54.711494&radius=5000&sort_point=20.568384,54.711494&sort=distance&fields={attr}&key={settings.GIS2_API_KEY}"
    # Выполняем HTTP-запрос
    try:
        request_data = requests.get(url, timeout=10).json()  # Указываем тайм-аут для запроса
        
        # Проверяем, есть ли ключ 'result' в ответе
        if 'result' in request_data and 'items' in request_data['result']:
            return request_data["result"]["items"]
        else:
            # Возвращаем пустой список, если 'result' или 'items' нет
            return []

    except requests.exceptions.RequestException as e:
        # Логируем ошибку, если была проблема с запросом
        print(f"Ошибка запроса к API 2GIS: {e}")
        return []

    except Exception as e:
        # Логируем другие ошибки
        print(f"Неожиданная ошибка: {e}")
        return []
