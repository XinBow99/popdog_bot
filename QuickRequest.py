import requests
import random
users = [
    ("github.com@XinBow99@request_dog", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"),
    ("tw-Xinbow99-1",                   "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"),
    ("tw-Xinbow99-2",                   "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"),
    ("tw-Xinbow99-3",                   "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"),
    ("TW-KHC-Xinbow99-1",               "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"),
    ("TW-KHC-Xinbow99-2",               "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"),
    ("TW-KHC-Xinbow99-3",               "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"),
    ("TW-KHC-Xinbow99-4",               "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"),
    ("www.linkedin.com@in@Shiwen99",    "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"),
    ("www.linkedin.com@in@Shiwen99",    "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"),
    ("www.linkedin.com@in@Shiwen99",    "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"),
    ("www.linkedin.com@in@Shiwen99",    "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"),
    ("www.linkedin.com@in@Shiwen99",    "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"),
    ("www.linkedin.com@in@Shiwen99",    "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"),
    ("www.linkedin.com@in@Shiwen99",    "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"),
    ("www.linkedin.com@in@Shiwen99",    "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"),
    ("www.linkedin.com@in@Shiwen99",    "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"),
    ("www.linkedin.com@in@Shiwen99",    "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx")
]
for user in users:
    x = user
    r = "http://{}:18116/trigger_path/create/{}/{}".format(
        "127.0.0.1",x[0], x[1])
    res = requests.get(r)
    print(res.text)
