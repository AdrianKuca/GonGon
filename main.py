from base64 import b64decode
import logging
import discord as dc
from discord.client import Client
from gongon import GonGon
logging.basicConfig(level=logging.INFO)

TOKEN = ""
with open("./secret", "r") as f:
    TOKEN = str(b64decode(f.read()), encoding="utf-8")
gongon = GonGon()
gongon.run(TOKEN)
