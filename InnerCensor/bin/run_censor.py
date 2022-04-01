#!/usr/bin/env python3

import argparse
from InnerCensor.commands import log_in, log_out, list_private_by_word, delete_by_word, print_channels, leave_channels, \
    find_by_list, del_by_list, print_channels_by_list, leave_by_list, delete_from_to
import sys
import datetime


def parse(argv):
    parser = argparse.ArgumentParser(prog="censor",
                                     description="A tool for cleansing your Telegram messages "
                                                 "from compromising messages.",
                                     epilog="Putin is a huilo. Russia will be free and Ukraine will be in peace.")

    subparsers = parser.add_subparsers()
    parser_login = subparsers.add_parser("login", help="Log in to Telegram")
    parser_login.set_defaults(func=log_in)

    parser_logout = subparsers.add_parser("logout", help="Log out from Telegram")
    parser_logout.set_defaults(func=log_out)

    parser_perslist = subparsers.add_parser("perslist", help="Get full list of messages in groups and personal "
                                                             "chats that contain given word")
    parser_perslist.add_argument("word")
    parser_perslist.set_defaults(func=list_private_by_word)

    parser_persdel = subparsers.add_parser("persdel", help="Delete all messages with chosen word. "
                                                           "Be careful, sometimes it leaves old messages untouched "
                                                           "so you would like to check it with perslist.")
    parser_persdel.add_argument("word")
    parser_persdel.set_defaults(func=delete_by_word)

    parser_publist = subparsers.add_parser("publist", help="List channels that contain given word")
    parser_publist.add_argument("word")
    parser_publist.set_defaults(func=print_channels)

    parser_pubdel = subparsers.add_parser("pubdel", help="Leave channels that contain given word")
    parser_pubdel.add_argument("word")
    parser_pubdel.set_defaults(func=leave_channels)

    parser_perslist_auto = subparsers.add_parser("perslistauto", help="Get full list of messages in groups and "
                                                                      "personal chats that contain words from list")
    parser_perslist_auto.set_defaults(func=find_by_list)

    parser_persdel_auto = subparsers.add_parser("persdelauto", help="Delete all messsages with words from the list. "
                                                                    "Be careful, sometimes it leaves old messages "
                                                                    "untouched so you would like to check it "
                                                                    "with perslistauto."
                                                )
    parser_persdel_auto.set_defaults(func=del_by_list)

    parser_publist_auto = subparsers.add_parser("publistauto", help="List channels that contain words from list")
    parser_publist_auto.set_defaults(func=print_channels_by_list)

    parser_publist_auto = subparsers.add_parser("pubdelauto", help="Leave channels that contain words from list")
    parser_publist_auto.set_defaults(func=leave_by_list)

    parser_del_from_to = subparsers.add_parser("delfromto", help="Delete all messages in personal chat or groups "
                                                                 "within a chosen period. Date in format YYYY-MM-DD. "
                                                                 "Period counts inclusively.")
    parser_del_from_to.set_defaults(func=delete_from_to)
    parser_del_from_to.add_argument("from_when", type=datetime.datetime.fromisoformat)
    parser_del_from_to.add_argument("to", type=datetime.datetime.fromisoformat,
                                    default=datetime.datetime.date(datetime.datetime.now()),
                                    nargs="?")

    try:
        res = parser.parse_args(argv)
        if hasattr(res, "word"):
            return res.func, (res.word,)
        elif hasattr(res, "from_when"):
            return res.func, (res.from_when, res.to)
        else:
            return res.func, ()
    except AttributeError:
        print("Invalid command. View incen -h for help.")
        return lambda: None, ()


def main():
    action, args = parse(sys.argv[1:])
    action(*args)


if __name__ == '__main__':
    main()
