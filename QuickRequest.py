import requests
'''
("Bot_Name", "Bot_Uuid")
'''
TestBots = [
    # replace Bot_Name and xxxxxxxx-1234-5678-9101-1234abcde1234 to your bot config
    ("Bot_Name", "989f8956-7413-49ad-9f90-954228366bad")
]
# Quick start your bots

# Call server config to start your bot
ServerConfig = {
    "ServerIP": "163.xx.xx.38",
    "ServerPORT": "18006",
    "ServerTriggerPath": "server-a"
}
# A simple bots loop
for bot in TestBots:
    x = bot
    #
    r = "http://{}:{}/{}/create/{}/{}".format(
        ServerConfig["ServerIP"],
        ServerConfig["ServerPORT"],
        ServerConfig["ServerTriggerPath"],
        x[0],
        x[1]
    )
    print(r)
    res = requests.get(r)
    print(res.text)
