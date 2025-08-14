#!/bin/bash

echo "Uninstalling AppImngr..."

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run with sudo."
    echo "Please run it like this: sudo $0"
    exit 1
fi

echo "Removing files..."

rm /usr/local/bin/appimngr

rm "$(eval echo ~${SUDO_USER:-$USER})/.local/share/icons/appimngr.svg"

rm "$(eval echo ~${SUDO_USER:-$USER})/.local/share/applications/AppImngr.desktop"

rm -r "$(eval echo ~${SUDO_USER:-$USER})/.local/share/applications-appimngr"

rm /etc/xdg/menus/applications-merged/appimage.menu

rm "$(eval echo ~${SUDO_USER:-$USER})/.local/share/desktop-directories/AppImages.directory"

rm -rf "$(eval echo ~${SUDO_USER:-$USER})/.local/share/appimngr"

echo "AppImngr Uninstalled!"
