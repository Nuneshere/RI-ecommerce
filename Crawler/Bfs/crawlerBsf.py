# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import sys
import time
import pandas as pd
import requests as rq
import urllib.request
from urllib.parse import urljoin
import urllib.robotparser as urobot
import validators
import csv
import tldextract



links = [
    "https://www.damyller.com.br",
    "https://www.boutiquedassi.com.br",
    "https://www.cuticutibaby.com.br",
    "https://www.bluk.com.br",
    "https://www.lojavillevie.com.br",
    "https://www.achados96.com.br",
    "https://www.bellaseda.online",
    "https://www.gregory.com.br",
    "https://www.lojasexclusiva.com.br",
    "https://www.dwz.com.br"]


#gravar o csv final do link
def gravarCsv(array,dominio):
    print("gravando...")
    wtr = csv.writer(open (str(dominio)+".csv", 'w'), delimiter=',', lineterminator='\n')
    for link in array : wtr.writerow (link)

#gravar o csv final do custo

def gravarCusto(array):
    print("gravando loops...")
    with open("custos.csv","a") as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=',')
        csvWriter.writerows(array)

user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.34 Safari/537.36'}

#classe mãe do crawler

class crawler:
    def __init__(self, link, maxPages):
        self.valid_links = [] # links validos
        self.invalids = [] #links invalidos
        self.link = link # link atual
        self.maxPages = maxPages #maxpages para busca
        self.loops = 0 # quantidade de loops até maxpages
        self.domain = "dale" #dominio atual
        self.time = 0 # tempo inicial

    # gets

    def get_my_links(self):
        print("tamanho da : ",len(self.valid_links))
        return self.valid_links

    def get_my_invalids(self):
        print("tamanho da : ",len(self.invalids))
        return self.invalids

    def get_loops(self):
        print("quantos loops foram feitos: ",self.loops)
        loops = self.loops
        self.loops=0
        return loops

    def get_domain(self):
        print(self.domain)
        return self.domain

    def get_time(self):
        print(self.time)
        return self.time

    #crawler bsf

    def bsfCrawl(self):
        time1 = time.time()
        count = 0
        visited = [self.link]
        url_atual = self.link
        url_original = self.link
        print("visitando:", url_atual)
        rp = urobot.RobotFileParser()
        autorizado = True
        ext = tldextract.extract(url_original)
        self.domain = ext.domain

        while( len(self.valid_links) < self.maxPages):
            print("entrei no link: ", url_atual)
            codigo_fonte = rq.get(url_atual, headers=user_agent)

            soup = BeautifulSoup(codigo_fonte.text,'lxml')
            crawler = soup.find_all('a', href=True) #buscando todos a
            for a in crawler: # para todos filhos crawlei
                href = a.get('href')
                link_final = urljoin(url_atual,href)
                autorizdo = rp.can_fetch("*", url_atual) #checando robotos.txt

                # eliminando links invalidos e com termos invalidos
                if(validators.url(link_final) == False ):
                    if(link_final not in self.invalids):
                        self.invalids.append(link_final)
                elif(link_final.find('tel:')==0):
                    if(link_final not in self.invalids):
                        self.invalids.append(link_final)
                elif(link_final.find('mailto:')==0):
                    if(link_final not in self.invalids):
                        self.invalids.append(link_final)
                elif(link_final.find('javascript:;')==0):
                    if(link_final not in self.invalids):
                        self.invalids.append(link_final)
                elif(link_final.find('javascript:void(0);')==0):
                    if(link_final not in self.invalids):
                        self.invalids.append(link_final)
                elif(autorizado and link_final not in visited):
                    self.valid_links.append(link_final)
                    visited.append(link_final)
                    # adicionando no array um link valido
            url_atual = self.valid_links[count]  # buscando agora com um nó

            count = count + 1
            self.loops = count
            print("agora estou com ", len(self.valid_links)/1000 * 100, "%" )

        time2 = time.time()
        self.time = (time2-time1)

cost=[]

 # rodando crawler para todos links
for link in links:
    bsfResponse=[]
    scrap = crawler(link,1000)
    scrap.bsfCrawl()
    bsfResponse.append(scrap.get_my_links())
    size = len(bsfResponse[0])
    domain= scrap.get_domain()
    gravarCsv(bsfResponse,domain)
    cost.append([domain,scrap.get_loops(),scrap.get_time(),size])
    gravarCusto(cost)



# bsfResponse=[]
# scrap = crawler(links[2],1000)
# scrap.bsfCrawl()
# bsfResponse.append(scrap.get_my_links())
# domain= scrap.get_domain()
# gravarCsv(bsfResponse,domain)
# cost.append([domain,scrap.get_loops(),scrap.get_time()])
