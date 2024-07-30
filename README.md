# Что делает программа

1. Получение информации о пользователе VK: Программа делает запрос к API VK, чтобы получить информацию о пользователе. Полученная информация сохраняется в файл json_vk.json.

2. Получение фотографий пользователя VK: Программа делает запрос к API VK для получения фотографий пользователя. Полученные данные сохраняются в файл json_vk_photos.json.

3. Фильтрация фотографий: Программа читает данные из файла json_vk_photos.json и фильтрует фотографии, выбирая только фотографии самого большого размера (размер z). Отфильтрованные данные сохраняются в файл all_photo_size_z.json.

4. Создание папки на Яндекс.Диске: Программа создает папку netology на Яндекс.Диске. Если папка уже существует, программа выводит соответствующее сообщение.

5. Загрузка фотографий на Яндекс.Диск: Программа загружает отфильтрованные фотографии на Яндекс.Диск в папку netology. Фотографии сохраняются с именами, соответствующими количеству лайков.

6. Удаление временных файлов: После загрузки на Яндекс.Диск временные файлы на локальном диске удаляются.

# Примечание

## Для получения токенов доступа вам потребуется зарегистрировать приложение в VK и Яндекс.Диск и получить соответствующие токены.

Для VK:

1. Перейдите на страницу создания приложения VK.
2. Создайте приложение и получите токен доступа.

Для Яндекс.Диска:

1. Перейдите на страницу Яндекс OAuth.
2. Создайте приложение и получите токен доступа.

Лицензия

Этот проект был разработан и адаптирован Shadowgraph (Никнейм создателя!)

## Требования

- Python 3.x
- requests

## Установка

1. Клонируйте репозиторий:

    ```sh
    git clone git@github.com:Shadowgraph-1/glowing-octo-fortnight.git
    cd glowing-octo-fortnight
    ```

2. Установите зависимости:

    ```sh
    pip install -r requirements.txt
    ```

## Конфигурация

1. Откройте файл `vk_yandex.py` в любом текстовом редакторе.
2. Найдите строки с токенами доступа и замените `ваш_access_token_yandex` и `ваш_access_token_vk` на ваши реальные токены доступа:

    ```python
    # Ваш access_token от YANDEX
    ACCESS_TOKEN_YANDEX = "ваш_access_token_yandex"

    # Ваш access_token от VK
    ACCESS_TOKEN_VK = "ваш_access_token_vk"
    ```

## Использование

Запустите программу:

```sh
python vk_yandex.py
