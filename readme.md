# POPDOG Bot

POPDOG Bot is a Python application for auto request click event of popdog RESTApi.

## Installation

Make sure your environment have those package.
- flask
- flask_cors
- threading
- requests
- time
- random
- argparse
- sys
- json

and `python version >= 3`
## Usage
### If you `only have an public IP.`
#### Please run this bash command. 
If you `only have an IP` or you want start on `one server(computer)`.
```bash
$python3 BotStart_NoAnotherIP.py -p 8080 -t trigger
```
- `-p` is Server start port
- `-t` is Server trigger route

Now you can access these routes.

To create a bot event
- http://`<ip>`:`<port>`/`<trigger>`/create/`<Bot_Name>`/`<Bot_UUID>`

To visit bot status

- http://`<ip>`:`<port>`/`<trigger>`/lastupdate

#### Success figure of start.
![start_one_ip](./DemoPhotos/start_one_ip.png "start_one_ip")

---
### If you have more than the one public ip.
#### Please run this bash command. 
```bash
$python3 BotStart_HaveAnotherIP.py -p 18006 -t test_trigger -cip 172.18.18.18 -cp 18006 -ct test_trigger
```
- `-p` is Server start port
- `-t` is Server trigger route
- `-cip` is Another Server of public ip or domain
- `-cp` is Another Server of running port
- `-ct` is Another Server of running trigger route

Now you can access these routes.

To create a bot event
- http://`<ip>`:`<port>`/`<trigger>`/create/`<Bot_Name>`/`<Bot_UUID>`

To visit bot status

- http://`<ip>`:`<port>`/`<trigger>`/lastupdate

#### Success figure of start.
![start_another](./DemoPhotos/start_another.png "start_another")
