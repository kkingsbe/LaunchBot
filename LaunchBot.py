import discord
import urllib.request
import json

class RocketLaunch:
    def __init__(self, id, name, windowstart, windowend, net, status, infourl, agencyname, vehicle, missionname):
        self.id = id
        self.name = name
        self.windowstart = windowstart
        self.windowend = windowend
        self.net = net
        self.status = status
        self.infourl = infourl
        self.agencyname = agencyname
        self.vehicle = vehicle
        self.missionname = missionname

class LaunchBot(discord.Client):
    msg_id = ""

    def load_settings(self):
        settings = open("launchbotconfig.txt", "r+").readlines()
        for setting in settings:
            if setting.startswith("msg_id"):
                self.msg_id = setting.split(": ")[1]
                print("Message ID: " + self.msg_id)

    async def test(self):
        channel = client.get_channel('577934410184130570')
        message = await client.get_message(channel, self.msg_id)
        await client.edit_message(message, "Test Edit")

    def parselaunches(self, file): #Parses the csv data into a list of RocketLaunch objects
        old = open(file, 'r+').readlines()
        launches = []
        for launch in old:
            id = launch.split(",")[0]
            name = launch.split(",")[1]
            windowstart = launch.split(",")[2]
            windowend = launch.split(",")[3]
            net = launch.split(",")[4]
            status = launch.split(",")[5]
            infourl = launch.split(",")[6]
            agencyname = launch.split(",")[7]
            vehicle = launch.split(",")[8]
            missionname = launch.split(",")[9]
            launches.append(RocketLaunch(id, name, windowstart, windowend, net, status, infourl, agencyname, vehicle, missionname))

    def savenewlaunches(self, newlaunches):
        f = open("launches.txt", "w+")
        for launch in newlaunches:
            f.write(str(launch.id) + "," + str(launch.name) + "," + str(launch.windowstart) + "," + str(launch.windowend) + "," + str(launch.net) + "," + str(launch.status) + "," + str(launch.infourl) + "," + str(launch.agencyname) + "," + str(launch.vehicle) + "," + str(launch.missionname) + "\n")
        f.close()

    async def updatecomment(self,launches):
        channel = client.get_channel('577934410184130570')
        message = await client.get_message(channel, self.msg_id)

        content = "Upcoming launches:\n" \
                  "------------------\n"
        for launch in launches:
            content += ("Mission: " + launch.missionname + "\nVehicle: " + launch.vehicle + "\nNet: " + launch.net +"\nWindow Start: " + launch.windowstart + "\n------------------")

        await client.edit_message(message, content)

    async def update_launches(self):
        oldlaunches = self.parselaunches("launches.txt")
        newlaunches = []

        with urllib.request.urlopen("https://launchlibrary.net/1.4/launch/next/1") as url:
            data = json.loads(url.read().decode())
            print(data)
            for launch in data['launches']:
                newlaunch = RocketLaunch(launch["id"], launch["name"], launch["windowstart"], launch["windowend"], launch["net"], launch["status"], launch["infoURL"], launch["location"]["pads"][0]["agencies"][0]["name"], launch["rocket"]["name"], launch["missions"][0]["name"])
                newlaunches.append(newlaunch)
            self.savenewlaunches(newlaunches)

        if oldlaunches != newlaunches:
            await self.updatecomment(newlaunches)

    async def on_ready(self):
        print('Logged on as', self.user)
        self.load_settings()
        await self.update_launches()
        #await self.test()
        await client.logout()

client = LaunchBot()
client.run('NTc3OTczMTY3ODcyNjcxNzQ1.XOc0EA.GCAdw-ujWR7MLrRYJA1EQeoytto')