import flask
from flask_cors import CORS
import threading
import requests
import time
import sys
import random
requests.packages.urllib3.disable_warnings()

# g
uuids = {

}

class DogError(Exception):
    pass

app = flask.Flask(__name__)
CORS(app)
if __name__ == "__main__":
    print("[SetConfig]loading...")
    if len(sys.argv) < 3:
        print('Command should be "python3 request_dog.py Call_Server_IP Trigger_Path" ')
        print("EX. python3 request_dog.py 192.168.1.1 c2aa6324eefeb4a11cf4ed")
        sys.exit()

    print("[SetConfig]Call server ip:", sys.argv[1])
    print("[SetConfig]trigger path:", sys.argv[2])

    app.config["call_server"] = sys.argv[1]
    app.config["trigger"] = sys.argv[2]
    print("[SetConfig]Successed!")
# create a user session
@app.route(f'/{app.config["trigger"]}/create/<user_name>/<uuid>', methods=['GET'])
def call_dog(user_name, uuid):
    user_name = user_name.replace('@', '/')
    dogThreading = threading.Thread(target=dog, args=(user_name, uuid,))
    dogThreading.start()
    return f"User name is {user_name}, and uuid is {uuid}"

# get your uuid information
@app.route(f'/{app.config["trigger"]}/lastupdate', methods=['GET'])
def get_lastupdate():
    global uuids
    return flask.jsonify(uuids)


def dog(user_name, uuid):
    global uuids
    url = "https://popdog.click/clicked/v2"
    data = {
        "clicks": 2000,
        # change username to your name
        "username": user_name,
        # change uuid to your uuid
        "uuid": uuid,
	"token": "03AGdBq26TUjzUhg_4sEo96WvNQaEruUFWyPBopfqnx0b5RKKhCpuKqje4gJ1zsePRuIwYfpMLtMIlMgXlnFwZsYmoLZBuX6J5c91TXnV_nWU0ASyzAA-1QaHS_g3bK9y25i5lCMSpTWBcrRIqCyw494ycyNwCraRE4m2XXADiMrW5J4RmIkyaWRNug14tRcp6GzSWkvUHrp2Uo9CQAiE-sr20HoStgmuf4bctInqisMMWwbcTh-gcjEpgci4IMB58Po0x8Jqn2ZPlAiJnZsjfT14AT_3i9hjhMYkwJ5wLVzvSZKbRjSFPbQ-CS-PT9gsMa2J1eU7ORCBVG99OH_p92cfQtXQh7fAzeaWlmOd2R_V-hD6lvvYwGYgzjuGXxtR5jdWFRjhkMsmQpn4c0YoBMQ16HyB8DGRFQb7zehwmPhlm89PMp1Oga0XbNKNfbgl5M4l6esMtdcB-x-10t1_zSqCjMPBHB7dhtFMqDWcCdu41m_4xevF4S_3EgZ8RxOCh53Q71ylwUigK"}
    req_times = 0
    start_click = 0
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
    while open('config.txt', 'r', encoding='utf-8').read().strip("\n") == "1":
        uuids[uuid] = {
            "bot_name": user_name,
            "req_times": req_times,
            "last_runtime": str(time.ctime())
        }
        try:
            res = requests.post(url, headers=headers, json=data, verify=False)
            req_times += 1
            if "Do not pet the Pop Dog too much" in res.text or res.status_code != 200:
                raise DogError("Pop Dog Request Error." + str(res.status_code))
            else:
                if start_click == 0:
                    start_click = int(res.json()['clicks'])
                print("[Perfect] {} [Elapsed time] {:.2f}s\n[UUID] {}\n[Name] {}\n[Res] {}\n[Diff] {}\n[x-ratelimit-remaining] {}\n{}".format(
                    req_times,time.time() - start_time,
                    uuid,
                    user_name,
                    res.text,
                    int(res.json()['clicks']) - start_click,
                    res.headers['x-ratelimit-remaining'],
                    "----------------------------------------------------"
                ))
                uuids[uuid].update({
                    'clicks': res.text,
                    'x-ratelimit-remaining':res.headers['x-ratelimit-remaining']
                })
                if int(res.headers['x-ratelimit-remaining']) == 1:
                    raise DogError("Change Server x-ratelimit-remaining is 1")
                if req_times % 25 == 0:
                    time.sleep(15)
                else:
                    time.sleep(7.5)
        except Exception as e:
            user_name = user_name.replace("/", "@")
            call_other_server(
                call_server=app.config["call_server"],
                user_name=user_name,
                uuid=uuid,
                trigger=app.config['trigger'],
                error_type= str(e)
            )
            break


def call_other_server(call_server, user_name, uuid, trigger, error_type):
    global uuids
    print("[ERROR-Wait-For-10-Secs]", user_name, error_type,
          '\n-------------------------------------------')
    print(requests.get(
        f"http://{call_server}:18116/{trigger}/create/{user_name}/{uuid}").text)
    uuids[uuid].update({
        'clicks': f'Call:{call_server}:18116'
    })
    print("[Watting for next request]")


app.run(host="0.0.0.0", port=18116, debug=False)
