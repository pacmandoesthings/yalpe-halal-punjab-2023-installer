#!/usr/bin/env python3
import os
import subprocess
import time
try:
    from colorama import Fore, Back, init
except:
    os.system("python3 -m pip install colorama")
    print("Rerun script please.")
    exit(1)

"""
made by pacmandev
"""


class WackyLogging:
    @staticmethod
    def Info(text):
        print(f"{Back.LIGHTBLUE_EX}{Fore.WHITE} INFO {Back.RESET}{Fore.RESET} {text}")

    @staticmethod
    def Input():
        output = input(f"{Back.CYAN}{Fore.WHITE} INPUT {Back.RESET}{Fore.RESET} ")
        return output

    @staticmethod
    def Success(text):
        print(f"{Back.GREEN}{Fore.WHITE} SUCCESS {Back.RESET}{Fore.RESET} {text}")

    @staticmethod
    def Error(text):
        print(f"{Back.RED}{Fore.WHITE} ERROR {Back.RESET}{Fore.RESET} {text}")

    @staticmethod
    def Warn(text):
        # let the intrusive thoughts in, make it say "warm"
        print(f"{Back.YELLOW}{Fore.WHITE} WARN {Back.RESET}{Fore.RESET} {text}")

def main():
    init(autoreset=True)  # Initialize colorama

    if os.popen('lsb_release -si').read().strip() == "Ubuntu":
        WackyLogging.Error("This script does not work on Ubuntu. Switch to Debian or anything Arch-based, for the love of god.")
        exit(1)

    linux_username = os.getlogin()
    desktop_file = os.path.expanduser("~/.local/share/applications/yalpwithnewinstaller.desktop")

    # Dep check
    try:
        subprocess.check_call(["wine64", "--version"])
    except subprocess.CalledProcessError:
        WackyLogging.Error("Looks like you don't have wine installed.")
        WackyLogging.Error("Please install it with your distribution's package manager.")
        exit(1)

    try:
        subprocess.check_call(["curl", "--version"])
    except subprocess.CalledProcessError:
        WackyLogging.Error("Looks like you don't have curl installed.")
        WackyLogging.Error("Please install it with your distribution's package manager.")
        exit(1)

    if linux_username == "root":
        WackyLogging.Error("Please don't run the script as root.")
        exit(1)

    os.system("clear")
    WackyLogging.Info("Welcome to the Yalp Linux Manager!")

    # Prompt
    WackyLogging.Info("Choose an option:")
    WackyLogging.Info("[1] Install Yalp")
    WackyLogging.Info("[2] Remove Yalp")
    WackyLogging.Info("[3] Exit")
    choice = WackyLogging.Input()

    if choice.lower() == "1":
        os.system("clear")
        WackyLogging.Info("Installing Yalp...")

        # Installer: Wine
        yalp_dir = os.path.expanduser("~/.thatisallweareyalpers/")
        os.makedirs(yalp_dir, exist_ok=True)
        os.chdir(yalp_dir)
        os.system("curl https://cdn.discordapp.com/attachments/1152330589735759972/1157955824635891812/installer.exe -o installer.exe")
        os.system("WINEDEBUG=-all wine64 installer.exe")
        WackyLogging.Info("Now installing URI...")

        # Installer: URI
        if not os.path.isfile(desktop_file):
            with open(desktop_file, "w") as desktop_file_handle:
                desktop_file_handle.write(f"""[Desktop Entry]
Name=Yalp
Exec={yalp_dir}bootstrap.sh %u
Type=Application
MimeType=x-scheme-handler/yalp;
NoDisplay=true""")

            with open(desktop_file, "r+") as desktop_file_handle:
                content = desktop_file_handle.read()
                content = content.replace(f"/home/{linux_username}/", f"/home/{linux_username}/")
                desktop_file_handle.seek(0)
                desktop_file_handle.write(content)

            os.system(f"xdg-mime default {desktop_file} x-scheme-handler/yalp")
            os.chdir(yalp_dir)
        else:
            WackyLogging.Info("Desktop file already exists. Skipping creation.")

        # Rest of the script...
        middleman_script = os.path.join(yalp_dir, "bootstrap.sh")
        with open(middleman_script, "w") as script_file:
            script_file.write('''#!/usr/bin/env bash

if [[ "$1" == "yalp:"* ]]; then
    ref="$1"

    WINEDEBUG=-all wine64 ~/.wine/drive_c/users/'''+linux_username+'''/AppData/Roaming/YalpVersions/Yalp.exe "$ref"
else
    echo "what happened? contact pacmandev on discord for help"
fi''')
        os.chmod(middleman_script, 0o755)
        os.system(f"xdg-mime default yalpwithnewinstaller.desktop x-scheme-handler/yalp")

        WackyLogging.Success("Yalp installed successfully! Verify this by attempting to join a game.")
    elif choice == "2":
        WackyLogging.Error("I'm too lazy to add that.")
        exit(0)
    else:
        os.system("clear")
        WackyLogging.Info("Exiting")
        exit(1)

    WackyLogging.Info("Exiting...")

if __name__ == "__main__":
    main()
