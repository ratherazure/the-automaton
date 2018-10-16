import discord

#Reference on how to return different types of objects.
#{"string": "Hello World!", "file": discord.File("C:/SomePathHere/image.png"), "embed": discord.Embed()}

def main(*args):
    return {"string": "Hello World!"}

if __name__ == "__main__":
    main()