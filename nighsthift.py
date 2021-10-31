
from random import randrange
import discord as dc


class NightShiftUtilities:
    async def openNightShift(self):
        for nightChannel in self.nightCategory.channels:
            # Show the night channels for the night role.
            overwrites = nightChannel.overwrites_for(self.nightRole)
            if not overwrites.view_channel or not overwrites.read_messages:
                overwrites.update(
                    view_channel=True, read_messages=True)
                await nightChannel.set_permissions(self.nightRole, overwrite=overwrites)

    async def closeNightShift(self):
        for nightChannel in self.nightCategory.channels:
            # Unshow the channels.
            overwrites = nightChannel.overwrites_for(self.nightRole)
            if overwrites.view_channel or overwrites.read_messages:
                overwrites.update(
                    view_channel=False, read_messages=False)
                await nightChannel.set_permissions(self.nightRole, overwrite=overwrites)
                # Purge messages on the text channels.
                if nightChannel.type == dc.ChannelType.text:
                    messages = await nightChannel.history(limit=100).flatten()
                    while len(messages):
                        messages = await nightChannel.history(limit=100).flatten()
                        await nightChannel.purge()

    # Night time announcments.

    async def announceNightTimeBegin(self):
        announces = [
            "Nastała noc...",
            "Ciemno wszędzie, głucho wszędzie, co to będzie? Co to będzie?",
            "Zapadł zmrok.",
            "Zapraszam na nocną!"
        ]
        for nightChannel in self.nightCategory.channels:
            if nightChannel.type == dc.ChannelType.text:
                await nightChannel.send(announces[randrange(0, len(announces))])

    async def announceNightTimeMiddle(self):
        announces = [
            "2:00 - nocna trwa w najlepsze.",
            "Wybiła druga, połowa nocnej za nami.",
            "*świerszcze*",
        ]
        for nightChannel in self.nightCategory.channels:
            if nightChannel.type == dc.ChannelType.text:
                await nightChannel.send(announces[randrange(0, len(announces))])

    async def announceNightTimeEnd(self):
        announces = [
            "Za dziesięć minut zamykam nocną.",
            "Uwaga! Nocna zostanie zamknięta za dziesięć minut!",
            "Do wszystkich uczestników: Nocna dobiega końca! Za dziesięć minut nie zostanie po niej ślad!",
        ]
        for nightChannel in self.nightCategory.channels:
            if nightChannel.type == dc.ChannelType.text:
                await nightChannel.send(announces[randrange(0, len(announces))])
