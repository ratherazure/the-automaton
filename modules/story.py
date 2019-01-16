import discord
import requests
import os
import json
import maya
import math

class Author():
    def getAuthorBase(self, data):
        data = data["included"]
        data = [entry for entry in data if entry["type"] == "user"]
        return data

    def __init__(self, data):
        data = self.getAuthorBase(data)[0]
        self.name = data["attributes"]["name"]
        self.avatar = data["attributes"]["avatar"]["32"]
        self.url = data["meta"]["url"]

class Story():

    def ordinal(self, n): #thanks, random dude on StackOverflow!
        n = int(n)
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
        if 11 <= (n % 100) <= 13:
            suffix = 'th'
        return str(n) + suffix

    def getCover(self, data):
        try:
            data["attributes"]["cover_image"]["full"]
        except KeyError:
            return None
        else:
            return data["attributes"]["cover_image"]["full"]

    def getStoryBase(self, data):
        data = data["data"][0]
        return data

    def __init__(self, data):
        dataBackup = data
        data = self.getStoryBase(data)
        self.author = Author(dataBackup)
        self.title = data["attributes"]["title"]
        self.description = data["attributes"]["short_description"]
        self.colour = discord.Colour(int(data["attributes"]["color"]["hex"], 16))
        self.status = data["attributes"]["completion_status"].title()
        self.ratio = format(data["attributes"]["num_likes"], ",d") + "/" + format(data["attributes"]["num_dislikes"], ",d")
        self.words = format(data["attributes"]["num_words"], ",d") + " Words" if data["attributes"]["num_words"] != 1 else format(data["attributes"]["num_words"], ",d") + " Word"
        self.chapters = format(data["attributes"]["num_chapters"], ",d") + " Chapters" if data["attributes"]["num_chapters"] != 1 else format(data["attributes"]["num_chapters"], ",d") + " Chapter"
        self.content_rating = "[" + data["attributes"]["content_rating"].title() + "]"
        self.tags = " ".join(["[" + entry["attributes"]["name"] + "]" for entry in dataBackup["included"] if entry["type"] == "story_tag"])
        self.date = maya.MayaDT.from_rfc3339(data["attributes"]["date_published"]).datetime().strftime("%A %d %B %Y").split(" ") #opening it up
        self.date[1] = self.ordinal(self.date[1].strip("0")) + " of" #making changes
        self.date = " ".join(self.date) #putting it back
        self.url = data["meta"]["url"]
        self.cover = self.getCover(data)

def formatEmbed(story):
    em = discord.Embed(title=story.title, description=story.description, url=story.url, colour=story.colour)
    em.set_author(name=story.author.name, icon_url=story.author.avatar, url=story.author.url)
    if story.cover is not None:
        em.set_thumbnail(url=story.cover)
    em.add_field(name="Current Status", value=story.status, inline=True)
    em.add_field(name="Likes/Dislikes", value=story.ratio, inline=True)
    em.add_field(name="Date Published", value=story.date, inline=False)
    em.add_field(name="Chapters", value=story.words + " & " + story.chapters, inline=False)
    em.add_field(name="Tags & Content Rating", value="{} - {}".format(story.tags, story.content_rating), inline=False)
    em.set_footer(text="Powered by the Fimfiction API", icon_url="https://static.fimfiction.net/images/logo-2x.png")
    return em

def main(*args):
    if len(args) == 0:
        return {"content": "```\nError {status}: {message}\n```".format(status = "400", message = "Bad Request; No Arguments were Recieved")}
    
    try:
        headers = {"Authorization": "bearer {}".format(open(os.path.join("data", "fimfictionToken.txt")).read())}
    except FileNotFoundError:
        headers = {}

    Response = requests.get("https://www.fimfiction.net/api/v2/stories?query={}&include=characters,tags,author&sort=-relevance&page[size]=1".format(args), headers=headers).text
    Response = json.loads(Response)

    if "errors" in Response and "data" not in Response:
        return {"content": "```\nError {status}: {message}\n```".format(status = Response["errors"][0]["status"], message = Response["errors"][0]["title"].title())}
    elif "data" in Response and "errors" not in Response and Response["data"] == []:
        return {"content": "```\nError {status}: {message}\n```".format(status = "404", message = "Search Query is Valid; No Data Returned")}
    else:
        return {"embed": formatEmbed(Story(Response))}

if __name__ == "__main__":
    main()