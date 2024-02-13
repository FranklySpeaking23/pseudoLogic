#imports
import requests
from bs4 import BeautifulSoup
from time import sleep
from colorama import Fore, Style

print(f"{Fore.RED}[Checking updates]{Style.RESET_ALL}")
try:
    #load the webpage with the newest version number
    url = "https://raw.githubusercontent.com/FranklySpeaking23/pseudoLogic/main/version.txt?token=GHSAT0AAAAAACNNTZMMU63BBG2EHU4YTIPCZNWB4FA"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    #extracting the version from the webpage
    version = doc.text.strip("\n")

    #reading the currently installed version
    with open("version.txt", "r") as file:
        cur_version = file.read().split("\n")[0]

    #showing information about the new version --> if there is a new one
    if str(cur_version) != str(version):
        print("Er is een nieuwe versie van de software beschikbaar!")
        print(f"Deze nieuwe versie is {version}")
        print("Je kan hem downloaden op https://github.com/FranklySpeaking23/pseudoLogic/tree/main")
        sleep(3)
except:
    print("Kijken voor nieuwe versie mislukt.")
    sleep(3)

print(f"{Fore.GREEN}[Checking updates]{Style.RESET_ALL}")