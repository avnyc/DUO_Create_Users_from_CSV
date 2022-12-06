# DUO_Create_Users_from_CSV

This script ingests:
1. USERNAME
2. USER_EMAIL
3. FULL_NAME
4. PHONE_Number

from an HR file and creates a DUO user then sends that person a text to finish setting up their DUO Account. DUO has a duo-client which made this process cake. A lot of the code was taken from here: https://github.com/duosecurity/duo_client_python/tree/master/examples. I modified it to my organization's needs. 
