import random
import cogs.channels as channels
import datetime
import pytz
import validators
from discord.ext import commands, tasks


days = {
    0: [
        "the day of the moon",
        "Moonday",
        "Monday",
    ],
    1: [
        "Tyr's day",
        "Tuesday",
        "Dndndndndndndnd"
    ],
    2: [
        "Odin's day",
        "Wednesday",
        "Wednesday, my dudes",
        "hump day",
        "Ness' wedding day",
        "https://www.youtube.com/watch?v=du-TY1GUFGk",
    ],
    3: [
        "Thor's day",
        "Thorsday",
        "civ day",
        "Thursday",
    ],
    4: [
        "Frigga's day",
        "Friday, Friday, gotta get down on Friday",
        "Friday",
    ],
    5: [
        "Saturn's day",
        "Saturday",
    ],
    6: [
        "the day of the sun",
        "Sunday",
        "Sunday, Sunday, Sunday",
    ],
}

templates = [
    "Today is {0}.",
    "Brothers, the day is {0}.",
    "Yoooooo, today is {0}! Brother.",
    "The day is {0}. Prepare yourself.",
    "What if I said to you that in fact, today is not {0}? I'd be lying.",
    "Rejoice, for today is {0}.",
    "{0}",
    "Today is {0}, I hope you have your pants on.",
    "Gentlemen, it is with great pleasure that I inform you. Today is {0}.",
]


class AnnounceDay(commands.Cog):

    def __init__(self, bot, start_tasks=True):
        self.bot = bot
        self.tz = pytz.timezone("US/Eastern")
        if start_tasks:
            self.on_hour.start()

    def cog_unload(self):
        self.on_hour.cancel()

    def should_announce_day(self):
        now = datetime.datetime.now(self.tz)
        return now.hour == 7

    def get_message(self):
        day = datetime.datetime.now(self.tz).weekday()
        message = random.choice(days[day])

        if validators.url(message):
            return f"A video to start your {day}: {message}"

        return random.choice(templates).format(message)

    @tasks.loop(hours=1.0)
    async def on_hour(self):
        await self.__on_hour()
    async def __on_hour(self):
        if self.should_announce_day():
            channel = self.bot.get_channel(channels.GENERAL)
            message = self.get_message()
            await channel.send(message)

    @on_hour.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()
