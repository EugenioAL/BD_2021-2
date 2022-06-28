import re
from typing import Set
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
    def __init__(self,cat_id,prod_asin):
        self.cat_id = cat_id
        self.asin = prod_asin

def splitByLine(dataText,productList,reviewsList,categoriasList,similarList,catsProdsList):
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
                    if(any(tmp.categoria_id == Lista2[a] for tmp in categoriasList) == False):
                        categoriasList.append(Categorias(Lista[a],Lista2[a]))
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




def parser(prodList,reviewsList,categoriasList,similaresList,catsProdsList):

    with open('amazon-meta.txt', encoding='latin-1') as file:
        file_contents = file.read()
        file_split_by_id = file_contents.split('Id:   ',-1)
    
    i=1
    count = 0
    
    while(i < len(file_split_by_id)):
        splitByLine(file_split_by_id[i],prodList,reviewsList,categoriasList,similaresList,catsProdsList)
        if(count > 20000):
            print("inserindo categorias...")
            inserir_categorias(get_connection(), categoriasList)


            print("inserindo produtos...")
            inserir_produtos(get_connection(), prodList)


            print("inserindo avalicacoes...")

            inserir_avaliacoes(get_connection(), reviewsList)

            print("inserindo categoriaprodutos...")

            inserir_produto_categoria(get_connection(), catsProdsList)

            print("inserindo similares...")

            inserir_similares(get_connection(),similaresList)
            count = 0
        else:
            count+=1
        i+=1
    print("inserindo categorias...")
    inserir_categorias(get_connection(), categoriasList)


    print("inserindo produtos...")
    inserir_produtos(get_connection(), prodList)


    print("inserindo avalicacoes...")

    inserir_avaliacoes(get_connection(), reviewsList)

    print("inserindo produtocategoria...")

    inserir_produto_categoria(get_connection(), catsProdsList)

    print("inserindo similares...")

    inserir_similares(get_connection(),similaresList)

    """"
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

def get_connection():
    #db configurações
    host = 'localhost'
    dbname = 'postgres'
    user = 'postgres'
    password = 'postgres'

    #string de conexão

    conn_string = 'host={0} user={1} dbname={2} password={3}'.format(host, user, dbname, password)

    conn = psycopg2.connect(conn_string)
    return conn

def inserir_categorias(conn, list_categorias):
    pattern = '[\']'
    cursor = conn.cursor()
    list_categorias = list(set(list_categorias))
    args = ''
    while(len(list_categorias) > 0):
        list_categorias[0].categoria_name = re.sub(pattern,'\'\'',list_categorias[0].categoria_name)
        args = args +'(' + str(list_categorias[0].categoria_id) + ',\'' + list_categorias[0].categoria_name + '\')'
        if(len(list_categorias) > 1):
            args = args + ','
        list_categorias.pop(0)
    cursor.execute("INSERT INTO categoria (id,nome)VALUES " + args + " ON CONFLICT (id) DO NOTHING")
    conn.commit()
    conn.close()
    cursor.close()

def inserir_produtos(conn, list_produtos):
    flag = '  discontinued product'
    pattern = '[\']'
    cursor = conn.cursor()
    args = ''
    while(len(list_produtos) > 0):
        list_produtos[0].title = re.sub(pattern,'\'\'',list_produtos[0].title)
        if(list_produtos[0].title != flag):
            args = args +'(\'' + str(list_produtos[0].asin) + '\',' + str(list_produtos[0].id) + ',\'' + list_produtos[0].title + '\',' + str(list_produtos[0].salesrank) + ',\'' + list_produtos[0].group +'\')'
            if(len(list_produtos) > 1):
                args = args + ','
            list_produtos.pop(0)
        else:
            args = args +'(\'' + str(list_produtos[0].asin) + '\',' + str(list_produtos[0].id) + ',\'' + list_produtos[0].title + '\'' + ',null' + ',null' + ')'
            if(len(list_produtos) > 1):
                args = args + ','
            list_produtos.pop(0)
    cursor.execute("INSERT INTO produto VALUES " + args + " ON CONFLICT (asin) DO NOTHING")
    conn.commit()
    conn.close()
    cursor.close()

def inserir_avaliacoes(conn, list_reviews):
    cursor = conn.cursor()
    args = ''
    while(len(list_reviews) > 0):
        args = args +'(\'' + str(list_reviews[0].asin) + '\',\'' + list_reviews[0].customer_id + '\',' + str(list_reviews[0].rating) + ',\'' + list_reviews[0].date + '\',' + str(list_reviews[0].votes) + ',' + str(list_reviews[0].helpful) + ')'
        if(len(list_reviews) > 1):
            args = args + ','
        list_reviews.pop(0)
    cursor.execute("INSERT INTO review (asin,customer,rating,date,votes,helpful)VALUES " + args)
    conn.commit()
    conn.close()
    cursor.close()

def inserir_produto_categoria(conn, list_cats_prod):
    cursor = conn.cursor()
    args = ''
    while(len(list_cats_prod) > 0):
        args = args +'(\'' + str(list_cats_prod[0].asin) + '\',' + str(list_cats_prod[0].cat_id) + ')'
        if(len(list_cats_prod) > 1):
            args = args + ','
        list_cats_prod.pop(0)
    cursor.execute("INSERT INTO produtocategoria VALUES " + args + " ON CONFLICT (asin,id_Categoria) DO NOTHING")
    conn.commit()
    conn.close()
    cursor.close()

def inserir_similares(conn, list_similares):
    cursor = conn.cursor()
    args = ''
    while(len(list_similares) > 0):
        args = args +'(\'' + list_similares[0].asin + '\',\'' + list_similares[0].sAsin + '\')'
        if(len(list_similares) > 1):
            args = args + ','
        list_similares.pop(0)
    cursor.execute("INSERT INTO similares VALUES " + args + " ON CONFLICT (asin,asin_sim) DO NOTHING")
    conn.commit()
    conn.close()
    cursor.close()

def criarTabela(conn):
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS produto(asin VARCHAR (20) PRIMARY KEY,id INT UNIQUE,title VARCHAR (500), salesrank INT,grupo VARCHAR(30));')
    cursor.execute('CREATE TABLE IF NOT EXISTS similares(asin VARCHAR(20),asin_sim VARCHAR(20),PRIMARY KEY (asin, asin_sim), FOREIGN KEY (asin) REFERENCES produto(asin))')
    cursor.execute('CREATE TABLE IF NOT EXISTS review(id SERIAL PRIMARY KEY,asin VARCHAR(20),customer VARCHAR(20),rating INT, date DATE, votes INT, helpful INT,FOREIGN KEY (asin) REFERENCES produto(asin))')
    cursor.execute('CREATE TABLE IF NOT EXISTS categoria(id INT PRIMARY KEY, nome VARCHAR(150))')
    cursor.execute('CREATE TABLE IF NOT EXISTS produtocategoria(asin VARCHAR(20), id_categoria INT, PRIMARY KEY (asin, id_categoria),FOREIGN KEY (asin) REFERENCES produto(asin));')
    conn.commit()
    conn.close()
    cursor.close()

criarTabela(get_connection())

parser(product,reviews,categorias,similares,catsProds)