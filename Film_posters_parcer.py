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
    with open('JSON/film.json', 'r', encoding='utf-8') as f:

        text = json.load(f)
        film_count = len(text)
        print(f"Количество фильмов в JSON = {film_count}")
        for i in text:
            film_name = i.get("name")
            film_ID = i.get("ID")
            film_href = domen + "/title/" + film_ID
            film_name = film_name.replace(" ", "_")
            # print(film_name)
            # print(film_href)
            # print("#"*20)


            print(f"Начинаем парсинг постеров фильма: {film_name}")


            req = requests.get(url=film_href, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")

            # создаем папку для хранения постеров фильма
            folder_name = f"data/films/{film_name}_{film_ID}"
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)

            # создаем папку для хранения html с данным актером
            folder_name = f"temp/films/{film_name}_{film_ID}"
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)

            # Сохраняем html-страницу данного фильма
            with open(f"temp/films/{film_name}_{film_ID}/{film_name}_{film_ID}_page.html", "w", encoding="utf-8") as file:
                file.write(req.text)

            # передаем сохраненный html файл в BeautifulSoup
            with open(f"temp/films/{film_name}_{film_ID}/{film_name}_{film_ID}_page.html", "r",
                      encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, "lxml")

            poster_href = domen+soup.find("div", class_="poster").find("a").get("href")
            poster_href = poster_href.split("?")[0]

            req = requests.get(url=poster_href, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            try:
                poster_img = soup.find("img",
                                         class_="MediaViewerImagestyles__LandscapeImage-sc-1qk433p-1 jcxEsx").get("src")
            except Exception:
                picture_img = soup.find("img", class_="MediaViewerImagestyles__PortraitImage-sc-1qk433p-0 jLzlho").get(
                    "src")
            req = requests.get(url=picture_img, headers=headers)
            out = open(f"data/films/{film_name}_{film_ID}/poster_{film_name}.jpg", "wb")
            out.write(req.content)
            out.close()
            print(f"Постер фильма: \"{film_name}\" успешно сохранен!")
        print("Работа завершена, все фотографии скачаны успешно.")


except Exception as ex:
    print(ex)