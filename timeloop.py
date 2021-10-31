import asyncio
import os
from datetime import date, datetime, timedelta
from time import time
from threading import Lock


class Event:
    def __init__(self, handler, args):
        self.handler = handler
        self.args = args
        self.lastRunTime = datetime.now() - timedelta(minutes=2)
        self.lock = Lock()

    async def run(self):
        self.lock.acquire()
        if datetime.now() > self.lastRunTime + timedelta(minutes=1):
            await self.handler(*self.args)
            self.lastRunTime = datetime.now()
        self.lock.release()


class CyclicEvent(Event):
    def __init__(self, seconds, handler, args):
        super().__init__(handler, args)
        self.seconds = seconds

    def isTime(self, ctr):
        return ctr % self.seconds == 0


class OnTimeEvent(Event):
    def __init__(self, hour, minute, handler, args):
        super().__init__(handler, args)
        self.hour = hour
        self.minute = minute

    def isTime(self, now):
        return now.hour == self.hour and now.minute == self.minute


class TimeLoop:
    def __init__(self, *args, **kwargs):
        self.cyclicEvents = []
        self.onTimeEvents = []
        super().__init__(*args, **kwargs)

    def registerCyclicEvent(self, seconds, handler, args=[]):
        self.cyclicEvents.append(CyclicEvent(seconds, handler, args))

    def registerOnTimeEvent(self, hour, minute, handler, args=[]):
        self.onTimeEvents.append(OnTimeEvent(hour, minute, handler, args))

    async def timeLoop(self):
        """Main GonGon event loop every second."""
        errorCounter = 0
        ctr = 0
        while True:
            try:
                timestamp = time()
                now = datetime.fromtimestamp(timestamp)
                for cyclicEvent in self.cyclicEvents:
                    if cyclicEvent.isTime(timestamp):
                        await cyclicEvent.run()

                for onTimeEvent in self.onTimeEvents:
                    if onTimeEvent.isTime(now):
                        await onTimeEvent.run()
                ctr += 1
                await asyncio.sleep(1)

            except Exception as ex:
                errorCounter += 1
                if errorCounter == 3:
                    os.system("sudo systemctl restart gongon")
                await self.messageCreator("Aaaa ratunku! Wyjebałem się, pomuż...\n" + str(ex))
                print("There's been a catastrophy:", str(ex))
                await asyncio.sleep(60*10)
