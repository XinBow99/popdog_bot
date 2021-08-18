import flask
import threading
import requests
import time
import sys
requests.packages.urllib3.disable_warnings()

# g
uuids = {

}

app = flask.Flask(__name__)

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
        "uuid": uuid
    }
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json;charset=utf-8",
        "Origin": "https://popdog.click",
        "Accept-Language": "zh-tw",
        "Host": "popdog.click",
        "User-Agent": uuid,
        "Referer": "https://popdog.click/",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    while open('config.txt', 'r', encoding='utf-8').read().strip("\n") == "1":
        uuids[uuid] = {
            user_name: str(time.ctime())
        }
        try:
            res = requests.post(url, headers=headers, json=data, verify=False)
            if "Do not pet the Pop Dog too much" in res.text or res.status_code != 200:
                raise "Pop Dog Request Error." + str(res.status_code)
            else:
                print("[Perfect]", user_name, '\n', res.text,
                      '\n-------------------------------------------')
                uuids[uuid].update({
                    'clicks': res.text
                })
                time.sleep(1.5)
        except:
            user_name = user_name.replace("/", "@")
            call_other_server(
                call_server=app.config["call_server"],
                user_name=user_name,
                uuid=uuid,
                trigger=app.config['trigger'],
                error_type="Except Error"
            )
            break


def call_other_server(call_server, user_name, uuid, trigger, error_type):
    global uuids
    time.sleep(3.6)
    print("[ERROR]", user_name, error_type,
          '\n-------------------------------------------')
    print(requests.get(
        f"http://{call_server}:18116/{trigger}/create/{user_name}/{uuid}").text)
    uuids[uuid].update({
        'clicks': f'Call:{call_server}:18116'
    })
    print("[Watting for next request]")


app.run(host="0.0.0.0", port=18116, debug=False)
