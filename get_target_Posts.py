import requests
import datetime
from access_tokens import access_token_friends
import time
import os

posts_list = []
positive_answers = ["y", "yes", ""]


def get_info(owner_id, offset):
    target_posts = requests.get("https://api.vk.com/method/wall.get?&owner_id={0}&count=100&offset={1}&access_token={2}&v=5.131".format(owner_id, offset, access_token_friends))
    posts = target_posts.json()["response"]["items"]
    for item in posts:
        if item["text"] != "":
            item = "Post ID {0} =>\nDate: {1}\n{2}".format(item["id"], datetime.datetime.fromtimestamp(item["date"]).strftime('%Y-%m-%d %H:%M:%S'), item["text"])
            print(item)
            posts_list.append(item)
        else:
            try:
                item = "Reposted from id {0} =>\nDate: {1}\n{2}".format(str(item["copy_history"][0]["owner_id"])[1:], datetime.datetime.fromtimestamp(item["date"]).strftime('%Y-%m-%d %H:%M:%S'), item["copy_history"][0]["text"])
                print(item)
                posts_list.append(item)
            except KeyError:
                pass

def target_Posts_output(owner_id):
    with open("VK_account_scan_results.txt", 'a') as output:
        output.write('TARGET (id = {}) POSTS => \n'.format(owner_id))
        for row in posts_list:
            output.write(str(row) + '\n')

def Posts():
    try:
        owner_id = input("Enter correct owner_id: ")
        print("Getting information...")
        offset = 0
        count = requests.get("https://api.vk.com/method/wall.get?owner_id={0}&count=100&offset={1}&access_token={2}&v=5.131".format(owner_id, offset, access_token_friends)).json()["response"]["count"]
        while offset < count:
            get_info(owner_id, offset)
            time.sleep(0.1)
            offset += 100
        print("Total amount of target \033[1;94mPosts \033[1;00mis\033[1;94m", count, "\033[1;00m")
        save_output = input("\nWould one like to save \033[1;94mVK \033[1;00mscan results (y/n)? ").lower()
        if save_output in positive_answers:
            target_Posts_output(owner_id)
            print("One can find \033[1;94mVK \033[1;00mscan results in \033[1;94m{}/VK_account_scan_results.txt\033[1;00m\n".format(os.getcwd()))
        else:
            print("")
    except KeyError:
        print("\n\033[1;91mNot correct input!\n\033[1;00m")
