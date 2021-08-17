import flask
import threading
import requests
import time
requests.packages.urllib3.disable_warnings()

app = flask.Flask(__name__)
@app.route('/trigger_key/<user_name>/<uuid>', methods=['GET'])
def call_dog(user_name, uuid):
    user_name = user_name.replace('@', '/')
    dogThreading = threading.Thread(target=dog, args=(user_name, uuid,))
    dogThreading.start()
    return f"User name is {user_name}, and uuid is {uuid}"


def dog(user_name, uuid):
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
        try:
            res = requests.post(url, headers=headers, json=data, verify=False)
            if "Do not pet the Pop Dog too much" in res.text:
                print("[Got error! should break]", res)
                # Call b server, if a server if got error.
                user_name = user_name.replace("/", "@")
                print(requests.get(
                    f"http://B_server ip or domain:18116/trigger_key/{user_name}/{uuid}").text)
                print("[Watting for next request]")
                break
            else:
                print("[Perfect]", user_name, res.text)
                # add sleep ref popdog.click source code in content
                time.sleep(5.603)
        except:
            print("[Got Request error! should break]")
            # Call b server, if a server if got error.
            user_name = user_name.replace("/", "@")
            print(requests.get(
                f"http://B_server ip or domain:18116/trigger_key/{user_name}/{uuid}").text)
            print("[Watting for next request]")
            break


app.run(host="0.0.0.0", port=18116, debug=True)
