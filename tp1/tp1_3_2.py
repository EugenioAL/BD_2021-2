import psycopg2
import re

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

    def __eq__(self, __o: object) -> bool:
        return self.asin == __o.asin and self.sAsin == __o.sAsin


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
                for idx in range(len(Lista)):
                    categorias.add((Lista2[idx], Lista[idx]))
                a = 0
                while(a < x):
                    if not catsProdsSet.intersection(set((Lista2[a],str(asin)))):
                        catsProdsSet.add((Lista2[a],str(asin)))
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

def parser(prodList,customerList,reviewsList,categoriasList,similaresList,catsProdsList):
    filename = "amazon-meta.txt"
    with open(filename, encoding='latin-1') as file:
        file_contents = file.read()
        file_split_by_id = file_contents.split('Id:   ',-1)

    i=1

    while(i < len(file_split_by_id)):
        splitByLine(file_split_by_id[i],prodList,customerList,reviewsList,categoriasList,similaresList,catsProdsList)
        i+=1


product = []
customer = []
reviews = []
categorias = set()
similares = []
catsProdsSet = set()
catsProds = []

def get_connection():
    #db configurações
    host = 'localhost'
    dbname = 'amazon'
    user = 'postgres'
    password = 'postgres'

    #string de conexão

    conn_string = 'host={0} user={1} dbname={2} password={3}'.format(host, user, dbname, password)

    conn = psycopg2.connect(conn_string)
    return conn

def inserir_categorias(conn, list_categorias):
    cursor = conn.cursor()
    args = ','.join(cursor.mogrify("(%s,%s)", i).decode('utf-8')
                for i in list_categorias)
    cursor.execute("INSERT INTO categoria VALUES " + args + " ON CONFLICT (id) DO NOTHING")
    conn.commit()
    conn.close()
    cursor.close()
    # for cat in list_categorias:
    #         postgres_insert_query = """ INSERT INTO categoria (id, nome) VALUES (%s,%s) ON CONFLICT (id) DO NOTHING """
    #         record_to_insert = (cat[0], cat[1])
    #         cursor.execute(postgres_insert_query, record_to_insert)
    #         conn.commit()

def inserir_produtos(conn, list_produtos):
    cursor = conn.cursor()
    args = ','.join(cursor.mogrify("(%s,%s,%s,%s,%s)", i).decode('utf-8')
                for i in list_produtos)
    cursor.execute("INSERT INTO produto VALUES " + args)
    conn.commit()
    conn.close()
    cursor.close()

def inserir_avaliacoes(conn, list_reviews: list):
    cursor = conn.cursor()
    args = ','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s)", i).decode('utf-8')
                for i in list_reviews)
    cursor.execute("INSERT INTO review (asin, customer, rating, date, votes, helpful) VALUES " + args)
    conn.commit()
    conn.close()
    cursor.close()

def inserir_produto_categoria(conn, list_cats_prod):
    cursor = conn.cursor()
    args = ','.join(cursor.mogrify("(%s,%s)", i).decode('utf-8')
                for i in list_cats_prod)
    cursor.execute("INSERT INTO produtocategoria VALUES " + args + " ON CONFLICT (asin, id_categoria) DO NOTHING")
    conn.commit()
    conn.close()
    cursor.close()

def inserir_similares(conn, list_similares):
    cursor = conn.cursor()
    args = ','.join(cursor.mogrify("(%s,%s)", i).decode('utf-8')
                for i in list_similares)
    cursor.execute("INSERT INTO similares VALUES " + args)
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

parser(product,customer,reviews,categorias,similares,catsProds)

criarTabela(get_connection())

print("inserindo categorias...")
inserir_categorias(get_connection(), list(categorias))

print("inserindo produtos...")
inserir_produtos(get_connection(), [(produto.asin, produto.id, produto.title, produto.salesrank, produto.group) for produto in product])


print("inserindo avalicacoes...")
int_reviews = intervalos = [intervalo for intervalo in range(0, len(reviews), 5_000)]
for i in range(1, len(int_reviews)):
    ini = int_reviews[i - 1]
    fim = int_reviews[i]
    if i == len(int_reviews) - 1:
        fim = len(reviews)

    inserir_avaliacoes(get_connection(), [(r.asin, r.customer_id, r.rating, r.date, r.votes, r.helpful) for r in reviews[ini:fim]])

inserir_produto_categoria(get_connection(), list(set([(c.asin, c.cat_id) for c in catsProds])))

inserir_similares(get_connection(), [(s.asin, s.sAsin) for s in similares])