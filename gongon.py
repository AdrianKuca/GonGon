import asyncio
from asyncio.tasks import sleep
import discord as dc
from discord.client import Client
from discord.ext import commands
from random import randrange
import funstuff as fs
from time import time
from os import getenv
from datetime import datetime
DEV = getenv("DEBUG", 1) == 1

if DEV == False:
    GUILD_ID = 702874201219924068
    WELCOME_ID = 702948154018103428 
    COUNTER_CHANNEL_ID = 808098557705453568
    GONCIARZ_ID = 690188854590046222
    NIGHT_CHANNELS_ID = [838814978789867580, 838815158288908319, 838815290909261846, 838815347725041714, 838815629984268338, 838815746229534751]
    GENERIC_ROLE_ID = 777233707319689278
    NIGHT_ROLE_ID = 838813946097565788
else:
    GUILD_ID = 824773607628472350
    WELCOME_ID = 824773607628472353
    COUNTER_CHANNEL_ID = 824773607628472354
    GONCIARZ_ID = 142327920747216896
    NIGHT_CHANNELS_ID = [825158625131626497, 838889194696081448, 839959183926886410]
    GENERIC_ROLE_ID = 838889435046740009
    NIGHT_ROLE_ID = 838889435046740009


intents = dc.Intents.default()
intents.members = True
intents.presences = True
GonGon = commands.Bot(command_prefix='/', intents=intents)


@GonGon.event
async def on_ready():
    '''Say hello when waking up.'''
    await fs.messageCreator(GonGon, fs.getHello() + " Wstałem." + (" ale debugowo" if DEV else " ale produkcyjnie"))
    mainGuild = dc.utils.get(GonGon.guilds, id=GUILD_ID)
    welcomeChannel = dc.utils.get(mainGuild.channels, id=WELCOME_ID)
    nightChannels = [dc.utils.get(mainGuild.channels, id=x) for x in NIGHT_CHANNELS_ID]
    genericRole = dc.utils.get(mainGuild.roles, id=GENERIC_ROLE_ID)
    nightRole = dc.utils.get(mainGuild.roles, id=NIGHT_ROLE_ID)
    gonciarzTimeChannel = dc.utils.get(mainGuild.channels, id=COUNTER_CHANNEL_ID)
    gonciarzUser = dc.utils.get(mainGuild.members, id=GONCIARZ_ID)

    isNightTime = False

    middleTimePassed = False
    tenMinutesTillDuskPassed = False
    lastStatus = "offline"
    # Main loop every second.
    ctr = 0
    while True:
        try:
            if ctr == 60*6:
                await fs.updateGonciarzTime(gonciarzTimeChannel)
                ctr = 0
            
            now = datetime.fromtimestamp(time())
            if now.hour >= 22 or now.hour < 6:
                isNightTime = True
            elif now.hour >= 6 or now.hour < 22:
                isNightTime = False

            if isNightTime:
                for nightChannel in nightChannels:
                    # Show the night channels for the night role.
                    overwrites = nightChannel.overwrites_for(nightRole)
                    if not overwrites.view_channel or not overwrites.read_messages:
                        overwrites.update(view_channel=True, read_messages=True)
                        await nightChannel.set_permissions(nightRole, overwrite=overwrites)
                        if nightChannel.type == dc.ChannelType.text:
                            await fs.announceNightTimeBegin(nightChannel)
                    
                    if nightChannel.type == dc.ChannelType.text:
                        if now.hour == 2 and not middleTimePassed:
                            await fs.announceNightTimeMiddle(nightChannel)
                            middleTimePassed = True

                        elif now.hour == 5 and now.minute == 50 and not tenMinutesTillDuskPassed:
                            await fs.announceNightTimeEnd(nightChannel)
                            tenMinutesTillDuskPassed = True

            else:
                for nightChannel in nightChannels:
                    # Unshow the channels.
                    overwrites = nightChannel.overwrites_for(nightRole)
                    if overwrites.view_channel or overwrites.read_messages:
                        overwrites.update(view_channel=False, read_messages=False)
                        await nightChannel.set_permissions(nightRole, overwrite=overwrites)
                        # Purge messages on the text channels.
                        if nightChannel.type == dc.ChannelType.text:
                            messages =  await nightChannel.history(limit=100).flatten()
                            while len(messages):
                                messages =  await nightChannel.history(limit=100).flatten()
                                await nightChannel.purge()



            gonciarzStatus = gonciarzUser.status.name
            if gonciarzStatus == "online" and lastStatus != "online":
                lastStatus = "online"
                await fs.announceGonciarzOnline(welcomeChannel)
            elif gonciarzStatus == "offline" and lastStatus != "offline":
                lastStatus = "offline"
                await fs.announceGonciarzOffline(welcomeChannel)

            ctr+=1
            await asyncio.sleep(1)

        except Exception as ex:
            await fs.messageCreator(GonGon,"Aaaa ratunku! Wyjebałem się, pomuż...\n" + str(ex))
            print("There's been a catastrophy:", str(ex))
            await asyncio.sleep(600)
            
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
    global lastFunMessage
    if message.guild == dc.utils.get(GonGon.guilds, id=GUILD_ID) \
        and message.author.id == GONCIARZ_ID and time() - lastFunMessage > 60*24:
        await message.channel.send(fs.getResponseToGonciarz())
        lastFunMessage = time()
        

@GonGon.event
async def on_member_join(member):
    '''Welcome people when they join the server.'''
    mainGuild = member.guild
    welcomeChannel = dc.utils.get(mainGuild.channels, id=WELCOME_ID)

    memberCount = len([m for m in mainGuild.members if not m.bot])
    await welcomeChannel.send(fs.getWelcome(member.mention, memberCount))

@GonGon.event
async def on_member_remove(member):
    mainGuild = member.guild
    welcomeChannel = dc.utils.get(mainGuild.channels, id=WELCOME_ID)

    memberCount = len([m for m in mainGuild.members if not m.bot])
    await welcomeChannel.send(fs.getGoodbye(member.name, memberCount))
