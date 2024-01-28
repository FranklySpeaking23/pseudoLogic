import requests
from bs4 import BeautifulSoup
from time import sleep

try:
    url = "https://sqfdsqfd.itch.io/pseudologic?secret=oUckP4kdtgDYoeEodtId4STw5M"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    text = doc.find("div", class_="columns")
    print(text)

    text = text.find_all("p")

    version = text[-1].text.split(":")[1].strip(" ")

    with open("version.txt", "r") as file:
        cur_version = file.read().split("\n")[0]

    if str(cur_version) != str(version):
        print("Er is een nieuwe versie van de software beschikbaar!")
        print(f"Deze nieuwe versie is {version}")
        print("Je kan hem downloaden op itch.io/sqfdsqfd.")
except:
    print("Kijken voor nieuwe versie mislukt.")
sleep(3)