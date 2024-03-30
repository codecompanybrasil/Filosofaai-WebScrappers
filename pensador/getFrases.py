import requests
import random
from bs4 import BeautifulSoup


class RandomFrases:

    def __init__(self, url):
        self.req = requests.get(url)
        self.soup = BeautifulSoup(self.req.text, 'html.parser')

    def getFrases(self):
        frases = []

        cards = self.soup.find_all("div", {"class": "thought-card"})

        for card in cards:
            frase = card.find("p")
            author = card.find("span", {"class": "author-name"})
            
            frases.append({
                "frase": str(frase.get_text()),
                "author": str(author.get_text())
            })

        return frases

    def montingQuery(self, frases):
        querys = []
        
        for frase in frases:
            query = f"INSERT INTO motivational_message (message, author, day) VALUES ('\"{frase['frase']}\"', '{frase['author']}', NOW());"
            querys.append(query)
            
        return querys
    
    def creatingSQLFile(self, querys):
        random.shuffle(querys)
        
        with open("frases.sql", "a+") as f:
            for query in querys:
                f.write(str(query) + "\n\n")


if __name__ == "__main__":
    for i in range(0, 5):
        starter = RandomFrases(f"https://www.pensador.com/frases_de_saudades/{i}/")
        frases = starter.getFrases()
        print(frases)
        query = starter.montingQuery(frases)
        starter.creatingSQLFile(query)
