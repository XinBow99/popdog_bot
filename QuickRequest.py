import requests

users = [
    ("tw-Xinbow99-1","UUID"),
    ("tw-Xinbow99-2","UUID"),
    ("tw-Xinbow99-3","UUID"),
    ("github.com@XinBow99@request_dog","UUID"),
    ("823打高端","UUID")
]
for user in users:
    x = user
    r = "http://Main_server_ip:18116/trigger_path/create/{}/{}".format(x[0],x[1])
    print((r))
    res = requests.get(r)
    print(res.text)