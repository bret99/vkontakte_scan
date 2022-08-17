import requests
import datetime
from access_tokens import access_token_photos
import sys
import os
import time
from requests.exceptions import ConnectionError

def get_target_photos(get_photos, owner_id):
    try:
        os.mkdir("id_{}_photos".format(owner_id))
    except FileExistsError:
        pass
    photo_index = 0
    while photo_index < len(get_photos.json()["response"]["items"]):
        try:
            with open("id_{0}_photos/photo_{1}.jpg".format(owner_id, datetime.datetime.fromtimestamp(get_photos.json()["response"]["items"][photo_index]["date"]).strftime('%Y-%m-%d %H:%M:%S')), "wb") as photo:
                photo.write(requests.get(get_photos.json()["response"]["items"][photo_index]["sizes"][-1]["url"]).content)
                photo_index += 1
        except ConnectionError:
            pass

def Photos():
    try:
        owner_id = input("Enter correct owner_id: ")
        print("\033[1;90m\nGetting information...\n\033[1;00m")
        photos_count = requests.get("https://api.vk.com/method/photos.getAll?owner_id={0}&count=200&offset=0&extended=1&access_token={1}&v=5.131".format(owner_id, access_token_photos)).json()["response"]["count"]
        print(
            "Total \033[1;94mPhotos \033[1;00mamount is \033[1;94m{}\033[1;00m\n".
            format(photos_count))
        photos_amount = input(
            "Enter the number of \033[1;94mPhotos \033[1;00mto download\033[1;00m: "
        )
        try:
            photos_amount = int(photos_amount)
        except ValueError:
            sys.exit("\033[1;91mWrong input!\033[1;00m")
        if photos_amount > 200:
            print("\033[1;90mDownloading photos...\0331;00m")
            offset = 0
            count = 200
            while offset < photos_amount:
                get_photos = requests.get("https://api.vk.com/method/photos.getAll?owner_id={0}&count={1}&offset={2}&extended=1&access_token={3}&v=5.131".format(owner_id, count, offset, access_token_photos))
                get_target_photos(get_photos, owner_id)
                time.sleep(0.1)
                offset += 200
                if (photos_amount - offset) < 200:
                    count = photos_amount - offset
    
            print("\nOne can find target \033[1;94mPhotos \033[1;00min \033[1;94m{0}/id_{1}_photos \033[1;00mdirectory.\n".format(os.getcwd(), owner_id))
        else:
            get_photos = requests.get("https://api.vk.com/method/photos.getAll?owner_id={0}&count={1}&offset=0&extended=1&access_token={2}&v=5.131".format(owner_id, photos_amount, access_token_photos))
            print("\033[1;90mDownloading photos...\033[1;00m")
            get_target_photos(get_photos, owner_id)
            print("\nOne can find target \033[1;94mPhotos \033[1;00min \033[1;94m{0}/id_{1}_photos \033[1;00mdirectory.\n".format(os.getcwd(), owner_id))
    except KeyError:
        print("\033[1;91mNot correct input or target account is private!\n\033[1;00m")
    except KeyboardInterrupt:
        sys.exit("\n")
