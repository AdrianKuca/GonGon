import discord as dc
import utilities
from time import time
from os import getenv
from discord.ext import commands
import phonebook

DEV = getenv("DEBUG", 1) == 1


class GonGon(utilities.Utilities, commands.Bot):
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
        self.genericRole = dc.utils.get(
            self.mainGuild.roles, id=phonebook.GENERIC_ROLE_ID)
        self.nightRole = dc.utils.get(
            self.mainGuild.roles, id=phonebook.NIGHT_ROLE_ID)
        self.gonciarzTimeChannel = dc.utils.get(
            self.mainGuild.channels, id=phonebook.COUNTER_CHANNEL_ID)
        self.gonciarzUser = dc.utils.get(
            self.mainGuild.members, id=phonebook.GONCIARZ_ID)
        # endregion IDS
        # region STATE
        self.lastFunMessage = -1
        # endregion STATE

    # region EVENTS
    async def on_ready(self):
        '''Say hello when waking up.'''
        self.initializeState()
        await self.messageCreator(self.getHello() + " Wstałem." + (" ale debugowo" if DEV else " ale produkcyjnie"))

    async def on_message(self, message):
        '''Respond to gonciarz when he writes on the chat.'''
        if message.guild == self.mainGuild \
                and message.author.id == phonebook.GONCIARZ_ID and time() - self.lastFunMessage > 60*24:
            await message.channel.send(self.getResponseToGonciarz())
            self.lastFunMessage = time()

    async def on_member_join(self, member):
        '''Welcome people when they join the server.'''
        memberCount = len([m for m in self.mainGuild.members if not m.bot])
        await self.welcomeChannel.send(self.getWelcome(member.mention, memberCount))

    async def on_member_remove(self, member):
        '''Announce someone leaving the server.'''
        memberCount = len([m for m in self.mainGuild.members if not m.bot])
        await self.welcomeChannel.send(self.getGoodbye(member.name, memberCount))
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
