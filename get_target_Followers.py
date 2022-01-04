import requests
import os
import time
from access_tokens import access_token_friends

followers_list = []
positive_answers = ["y", "yes", ""]
AD_intersections_list = []


def get_info(user_id, offset, ids):
    target_followers = requests.get(
        "https://api.vk.com/method/users.getFollowers?&user_id={0}&fields=first_name,last_name,city&count=1000&offset={1}&access_token={2}&v=5.131"
        .format(user_id, offset, access_token_friends))
    followers = target_followers.json()["response"]["items"]
    if ids in positive_answers:
        for item in followers:
            try:
                item = item["first_name"] + " " + item[
                    "last_name"] + " " + "id={}".format(
                        item["id"]) + " " + item["city"]["title"]
                print(item)
                followers_list.append(item)
            except KeyError:
                item = item["first_name"] + " " + item[
                    "last_name"] + " " + "id={}".format(item["id"])
                print(item)
                followers_list.append(item)
    else:
        for item in followers:
            item = item["first_name"] + " " + item["last_name"]
            print(item)
            followers_list.append(item)


def target_Followers_output(user_id):
    with open("VK_account_scan_results.txt", 'a') as output:
        output.write('TARGET (id = {}) FOLLOWERS => \n'.format(user_id))
        for row in followers_list:
            output.write(str(row) + '\n')


def AD_scan(AD_scan_results):
    formatted_AD_users_list = []
    final_AD_users_list = []
    with open(AD_scan_results) as AD:
        for item in AD.readlines():
            formatted_AD_users_list.append(item)
    for line in formatted_AD_users_list:
        line = " ".join(line.split())
        final_AD_users_list.append(line)
    for line in followers_list:
        for item in final_AD_users_list:
            if line in item:
                AD_intersections_list.append(
                    "Active Directory user: {0} => VK user: {1}\n".format(
                        item, line))
                print(
                    "\033[1;95mActive Directory user: \033[1;00m{0} => \033[1;94mVK user: \033[1;00m{1}\033[1;00m"
                    .format(item, line))


def compare_results(user_id):
    compare_files = input(
        "\nWould one like to compare \033[1;94mVK \033[1;00maccount scan results with \033[1;95mActive Directory \033[1;00musers scan results (y/n)? "
    ).lower()
    if compare_files in positive_answers:
        target_Followers_output(user_id)
        AD_users_scan_script = input(
            "Would one like to scan \033[1;95mActive Directory \033[1;00m(y/n)? "
        ).lower()
        if AD_users_scan_script in positive_answers:
            AD_scan_command = input(
                "Enter the powershell command to scan \033[1;95mActive Directory \033[1;00musers (without saving results to txt file) or press <Enter> to run default command: "
            )
            if AD_scan_command == "":
                os.system(
                    "powershell.exe -ExecutionPolicy ByPass -c 'Get-ADUser -Filter * | Format-Table GivenName, Surname | Out-File -FilePath AD_scan_results.txt -Encoding UTF8'"
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
            target_Followers_output(user_id)
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
            target_Followers_output(user_id)
            print(
                "One can find \033[1;94mVK \033[1;00mscan results in \033[1;94m{}/VK_account_scan_results.txt\033[1;00m\n"
                .format(os.getcwd()))
        else:
            print("")

    if len(AD_intersections_list) != 0:
        with open("AD_vs_VK_{}_intersections.txt".format(user_id),
                  "a") as AD_inter:
            for item in AD_intersections_list:
                AD_inter.write(item)
        print(
            "One can find \033[1;95mActive Directory \033[1;00mand \033[1;94mVK \033[1;00mintersections in \033[1;94m{0}/AD_vs_VK_{1}_intersections.txt\033[1;00m\n"
            .format(os.getcwd(), user_id))


def Followers():
    try:
        user_id = input("Enter correct user_id: ")
        print("Getting information...")
        offset = 0
        count = requests.get(
            "https://api.vk.com/method/users.getFollowers?&user_id={0}&fields=first_name,last_name,city&count=1000&offset={1}&access_token={2}&v=5.131"
            .format(user_id, offset,
                    access_token_friends)).json()["response"]["count"]
        ids = input("Would one like to get cities and IDs (y/n)? ").lower()
        while offset < count:
            get_info(user_id, offset, ids)
            time.sleep(0.1)
            offset += 1000
        print("Total amount of target \033[1;94mFollowers \033[1;00mis\033[1;94m",
              count, "\033[1;00m")
        compare_results(user_id)
    except KeyError:
        print("\n\033[1;91mNot correct input!\n\033[1;00m")
