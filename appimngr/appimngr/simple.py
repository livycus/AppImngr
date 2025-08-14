"""Module intended for internal functions"""

import configparser
import io
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

import settings
from InquirerPy import inquirer

# lists


def listall():
    """Function that lists all available AppImages"""
    imgs_path = f"{settings.path}/AppImages"
    all_imgs = os.listdir(imgs_path)
    for img in all_imgs:
        print(img)
    return all_imgs


def listinstalled():
    """Function that lists all installed AppImages"""
    installed_path = f"{settings.homepath}/.local/share/applications-appimngr"
    installed_imgs = os.listdir(installed_path)
    for img in installed_imgs:
        print(img)
    return installed_imgs


def listnew():
    """Function that lists all yet to be installed AppImages"""
    all_imgs = silentcheck(listall)
    installed_imgs = silentcheck(listinstalled)
    all_imgs_norm = {normalize(item): item for item in all_imgs}
    installed_imgs_norm = {normalize(item): item for item in installed_imgs}
    real_imgs = []
    for img in all_imgs_norm:
        if img not in installed_imgs_norm:
            real_imgs.append(all_imgs_norm[img])
            print(all_imgs_norm[img])
    return real_imgs


# internal utils


def picker(choices_func, msg):
    """Picker function"""
    try:
        choices = silentcheck(choices_func)
        if not choices:
            print("No items to select.")
            return
        selected = inquirer.select(
            message=msg, choices=choices, default=choices[0]
        ).execute()
        print(f"{selected} selected.")
        return selected
    except KeyboardInterrupt:
        print("Exiting gracefully...")


def silentcheck(func):
    """Function intended to call other functions silently"""
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        var = func()
    finally:
        sys.stdout = old_stdout
    return var


def normalize(namecheck):
    """Function to normalize file names for list matching"""
    namecheck = namecheck.lower()
    if namecheck.endswith(".appimage"):
        namecheck = namecheck[:-9]
    if namecheck.endswith(".desktop"):
        namecheck = namecheck[:-8]
    return namecheck


def installpath(install_name):
    """Function intended for creating temporary install path in /tmp"""
    install_path = Path("/tmp/appimngr") / install_name
    if install_path.exists():
        shutil.rmtree(install_path)
    install_path.mkdir(parents=True, exist_ok=True)
    print(f"Created install path: '{install_path}'")
    return install_path


def extractimg(img2ext, ext_dir):
    """Function that extracts AppImage to temporary install path in /tmp"""
    img_path = f"{settings.path}/AppImages/{img2ext}"
    print(f"Extracting {img_path} ...")
    st = os.stat(img_path)
    if not st.st_mode & stat.S_IXUSR:
        os.chmod(img_path, st.st_mode | stat.S_IXUSR)
    working_dir = f"{settings.path}"
    subprocess.run(
        [str(img_path), "--appimage-extract"], cwd=str(working_dir), check=True
    )
    extracted_dir = f"{settings.path}/squashfs-root"
    shutil.move(str(extracted_dir), str(ext_dir))
    print(f"Contents extracted to {ext_dir}")
    return ext_dir


def config_rw(file, path, op, new_arg, values=None):
    """Function for reading and writing *.desktop config files"""
    config = configparser.ConfigParser(interpolation=None, strict=False)
    config.optionxform = str
    section = "Desktop Entry"
    if op == "read":
        if path == settings.apps_main:
            r_file = path / file
        else:
            r_file = next(path.rglob("*desktop"), None)
            if not r_file:
                print("No *.desktop file found. Aborting...")
                return None
        print(f"Fetching data from {r_file}...")
        config.read(r_file, encoding="utf-8")
        app_name = config[section].get("Name", None)
        app_icon = config[section].get("Icon", None)
        app_exec = config[section].get("Exec", None)
        print(f"Finished fetching data from {r_file}.")
        return {"app_name": app_name, "app_icon": app_icon, "app_exec": app_exec}
    if op == "write":
        if not values:
            print("No values to write. Aborting...")
            return
        app_name = values["app_name"]
        app_icon = values["app_icon"]
        app_exec = values["app_exec"]
        w_file = f"{path}/{file}"
        if not os.path.isfile(w_file):
            print("No *.desktop file to write to. Aborting...")
            return None
        print(f"Writing data to {w_file}...")
        config.read(w_file, encoding="utf-8")
        config[section]["Name"] = app_name
        config[section]["Icon"] = app_icon
        config[section]["Exec"] = new_arg
        with open(w_file, "w", encoding="utf-8") as f:
            config.write(f)
            print(f"Finished writing data to {w_file}.")


def rw_info(install_path, file, new_arg):
    """Function that fetches information needed for installation and creates *.desktop entry"""
    desktop_file = next(install_path.rglob("*desktop"), None)
    read_values = config_rw(desktop_file, install_path, "read", None)
    filename_desktop = file[:-9] + ".desktop"
    made_file = f"{settings.apps_main}/{filename_desktop}"
    shutil.copy(settings.example_file, made_file)
    config_rw(
        filename_desktop, settings.apps_main, "write", new_arg, values=read_values
    )
    read_values.update(
        {
            "desktop_file": desktop_file,
            "made_file": made_file,
            "filename_desktop": filename_desktop,
        }
    )
    return read_values


