# AppImngr

AppImngr a lightweight AppImages manager.

[![PGP](https://apps.kde.org/app-icons/org.kde.kleopatra.svg)](https://github.com/livycus/PGP)

*Verify PGP signed arhive version found under releases of this software by importing my public key above with kleopatra or similar software then running 'gpg --verify /path/to/AppImngr.tar.gz.sig /path/to/AppImngr.tar.gz'*

## Description

AppImngr is a command-line tool intended for managing of AppImages written in python. Currently it allows for basic operations such as installing/uninstalling AppImages by creating/removing appropriate desktop entries, icons, menu entries, ...

## Requirements

Python3 (Tested with v3.11.2)

InquirerPy ( - pip install InquirerPy )

*This software was written and tested on Debian 12 (KDE Plasma 5.27.5) and may require installing additional dependencies on different distributions.*

*Currently also tested to work on: Debian 13 (KDE Plasma 6.3.6)*

## Setup and usage

### Setup

To install AppImngr run:

```
git clone https://github.com/livycus/AppImngr

cd AppImngr

sudo chmod +x ./install.sh

sudo ./install.sh
```
*Disclaimer: If a folder ~/AppImages already exists on the system it should be backed up to a different location or the installation script will remove it. This is necessary to prevent recursion with symlink.*

After installation cloned folder can be removed since all necessary files will be copied to proper directories. Too uninstall AppImngr run:

```
cd ~/.local/share/appimngr

sudo ./uninstall.sh
```

This will remove AppImngr and all related files.

### Usage

- To launch the application either run 'appimngr' as user (without sudo) in the terminal of your choosing or run it with it's desktop entry under Utilities category.
*Desktop entry will run AppImngr in default terminal emulator to change the terminal either set a different default terminal or edit Exec line and set Terminal to false.*

- Running 'help' while in the application environment will list all available commands.

- After installing a /home/user/AppImages" directory with symlink to /home/user/.local/share/appimngr/AppImages will appear, to make AppImage files visible to AppImngr they must be in the latter directory (they must also remain there after to be accessible by their desktop entries). The AppImages folder (/home/user/AppImages) may be moved around without breaking the link.

- Recommended is to run 'installall' after moving AppImage file(s) into AppImages directory and to run uninstall for removing specific apps.

- AppImngr follows GNU Readline conventions.

- Installing and uninstalling prompts for sudo password due to permission requirements to /usr/local/bin directory.

- If AppImage file(s) were removed before uninstalling run 'clean' to remove associated files created by this software.

- Installed AppImages may be runned through their desktop entries or by typing lowercase application names in the terminal (if application name contains " " it is replaced by "-" for terminal use).

## License

GNU GENERAL PUBLIC LICENSE

Version 3, 29 June 2007

Copyright (C) 2025 livycus

Licensed under the GNU GPL v3. See LICENSE file or https://www.gnu.org/licenses/gpl-3.0.txt or https://opensource.org/license/gpl-3-0.
