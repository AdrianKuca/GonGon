from base64 import b64decode
from gongon import GonGon

TOKEN = ""
with open("./secret", "r") as f:
    TOKEN = str(b64decode(f.read()), encoding="utf-8")

client = GonGon()
client.run(TOKEN)