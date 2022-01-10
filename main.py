import concurrent.futures
import os
import requests

from utils import time_tracker


ALBUMS_URL = 'https://jsonplaceholder.typicode.com/albums/'
PHOTOS_URL = 'https://jsonplaceholder.typicode.com/photos/'


class UploadInfo:

    @staticmethod
    def get_all_albums(url: str) -> dict:
        resp = requests.get(url)
        albums = resp.json()
        albums_dict = {album['id']: album['title'] for album in albums}
        return albums_dict

    @staticmethod
    def get_all_photos(url: str) -> dict:
        resp = requests.get(url)
        return resp.json()


class PhotoSaver:
    """Класс для сохранения фото по нужным папкам"""

    @staticmethod
    def save_photo(url: str, photo_title: str, album_name: str) -> None:
        response = requests.get(url)
        if not os.path.exists(f'{album_name}'):
            os.makedirs(f'{album_name}')
        with open(f'{album_name}/{photo_title}.png', "wb") as image:
            image.write(response.content)


@time_tracker
def main():
    photos = UploadInfo.get_all_photos(PHOTOS_URL)
    albums = UploadInfo.get_all_albums(ALBUMS_URL)

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for photo in photos:
            executor.submit(
                PhotoSaver.save_photo,
                photo['url'],
                photo['title'],
                albums[photo['albumId']]
            )


if __name__ == '__main__':
    main()
