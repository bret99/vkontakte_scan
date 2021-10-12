import requests
from access_tokens import access_token_friends
import os

groups_list = []
positive_answers = ['yes', 'y', '']


def target_Groups_output():
    with open("VK_account_scan_results.txt", 'a') as output:
        output.write('TARGET GROUPS => \n')
        for row in groups_list:
            output.write(str(row) + '\n')


def Groups():
    target = input("Enter correct user_id: ")
    print("Getting information...")
    groups = requests.get(
        "https://api.vk.com/method/groups.get?user_id={0}&extended=1&count=1000&access_token={1}&v=5.131"
        .format(target, access_token_friends))
    data = groups.json()["response"]["items"]
    ids = input("Would one like to get \033[1;94mGroups \033[1;00mIDs (y/n)? "
                ).lower()
    if ids in positive_answers:
        for item in data:
            item = item["name"] + " " + "id={}".format(item["id"])
            print(item)
            groups_list.append(item)
    else:
        for item in data:
            item = item["name"]
            print(item)
            groups_list.append(item)
    print(
        "Total amount of target S\033[1;94mubscriptions i\033[1;00ms\033[1;95m",
        groups.json()["response"]["count"], "\033[1;00m")
    save_output = input(
        "\nWould one like to save \033[1;94mVK \033[1;00mscan results (y/n)? "
    ).lower()
    if save_output in positive_answers:
        target_Groups_output()
        print(
            "One can find \033[1;94mVK \033[1;00mscan results in \033[1;94m{}/VK_account_scan_results.txt\033[1;00m\n"
            .format(os.getcwd()))
    else:
        print("")
