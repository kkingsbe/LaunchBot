import discord

print("Creating launches.txt...")
f = open("launches.txt", "w+")
f.close()
print("Success!")

class Setup(discord.Client):
    async def on_ready(self):
        print("Creating message in #launch-manifest channel and getting the message id...")
        msg_id = await client.send_message(discord.Object(id='577934410184130570'), 'Test Message (more coming soon :)')
        f = open("launchbotconfig.txt", "w+")
        f.write("msg_id: " + msg_id.id)
        f.close()
        print("Success!")
        await client.logout()

client = Setup()
client.run('NTc3OTczMTY3ODcyNjcxNzQ1.XOc0EA.GCAdw-ujWR7MLrRYJA1EQeoytto')