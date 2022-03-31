from InnerCensor import client, DANGEROUS_LIST
from InnerCensor.main import search_messages, print_messages, get_channels, get_msg_from_to, \
    update_expires, read_expires
from termcolor import colored
from telethon import functions as fc
import datetime


async def check_expired():
    if datetime.datetime.now() >= read_expires():
        res = await client(fc.help.GetTermsOfServiceUpdateRequest())
        update_expires(res.expires)
        if hasattr(res, "terms_of_service"):
            print("check your Telegram for a terms of agreement update.")


def execute_in_loop(func):
    def wrapper(*args, **kwargs):
        client.loop.run_until_complete(client.connect())
        return client.loop.run_until_complete(func(*args, **kwargs))

    return wrapper


def check_connection(func):
    async def wrapper(*args, **kwargs):
        if await client.is_user_authorized():
            await check_expired()
            await func(*args, **kwargs)
        else:
            print(colored("Error: user unauthorized", "red"))

    return wrapper


@execute_in_loop
async def log_in():
    await client.start()


@execute_in_loop
@check_connection
async def log_out():
    await client.log_out()
    update_expires(datetime.datetime.now())


@execute_in_loop
@check_connection
async def list_private_by_word(word):
    await print_messages(search_messages(word, chat_type="personal"))


@execute_in_loop
@check_connection
async def delete_by_word(word):
    async for message in search_messages(word, chat_type="personal"):
        await message.delete()


@execute_in_loop
@check_connection
async def print_channels(word):
    channels = await get_channels(word)
    for channel in channels:
        print(colored(channel, "yellow"))


@execute_in_loop
@check_connection
async def leave_channels(word):
    channels = await get_channels(word)
    for channel in channels:
        await client.delete_dialog(channel)


def find_by_list():
    for word in DANGEROUS_LIST:
        print(colored(f"by {word}", "blue"))
        list_private_by_word(word)


def del_by_list():
    for word in DANGEROUS_LIST:
        delete_by_word(word)


@execute_in_loop
@check_connection
async def print_channels_by_list():
    channels = set()
    for word in DANGEROUS_LIST:
        channels |= await get_channels(word)
    for channel in channels:
        print(colored(channel, "yellow"))


def leave_by_list():
    for word in DANGEROUS_LIST:
        leave_channels(word)


@execute_in_loop
@check_connection
async def delete_from_to(begin, end):
    async for msg in get_msg_from_to(begin, end):
        await msg.delete()




