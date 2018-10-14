import os
import sys
import discord
import asyncio
import crayons
import colorama
import types

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
        #await self.close()

    async def on_message(self, message):
        pass

if __name__ == "__main__":

    colorama.init()
    __version__ = "0.0.1"
    CommandHandle = "/"

    client = TheClient()
    client.run(open(os.path.join("data", "discordToken.txt")).read())