#!/bin/bash

echo "Installing AppImngr..."

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run with sudo."
    echo "Please run it like this: sudo $0"
    exit 1
fi

echo "Making directories and copying files..."

# bin

chown root:root ./bin/appimngr
chmod 755 ./bin/appimngr
cp ./bin/appimngr /usr/local/bin

# app files

rm ./appimngr/AppImages/blank
chmod +x ./appimngr/uninstall.sh
chmod +x ./appimngr/appimngr/bin
cp -a ./appimngr "$(eval echo ~${SUDO_USER:-$USER})/.local/share/"
rm -rf "$(eval echo ~${SUDO_USER:-$USER})/AppImages"
ln -s "$(eval echo ~${SUDO_USER:-$USER})/.local/share/appimngr/AppImages" "$(eval echo ~${SUDO_USER:-$USER})/AppImages"

# menu

mkdir -p /etc/xdg/menus/applications-merged
cp appimage.menu /etc/xdg/menus/applications-merged

mkdir -p "$(eval echo ~${SUDO_USER:-$USER})/.local/share/desktop-directories"
cp AppImages.directory "$(eval echo ~${SUDO_USER:-$USER})/.local/share/desktop-directories"

# icons

cp -a appimngr.svg "$(eval echo ~${SUDO_USER:-$USER})/.local/share/icons"

# desktop entry

chown "${SUDO_USER:-$USER}:${SUDO_USER:-$USER}" AppImngr.desktop
chmod +x AppImngr.desktop
mkdir -p "$(eval echo ~${SUDO_USER:-$USER})/.local/share/applications/"
chown 1000:1000 "$(eval echo ~${SUDO_USER:-$USER})/.local/share/applications/"
cp -a AppImngr.desktop "$(eval echo ~${SUDO_USER:-$USER})/.local/share/applications/"

# dir for desktop entries

mkdir -p "$(eval echo ~${SUDO_USER:-$USER})/.local/share/applications-appimngr"
chown 1000:1000 "$(eval echo ~${SUDO_USER:-$USER})/.local/share/applications-appimngr"

echo "AppImngr Installed!"
