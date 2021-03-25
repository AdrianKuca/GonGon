import os
from base64 import b64decode
import discord

TOKEN = ""
with open("./secret", "r") as f:
    TOKEN = str(b64decode(f.read()), encoding="utf-8")

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)