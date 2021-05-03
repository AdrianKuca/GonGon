import asyncio
from asyncio.tasks import sleep
import discord as dc
from discord.client import Client
from discord.ext import commands
from random import randrange
import funstuff as fs
from time import time
from os import getenv
DEV = getenv("DEBUG", 1) == 1

if DEV == False:
    GUILD_ID = 702874201219924068
    WELCOME_ID = 702948154018103428
    COUNTER_CHANNEL_ID = 808098557705453568
    GONCIARZ_ID = 690188854590046222
else:
    GUILD_ID = 824773607628472350
    WELCOME_ID = 824773607628472353
    COUNTER_CHANNEL_ID = 824773607628472354
    GONCIARZ_ID = 142327920747216896

intents = dc.Intents.default()
intents.members = True
intents.presences = True
GonGon = commands.Bot(command_prefix='/', intents=intents)



@GonGon.event
async def on_ready():
    '''Say hello when waking up.'''
    #await helloChannel.send(fs.getHello() + " Wstałem.")
    mainGuild = dc.utils.get(GonGon.guilds, id=GUILD_ID)
    welcomeChannel = dc.utils.get(mainGuild.channels, id=WELCOME_ID)
    gonciarzTimeChannel = dc.utils.get(mainGuild.channels, id=COUNTER_CHANNEL_ID)
    gonciarzUser = dc.utils.get(mainGuild.members, id=GONCIARZ_ID)

    lastStatus = "offline"
    await fs.updateGonciarzTime(gonciarzTimeChannel)
    # Main loop every second.
    ctr = 0
    while True:
        try:
            if ctr == 60*6:
                await fs.updateGonciarzTime(gonciarzTimeChannel)
                ctr = 0

            gonciarzStatus = gonciarzUser.raw_status
            if gonciarzStatus == "online" and lastStatus != "online":
                lastStatus = "online"
                await fs.announceGonciarzOnline(welcomeChannel)
            elif gonciarzStatus == "offline" and lastStatus != "offline":
                lastStatus = "offline"
                await fs.announceGonciarzOffline(welcomeChannel)


            ctr+=1
            await asyncio.sleep(1)

        except Exception as ex:
@GonGon.command(
    name="czy", 
    help='Zadaj pytanie a przeznaczenie odpowie! Przykład: /czy kuca jest głupi'
)
async def eightBall(ctx, *args):
    answer = fs.getAnswer()
    await ctx.reply(answer)
            
@GonGon.command(
    name="bombel"
)
async def bubble(ctx, *args):
    sideSize = 9
    message = (("||pop||"*sideSize)+"\n")*sideSize
    await ctx.send(message)

lastFunMessage = 0
@GonGon.listen()
async def on_message(message):
    if message.author.id == GONCIARZ_ID and time() - lastFunMessage > 60*24:
        await message.channel.send(fs.getResponseToGonciarz())
        

@GonGon.event
async def on_member_join(member):
    '''Welcome people when they join the server.'''
    mainGuild = dc.utils.get(GonGon.guilds, id=GUILD_ID)
    welcomeChannel = dc.utils.get(mainGuild.channels, id=WELCOME_ID)

    memberCount = len([m for m in mainGuild.members if not m.bot])
    await welcomeChannel.send(fs.getWelcome(member.mention, memberCount))

@GonGon.event
async def on_member_remove(member):
    mainGuild = dc.utils.get(GonGon.guilds, id=GUILD_ID)
    welcomeChannel = dc.utils.get(mainGuild.channels, id=WELCOME_ID)

    memberCount = len([m for m in mainGuild.members if not m.bot])
    await welcomeChannel.send(fs.getGoodbye(member.mention, memberCount))

@GonGon.command(
    name="czy", 
    help='Zadaj pytanie a przeznaczenie odpowie! Przykład: /czy kuca jest głupi'
)
async def eightBall(ctx, *args):
    answer = fs.getAnswer()
    await ctx.reply(answer)

@GonGon.command(
    name="bombel"
)
async def bubble(ctx, *args):
    sideSize = 9
    message = (("||pop||"*sideSize)+"\n")*sideSize
    await ctx.send(message)
