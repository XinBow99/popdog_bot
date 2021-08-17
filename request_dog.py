import flask
import threading
import requests
import time
requests.packages.urllib3.disable_warnings()

app = flask.Flask(__name__)
@app.route('/trigger_path', methods=['GET'])
def home():
    dogThreading = threading.Thread(target=dog)
    dogThreading.start()
    return "Done!"


def dog():
    url = "https://popdog.click/clicked/v2"
    data = {
        "clicks": 2000,
        # change username to your name
        "username": "github.com/XinBow99/request_dog",
        # change uuid to your uuid
        "uuid": ""
    }
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json;charset=utf-8",
        "Origin": "https://popdog.click",
        "Accept-Language": "zh-tw",
        "Host": "popdog.click",
        "User-Agent": "WTF",
        "Referer": "https://popdog.click/",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    while open('config.txt', 'r', encoding='utf-8').read().strip("\n") == "1":
        res = requests.post(url, headers=headers, json=data, verify=False).text
        if "Do not pet the Pop Dog too much" in res:
            print("[Got error! should break]", res)
            # Call b server, if a server if got error.
            time.sleep(2)
            print(requests.get(
                "http://your server ip or domain:18116/trigger_path").text)
            print("[Watting for next request]")
            break
        else:
            print(res, "[Great]")


app.run(host="0.0.0.0", port=18116, debug=True)
