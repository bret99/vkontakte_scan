import requests
from access_tokens import access_token_photos
import sys
import os


def photo_download(number, get_photos):
    print("Downloading...")
    photo_index = 0
    while photo_index < number:
        with open("photo_{}.jpg".format(photo_index), "wb") as photo:
            photo.write(
                requests.get(get_photos.json()["response"]["items"]
                             [photo_index]["sizes"][-1]["url"]).content)
        photo_index += 1
    print("One can find target \033[1;94mPhotos \033[1;00min {} directory\n.".
          format(os.getcwd()))


def Photos():
    target = input("Enter correct owner_id: ")
    photos = requests.get(
        "https://api.vk.com/method/photos.getAll?owner_id={0}&count=200&access_token={1}&v=5.131"
        .format(target, access_token_photos))
    count = photos.json()["response"]["count"]
    print(
        "Total \033[1;94mPhotos \033[1;00mamount is \033[1;94m{}\033[1;00m\n".
        format(count))
    photos_amount = input(
        "Enter the number of \033[1;94mPhotos \033[1;00mto download or press <Enter> to download all \033[1;94mPhotos\033[1;00m: "
    )
    try:
        photos_amount = int(photos_amount)
    except ValueError:
        sys.exit("\033[1;91mWrong input!\033[1;00m")
    if photos_amount == "":
        photo_download(count, photos)
    else:
        photo_download(photos_amount, photos)
