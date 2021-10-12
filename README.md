# vkontakte_scan
This is a framework for VK account scannnig and finding intersections with Active Directory users and not only.
One should remember about some possible errors with Windows cyrillic encoding during getting Active Directory scan results (pay your attention to default powershell command in line 69 of get_Friends_and_Followers.py). Maybe the best way is to prepare Active Directory results in txt file beforehand.
One should get vk.com access_tokens with 'friends' and 'photos' permissions (https://vk.com/dev/first_guide). To get these ones one should make StandAlone application and insert its ID in GET request 'https://oauth.vk.com/authorize?client_id={YOUR_APP_ID}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope={friends_or_photos}&response_type=token&v=5.52' where YOUR_APP_ID and friends (or photos) should without {}. After access_token/tokens is/are gotten one should insert these keys to access_tokens.py.
For best intersections results do not choose IDs and cities when one's input requested. Use those ones just to get more information about target.
One should remember about running this framework for Active Directory intersections results is correct inside of domain as well. 

P.S. Private accounts are unreachable.
Tested on WSL.
