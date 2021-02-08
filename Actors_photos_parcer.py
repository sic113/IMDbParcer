import requests
import json
from bs4 import BeautifulSoup
import lxml
import os

domen = "https://www.imdb.com"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.344"
}

try:
    with open('JSON/actors.json', 'r', encoding='utf-8') as f:
        text = json.load(f)
        actors_count = len(text)
        print(f"Количество актеров в JSON = {actors_count}")
        for i in text:
            actor_name = i.get("name")
            actor_ID = i.get("ID")
            actor_href = domen+"/name/"+actor_ID
            actor_name = actor_name.replace(" ", "_")



            print(f"Начинаем парсинг фотографий актера: {actor_name}")

            # парсинг фото актера
            req = requests.get(url=actor_href, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")


            # создаем папку для хранения фотографий с данным актером
            folder_name = f"data/actors/{actor_name}_{actor_ID}"
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)

            # создаем папку для хранения html с данным актером
            folder_name = f"temp/actors/{actor_name}_{actor_ID}"
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)

            # Сохраняем html-страницу данного актера
            with open(f"temp/actors/{actor_name}_{actor_ID}/{actor_name}_{actor_ID}_page.html", "w", encoding="utf-8") as file:
                file.write(req.text)

            # передаем сохраненный html файл в BeautifulSoup
            with open(f"temp/actors/{actor_name}_{actor_ID}/{actor_name}_{actor_ID}_page.html", "r", encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, "lxml")

            # достаем ссылку на альбом со всеми фотографиями
            all_photos_href = domen+soup.find("div", class_="mediastrip_container").find("div", class_="see-more").find("a").get("href")
            # print(all_photos_href)

            # переходим по новой ссылке в альбом
            req = requests.get(url=all_photos_href, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")

            # сохраняем html файл с альбомом фотографий актера
            with open(f"temp/actors/{actor_name}_{actor_ID}/{actor_name}_{actor_ID}_album.html", "w", encoding="utf-8") as file:
                file.write(req.text)

            # передаем сохраненный html файл в BeautifulSoup
            with open(f"temp/actors/{actor_name}_{actor_ID}/{actor_name}_{actor_ID}_album.html", "r", encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, "lxml")

            # собираем все ссылки на фотографии в высоком разрешении
            soup_photos_hrefs = soup.find("div", class_="media_index_thumb_list").find_all("a")
            # print(soup_photos_hrefs)
            list_photos_hrefs = []
            for href in soup_photos_hrefs:
                big_photo_href = domen+href.get("href")
                # наполняем список ссылками
                list_photos_hrefs.append(big_photo_href)

            count = 1
            print("Всего фотографий обнаружено:" + str(len(list_photos_hrefs)))
            # print(list_photos_hrefs)

            # переходим по каждой ссылке в цикле сохраняя фото
            for item in list_photos_hrefs:
                req = requests.get(url=item, headers=headers)
                soup = BeautifulSoup(req.text, "lxml")
                try:
                    picture_href = soup.find("img", class_="MediaViewerImagestyles__LandscapeImage-sc-1qk433p-1 jcxEsx").get("src")
                except Exception:
                    picture_href = soup.find("img", class_="MediaViewerImagestyles__PortraitImage-sc-1qk433p-0 jLzlho").get(
                        "src")
                # print(picture_href)
                req = requests.get(url=picture_href, headers=headers)
                out = open(f"data/actors/{actor_name}_{actor_ID}/photo_{count}.jpg", "wb")
                out.write(req.content)
                out.close()
                print(f"Фото №{count} успешно сохранено!")
                count += 1

    print("Работа завершена, все фотографии скачаны успешно.")

except Exception as ex:
    print(ex)
