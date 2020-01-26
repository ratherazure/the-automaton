import os
import sys
import discord
import asyncio
import crayons
import colorama
import types
import re
import json
import random

import modules
from modules import *

class TheClient(discord.Client):
    async def on_ready(self):
        application = await self.application_info()
        print("--------------------------------")
        print("Logged in successfully.")
        print("Currently logged in as: {}.".format(crayons.cyan(self.user.name)))
        print("Currently logged in as: {}.".format(crayons.cyan(self.user.id)))
        print("Current owner is: {}.".format(crayons.cyan(application.owner)))
        print("{} currently has access to...".format(crayons.cyan(self.user.name)))
        if len(self.guilds) > 0:
            for server in self.guilds:
                print("- {}".format(server))
        else:
            print(crayons.red("There are no servers this bot is connected to."))
        print("--------------------------------")

    async def on_message(self, message):
        response = None
        if message.content.startswith(commandInvoker):
            if checkifModuleExists(message.content.split(" ")[0][len(commandInvoker):]):
                command = message.content.split(" ")[0][len(commandInvoker):]
                parameters = message.content.split(" ")[1:] #if there are no predetermined parameters, take them from the message itself.
                response = sys.modules["modules.{}".format(message.content.split(" ")[0][len(commandInvoker):])].main(*parameters)

        if response != None:
            await message.channel.send(content = response.get("content", None), embed = response.get("embed", None), file = response.get("file", None))

def checkifModuleExists(moduleinQuestion): #checks if custom module is imported
    return "modules.{module}".format(module = moduleinQuestion) in sys.modules.keys()

if __name__ == "__main__":

    colorama.init()
    commandInvoker = "/"

    interceptResponses = json.loads(open(os.path.join("data", "responses.json")).read())

    client = TheClient()
    client.run(open(os.path.join("data", "discordToken.txt")).read())