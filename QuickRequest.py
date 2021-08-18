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
    r = "http://163.18.18.38:18116/73ae31d8dac2aab4a11cf4ed6324eefe/create/{}/{}".format(x[0],x[1])
    print((r))
    res = requests.get(r)
    print(res.text)