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

        if message.content.startswith(commandInvoker) and commands.get(message.content.split(" ")[0][len(commandInvoker):], [None, None])[0] != [None, None]: #if message starts with the command handle and is in the command dictionary then...
            command = commands.get(message.content.split(" ")[0][len(commandInvoker):], [None, None]) #take the invoked command and return with a python pointer to a function
            if command[1] == []: #for some reason, one line if statements don't work here?
                parameters = message.content.split(" ")[1:] #if there are no predetermined parameters, take them from the message itself.
            else:
                parameters = command[1]
            response = command[0](*parameters) #execute the function with the parameters.

        if response == None: #if the a response has not yet been set then...
            for entry in interceptResponses: #if any of the triggers exists in any part message, then...
                if re.search(r"\b{}\b".format(entry), message.content, re.IGNORECASE) != None:
                    payload = random.choice(interceptResponses[entry])
                    response = {"content": payload, "file": None, "embed": None} #set the payload

        if response != None: #don't send nothing
            await message.channel.send(content = response.get("content", None), embed = response.get("embed", None), file = response.get("file", None))


if __name__ == "__main__":

    colorama.init()
    commandInvoker = "/"

    #the place where you map a command to the function, and also where you specify your parameters
    commands = {
        "debug": (modules.debug, ["Hello", "World", "!"]),
        "story": (modules.story, [])
    }

    interceptResponses = json.loads(open(os.path.join("data", "responses.json")).read())

    client = TheClient()
    client.run(open(os.path.join("data", "discordToken.txt")).read())