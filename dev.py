from colorama import Fore, Style
from json import load

def log(tekst, type = "default"):
    if SETTINGS["window"]["logs"]:
        match type:
            case "default":
                print(tekst)
            case "log":
                print(f"{Fore.YELLOW}- {tekst} -{Style.RESET_ALL}")
            case "func-s":
                print(f"{Fore.RED}[{tekst}]{Style.RESET_ALL}")
            case "func-e":
                print(f"{Fore.GREEN}[{tekst}]{Style.RESET_ALL}")

def load_settings():
    with open("settings.json", "r") as file:
        settings = load(file)
    return settings

SETTINGS = load_settings()