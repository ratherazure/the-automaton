import os
import sys
import discord
import asyncio
import crayons
import colorama
import types

import modules

class TheClient(discord.Client):
    async def on_ready(self):
        application = await self.application_info()
        print("--------------------------------")
        print("Logged in successfully.")
        print("Currently logged in as: {}.".format(crayons.cyan(self.user.name)))
        print("Currently logged in as: {}.".format(crayons.cyan(self.user.id)))
        print("Current owner is: {}.".format(crayons.cyan(application.owner)))
        print("{} currently has access to...".format(crayons.cyan(self.user.name)))
        for server in self.guilds:
            print("- {}".format(server))
        print("--------------------------------")

    async def on_message(self, message):
        if message.content.startswith("/") and commands.get(message.content.split(" ")[0][1:], [None, None])[0] != None: #if message starts with the command handle and is in the command dictionary then...
            response = commands.get(message.content.split(" ")[0][1:], [None, None])
            response = response[0](*response[1]) #execute the function with the parameters.
            await message.channel.send(content = response.get("content", None), embed = response.get("embed", None), file = response.get("file", None)) #aaand off it goes!


if __name__ == "__main__":

    colorama.init()
    commandHandle = "/"

    #the place where you map a command to the function, and also where you specify your parameters
    commands = {
        "debug": (modules.debug, ["Hello", "World", "!"])
    }

    client = TheClient()
    client.run(open(os.path.join("data", "discordToken.txt")).read())