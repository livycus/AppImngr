"""Module housing the terminal"""

import readline

import settings
from composite import *
from simple import *

print("Welcome to AppImngr!\n\nType 'help' to list all options\n ")


def help():
    """Function that lists commands"""
    help_file = f"{settings.path}/appimngr/help.txt"
    with open(help_file, "r", encoding="utf-8") as file:
        contents = file.read()

    print(contents)


def version():
    """Function that outputs version of AppImngr"""
    print(settings.VER)


ver = version


USER_COMMANDS = [
    "install",
    "installall",
    "reinstall",
    "reinstallall",
    "uninstall",
    "uninstallall",
    "clean",
    "listnew",
    "listall",
    "listinstalled",
]


def completer(text, state):
    """Terminal autocompleter"""
    options = [cmd for cmd in USER_COMMANDS if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    return None


readline.set_completer(completer)
readline.parse_and_bind("tab: complete")


def terminal():
    """Terminal"""
    try:
        while True:
            try:
                cmnd = input("- ")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            if cmnd.lower() == "exit":
                break
            try:
                print("")
                func = globals()[cmnd]
                func()
                print("")
            except KeyError:
                print(
                    f"No function named '{cmnd}' exists.\nType 'help' to list all functions.\n"
                )
            except TypeError:
                print(f"'{cmnd}' is not callable.\n")
    except KeyboardInterrupt:
        print("\nExiting...")


terminal()
