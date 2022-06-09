from typing import List


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
        self.cat_id = 0
        self.cat_name = ""
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
        x = 6 + catQt+1
        Lista = dataLines[x].split("reviews: total: ",-1)
        Lista = Lista[1].split("  ",-1)
        reviewsQt = int(Lista[0])
        finalLine = reviewsQt + x
        x += 1
        print(Lista)
        print(reviewsQt)

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
    #for i in range(len(tmpProduct)):
    #    print(tmpProduct[i].title)

    #for i in range(len(similares)):
    #    print(similares[i].sAsin)

    for i in range(len(reviews)):
        print(reviews[i].data)

    #fr = "|Books[283155]|Subjects[1000]|Religion & Spirituality[22]|Christianity[12290]|Clergy[12360]|Preaching[12368]"
    #fd = fr.split('|',-1)

    
    #cd = fd[1].split('[',1)
    
    #catID = int(''.join(filter(str.isdigit,fd[1])))




parser()
