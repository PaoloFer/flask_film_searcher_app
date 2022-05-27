"""
In questo modulo ho scritto tutte le funzioni necessarie (credo) per ottenere i dati dal sito e per poterli poi manipolare nel mio sito.
"""

import bs4
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests
from flask import request
import concurrent.futures
class Scraping:
    def __init__(self):
        self.MOST_POPULAR = "https://www.imdb.com/what-to-watch/popular/?ref_=watch_tpks_tab"
        self.HOME = "https://www.imdb.com"

        self.response = requests.get(self.MOST_POPULAR)
        self.response.raise_for_status() #genera una risposta se la response è in stato di errore

        self.soup = bs4.BeautifulSoup(self.response.text, "html.parser")#estraiamo il codice della pagina html e la salviamo nella variabile soup


    def PosterImage(self):
        """
        Questo metodo restituisce l'array con tutte i riferimenti alla immagini in quanto le immagini sono presenti nella td --> posterColumn
        """
        td = self.soup.find_all("td", class_="posterColumn")
        return td

    def GetData(self):
        """
        Questo metodo aggiunge al file data_file.txt i 100 elementi messi dal sito 
        """
        data1 = open("txtdata/data_film_title.txt","a")
        data2 = open("txtdata/data_img.txt","a")
        data3 = open("txtdata/data_film_link.txt","a")



        response = requests.get("https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm")
        response.raise_for_status() #genera una risposta se la response è in stato di errore

        soup = bs4.BeautifulSoup(response.text, "html.parser")
        #get all the <td> element with the class --> titleColumn from the page 
        find = soup.find_all("td",{"class":"posterColumn"})

        for element in find:

            #get title
            title = element.a.img["alt"] #comando contents restituisce il contenuto di testo del tag 
            #get link
            link = element.a["href"]
            
            #get image
            img=element.a.img["src"]
            #vado a manipolare il link dell'immagine in quanto al suo interno è presente una porzione che ridimensiona l'immagini più piccola ma io la volgio originale
            if "@." in img:
                data2.write(img[:img.find("@.")+2]+"jpg\n")
            else:
                data2.write(img[:img.find(".",34)]+".jpg\n")

            data1.write(title+"\n")
            data3.write(self.HOME+link+"\n")
            

    
    def FindImage(self,link):
        """
        Questo metodo si occupa di prendere la cover del film dalla singola pagina
        -cose da fare per evitare di fare migliaia di request o utilizzare il multithread per velocizzare il tutto o non caricare le immagini
        """
        #//Part_1 of FindImage//
        data2= open("txtdata/data_img.txt","a")
        #create the new link adding the HOME to it and then send a request at that URL to get the page we want
        NewLink=self.HOME+link
        response=requests.get(NewLink)


        soup = bs4.BeautifulSoup(response.text, "html.parser")

        #sotre all the element with <a> tat and the class --> ipc-lockup-overlay ipc-focusable(findall return an array) and then take the first element of the array(is the onlyone, but i want to have an array to have an easier access to the information)
        datas = soup.find_all("a",{"class":"ipc-lockup-overlay ipc-focusable"})
        ImgLink = datas[0]["href"]

        
        #//Part_2 of FindImage//

        #from the link i have just got i send a request to get the page and then get the image from that page
        response2 =  requests.get(self.HOME+ImgLink)

        soup2 = bs4.BeautifulSoup(response2.text, "html.parser")

        datas2= soup2.find_all("img", {"class" : "sc-7c0a9e7c-0 hXPlvk"})
        #image link that i can use in my website
        CoverLink = datas2[0]["src"]
        data2.write(CoverLink+"\n")
        return 

    def FindImage2(self,link):
        #//Part_1 of FindImage//

        #create the new link adding the HOME to it and then send a request at that URL to get the page we want
        NewLink=self.HOME+link
        response=requests.get(NewLink)


        soup = bs4.BeautifulSoup(response.text, "html.parser")

        #sotre all the element with <a> tat and the class --> ipc-lockup-overlay ipc-focusable(findall return an array) and then take the first element of the array(is the onlyone, but i want to have an array to have an easier access to the information)
        datas = soup.find_all("a",{"class":"ipc-lockup-overlay ipc-focusable"})
        ImgLink = datas[0]["href"]

        
        #//Part_2 of FindImage//

        #from the link i have just got i send a request to get the page and then get the image from that page
        response2 =  requests.get(self.HOME+ImgLink)

        soup2 = bs4.BeautifulSoup(response2.text, "html.parser")

        datas2= soup2.find_all("img", {"class" : "sc-7c0a9e7c-0 hXPlvk"})
        #image link that i can use in my website
        CoverLink = datas2[0]["src"]
        
        return CoverLink 
    def GetImage(self,link):
        if "@." in link:
            return(link[:link.find("@.")+2]+"jpg")
        else:
            return(link[:link.find(".",34)]+".jpg")





    def SearchData(self,word):
        """
        Questo metodo cerca dalla barra di ricerca il nome dato dall'utente per poi restituire il risultato
        """
        if word is None:
            word=""
        if " " in word:
            word = word.replace(" ","+")
        string=f"https://www.imdb.com/find?q={word}&ref_=nv_sr_sm"
        response = requests.get(string)
        response.raise_for_status() #genera una risposta se la response è in stato di errore

        soup = bs4.BeautifulSoup(response.text, "html.parser")
        datas = soup.find("div",{"class":"findSection"})
        data = datas.find_all("td",{"class":"primary_photo"})
        title = datas.find_all("td",{"class":"result_text"})
        output=[]

        for element in data:
            image=element.a.img["src"]

            output.append([image])

        for element in range(0,len(title)):
            output[element].append(title[element].text)
            output[element].append(self.HOME+title[element].a["href"])            
        return output



    


if __name__ == "__main__":
    web = Scraping()