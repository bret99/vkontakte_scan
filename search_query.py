import requests
import os
from access_tokens import access_token_friends

search_query_results = []
positive_answers = ['yes', 'y', '']


def target_Search_output(user_id):
    if len(search_query_results) != 0:
        with open("VK_account_search_results.txt", 'a') as output:
            output.write('SEARCH RESULTS IN TARGET (id = {}) FRIENDS => \n'.format(user_id))
            for row in search_query_results:
                output.write(str(row) + '\n')

def Search():
    try:
        user_id = input("Enter correct user_id: ")
        search_query_request = input(
            "Enter the \033[1;94mSearch \033[1;00mquery: ")
        print("\033[1;90m\nGetting information...\n\033[1;00m")
        search_query = requests.get(
            "https://api.vk.com/method/friends.search?user_id={0}&q={1}&count=1000&fields=first_name,last_name,city&access_token={2}&v=5.131"
            .format(user_id, search_query_request, access_token_friends))
        data = search_query.json()["response"]["items"]
        ids = input("Would one like to get cities and IDs (y/n)? ").lower()
        if ids in positive_answers:
            for item in data:
                try:
                    item = item["first_name"] + " " + item[
                        "last_name"] + " " + "id={}".format(
                            item["id"]) + " " + item["city"]["title"]
                    print(item)
                    search_query_results.append(item)
                except KeyError:
                    item = item["first_name"] + " " + item[
                        "last_name"] + " " + "id={}".format(item["id"])
                    print(item)
                    search_query_results.append(item)
        else:
            for item in data:
                item = item["first_name"] + " " + item["last_name"]
                print(item)
                search_query_results.append(item)
        save_output = input(
            "\nWould one like to save \033[1;94mVK \033[1;00msearch results (y/n)? "
        ).lower()
        if save_output in positive_answers:
            target_Search_output(user_id)
            print(
                "One can find \033[1;94mVK \033[1;00mscan results in \033[1;94m/{}VK_account_search_results.txt\033[1;00m\n"
                .format(os.getcwd()))
        else:
            print("")
    except KeyError:
        print("\033[1;91mNot correct input or target account is private!\n\033[1;00m")
