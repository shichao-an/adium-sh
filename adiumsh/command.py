# -*- coding: utf-8 -*-
import argparse
import sys
from .settings import (DEFAULT_SERVICE, DEFAULT_ACCOUNT, DEFAULT_BUDDY)


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
        parse_receive(parser, args)
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
    pass
