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
        if message.content.startswith(commandInvoker) and commands.get(message.content.split(" ")[0][len(commandInvoker):], [None, None])[0] != [None, None]: #if message starts with the command handle and is in the command dictionary then...
            command = commands.get(message.content.split(" ")[0][len(commandInvoker):], [None, None]) #take the invoked command and return with a python pointer to a function
            if command[1] == []: #for some reason, one line if statements don't work here?
                parameters = message.content.split(" ")[1:] #if there are no predetermined parameters, take them from the message itself.
            else:
                parameters = command[1]
            response = command[0](*parameters) #execute the function with the parameters.
            await message.channel.send(content = response.get("content", None), embed = response.get("embed", None), file = response.get("file", None)) #whatever it gets back, just send it. no validation.


if __name__ == "__main__":

    colorama.init()
    commandInvoker = "/"

    #the place where you map a command to the function, and also where you specify your parameters
    commands = {
        "debug": (modules.debug, ["Hello", "World", "!"]),
        "story": (modules.story, [])
    }

    client = TheClient()
    client.run(open(os.path.join("data", "discordToken.txt")).read())