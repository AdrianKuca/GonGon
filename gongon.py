from datetime import datetime
import discord as dc
import utilities
import nighsthift
import timeloop
from time import time
from os import getenv
from discord.ext import commands
import phonebook

DEV = getenv("DEBUG", 1) == 1


class GonGon(utilities.Utilities, nighsthift.NightShiftUtilities, timeloop.TimeLoop, commands.Bot):
    def __init__(self) -> None:
        intents = dc.Intents.default()
        intents.members = True
        intents.presences = True
        super().__init__(command_prefix='/', intents=intents, case_insensitive=True)

        # region REGISTER COMMANDS
        self.command(
            name="czy",
            help='Zadaj pytanie a przeznaczenie odpowie! Przykład: /czy kuca jest głupi'
        )(self.eightBall)
        self.command(
            name="bombel"
        )(self.bubble)
        # endregion REGISTER COMMANDS

    def initializeState(self):
        # region IDS
        self.mainGuild = dc.utils.get(self.guilds, id=phonebook.GUILD_ID)
        self.welcomeChannel = dc.utils.get(
            self.mainGuild.channels, id=phonebook.WELCOME_ID)
        self.nightChannels = [dc.utils.get(self.mainGuild.channels, id=x)
                              for x in phonebook.NIGHT_CHANNELS_ID]
        self.movieChannel = dc.utils.get(
            self.mainGuild.channels, id=phonebook.MOVIE_CHANNEL)
        self.nightCategory = dc.utils.get(
            self.mainGuild.categories, id=phonebook.NIGHT_CATEGORY_ID)
        self.genericRole = dc.utils.get(
            self.mainGuild.roles, id=phonebook.GENERIC_ROLE_ID)
        self.nightRole = dc.utils.get(
            self.mainGuild.roles, id=phonebook.NIGHT_ROLE_ID)
        self.gonciarzTimeChannel = dc.utils.get(
            self.mainGuild.channels, id=phonebook.COUNTER_CHANNEL_ID)
        self.mayTimeChannel = dc.utils.get(
            self.mainGuild.channels, id=phonebook.COUNTER_CHANNEL_ID)
        self.gonciarzUser = dc.utils.get(
            self.mainGuild.members, id=phonebook.GONCIARZ_ID)
        # endregion IDS
        # region STATE
        self.lastFunMessage = -1
        self.nightTimeStartHour = 22
        self.nightTimeStartMinute = 00
        self.nightTimeEndHour = 6
        self.nightTimeEndMinute = 00
        # endregion STATE
        # region TIMELOOP EVENTS
        self.registerCyclicEvent(60*6, self.updateGonciarzTime)
        self.registerCyclicEvent(60*6, self.updateMayTime)
        self.registerOnTimeEvent(
            self.nightTimeStartHour, self.nightTimeStartMinute, self.openNightShift)
        self.registerOnTimeEvent(
            self.nightTimeStartHour, self.nightTimeStartMinute, self.announceNightTimeBegin)
        self.registerOnTimeEvent(
            2, 00, self.announceNightTimeMiddle)
        self.registerOnTimeEvent(
            5, 50, self.announceNightTimeEnd)
        self.registerOnTimeEvent(6, 00, self.closeNightShift)
        # endregion TIMELOOP EVENTS
    # region EVENTS

    async def on_ready(self):
        '''Say hello when waking up and bring everything to proper states.'''
        self.initializeState()
        await self.messageCreator(self.getHello() + " Wstałem." + (" ale debugowo" if DEV else " ale produkcyjnie"))

        # If starts at night, open nightshift quietly.
        now = datetime.fromtimestamp(time())
        if now.hour >= self.nightTimeStartHour or now.hour < self.nightTimeEndHour:
            isNightTime = True
        elif now.hour >= self.nightTimeEndHour or now.hour < self.nightTimeStartHour:
            isNightTime = False
        if isNightTime:
            await self.openNightShift()
        else:
            await self.closeNightShift()

            # Start blocking timeloop
        await self.timeLoop()

    async def on_message(self, message):
        '''Respond to gonciarz when he writes on the chat.'''
        if message.guild == self.mainGuild \
                and message.author.id == phonebook.GONCIARZ_ID and time() - self.lastFunMessage > 60*24:
            await message.channel.send(self.getResponseToGonciarz())
            self.lastFunMessage = time()
        await super().on_message(message)

    async def on_member_join(self, member):
        '''Welcome people when they join the server.'''
        memberCount = len([m for m in self.mainGuild.members if not m.bot])
        await self.welcomeChannel.send(self.getWelcome(member.mention, memberCount))
    # endregion EVENTS

    # region COMMANDS
    async def eightBall(self, ctx, *args):
        answer = self.getAnswer()
        await ctx.reply(answer)

    async def bubble(self, ctx, *args):
        sideSize = 9
        message = (("||pop||"*sideSize)+"\n")*sideSize
        await ctx.send(message)
    # endregion COMMANDS
