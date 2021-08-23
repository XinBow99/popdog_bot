# packages import
import flask
from flask import config
from flask_cors import CORS
import threading
import requests
import time
import random
import argparse
import sys
import json
import gc
requests.packages.urllib3.disable_warnings()
###########################
# Global variables
# uuids is saving the all of bots status of this server.
uuids = {

}
###########################


class DogError(Exception):
    ###########################
    # Simple Error handle function
    pass


###########################
# Create a server by flask
app = flask.Flask(__name__)
# Set Cross header. Make sure calling of RESTApi is working. When you want to show bot status to yuor website.
# You can get bot status by this url
# http://ip:port/trigger_route/lastupdate
CORS(app)
# Get your start command argv value
if __name__ == "__main__":
    print("[SetConfig]loading...")
    # Set Argument parser variable
    ServerStartArgvParser = argparse.ArgumentParser()
    # Set rules of command
    # This server
    ServerStartArgvParser.add_argument(
        "-p",
        "--StartPort",
        type=int,
        help="Set the port of your server"
    )
    ServerStartArgvParser.add_argument(
        "-t",
        "--StartTriggerPath",
        type=str,
        help="Set the trigger route of current server"
    )
    #  Call of another running server config, when this server getting error on request POPDOG's API or other error.
    ServerStartArgvParser.add_argument(
        "-cip",
        "--CallServerIp",
        type=str,
        help="Set the ip of another running server. When this server getting error on request POPDOG's API, and the current server will send the currently running robot to another server"
    )
    ServerStartArgvParser.add_argument(
        "-cp",
        "--CallServerPort",
        type=int,
        help="Set the port of another running server. When this server getting error on request POPDOG's API, and the current server will send the currently running robot to another server"
    )
    ServerStartArgvParser.add_argument(
        "-ct",
        "--CallServerTriggerPath",
        type=str,
        help="Set the trigger route of another running server"
    )
    # Get arg values
    ServerArgs = ServerStartArgvParser.parse_args()
    # Check Args is existed

    def checkArgsNone(arg):
        if arg == None:
            sys.exit("Make sure your argv is correct! Such as:\n$python3 request_dog.py -p 8080 -t trigger -cip 192.168.1.2 -cp 8080 -ct serverB_Trigger")

    # Print your configure
    print("========================")
    print("[CurrectServer]configures.")
    checkArgsNone(ServerArgs.StartPort)
    print("[CurrectServer]PORT:", ServerArgs.StartPort)
    checkArgsNone(ServerArgs.StartTriggerPath)
    print("[CurrectServer]Trigger Route:", ServerArgs.StartTriggerPath)
    print("========================")
    # Another server
    print("[BackupServer]configures.")
    checkArgsNone(ServerArgs.CallServerIp)
    print("[BackupServer]IP:", ServerArgs.CallServerIp)
    checkArgsNone(ServerArgs.CallServerPort)
    print("[BackupServer]PORT:", ServerArgs.CallServerPort)
    checkArgsNone(ServerArgs.CallServerTriggerPath)
    print("[BackupServer]Trigger Route:", ServerArgs.CallServerTriggerPath)
    print("========================")
    # End of Arg parser
    app.config["ServerConfig"] = {
        "CurrentServer": {
            "port": ServerArgs.StartPort,
            "trigger": ServerArgs.StartTriggerPath
        },
        "BackupServer": {
            "ip": ServerArgs.CallServerIp,
            "port": ServerArgs.CallServerPort,
            "trigger": ServerArgs.CallServerTriggerPath
        }
    }
    print("[SetConfig]Successed!")
#################################################################################
# create a user session route                                                   #
# path: http://IP:startPort/trigger/create/testbot/xxxxx-1234-5678-2133-asdfghj #
# method: Get                                                                   #
# params:                                                                       #
# - bot_name                                                                    #
# - bot_uuid                                                                    #
# Success Return: Bot name is {bot_name}, and uuid is {bot_uuid}                #
#################################################################################
@app.route(f'/{app.config["ServerConfig"]["CurrentServer"]["trigger"]}/create/<bot_name>/<uuid>', methods=['GET'])
def call_dog(bot_name, uuid):
    # Get you bot name. And make "/" replace to "@" in your bot name, if name is xxx/yyy/zzz.
    bot_name = bot_name.replace('@', '/')
    # Creat a thead for bot.
    dogThreading = threading.Thread(target=dog, args=(bot_name, uuid,))
    dogThreading.start()
    return f"Bot name is {bot_name}, and uuid is {uuid}"
#########################################################################
#########################################################################
# Get all of running bot's status!                                      #
# path: http://IP:startPort/trigger/lastupdate                          #
# method: Get                                                           #
# Success Return json:                                                  #
# {                                                                     #
#  "<uuid>": {                                                          #
#    "bot_name": "<bot_name>",                                          #
#    "clicks": "{\"clicks\":63603098,\"dailyClicks\":6758000}",         #
#    "last_runtime": "Fri Aug 20 21:45:05 2021",                        #
#    "req_times": 10,                                                   #
#    "x-ratelimit-remaining": "24"                                      #
#  }                                                                    #
# }                                                                     #
# req_times is bot total times of request click. When start bot.        #
# x-ratelimit-remaining is how times bot can request on current server  #
#########################################################################
@app.route(f'/{app.config["ServerConfig"]["CurrentServer"]["trigger"]}/lastupdate', methods=['GET'])
def get_lastupdate():
    '''
    Return status by application/json
    '''
    global uuids
    return flask.jsonify(uuids)
#########################################################################


