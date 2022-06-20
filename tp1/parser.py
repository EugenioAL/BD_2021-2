import re

class Product:
    def __init__(self):
        self.id = None
        self.asin = None
        self.title = None
        self.group = None
        self.salesrank = None
        self.categoria = None

class Similar:
    def __init__(self):
        self.asin = None
        self.sAsin = None

class Grupo:
    def __init__(self) -> None:
        self.nome = None


class Categorias:
    def __init__(self):
        self.catpai = None
        self.catpai_id = None
        self.subcat_name = None
        self.subcat_id = None
class Reviews:
    def __init__(self):
        self.asin = None
        self.date = None
        self.customer_id = None
        self.rating = None
        self.votes = None
        self.helpf = None

def splitByLine(dataText,productList,grupoList,reviewsList,categoriasList,similarList):
    tmpProduct = Product()
    tmpGrupos = Grupo()
    tmpReviews = Reviews()
    tmpCategorias = Categorias()
    tmpSimilar = Similar()
    Lista = []
    
    dataLines = dataText.split('\n', -1)
    tmpProduct.id = int(dataLines[0])
    Lista = dataLines[1].split("ASIN: ",-1)
    tmpProduct.asin = Lista[1]
    Lista =  dataLines[2].split("title: ",-1)
    if(len(Lista) > 1):
        tmpProduct.title = Lista[1]
        Lista =  dataLines[3].split("group: ",-1)
        tmpGrupos.nome = Lista[1]
        Lista =  dataLines[4].split("salesrank: ",-1)
        tmpProduct.salesrank = int(Lista[1])
        productList.append(tmpProduct)
        Lista = dataLines[5].split("similar: ")
        Lista = Lista[1].split("  ",-1)
        simQt = int(Lista[0])
        tmpSimilar.asin = tmpProduct.asin
        if(simQt > 0):
            i = 1
            while(i <= simQt):
                similarList.append(Similar())
                similarList[len(similarList)-1].sAsin = Lista[i]
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
        if(reviewsQt > 0):
            finalCategorias = reviewsQt + x
            x += 1
            while(x <= finalCategorias and x < len(dataLines)):
                Lista = re.findall(r'[0-9a-zA-Z\-]+',dataLines[x])
                if(len(Lista) == 9):
                    tmpReviews.asin = tmpProduct.asin
                    tmpReviews.date = Lista[0]
                    tmpReviews.customer_id = Lista[2]
                    tmpReviews.rating = int( Lista[4])
                    tmpReviews.votes = int(Lista[6])
                    tmpReviews.helpf = int(Lista[8])
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


product = []
customer = []
reviews = []
categorias = []
similares = []


def parser(prodList,customerList,rebiesList,categoriasList,similaresList):

    with open('amazon-meta.txt', encoding='latin-1') as file:
        file_contents = file.read()
        file_split_by_id = file_contents.split('Id:   ',-1)
    
    i=1
    
    while(i < len(file_split_by_id)):
        splitByLine(file_split_by_id[i],prodList,customerList,rebiesList,categoriasList,similaresList)
        i+=1

    for i in range(len(prodList)):
        print(prodList[i].title)




parser(product,customer,reviews,categorias,similares)
