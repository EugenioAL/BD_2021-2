from typing import List
import re

class Product:
    def __init__(self):
        self.id = 0
        self.asin = 0
        self.title = ""
        self.group = ""
        self.salesrank = 0
        self.categoria = ''

class Similar:
    def __init__(self):
        self.asin = 0
        self.sAsin = 0

class Grupo:
    def __init__(self) -> None:
        self.nome = ''


class Categorias:
    def __init__(self):
        self.catpai = ""
        self.catpai_id = 0
        self.subcat_name = ""
        self.subcat_id = 0
class Reviews:
    def __init__(self):
        self.asin = ""
        self.date = ""
        self.customer_id = 0
        self.rating = 0
        self.votes = 0
        self.helpf = 0

def splitByLine(dataText,productList,grupoList,reviewsList,categoriasList,similarList):
    tmpProduct = Product()
    tmpGrupos = Grupo()
    tmpReviews = Reviews()
    tmpCategorias = Categorias()
    tmpSimilar = Similar()
    Lista = []
    
    dataLines = dataText.split('\n', -1)
    #for i in range(len(dataLines)):
        #print(  "linha:\t",i)
        #print(dataLines[i])
    tmpProduct.id = int(dataLines[0])
    #print("Produto id:\t",tmpProduct.id)
    Lista = dataLines[1].split("ASIN: ",-1)
    tmpProduct.asin = Lista[1]
    #print("Produto asin:\t",tmpProduct.asin)
    Lista =  dataLines[2].split("title: ",-1)
    if(len(Lista) > 1):
        tmpProduct.title = Lista[1]
        #print("Produto titulo:\t",tmpProduct.title)
        Lista =  dataLines[3].split("group: ",-1)
        tmpGrupos.nome = Lista[1]
        #print("Grupo:\t\t",tmpGrupos.nome)
        Lista =  dataLines[4].split("salesrank: ",-1)
        tmpProduct.salesrank = int(Lista[1])
        #print("Salesrank:\t",tmpProduct.salesrank)
        productList.append(tmpProduct)
        Lista = dataLines[5].split("similar: ")
        Lista = Lista[1].split("  ",-1)
        simQt = int(Lista[0])
        tmpSimilar.asin = tmpProduct.asin
        i = 1
        #print(Lista)
        while(i <= simQt):
            similarList.append(Similar())
            similarList[len(similarList)-1].sAsin = Lista[i]
            i+=1
        Lista = dataLines[6].split("categories: ",-1)
        catQt = int(Lista[1])
        i = 1
        while(i <= catQt):
            Lista = re.findall(r'[a-z &\-A-Z]+', dataLines[6+i])
            Lista.pop(0)
            x = len(Lista)
            Lista2 = re.findall(r'[0-9]+', dataLines[6+i])
            a = 0
            while(a < x):
                if(a > 0):
                    tmpCategorias.catpai = Lista[a-1]
                    tmpCategorias.catpai_id = int(Lista2[a-1])
                    tmpCategorias.subcat_name = Lista[a]
                    tmpCategorias.subcat_id = int(Lista2[a])
                else:
                    tmpCategorias.catpai = Lista[a]
                    tmpCategorias.catpai_id = int(Lista2[a])
                    tmpCategorias.subcat_name = Lista[a]
                    tmpCategorias.subcat_id = (Lista2[a])
                categoriasList.append(Categorias())
                categoriasList[len(categoriasList)-1].catpai = tmpCategorias.catpai
                categoriasList[len(categoriasList)-1].catpai_id =tmpCategorias.catpai_id
                categoriasList[len(categoriasList)-1].subcat_name = tmpCategorias.subcat_name
                categoriasList[len(categoriasList)-1].subcat_id = tmpCategorias.subcat_id
                a+=1
            i+=1
        x = 6 + catQt+1
        Lista = re.findall(r"[0-9]+",dataLines[x])
        reviewsQt = int(Lista[0])
        finalCategorias = reviewsQt + x
        x += 1
        while(x <= finalCategorias):
            Lista = re.findall(r'[0-9a-zA-Z\-]+',dataLines[x])
            tmpReviews.asin = tmpProduct.asin
            tmpReviews.date = Lista[0]
            tmpReviews.customer_id = Lista[2]
            tmpReviews.rating = Lista[4]
            tmpReviews.votes = Lista[6]
            tmpReviews.helpf = Lista[8]
            reviewsList.append(Reviews())
            reviewsList[len(reviewsList)-1].date = tmpReviews.date
            reviewsList[len(reviewsList)-1].customer_id = tmpReviews.customer_id
            reviewsList[len(reviewsList)-1].rating = tmpReviews.rating
            reviewsList[len(reviewsList)-1].votes = tmpReviews.votes
            reviewsList[len(reviewsList)-1].helpf = tmpReviews.helpf
            x+=1

    else:
        tmpProduct.title = Lista[0]
        productList.append(tmpProduct)
        #print("Produto titulo:\t",tmpProduct.title)





def parser():
    tmpProduct = []
    customer = []
    reviews = []
    categorias = []
    similares = []

    with open('ptest.txt', encoding='latin-1') as file:
        file_contents = file.read()
        file_split_by_id = file_contents.split('Id:   ',-1)
    
    i=1
    
    while(i < len(file_split_by_id)):
        splitByLine(file_split_by_id[i],tmpProduct, customer, reviews,categorias,similares)
        i+=1
    for i in range(len(tmpProduct)):
        print(tmpProduct[i].title)

    for i in range(len(similares)):
        print(similares[i].sAsin)

    for i in range(len(reviews)):
        print(reviews[i].date)


    #for i in range(len(categorias)):
    #    print("CatPai:\t",categorias[i].catpai,"\tSub:\t",categorias[i].subcat_name)
    #fr = "|Books[283155]|Subjects[1000]|Religion & Spirituality[22]|Christianity[12290]|Clergy[12360]|Preaching[12368]"
    #fd = fr.split('|',-1)

    
    #cd = fd[1].split('[',1)
    
    #catID = int(''.join(filter(str.isdigit,fd[1])))




parser()