def link_desktop(values=None):
    """Function that creates a linked desktop entry that DE's can read"""
    if not values:
        print("No desktop files found to link. Aborting...")
        return
    made_file = values["made_file"]
    filename_desktop = values["filename_desktop"]
    linked_file = f"{settings.apps_linked}/{filename_desktop}"
    print(f"Linking {linked_file} to {made_file}")
    files_in_apps_linked = os.listdir(settings.apps_linked)
    if filename_desktop in files_in_apps_linked:
        subprocess.run(["rm", linked_file], check=False)
    subprocess.run(["ln", "-s", made_file, linked_file], check=False)
    files_in_apps_linked_new = os.listdir(settings.apps_linked)
    if filename_desktop in files_in_apps_linked_new:
        print(f"Linked {linked_file} to {made_file}.")
        return
    else:
        print(f"Failed linking {linked_file} to {made_file}")


def copy_icons(install_path, values=None):
    """Function that copies AppImages icons to ~/.local/share/icons"""
    print("Copying icons...")
    if not values:
        print("No icon information found. Aborting...")
        return
    app_icon = values["app_icon"]
    if app_icon.endswith(".svg") or app_icon.endswith(".png"):
        icon_location = next(install_path.rglob(app_icon), None)
        shutil.copy(icon_location, settings.icons_dir)
    else:
        icon_svg = next(install_path.rglob(f"{app_icon}.svg"), None)
        if not icon_svg:
            icon_png = next(install_path.rglob(f"{app_icon}.png"), None)
            if not icon_png:
                print("No icon file found. Aborting...")
                return None
            shutil.copy(icon_png, settings.icons_dir)
        shutil.copy(icon_svg, settings.icons_dir)
    print("Finished copying icons.")


def makebin(new_arg, values=None):
    """Function that creates bin entries for usage through system terminal"""
    print("Preparing bin file...")
    if not values:
        print("No information found to build bin file. Aborting...")
        return
    app_name = values["app_name"]
    try:
        name_norm = normalize(app_name)
        name_norm_spaceless = name_norm.replace(" ", "-")
        bin_example = f"{settings.path}/appimngr/bin"
        bin_made = f"/usr/local/bin/{name_norm_spaceless}"
        bin_cmd = f"sudo cp -a '{bin_example}' '{bin_made}' && sudo sh -c 'echo \"{new_arg}\" >> \"{bin_made}\"'"
        subprocess.run(bin_cmd, shell=True, check=True)
        print(
            f"Bin entry created, you may now open the appimage by running {name_norm_spaceless} in the terminal."
        )
    except subprocess.CalledProcessError as e:
        print(f"Failed making bin file with return code {e.returncode}.")
        return


def removeicon(icon_path):
    """Function that removes icon added by installation"""
    print("Removing icon...")
    if icon_path.endswith(".svg") or icon_path.endswith(".png"):
        os.remove(icon_path)
    else:
        icon_svg = Path(f"{icon_path}.svg")
        if not icon_svg.exists():
            icon_png = Path(f"{icon_path}.png")
            if not icon_png.exists():
                print("No icon file found. Proceeding with other files...")
                return None
            os.remove(icon_png)
        os.remove(icon_svg)
    print("Finished removing icon.")


def yesorno(prompt):
    """Simple yes or no function"""
    while True:
        response = input(prompt).strip().lower()
        if response in ("y", "n"):
            return response


def removebin(app_name):
    """Function that removes bin entry added by installation"""
    app_name_norm = normalize(app_name)
    bin_name = app_name_norm.replace(" ", "-")
    bin_file = settings.bin_path / bin_name
    print(f"Removing {bin_file}...")
    remove_bin_cmd = f"sudo rm '{bin_file}'"
    subprocess.run(remove_bin_cmd, shell=True, check=False)
    print("Finished removing bin entry")


def safeosremove(file):
    """Function that runs os.remove(file) while avoiding crashes"""
    try:
        os.remove(file)
    except FileNotFoundError:
        print(f"{file} does not exist.")
    except PermissionError:
        print(f"No permission to delete {file}.")
    except OSError as e:
        print(f"Other error: {e}")


# cores


def installcore(file):
    """Function that combines all background installation elements"""
    install_path = installpath(file)
    extractimg(file, install_path)
    new_arg = f"{settings.path}/AppImages/{file}"
    read_values = rw_info(install_path, file, new_arg)
    link_desktop(values=read_values)
    copy_icons(install_path, values=read_values)
    makebin(new_arg, values=read_values)


def uninstallcore(file):
    """Function that combines all background uninstallation elements"""
    desktop_entry = settings.apps_main / file
    link_file = settings.apps_linked / file
    print(f"Fetching data from {desktop_entry}...")
    read_values = config_rw(file, settings.apps_main, "read", None, None)
    if read_values:
        app_name = read_values["app_name"]
        app_icon = read_values["app_icon"]
        app_exec = read_values["app_exec"]
        print(f"Successfully fetched data.")
    else:
        print(f"Failed to fetch data from {desktop_entry}. Aborting...")
        return
    print(f"Removing {desktop_entry}...")
    safeosremove(desktop_entry)
    print(f"{desktop_entry} removed proceeding to remove {link_file}...")
    safeosremove(link_file)
    icon_path = f"{settings.icons_dir}/{app_icon}"
    removeicon(icon_path)
    removebin(app_name)
    print(f"Corresponding *.AppImage file is:\n{app_exec}")
    response = yesorno("Do you wish to remove it? (y/n): ")
    if response == "y":
        print("Removing *.AppImage file...")
        safeosremove(app_exec)
        return


# debug


def testpath():
    """Debug function to test paths"""
    print(settings.path)
