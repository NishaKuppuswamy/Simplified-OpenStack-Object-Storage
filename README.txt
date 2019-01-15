Welcome to OpenStack in Python 3.4

Folder Structure

OpenStack
 |__ _init_.py
 |__ client
     |__ operation
        |__ _init_.py
        |__ Delete.py
        |__ Download.py
        |__ factory.py
        |__ List.py
        |__ Operation.py
        |__ Upload.py
        |__ Add.py
        |__ Remove.py
     |__ bo
        |__ FileMigrate.py
     |__Client.py
     |__ CommandClient.py
 |__ server
     |__ operation
        |__ _init_.py
        |__ Delete.py
        |__ Download.py
        |__ factory.py
        |__ List.py
        |__ Operation.py
        |__ Upload.py
        |__ Remove.py
        |__ Add.py
      |__ bo
         |__ FileMigrate.py
     |__ _init_.py
     |__ command.py
     |__ fileTransfer.py
     |__ partition.py
     |__ServerThread.py
 |__ README.txt
 
 Steps to run:
 
 1. login to new terminal
 2. enter: setup python-3.4
 3. enter: cd P1/server/
 4. enter: python3 ServerThread.py
 5. enter: server 16 129.210.16.80 129.210.16.81 129.210.16.83 129.210.16.86
   5. a. copy client ip port from terminal
 6. login to new terminal
 7. enter: setup python-3.4
 8. enter: cd P1/client/
 9. enter: python3 Client.py
 10. enter: client linux60819 43643 (replace server ip/hostname and port displayed in server terminal)
 11. enter: upload username/filename.txt (filename.txt should be placed in folder P1/client/, filename.txt uploaded to Main Ip Machine under folder /tmp/loginname/username, filename.txt uploaded to Backup Ip Machine under folder /tmp/loginname/username)
 12. enter: list username (checks if the files are in the designated main disk and backup disk. If not move the files to the designated machines and den display list of files in each ip machine)
 13. enter: download username/filename.txt (downloaded to folder P1/client and displays the contents of the downloaded file)
 14. enter: delete usernmae/filename.txt (filename.txt deleted from Main Ip Machine under folder /tmp/loginname/username, filename.txt deleted from Backup Ip Machine under folder /tmp/loginname/username)
15. enter: add ip (enter ip address, enter new ip,  displays the partition number that undergoes change and contains a file)
16. enter: remove ip (enter ip address, enter old ip that is already added to table,  displays the partition number that undergoes change in disk and that contains file)
