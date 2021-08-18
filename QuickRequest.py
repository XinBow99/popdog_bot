import requests
import random
users = [
    ("github.com@XinBow99@request_dog", "1234567-1234-4aa0-2133-jfwnefhjjfekw"),
    ("tw-Xinbow99-1",                   "1234567-1234-5678-2133-jfwnefhjjfekw"),
    ("tw-Xinbow99-2",                   "1234567-1234-5678-2133-jfwnefhjjfekw"),
    ("tw-Xinbow99-3",                   "1234567-1234-5678-2133-jfwnefhjjfekw"),
    ("TW-KHC-Xinbow99-1",               "1234567-1234-5678-2133-jfwnefhjjfekw"),
    ("TW-KHC-Xinbow99-2",               "1234567-1234-5678-2133-jfwnefhjjfekw"),
    ("TW-KHC-Xinbow99-3",               "1234567-1234-5678-2133-jfwnefhjjfekw"),
    ("TW-KHC-Xinbow99-4",               "1234567-1234-5678-2133-jfwnefhjjfekw"),
    ("www.linkedin.com@in@Shiwen99",    "1234567-1234-5678-2133-jfwnefhjjfekw"),
    ("www.linkedin.com@in@Shiwen99",    "1234567-1234-5678-2133-jfwnefhjjfekw"),
    ("www.linkedin.com@in@Shiwen99",    "1234567-1234-5678-2133-jfwnefhjjfekw"),
    ("www.linkedin.com@in@Shiwen99",    "1234567-1234-5678-2133-jfwnefhjjfekw"),
    ("www.linkedin.com@in@Shiwen99",    "1234567-1234-5678-2133-jfwnefhjjfekw"),
    ("www.linkedin.com@in@Shiwen99",    "1234567-1234-5678-2133-jfwnefhjjfekw"),
    ("www.linkedin.com@in@Shiwen99",    "1234567-1234-5678-2133-jfwnefhjjfekw"),
    ("www.linkedin.com@in@Shiwen99",    "1234567-1234-5678-2133-jfwnefhjjfekw"),
    ("www.linkedin.com@in@Shiwen99",    "1234567-1234-5678-2133-jfwnefhjjfekw"),
    ("www.linkedin.com@in@Shiwen99",    "1234567-1234-5678-2133-jfwnefhjjfekw")
]
for user in users:
    x = user
    r = "http://{}:18117/trigger_path/create/{}/{}".format("127.0.0.1",x[0], x[1])
    res = requests.get(r)
    print(res.text)
