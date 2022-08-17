import requests
from access_tokens import access_token_friends
import os
import time

groups_list = []
positive_answers = ['yes', 'y', '']


def get_info(user_id, offset, ids):
    target_groups = requests.get(
        "https://api.vk.com/method/groups.get?user_id={0}&extended=1&count=1000&offset={1}&access_token={2}&v=5.131"
        .format(user_id, offset, access_token_friends))
    groups = target_groups.json()["response"]["items"]
    if ids in positive_answers:
        for item in groups:
            item = item["name"] + " " + "id={}".format(item["id"])
            print(item)
            groups_list.append(item)
    else:
        for item in groups:
            item = item["name"]
            print(item)
            groups_list.append(item)


def target_Groups_output(user_id):
    with open("VK_account_scan_results.txt", 'a') as output:
        output.write('TARGET (id = {}) GROUPS => \n'.format(user_id))
        for row in groups_list:
            output.write(str(row) + '\n')


def Groups():
    try:
        user_id = input("Enter correct user_id: ")
        print("\033[1;90m\nGetting information...\n\033[1;00m")
        offset = 0
        count = requests.get(
            "https://api.vk.com/method/groups.get?user_id={0}&extended=1&count=1000&offset={1}&access_token={2}&v=5.131"
            .format(user_id, offset,
                    access_token_friends)).json()["response"]["count"]
        ids = input("Would one like to get cities and IDs (y/n)? ").lower()
        while offset < count:
            get_info(user_id, offset, ids)
            time.sleep(0.1)
            offset += 1000
        print("Total amount of target \033[1;94mGroups \033[1;00mis\033[1;94m",
              count, "\033[1;00m")
        save_output = input(
            "\nWould one like to save \033[1;94mVK \033[1;00mscan results (y/n)? "
        ).lower()
        if save_output in positive_answers:
            target_Groups_output(user_id)
            print(
                "One can find \033[1;94mVK \033[1;00mscan results in \033[1;94m{}/VK_account_scan_results.txt\033[1;00m\n"
                .format(os.getcwd()))
        else:
            print("")
    except KeyError:
        print("\033[1;91mNot correct input or target account is private!\n\033[1;00m")
    except KeyboardInterrupt:
        sys.exit("\n")
