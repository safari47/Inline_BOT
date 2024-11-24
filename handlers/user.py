from aiogram import Router, F
from aiogram.types import (
    InlineQuery,
    InlineQueryResultGif,
    Message,
    InlineQueryResultContact,
    Location,
    InlineQueryResultArticle,
    InlineQueryResultVenue,
)
from aiogram.filters import CommandStart
from keyboards.keyboard import main_kb
from utils.api import search_gifs, search_contact, search_organization
from config.config import bot

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    username = message.from_user.first_name
    await message.answer(
        text=f"✨ Привет, {username}! ✨\n\nНажав на кнопку, ты сможешь написать мне слово, а я найду для тебя подходящую  информацию! 🎉",
        reply_markup=main_kb(),
    )


# @router.inline_query()
# async def gifs_search(inline_query: InlineQuery):
#     """
#     Обработчик InlineQuery с использованием Giphy API
#     """
#     query = inline_query.query  # Текст, введённый пользователем
#     offset = inline_query.offset  # Считываем текущий offset
#     if not offset:
#         offset = 0
#     else:
#         offset = int(offset)  # Переводим offset в число

#     # Определяем лимит (количество гифок на странице)
#     limit = 25

#     # Получаем GIF-данные с учетом смещения и лимита
#     data_gif = await search_gifs(query=query, offset=offset, limit=limit)

#     # Создаём InlineQueryResultGif для каждого GIF
#     result = []
#     for i, gif in enumerate(data_gif):
#         result.append(
#             InlineQueryResultGif(
#                 id=str(i + offset),  # Уникальный ID для каждого результата
#                 gif_url=gif["images"]["original"]["url"],  # URL GIF
#                 thumbnail_url=gif["images"]["preview"]["mp4"],  # Превью
#                 title=gif["title"],  # Заголовок GIF
#             )
#         )

#     # Проверяем, есть ли следующие страницы
#     next_offset = offset + limit if len(data_gif) == limit else None

#     # Отправляем результаты с `next_offset` в ответе
#     await bot.answer_inline_query(
#         inline_query.id,
#         results=result,
#         is_personal=True,  # Персональные данные пользователя
#         next_offset=str(next_offset) if next_offset is not None else '',  # Следующий оффсет
#     )


# @router.inline_query()
# async def contact_search(inline_query: InlineQuery):
#     """
#     Функция представляющая из себя справочник номеров
#     """
#     contact_data = await search_contact(inline_query.query)
#     result = []
#     for i, contact in enumerate(contact_data):
#         result.append(
#             InlineQueryResultContact(
#                 id=str(i),
#                 phone_number=contact.phone_number,
#                 first_name=contact.first_name,
#                 last_name=contact.last_name,
#                 vcard=f"BEGIN:VCARD\nVERSION:3.0\nN:{contact.last_name};{contact.first_name}\nFN:{contact.first_name} {contact.last_name}\nTEL;TYPE=CELL:{contact.phone_number}\nEND:VCARD",
#             )
#         )
#     await bot.answer_inline_query(inline_query.id, results=result)


@router.inline_query()
async def search_map(inline_query: InlineQuery):
    # Проверяем наличие локации
    if inline_query.location:
        latitude = inline_query.location.latitude
        longitude = inline_query.location.longitude

        # Вызываем функцию поиска организаций на основе координат и запроса
        organization = await search_organization(
            query=inline_query.query,
            latitude=latitude,
            longitude=longitude,
        )
        
        # Если организация найдена
        if organization:
            results = []
            for i, item in enumerate(organization):
                # Проверяем, доступно ли фото
                photo = item["external_content"][0].get("main_photo_url") if item.get("external_content") else None

                # Добавляем объект в inline-результаты
                results.append(
                    InlineQueryResultVenue(
                        id=str(i),
                        latitude=item["point"]["lat"],
                        longitude=item["point"]["lon"],
                        title=item["name"],
                        address=item["address_name"],
                        thumbnail_url=photo,
                    )
                )
            # Отправляем результаты пользователю
            await inline_query.answer(results=results, cache_time=10)

        else:
            # Если ничего не найдено, отправляем уведомление
            await inline_query.answer(
                results=[],
                switch_pm_text="Ничего не найдено, попробуйте изменить запрос.",
                switch_pm_parameter="no_results"
            )
    
    else:
        # Если локация отсутствует, информируем пользователя
        await inline_query.answer(
            results=[],
            switch_pm_text="Пожалуйста, включите передачу геолокации!",
            switch_pm_parameter="location_help"
        )