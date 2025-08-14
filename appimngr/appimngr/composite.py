"""Module intended for composite functions called through main.py"""

import configparser
import io
import os
import subprocess
from pathlib import Path

import settings
from simple import *

# install


def install():
    """Function that runs installer"""
    try:
        picked_file = picker(listnew, "Select AppImage you wish to install: ")
        if not picked_file:
            print("Returning...")
            return
        print(f"Installing {picked_file}...")
        installcore(picked_file)
        print(f"Finished installing {picked_file}.")
        subprocess.run(
            [
                "update-desktop-database",
                f"{settings.homepath}/.local/share/applications",
            ],
            check=False,
        )
    except KeyboardInterrupt:
        return


def installall():
    """Function that runs autoinstaller on all new files"""
    print("Proceeding to install the following AppImages:\n")
    new_imgs = listnew()
    print("\nInstalling...")
    for img in new_imgs:
        installcore(img)
    subprocess.run(
        ["update-desktop-database", f"{settings.homepath}/.local/share/applications"],
        check=False,
    )
    print("Done.")


# reinstall


def reinstall():
    """Function that runs reinstaller"""
    try:
        picked_file = picker(listall, "Select AppImage you wish to (re)install: ")
        if not picked_file:
            print("Returning...")
            return
        print(f"Installing {picked_file}...")
        installcore(picked_file)
        print(f"Finished installing {picked_file}.")
        subprocess.run(
            [
                "update-desktop-database",
                f"{settings.homepath}/.local/share/applications",
            ],
            check=False,
        )
    except KeyboardInterrupt:
        return


def reinstallall():
    """Function that runs autoreinstaller on all new files"""
    print("Proceeding to (re)install the following AppImages:\n")
    all_imgs = listall()
    print("\nInstalling...")
    for img in all_imgs:
        installcore(img)
    subprocess.run(
        ["update-desktop-database", f"{settings.homepath}/.local/share/applications"],
        check=False,
    )
    print("Done.")


# uninstall


def uninstall():
    """Function that runs uninstaller"""
    try:
        picked_file = picker(listinstalled, "Select AppImage you wish to uninstall: ")
        if not picked_file:
            print("Returning...")
            return
        print(f"Installing {picked_file}...")
        uninstallcore(picked_file)
        print(f"Finished uninstalling {picked_file}.")
        subprocess.run(
            [
                "update-desktop-database",
                f"{settings.homepath}/.local/share/applications",
            ],
            check=False,
        )
    except KeyboardInterrupt:
        return


def uninstallall():
    """Function that runs autouninstaller on all files"""
    print("Proceeding to uninstall the following apps:\n")
    installed_imgs = listinstalled()
    print("\nUninstalling...")
    for img in installed_imgs:
        uninstallcore(img)
    subprocess.run(
        ["update-desktop-database", f"{settings.homepath}/.local/share/applications"],
        check=False,
    )
    print("Done.")


def clean():
    """Function that runs cleaner"""
    print("Files to probe:\n")
    installed_imgs = listinstalled()
    print("\nProbing...")
    for img in installed_imgs:
        desktop_file = settings.apps_main / img
        read_values = config_rw(desktop_file, settings.apps_main, "read", None, None)
        if read_values:
            app_name = read_values["app_name"]
            app_icon = read_values["app_icon"]
            app_exec = read_values["app_exec"]
        else:
            print(f"Failed to probe {desktop_file}. Skipping")
            continue
        icon_path = f"{settings.icons_dir}/{app_icon}"
        link_file = settings.apps_linked / img
        appimg_path = Path(app_exec)
        if appimg_path.exists():
            print(f"{appimg_path} exists. Proceeding to next entry...")
            continue
        print(f"{appimg_path} does not exit. Removing {img} entry...")
        safeosremove(desktop_file)
        print("Removing linked desktop entry...")
        safeosremove(link_file)
        print("Removed linked entry.")
        removeicon(icon_path)
        removebin(app_name)
    subprocess.run(
        ["update-desktop-database", f"{settings.homepath}/.local/share/applications"],
        check=False,
    )
    print("Finished cleaning.")
