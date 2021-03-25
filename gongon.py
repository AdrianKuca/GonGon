import discord as dc
# Servers
GRAVEYARD = "702874201219924068"
POLYGON = "702874201219924068"

# Channels
HELLO = "702948154018103428"

class GonGon(dc.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_member_join(member):
        await member.create_dm()