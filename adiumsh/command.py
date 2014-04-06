# -*- coding: utf-8 -*-
import argparse
import sys
from .settings import (DEFAULT_SERVICE, DEFAULT_ACCOUNT, DEFAULT_BUDDY,
                       DEFAULT_CHAT, CONFIG_PATH)
from .utils import get_config


def parse_args():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]',
                                     prog='adiumsh')
    account_help = 'account used to send the message (for alias)'
    parser.add_argument('-t', '--account',
                        help=account_help)
    parser.add_argument('-s', '--service',
                        help='service associated with the account')
    subparsers = parser.add_subparsers(dest='command')
    parser_send = subparsers.add_parser('send')

    parser_send.add_argument('-m', '--message',
                             help='message to send')
    send_buddy_group = parser_send.add_mutually_exclusive_group()
    send_buddy_group.add_argument('-b', '--buddy',
                                  help='name of the target account')
    send_buddy_group.add_argument('-a', '--alias',
                                  help='alias of the target account')
    parser_receive = subparsers.add_parser('receive')
    parser_receive.add_argument('-c', '--chat',
                                help='chat method to use')
    args = parser.parse_args()
    args.service = args.service or DEFAULT_SERVICE
    args.account = args.account or DEFAULT_ACCOUNT
    if not args.service or not args.account:
        msg = 'Must specify service and account'
        raise parser.error(msg)

    # `send` subcommand
    if args.command == 'send':
        parse_send(parser_send, args)
    # `receive` subcommand
    elif args.command == 'receive':
        parse_receive(parser_receive, args)
    return args


def parse_send(parser, args):
    if not args.buddy and not args.alias:
        args.buddy = args.buddy or DEFAULT_BUDDY
        if not args.buddy:
            msg = 'Must specify either buddy or alias'
            raise parser.error(msg)
    if not args.message:
        message = sys.stdin.read()
        message = message.strip()
        if not message:
            msg = 'Message cannot be empty'
            raise parser.error(msg)
        args.message = message
    else:
        if not args.message.strip():
            msg = 'Message cannot be empty'
            raise parser.error(msg)


def parse_receive(parser, args):
    args.chat = args.chat or DEFAULT_CHAT
    if not args.chat:
        msg = 'Must specify default chat'
        parser.error(msg)
    else:
        chat = args.chat
        chat_config = get_config(CONFIG_PATH, 'chat-' + chat)
        if chat_config is None:
            msg = 'Chat "%s" does not exist in the config file' % chat
            parser.error(msg)
        if chat == 'simi':
            if not chat_config.get('simi-key'):
                msg = 'Must set simi key in the config file'
                parser.error(msg)
        else:
            if not chat_config.get('patterns'):
                msg = 'Must set chat patterns in the config file'
                parser.error(msg)
