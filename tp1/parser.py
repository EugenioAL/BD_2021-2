import re
import psycopg2

class Product:
    def __init__(self,id,asin,title,group,salesrank):
        self.id = id
        self.asin = asin
        self.title = title
        self.group = group
        self.salesrank = salesrank

class Similar:
    def __init__(self,asin,sAsin):
        self.asin = asin
        self.sAsin = sAsin


class Categorias:
    def __init__(self,categoria_name,categoria_id):
        self.categoria_name = categoria_name
        self.categoria_id = categoria_id


class Reviews:
    def __init__(self,asin,date,customer_id,rating,votes,helpful):
        self.asin = asin
        self.date = date
        self.customer_id = customer_id
        self.rating = rating
        self.votes = votes
        self.helpful = helpful

class CatsProducts():
    def __init__(self,val_id,val_asin):
        self.cat_id = val_id
        self.asin = val_asin

def splitByLine(dataText,productList,grupoList,reviewsList,categoriasList,similarList,catsProdsList):
    Lista = []
    
    dataLines = dataText.split('\n', -1)
    id = int(dataLines[0])
    Lista = dataLines[1].split("ASIN: ",-1)
    asin = Lista[1]
    Lista =  dataLines[2].split("title: ",-1)
    if(len(Lista) > 1):
        title = Lista[1]
        Lista =  dataLines[3].split("group: ",-1)
        grupo = Lista[1]
        Lista =  dataLines[4].split("salesrank: ",-1)
        salesrank = int(Lista[1])
        productList.append(Product(id,asin,title,grupo,salesrank))
        Lista = dataLines[5].split("similar: ")
        Lista = Lista[1].split("  ",-1)
        simQt = int(Lista[0])
        if(simQt > 0):
            i = 1
            while(i <= simQt):
                similarList.append(Similar(asin,Lista[i]))
                i+=1
        Lista = dataLines[6].split("categories: ",-1)
        catQt = int(Lista[1])
        if(catQt > 0):
            i = 1
            while(i <= catQt):
                Lista = dataLines[6+i].split('|',-1)
                for f in range(len(Lista)):
                    Lista[f] = re.sub('[[0-9]+]','',Lista[f])
                Lista.pop(0)
                x = len(Lista)
                Lista2 = re.findall(r'[0-9]+', dataLines[6+i])
                for f in range(len(Lista2)):
                    Lista2[f] = int(re.sub('\[\]','',Lista2[f]))
                a = 0
                while(a < x):
                    catsProdsList.append(CatsProducts(Lista2[a],asin))
                    a+=1
                i+=1
        x = 6 + catQt+1
        Lista = re.findall(r"[0-9]+",dataLines[x])
        reviewsQt = int(Lista[0])
        if(reviewsQt > 0):
            finalCategorias = reviewsQt + x
            x += 1
            while(x <= finalCategorias and x < len(dataLines)):
                Lista = re.findall(r'[0-9a-zA-Z\-]+',dataLines[x])
                if(len(Lista) == 9):
                    reviewsList.append(Reviews(asin,Lista[0],Lista[2],int(Lista[4]),int(Lista[6]),int(Lista[8])))
                x+=1

    else:
        productList.append(Product(id,asin,Lista[0],None,None))


product = []
customer = []
reviews = []
categorias = []
similares = []
catsProds = []




def parser(prodList,customerList,reviewsList,categoriasList,similaresList,catsProdsList):

    with open('amazon-meta.txt', encoding='latin-1') as file:
        file_contents = file.read()
        file_split_by_id = file_contents.split('Id:   ',-1)
    
    i=1
    
    while(i < len(file_split_by_id)):
        splitByLine(file_split_by_id[i],prodList,customerList,reviewsList,categoriasList,similaresList,catsProdsList)
        i+=1

    """
    for i in range(len(prodList)):
        print("id:\t",prodList[i].id,"asin:\t",prodList[i].asin,"title:\t",prodList[i].title,'grupo:\t',prodList[i].group,'salesrank:\t',prodList[i].salesrank)
    
    for i in range(len(similaresList)):
        print("asin:\t",similaresList[i].asin,"Sasin:\t",similaresList[i].sAsin)

    for i in range(len(categoriasList)):
        print("Cat name:\t",categoriasList[i].categoria_name,"Cat ID:\t",categoriasList[i].categoria_id)

    for i in range(len(reviewsList)):
        print("asin:\t",reviewsList[i].asin,"data:\t",reviewsList[i].date,"customer id:\t",reviewsList[i].customer_id,'rating:\t',reviewsList[i].rating,'votes:\t',reviewsList[i].votes,'helpful\t',reviewsList[i].helpful)

    for i in range(len(catsProdsList)):
        print("Cat ID:\t",catsProdsList[i].cat_id,"PROD asin:",catsProdsList[i].asin)
    """

parser(product,customer,reviews,categorias,similares,catsProds)
