import sys
import os
from get_target_Friends import Friends
from get_target_Followers import Followers
from get_target_Subscriptions import Subscriptions
from get_target_Groups import Groups
from get_target_Photos import Photos
from search_query import Search

positive_answers = ['yes', 'y', '']


def main_menu():
    print(
        "\033[1;94mVK Scanner \033[1;00mmodules:\n\n[\033[1;94m1\033[1;00m] Get target \033[1;94mFriends\n\033[1;00m[\033[1;94m2\033[1;00m] Get target \033[1;94mFollowers\n\033[1;00m[\033[1;94m3\033[1;00m] Get target \033[1;94mSubscriptions\n\033[1;00m[\033[1;94m4\033[1;00m] Get target \033[1;94mGroups\n\033[1;00m[\033[1;94m5\033[1;00m] Get target \033[1;94mPhotos\033[1;00m\n[\033[1;94m6\033[1;00m] \033[1;94mSearch \033[1;00mquery in target \033[1;94mFriends\033[1;00m\n[\033[1;94m99\033[1;00m] Exit\n"
    )
    choose_module = input("Enter module number: ")
    if choose_module == "1":
        Friends()
        main_menu()
    elif choose_module == "2":
        Followers()
        main_menu()
    elif choose_module == "3":
        Subscriptions()
        main_menu()
    elif choose_module == "4":
        Groups()
        main_menu()
    elif choose_module == "5":
        Photos()
        main_menu()
    elif choose_module == "6":
        Search()
        main_menu()
    elif choose_module == "99":
        sys.exit()
    else:
        sys.exit("\033[1;91mWrong input!\033[1;00m")


main_menu()
