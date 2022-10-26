#!/usr/bin/env python
"""
Application shell command manager
"""
import argparse
import asyncio

from loguru import logger

from user.models import UserDBModel

event_loop = asyncio.get_event_loop()


def handle_create_user(args: argparse.Namespace):
    """Handler to create a new User"""
    user = event_loop.run_until_complete(UserDBModel.get(email=args.email))
    if user:
        logger.error(f"The user {user} already exists")
        return 

    roles = [role.strip() for role in args.roles.split(",")]
    payload = {
        "email": args.email,
        "password": args.password,
        "fullname": args.fullname,
        "roles": roles
    }
    user = event_loop.run_until_complete(UserDBModel.create(payload))
    logger.info(f"User {user} is created with payload")
    logger.info(payload)


def handle_get_user(args: argparse.Namespace):
    user = event_loop.run_until_complete(UserDBModel.get(email=args.email))
    logger.info(f"User requested is: {user}")


def handle_delete_all_users(args: argparse.Namespace):
    deleted = event_loop.run_until_complete(UserDBModel.delete_all())
    logger.info(f"Number of users deleted: {deleted}")

def handle_delete_user(args: argparse.Namespace):
    user = event_loop.run_until_complete(UserDBModel.get(email=args.email))
    if not user:
        logger.error(f"User with email {args.email} is not found")
        return
    event_loop.run_until_complete(user.delete())
    logger.info(f"User is {user} has been deleted")


command_handler_dict = {
    "createuser": handle_create_user,
    "getuser": handle_get_user,
    "deleteallusers": handle_delete_all_users,
    "deleteuser": handle_delete_user,
}

if __name__ == '__main__':
    main_parser = argparse.ArgumentParser(description='Applicaiton shell command manager.')
    subparser = main_parser.add_subparsers(help='commands', dest="command")

    createuser_parser = subparser.add_parser("createuser")
    createuser_parser.add_argument("--email", help="New user email")
    createuser_parser.add_argument("--pass", dest="password", help="New user raw password")
    createuser_parser.add_argument("--fullname", dest="fullname", help="New user full name (First N., Second N.)")
    createuser_parser.add_argument("--roles", dest="roles", help="New user roles", default="")

    getuser_parser = subparser.add_parser("getuser")
    getuser_parser.add_argument("--email", help="User email")

    delete_all_users_parser = subparser.add_parser("deleteallusers")

    delete_user_parser = subparser.add_parser("deleteuser")
    delete_user_parser.add_argument("--email", help="User email to delete it by")

    main_args = main_parser.parse_args()

    command = main_args.command
    handler = command_handler_dict.get(command)
    if not handler:
        logger.error("Command is not supported")
    else:
        handler(main_args)
