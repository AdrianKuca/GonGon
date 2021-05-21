from random import randrange
from datetime import datetime

helloes = ["Hej!", "Cześć!", "Dzień dobry!", "Uszanowanko! (wow)"]

answers = [
    "Tak", "Nie", "Może", "Nie wiem :c",
    "Oczywiście, że tak", "Oczywiście, że nie", "Jeden rabin powie tak, drugi rabin powie nie", "Zarobiony jestem, zapytaj ponownie innym razem",
    "Oj tak", "Nie sądzę", "Kto wie?", "Nie zawracaj mi teraz głowy",
    "Mhm", "Nie-e", "I tak, i nie", "Głupie pytanie.",
]


def getHello():
    return helloes[randrange(0, len(helloes))]

def getWelcome(memberName, population):
    hello = getHello()
    welcomes = [
        f"{hello} Witaj wśród nocnej ciszy, {memberName}! Populacja serwera zwiększa się, Panie: {population}.",
        f"{hello} Witaj wśród cmentarzu disco, {memberName}! Populacja serwera wynosi już {population}.",
    ]
    return welcomes[randrange(0, len(welcomes))]

def getGoodbye(memberName, population):
    goodbyes = [
        f"{memberName} umarł/a! Pozostało jeszcze {population} uczestników.",
        f"{memberName} wypierdolił/a! Zostało nam jeszcze {population} uczestników do wypierdalania.",
        f"{memberName} sobie poszedł/a!",
        f"Żegnaj {memberName}!.. :crying_cat_face: :crying_cat_face: :crying_cat_face: Zostało nas tylko {population}",
        f"{memberName} znikł :c ||Populacja: {population}||",
    ]
    return goodbyes[randrange(0, len(goodbyes))]

def getResponseToGonciarz():
    response = [
        "UWAGA! TO NIE JEST PRAWDZIWY GONCIARZ, NIE SŁUCHAJCIE GO!",
        "Na tym serwerze nie ma miejsca na dwóch Gonciarzów, stawaj do walki.",
        "To ja jestem Gonciarzem!",
        "Fenek na prezydenta!",
        "Co to w ogóle znaczy być prawdziwym Gonciarzem..\nCzy ja jestem prawdziwy?..\nCzym jest prawdziwość?....",
    ]
    return response[randrange(0,len(response))]
    
def getAnswer():
    return answers[randrange(0,len(answers))]

async def updateGonciarzTime(channel):
    now = datetime.now()
    gonciarzTime = datetime.fromtimestamp(1590344553)
    delta = now-gonciarzTime
    await channel.edit(name=f"{delta.days}d, {delta.seconds//3600}h, {(delta.seconds%3600)//60}m")

# Night time announcments.

async def announceNightTimeBegin(channel):
    announces = [
        "Nastała noc...",
        "Ciemno wszędzie, głucho wszędzie, co to będzie? Co to będzie?",
        "Zapadł zmrok.",
        "Zapraszam na nocną!"
    ]
    await channel.send(announces[randrange(0,len(announces))])

async def announceNightTimeMiddle(channel):
    announces = [
        "2:00 - nocna trwa w najlepsze.",
        "Wybiła druga, połowa nocnej za nami.",
        "*świerszcze*",
    ]
    await channel.send(announces[randrange(0,len(announces))])

async def announceNightTimeEnd(channel):
    announces = [
        "Za dziesięć minut zamykam nocną.",
        "Uwaga! Nocna zostanie zamknięta za dziesięć minut!",
        "Do wszystkich uczestników: Nocna dobiega końca! Za dziesięć minut nie zostanie po niej ślad!",
    ]
    await channel.send(announces[randrange(0,len(announces))])

# Gonciarz announcments.

async def announceGonciarzOnline(channel):
    announces = [
        "GONCIARZ PRZYSZEDŁ, CHOWAĆ SIĘ!",
        "Zostaliśmy zaszczyceni obecnością jegomościa Krzysztofa Gonciarza.",
        "BONKERS!",
    ]
    await channel.send(announces[randrange(0,len(announces))])

async def announceGonciarzOffline(channel):
    announces = [
        "Gonciarza już z nami nie ma, miał piękny pogrzeb.",
        "Gonciarz, Gonciarz i po Gonciarzu.",
        "Wszystko co dobre kiedyś się kończy, no i właśnie się to skończyło. Gonciarz sobie znów poszedł.",
    ]
    await channel.send(announces[randrange(0,len(announces))])

async def messageCreator(self, message):
    appInfo = await self.application_info()
    await appInfo.owner.send(message)