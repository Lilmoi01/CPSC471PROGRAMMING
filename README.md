# CPSC 471 Programming Project
In this project, we were to create a simplified FTP server and FTP client in which the client will connect to the server and
support uploading and downloading of files to and from the server. 

### Group Members ### 
1. Moises Cerda
                  
2. Vinh Nguyen
   vinhgod123@csu.fullerton.edu
3. Ian Gabriel Vista
   
4. Irena Nguyen
   irenanguyen@csu.fullerton.edu

### Programming Language ###
- Python 3.8 or higher

### How to execute project ### 
1. Server Setup:
   - Open ```serv.py``` on VSCode and run the file in a python-designated terminal.
     
   - The terminal for ```serv.py``` should display:
     ``` Server listening on 127.0.0.1:65432 ```
     
2. Client Setup:
   - Now that the server is running, open ```cli.py``` on VSCode and run the file in a python-designated terminal.
     
   - The terminal for ```cli.py``` should display:
     ``` Enter command (ls, get <file>, put <file>, quit): ```
     
   - Use the following commands in client:
     - ```ls: ``` :Lists all files on the server.
     - ```get <file>``` : Download a file from server.
     - ```put <file>``` : Upload a file to server.
     - ```quit``` : Exits the client. 

### Special Notes ###
- File Transfer:
  - When using ```get``` command, files will be saved in the client's directory with a prefix ```downloaded_```.
  - When using the ```put``` command, ensure the file exists in the client's directory.

- Error Handling:
  - If a file is not found on the server (using ```get``` or ```put```), the client will display: ```Error: File '<file>' not found on the client.```.

- Default Configuration:
  - Server Host: ```127.0.0.1```
  - Server Port: ```65432```
  - Both the server and client will be running simultaneously; however, ```serv.py``` must run first before ```cli.py```.
