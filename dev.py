from colorama import Fore, Style

def log(tekst, type = "default"):
    if True:
        match type:
            case "default":
                print(tekst)
            case "log":
                print(f"{Fore.YELLOW}- {tekst} -{Style.RESET_ALL}")
            case "func-s":
                print(f"{Fore.RED}[{tekst}]{Style.RESET_ALL}")
            case "func-e":
                print(f"{Fore.GREEN}[{tekst}]{Style.RESET_ALL}")
