import requests
import json
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ваш access_token от YANDEX
ACCESS_TOKEN_YANDEX = "Ваш access_token от YANDEX"

# Ваш access_token от VK
ACCESS_TOKEN_VK = "Ваш access_token от VK"

# Параметры запроса для получения информации о пользователе
PARAMS_INFO = {
    "access_token": ACCESS_TOKEN_VK,
    "v": "5.131",  # Версия API ВКонтакте
    "user_ids": "Заменить на свой id из VK",  # Имя пользователя или его ID
    "fields": "photo_id",  # Поля, которые вы хотите получить (например, photo_id)
}

# Параметры запроса для получения фотографий пользователя
PARAMS_PHOTO = {
    "owner_id": "1",  # ID пользователя (замените на ID пользователя)
    "album_id": "profile",  # Альбом, из которого хотите получить фотографии
    "extended": 1,
    "count": 5,
    "rev": 1,  # Порядок сортировки фотографий
    "photo_sizes": 1,  # Возвращать ли размеры фотографий
    "access_token": ACCESS_TOKEN_VK,
    "v": "5.131",  # Версия API ВКонтакте
}

def user_info():
    # Выполнение GET-запроса
    user_get = requests.get("https://api.vk.com/method/users.get", params=PARAMS_INFO)

    # Преобразование ответа в JSON формат
    json_data = user_get.json()

    # Сохранение JSON данных в файл
    with open("json_vk.json", "w") as js:
        json.dump(json_data, js, indent=2)

    return json_data

def user_photo():
    # Выполнение GET-запроса
    user_get_photo = requests.get("https://api.vk.com/method/photos.get", params=PARAMS_PHOTO)

    # Преобразование ответа в JSON формат
    json_data = user_get_photo.json()

    # Сохранение JSON данных в файл
    with open("json_vk_photos.json", "w") as js_p:
        json.dump(json_data, js_p, indent=2)

    return json_data

def filtred_photo():
    with open("json_vk_photos.json", "r") as fl_p:
        data = json.load(fl_p)
        if "response" in data:
            photo_set = data["response"]["items"]
            photo_sort = []
            for photo in photo_set:
                max_size_photo = max(photo["sizes"], key=lambda size: size["width"])
                if max_size_photo["type"] == "z":
                    max_size_photo["likes"] = photo["likes"]["count"]
                    photo_sort.append(max_size_photo)
            
            # Сохранение отфильтрованных данных в новый файл
            with open("all_photo_size_z.json", "w") as ph_all:
                json.dump(photo_sort, ph_all, indent=2)
            return photo_sort
        return None

def yandex_create_folder(path):
    url = "https://cloud-api.yandex.net/v1/disk/resources"
    headers = {"Authorization": f"OAuth {ACCESS_TOKEN_YANDEX}"}
    params = {"path": path}
    response = requests.put(url, headers=headers, params=params)
    if response.status_code != 201:
        logging.info(f"Папка '{path}' уже существует или возникла ошибка: {response.status_code}")

def yandex_get_upload_link(path, overwrite=True):
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {"Authorization": f"OAuth {ACCESS_TOKEN_YANDEX}"}
    params = {"path": path, "overwrite": "true" if overwrite else "false"}
    response = requests.get(upload_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get("href")

def yandex_upload_file(upload_url, file_path):
    with open(file_path, "rb") as f:
        response = requests.put(upload_url, files={"file": f})
    response.raise_for_status()

def save_filtered_photos_to_yandex():
    folder_path = "netology"
    
    # Создаем папку на локальном диске, если она не существует
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Создаем папку на Яндекс.Диске
    yandex_create_folder(folder_path)
    
    filtered_photos = filtred_photo()
    for photo in filtered_photos:
        file_name = f"{photo['likes']}.jpg"
        file_path = os.path.join(folder_path, file_name)
        
        # Скачать фотографию с URL и сохранить на локальном диске временно
        photo_url = photo['url']
        photo_data = requests.get(photo_url)
        with open(file_path, "wb") as file:
            file.write(photo_data.content)
        
        # Загрузить на Яндекс.Диск
        upload_link = yandex_get_upload_link(f"{folder_path}/{file_name}")
        yandex_upload_file(upload_link, file_path)
        
        # Удалить временный файл с локального диска
        os.remove(file_path)
    
    logging.info("Файлы успешно загружены на Яндекс.Диск")

print(user_info())
print(user_photo())
save_filtered_photos_to_yandex()
