import requests
import os
from access_tokens import access_token_friends

subscriptions_list = []
positive_answers = ['yes', 'y', '']


def target_Subscriptions_output():
    with open("VK_account_scan_results.txt", 'a') as output:
        output.write('TARGET SUBSCRIPTIONS => \n')
        for row in subscriptions_list:
            output.write(str(row) + '\n')


def AD_scan(AD_scan_results):
    for line in subscriptions_list:
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
        target_Subscriptions_output()
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
        ).lower()
        if save_output in positive_answers:
            target_Subscriptions_output()
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
            target_Subscriptions_output()
            print(
                "One can find \033[1;94mVK \033[1;00mscan results in \033[1;94m{}/VK_account_scan_results.txt\033[1;00m\n"
                .format(os.getcwd()))
        else:
            print("")


def Subscriptions():
    target = input("Enter correct user_id: ")
    print("Getting information...")
    subscriptions = requests.get(
        "https://api.vk.com/method/users.getSubscriptions?user_id={0}&extended=1&count=200&access_token={1}&v=5.131"
        .format(target, access_token_friends))
    data = subscriptions.json()["response"]["items"]
    ids = input(
        "Would one like to get \033[1;94mSubscriptions \033[1;00mIDs (y/n)? "
    ).lower()
    if ids in positive_answers:
        for item in data:
            try:
                item = item["name"] + " " + "id={}".format(item["id"])
                print(item)
                subscriptions_list.append(item)
            except KeyError:
                item = item["first_name"] + " " + item[
                    "last_name"] + " " + "id={}".format(item["id"])
                print(item)
                subscriptions_list.append(item)
    else:
        for item in data:
            try:
                item = item["name"]
                print(item)
                subscriptions_list.append(item)
            except KeyError:
                item = item["first_name"] + " " + item["last_name"]
                print(item)
                subscriptions_list.append(item)
    print(
        "Total amount of target\033[1;94m Subscriptions\033[1;00m is\033[1;95m",
        subscriptions.json()["response"]["count"], "\033[1;00m")
    compare_results()
