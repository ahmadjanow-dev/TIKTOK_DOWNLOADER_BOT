# Создаем бота для скачивания видео с TikTok.
# Импортируем необходимые библиотеки.
from aiogram import Bot, Dispatcher, types, executor
# Импортируем токен для Telegram бота из файла config.
from config import token
# Импортируем другие необходимые библиотеки.
import os, time, logging, requests, random

# Создаем объект бота и диспетчер.
bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Обработчик команды /start.
@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.full_name}")

# Обработчик для скачивания и отправки видео.
@dp.message_handler()
async def download_send_video(message: types.Message):
    # Получаем ссылку на видео.
    await message.answer("Скачиваю видео...")
    # Разделяем ссылку по знаку "?" для получения ID видео.
    get_id_video = message.text.split('?')
    # Разделяем URL по символу "/" и получаем кортеж, в котором 5-й элемент содержит ID видео.
    current_id = get_id_video[0].split('/')[5]

    # Получаем информацию о видео через TikTok API.
    video_api = requests.get(f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={current_id}').json()
    video_url = video_api.get('aweme_list')[0].get('video').get('play_addr').get('url_list')[0]
   
    if video_url:
        title_video = video_api.get('aweme_list')[0].get('desc')
        if title_video != ' ':
            title_video = random.randint(1111, 22222)
        try:
            # Сохраняем видео в локальный файл.
            with open(f'video/{title_video}.mp4', 'wb') as video_file:
                video_file.write(requests.get(video_url).content)
            await message.answer("Видео успешно скачано, отправляю...")
        except Exception as error:
            print(f"Error: {error}")
        
        # Отправляем скачанное видео в Telegram.
        try:
            with open(f'video/{title_video}.mp4', 'rb') as send_file:
                await message.answer_video(send_file)
        except Exception as error:
            await message.answer(f"Ошибка: {error}")

# Запускаем бота.
executor.start_polling(dp, skip_updates=True)
