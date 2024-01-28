import requests
from bs4 import BeautifulSoup
from time import sleep

try:
    url = "https://raw.githubusercontent.com/FranklySpeaking23/pseudoLogic/main/version.txt?token=GHSAT0AAAAAACNNTZMMU63BBG2EHU4YTIPCZNWB4FA"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    version = doc.text


    with open("version.txt", "r") as file:
        cur_version = file.read().split("\n")[0]

    if str(cur_version) != str(version):
        print("Er is een nieuwe versie van de software beschikbaar!")
        print(f"Deze nieuwe versie is {version}")
        print("Je kan hem downloaden op https://github.com/FranklySpeaking23/pseudoLogic/tree/main")
    else:
        print("Er is geen nieuwe versie beschikbaar")
except:
    print("Kijken voor nieuwe versie mislukt.")
sleep(3)
