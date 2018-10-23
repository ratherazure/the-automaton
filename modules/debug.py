import discord

#Reference on how to return different types of objects.
#{"content": "Hello World!", "file": discord.File("C:/SomePathHere/image.png"), "embed": discord.Embed()}

def main(*args):
    return {"content": "Hello World!"}

if __name__ == "__main__":
    main()