def dog(bot_name: str, uuid: str):
    '''
    This method is handle single bot.
    - bot_name: your bot name
    - uuid: your bot uuid
    '''
    global uuids
    # Click request url and datas
    url = "https://popdog.click/clicked/v2"
    ################################################################
    # handle bot times
    req_times = 0
    # to calculate diff times between last clicks and first clicks
    start_click = 0
    # to calculate remaining time.
    start_time = time.time()
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json;charset=utf-8",
        "Origin": "https://popdog.click",
        "Accept-Language": "zh-tw",
        "Host": "popdog.click",
        "User-Agent": uuid + str(random.randint(1, 1000000)),
        "Referer": "https://popdog.click/",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    pop_dog_session = requests.Session()
    pop_dog_max_retries = requests.adapters.HTTPAdapter(max_retries=0)
    pop_dog_session.mount('http://', pop_dog_max_retries)
    pop_dog_session.mount('https://', pop_dog_max_retries)
    pop_dog_session.headers = headers
    pop_dog_session.verify = False
    ###############################
    # A loop, until bot got error #
    ###############################
    while True:
        # Set a variable of Config.json
        config = open(file="config.json", mode="r", encoding="utf-8")
        readConfig = json.loads(
            config.read()
        )
        config.close()
        data = {
            # pop per request. Max 2000000 ? not sure. Min 1.
            "clicks": random.randint(readConfig["PopRange"]["Min"],readConfig["PopRange"]["Max"]),
            # change username to your name
            "username": bot_name,
            # change uuid to your uuid
            "uuid": uuid,
            "token": "disabled"
            }
        # If BotStart value is 0
        if readConfig["BotStart"] == 0:
            print("[Config]{}\nBotStart value is change to 0!\n{}".format(
                bot_name,
                "----------------------------------------------------"
            ))
            break
        elif readConfig["BotStart"] == 1:
            uuids[uuid] = {
                "bot_name": bot_name,
                "req_times": req_times,
                "last_runtime": str(time.ctime())
            }
            try:
                # To reuqest popdog api.
                resRequestStartTime = time.time()
                res = pop_dog_session.post(url, json=data, timeout=(.5, 2))
                # Add Request times
                resRequestEndTime = time.time()
                requestRemainingTime = "{:.2f}".format(
                    resRequestEndTime - resRequestStartTime)
                req_times += 1
                # If request too much
                if "Do not pet the Pop Dog too much" in res.text or res.status_code != 200:
                    # Throw an error.
                    raise DogError("Pop Dog Request Error." +
                                   str(res.status_code))
                else:
                    # Set First Clicks Value.
                    if start_click == 0:
                        start_click = int(res.json()['clicks'])
                    ElapsedTime = time.time() - start_time
                    Diff = int(res.json()['clicks']) - start_click
                    Avg = Diff / ElapsedTime
                    print("[Perfect] {}\n[Elapsed time] {:.2f}s\n[UUID] {}\n[Name] {}\n[Res] {}\n[Diff] {}\n[Avg] {}\n[PopdogRemainingTime] {}\n[x-ratelimit-remaining] {}\n{}".format(
                        req_times, ElapsedTime,
                        uuid,
                        bot_name,
                        res.text,
                        Diff,
                        Avg,
                        requestRemainingTime,
                        res.headers['x-ratelimit-remaining'],
                        "----------------------------------------------------"
                    ))
                    uuids[uuid].update({
                        'clicks': res.text,
                        'x-ratelimit-remaining': res.headers['x-ratelimit-remaining']
                    })
                    # Popdog ratelimit is 25. x-ratelimit-remaining is bot remaining times, if value equal to 1, should change another server to clicking continue.
                    if int(res.headers['x-ratelimit-remaining']) <= 1:
                        raise DogError(
                            "Change Server x-ratelimit-remaining is 1 or below!")
                    # pop per times should wait 8 secs to clicking continue
                    time.sleep(readConfig["PopDelay"])
            except Exception as e:
                # To handle all errors
                # Because it's got an error, We need change another server and request create route. So Replace "/" to "@"
                bot_name = bot_name.replace("/", "@")
                call_another_server(
                    call_server=app.config["ServerConfig"]["BackupServer"],
                    bot_name=bot_name,
                    uuid=uuid,
                    error_type=str(e)
                )
                gc.collect()
                # break this loop and thread.
                break
        else:
            print(
                "[Config Error]Variable of BotStart in config.json value should be 0 or 1! Please improve immediately ")
            break


def call_another_server(call_server: dict, bot_name: str, uuid: str, error_type: str):
    '''
    This method is handle change server event.
    - call_server: Another server config. Type should be dict.
    - bot_name: bot name!
    - uuid: bot uuid
    - error_type: To display what error throw.
    '''
    global uuids
    if 'timeout' not in error_type:
        time.sleep(16)
    responseText = requests.get(
        f"http://{call_server['ip']}:{call_server['port']}/{call_server['trigger']}/create/{bot_name}/{uuid}").text
    displayStrings = "[Error] {}\n[BotName] {}\n[BotUuid] {}\n[BackupServerIP] {}\n[BackupServerPORT] {}\n[BackupServerApiStatusText] {}\n[Watting for next request]\n-------------------------------------------".format(
        error_type,
        bot_name,
        uuid,
        call_server['ip'],
        call_server['port'],
        responseText
    )
    uuids[uuid].update({
        'clicks': f'Call:{call_server["ip"]}:{call_server["port"]}'
    })
    print(displayStrings)


# Start Server
app.run(host="0.0.0.0",
        port=app.config["ServerConfig"]["CurrentServer"]["port"], debug=False)
