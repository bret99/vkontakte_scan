import requests
import os
from access_tokens import access_token_friends

friends_list = []
followers_list = []
positive_answers = ['yes', 'y', '']


def get_info(method, users):
    data = method.json()["response"]["items"]
    ids = input("Would one like to get cities and IDs (y/n)? ").lower()
    if ids in positive_answers:
        for item in data:
            try:
                item = item["first_name"] + " " + item[
                    "last_name"] + " " + "id={}".format(
                        item["id"]) + " " + item["city"]["title"]
                print(item)
                users.append(item)
            except KeyError:
                item = item["first_name"] + " " + item[
                    "last_name"] + " " + "id={}".format(item["id"])
                print(item)
                users.append(item)
    else:
        for item in data:
            item = item["first_name"] + " " + item["last_name"]
            print(item)
            users.append(item)


def target_Friends_and_Followers_output():
    with open("VK_account_scan_results.txt", 'a') as output:
        output.write('TARGET FRIENDS => \n')
        for row in friends_list:
            output.write(str(row) + '\n')
        output.write('TARGET FOLLOWERS => \n')
        for row in followers_list:
            output.write(str(row) + '\n')


def AD_scan(AD_scan_results):
    friends_and_followers_list = friends_list + followers_list
    for line in friends_and_followers_list:
        with open(AD_scan_results) as AD:
            for item in AD.readlines():
                if line in item:
                    print(
                        "\033[1;95mActive Directory user: \033[1;00m{0}=> \033[1;94mVK user: \033[1;00m{1}\033[1;00m"
                        .format(item, line))


def compare_results():
    compare_files = input(
        "\nWould one like to compare \033[1;94mVK \033[1;00maccount scan results with \033[1;95mActive Directory \033[1;00musers scan results (y/n)? "
    ).lower()
    if compare_files in positive_answers:
        target_Friends_and_Followers_output()
        AD_users_scan_script = input(
            "Would one like to scan \033[1;95mActive Directory \033[1;00m(y/n)? "
        ).lower()
        if AD_users_scan_script in positive_answers:
            AD_scan_command = input(
                "Enter the powershell command to scan \033[1;95mActive Directory \033[1;00musers (without saving results to txt file) or press <Enter> to run default command: "
            )
            if AD_scan_command == "":
                os.system(
                    "powershell.exe -ExecutionPolicy ByPass -c 'Get-ADUser -Filter * | Format-Table Name | Out-File -FilePath AD_scan_results.txt -Encoding UTF8'"
                )
            else:
                os.system(
                    "powershell.exe -ExecutionPolicy ByPass -c '{} | Out-File -FilePath AD_scan_results.txt -Encoding UTF8'"
                    .format(AD_scan_command))
            AD_scan("AD_scan_results.txt")
            os.system("rm AD_scan_results.txt")
        else:
            AD_users_scan = input(
                "Enter path to file with \033[1;94mActive Directory \033[1;00musers: "
            )
            AD_scan(AD_users_scan)
        save_output = input(
            "\nWould one like to save \033[1;94mVK \033[1;00mscan results (y/n)? "
        )
        if save_output in positive_answers:
            target_Friends_and_Followers_output()
            print(
                "One can find \033[1;94mVK \033[1;00mscan results in \033[1;94m{}/VK_account_scan_results.txt\033[1;00m\n"
                .format(os.getcwd()))
        else:
            os.system("rm VK_account_scan_results.txt")
            print("")

    else:
        save_output = input(
            "\nWould one like to save \033[1;94mVK \033[1;00mscan results (y/n)? "
        ).lower()
        if save_output in positive_answers:
            target_Friends_and_Followers_output()
            print(
                "One can find \033[1;94mVK \033[1;00mscan results in \033[1;94m/{}VK_account_scan_results.txt\033[1;00m\n"
                .format(os.getcwd()))
        else:
            print("")


def Friends_and_Followers():
    get_friends = input(
        "Would one like to get target \033[1;94mFriends \033[1;00m(y/n)? "
    ).lower()
    if get_friends in positive_answers:
        target = input("Enter correct user_id: ")
        print("Getting information...")
        friends = requests.get(
            "https://api.vk.com/method/friends.get?user_id={0}&fields=first_name,last_name,city&access_token={1}&v=5.131"
            .format(target, access_token_friends))
        get_info(friends, friends_list)
        print(
            "Total amount of target \033[1;94mFriends \033[1;00mis\033[1;95m",
            friends.json()["response"]["count"], "\033[1;00m")
        get_followers = input(
            "Would one like to get target \033[1;94mFollowers \033[1;00m(y/n)? "
        ).lower()
        if get_followers in positive_answers:
            print("Getting iformation...")
            followers = requests.get(
                "https://api.vk.com/method/users.getFollowers?user_id={0}&fields=first_name,last_name,city&count=1000&access_token={1}&v=5.131"
                .format(target, access_token_friends))
            get_info(followers, followers_list)
            print(
                "Total amount of target \033[1;94mFollowers \033[1;00mis\033[1;95m",
                followers.json()["response"]["count"], "\033[1;00m")
            compare_results()
        else:
            compare_results()
    else:
        get_followers = input(
            "Would one like to get target \033[1;94mFollowers \033[1;00m(y/n)? "
        ).lower()
        if get_followers in positive_answers:
            print("Getting information...")
            followers = requests.get(
                "https://api.vk.com/method/users.getFollowers?user_id={0}&fields=first_name,last_name&count=1000&access_token={1}&v=5.131"
                .format(target, access_token_friends))
            get_info(followers, followers_list)
            print(
                "Total amount of target \033[1;94mFollowers \033[1;00mis\033[1;95m",
                followers.json()["response"]["count"], "\033[1;00m")
            compare_results()
        else:
            print("")
