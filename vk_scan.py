import requests
import os

positive_answers = ['yes', 'y', '']
friends_list = []
followers_list = []

access_token = input("Enter your VK access_token: ")
target = input("Enter correct user_id: ")

def get_info(method, users):
    data = method.json()["response"]["items"]
    ids = input("Would one like to get cities and IDs (y/n)? ")
    if ids in positive_answers:
        for item in data:
            try:
                item = item["first_name"] + " " + item["last_name"] + " " + "id={}".format(item["id"]) + " " + item["city"]["title"]
                print(item)
                users.append(item)
            except KeyError:
                item = item["first_name"] + " " + item["last_name"] + " " + "id={}".format(item["id"])
                print(item)
                users.append(item)
    else:
        for item in data:
            item = item["first_name"] + " " + item["last_name"]
            print(item)
            users.append(item)


def target_output():
    with open("VK_account_scan_results.txt", 'a') as output:
        output.write('TARGET [id = {}] FRIENDS => \n'.format(target))
        for row in friends_list:
            output.write(str(row) + '\n')
        output.write('TARGET [id = {}] FOLLOWERS => \n'.format(target))
        for row in followers_list:
            output.write(str(row) + '\n')


def AD_scan(AD_scan_results):
    with open('VK_account_scan_results.txt', 'r') as file1:
        with open(AD_scan_results) as file2:
            same = set(file1).intersection(file2)
    print("\033[1;92mComparison results are =>\033[1;00m")
    for line in same:
        print(line)


get_friends = input("Would one like to get target friends (y/n)? ").lower()
if get_friends in positive_answers:
    friends = requests.get("https://api.vk.com/method/friends.get?user_id={0}&fields=first_name,last_name,city&access_token={1}&v=5.131".format(target, access_token))
    get_info(friends, friends_list)
    print("\033[1;95mTotal amount of target friends is\033[1;94m", friends.json()["response"]["count"], "\033[1;00m")
    get_followers = input("Would one like to get target folowers (y/n)? ")
    if get_followers in positive_answers:
        followers = requests.get("https://api.vk.com/method/users.getFollowers?user_id={0}&fields=first_name,last_name,city&count=1000&access_token={1}&v=5.131".format(target, access_token))
        get_info(followers, followers_list)
        print("\033[1;95mTotal amount of target folowers is\033[1;94m", followers.json()["response"]["count"], "\033[1;00m")
    else:
        pass 
else:
    get_followers = input("Would one like to get target folowers (y/n)? ")
    if get_followers in positive_answers:
        followers = requests.get("https://api.vk.com/method/users.getFollowers?user_id={0}&fields=first_name,last_name&count=1000&access_token={1}&v=5.131".format(target, access_token))
        get_info(followers, followers_list)
        print("\033[1;95mTotal amount of target folowers is\033[1;94m", followers.json()["response"]["count"], "\033[1;00m")
    else:
        pass 

compare_files = input("Would one like to compare VK account scan results with Active Directory users scan results (y/n)? ")
if compare_files in positive_answers:
    target_output()
    AD_users_scan_script = input("Would one like to scan Active Directory (y/n)? ")
    if AD_users_scan_script in positive_answers:
        os.system("powershell.exe -ExecutionPolicy ByPass -c 'Get-ADUser -Filter * | ft Name | Out-File -FilePath AD_scan_results.txt -Encoding UTF8'")
        AD_scan("AD_scan_results.txt")
        os.system("AD_scan_results.txt")
    else:
        AD_users_scan = input("Enter path to file with Active Directory users: ")
        AD_scan(AD_users_scan)
    save_output = input("Would one like to save VK scan results (y/n)? ")
    if save_output in positive_answers:
        target_output()
        print("\033[1;95mOne can find VK scan results in \033[1;94mVK_account_scan_results.txt\033[1;00m")
    else:
        os.system("rm VK_account_scan_results.txt")

else:
    save_output = input("Would one like to save VK scan results (y/n)? ")
    if save_output in positive_answers:
        target_output()
        print("\033[1;95mOne can find VK scan results in \033[1;94mVK_account_scan_results.txt\033[1;00m")
    else:
        pass 


