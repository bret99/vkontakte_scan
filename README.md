# vkontakte_scan
Script for VK account friends and followers scannnig and finding intersections with Active Directory users.
One should remember about some possible errors with Windows cyrillic encoding during getting Active Directory scan results (pay your attention to powershell command in line 76 of script). Maybe the best way is to prepare Active Directory results in txt file beforehand. Though using 76 line powershell command is OK for me as well.
Of course one should get vk.com access_token.

P.S.For best results do not choose IDs and cities when one's input requested. 
Tested on WSL.
