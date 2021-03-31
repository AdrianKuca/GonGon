from base64 import b64decode
from gongon import GonGon
import logging
logging.basicConfig(level=logging.INFO)

TOKEN = ""
with open("./secret", "r") as f:
    TOKEN = str(b64decode(f.read()), encoding="utf-8")

GonGon.run(TOKEN)