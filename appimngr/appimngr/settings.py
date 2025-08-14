"""Module intended for information that might need to be quickly modified"""

import os
from pathlib import Path

VER = "Version 0.1"

homepath = Path(os.path.expanduser("~"))

share_path = Path(f"{homepath}/.local/share")

path = Path(f"{share_path}/appimngr")

main_path = Path(f"{path}/appimngr")

example_file = Path(f"{main_path}/example.desktop")

apps_main = Path(f"{share_path}/applications-appimngr")

apps_linked = Path(f"{share_path}/applications")

icons_dir = Path(f"{share_path}/icons")

bin_path = Path("/usr/local/bin")
