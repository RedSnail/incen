from telethon.tl.types import Chat, Channel, User
from termcolor import colored
import asyncio
import datetime
import pytz

from . import client


def short_name(chat):
    if isinstance(chat, Chat):
        return chat.title, "red"
    if isinstance(chat, User):
        return chat.username, "green"
    if isinstance(chat, Channel):
        return chat.title, "yellow"


async def async_filter(decider, generator):
    async for item in generator:
        if decider(item):
            yield item


def search_messages(word, chat_type="all"):
    if chat_type == "all":
        return client.iter_messages(None, search=word)
    if chat_type == "personal":
        return async_filter(lambda message: isinstance(message.chat, User) or isinstance(message.chat, Chat),
                            client.iter_messages(None, search=word))
    if chat_type == "public":
        return async_filter(lambda message: isinstance(message.chat, Channel), client.iter_messages(None, search=word))


async def print_messages(messages):
    async for message in messages:
        print(colored(message.date.strftime("%Y/%m/%d, %H:%M:%S"), "magenta"))
        print(f"{colored(*short_name(message.chat))}:\n{message.text}")
        print(colored("=============================", "grey"))


async def get_channels(word):
    channels = set()
    async for message in search_messages(word, chat_type="public"):
        channels.add(message.chat.title)

    return channels


def get_msg_from_to(begin, end):
    local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    begin = begin.replace(tzinfo=local_timezone).astimezone(pytz.UTC)
    end = end.replace(tzinfo=local_timezone).astimezone(pytz.UTC)
    msg_filter = lambda message: (isinstance(message.chat, User) or isinstance(message.chat, Chat)) and \
                                 end >= message.date >= begin

    return async_filter(msg_filter, client.iter_messages(None, offset_date=end + datetime.timedelta(days=1)))


def update_expires(date):
    with open("expires_date.txt", "w") as out:
        out.write(date.isoformat())


def read_expires():
    try:
        with open("expires_date.txt", "r") as inp:
            text = inp.read().strip()
            return datetime.datetime.fromisoformat(text)
    except FileNotFoundError:
        return datetime.datetime.now() - datetime.timedelta(days=1)
