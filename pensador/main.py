import requests
from bs4 import BeautifulSoup

class Pensador:
    def __init__(self, url=""):
        if url:
            self.updateReq(url)
    
    def updateReq(self, url):
        self.req = requests.get(url)
        self.soup = BeautifulSoup(self.req.text, 'html.parser')
        
    def getAuthorPages(self, authorURL):
        page = 1
        frases_obtidas = []
        while True:
            #Fazendo requisição para a página:
            self.updateReq(f"{authorURL}{page}/")
            
            #Pegando qual o limite de frases dessa página
            print(f"Passando pela página {page}")
            description = self.soup.find("div", {"class": "description"})
            rangeFrases = description.find_all("strong")[0]
            totalFrases = description.find_all("strong")[1]
            rangeFrases = rangeFrases.text.split("-")[1].strip()
            if rangeFrases == totalFrases.text:
                break
            
            #Pegando frases da página:
            frases_obtidas.append(self.__getAutorPhrasis(f"{authorURL}{page}/"))
            page += 1
        
        return frases_obtidas
            
            
        
    
    def __getAutorPhrasis(self, authorURL):
        self.updateReq(authorURL)
        frases_obtidas = []
        frases = self.soup.find_all("p", {"class": "frase"})
        for frase in frases:
            frases_obtidas.append(frase.text)
            
        return frases_obtidas
            
if __name__ == "__main__":
    starter = Pensador()
    print(starter.getAuthorPages("https://www.pensador.com/autor/platao/"))
    