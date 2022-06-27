
import json
from re import match
from io import TextIOWrapper
from typing import List, Dict
from psycopg2 import connect
import operator
from functools import reduce

global_categories = set()
global_products = dict()

class Constants():
    DOWNLOADED = 2
    AVR_RATING = 4

    TOTAL_VALUE = 1
    DOWNLOADED_VALUE = 3
    AVR_RATING_VALUE = 5

    MAX_ENTRIES_PER_BLOCK = 5000


class Entry:

    def __init__(self):
        self.mId = -1
        self.mAsin = ""
        self.mTitle = ""
        self.mGroup = ""
        self.mSalesrank = -1
        self.mSimilar = []
        self.mCategories = []
        self.mDownloaded = -1
        self.mAvrRating = -1
        self.mReviews = []
        self.mDiscontinued = False
        self.mJsonDict: Dict = {}

    def jsonInit(self) -> dict:
        self.mJsonDict = {"id": self.mId, "asin": self.mAsin, "title": self.mTitle, "group": self.mGroup,
                          "salesrank": self.mSalesrank, "similar": self.mSimilar, "categories": self.mCategories,
                          "reviews": self.mReviews, "downloaded": self.mDownloaded, "avrRating": self.mAvrRating, "discontinued": self.mDiscontinued}

    def addSimilar(self, itemId: str):
        self.mSimilar.append(itemId)

    def addReview(self, review: dict):
        self.mReviews.append(review)

    def setId(self, itemId: int):
        self.mId = itemId

    def setAsin(self, asin: str):
        self.mAsin = asin

    def setTitle(self, title: str):
        self.mTitle = title

    def setGroup(self, group: str):
        self.mGroup = group

    def setSalesrank(self, salesrank: int):
        self.mSalesrank = salesrank

    def setAvrRating(self, avrRating: float):
        self.mAvrRating = avrRating

    def addCategorie(self, categorieItem: str):
        self.mCategories.append(categorieItem)

    def setDownloaded(self, value: int):
        self.mDownloaded = value


def reviewDict(date: str, customer: str, rating: int, votes: int, helpful: int) -> dict:
    return {"date": date, "customer": customer,
            "rating": int(rating), "votes": int(votes), "helpfull": int(helpful)}


def idKey(entry: Entry, itemId: str, file: TextIOWrapper = None):
    entry.setId(int(itemId.strip()))


def asinKey(entry: Entry, asin: str, file: TextIOWrapper = None):
    entry.setAsin(asin.strip())


def titleKey(entry: Entry, title: str, file: TextIOWrapper = None):
    entry.setTitle(title.strip())


def groupKey(entry: Entry, group: str, file: TextIOWrapper = None):
    entry.setGroup(group.strip())


def salesrankKey(entry: Entry, salesrank: str, file: TextIOWrapper = None):
    entry.setSalesrank(int(salesrank.strip()))


def similarKey(entry: Entry, similar: List[str], file: TextIOWrapper = None):

    similiarListSplited = similar.split()
    numberOfItems = int(similiarListSplited[0])

    if numberOfItems > 0:
        similarListId = similiarListSplited[1:]

        for item in similarListId:
            entry.addSimilar(item.strip())


def categorieKey(entry: Entry, categorie: str, file: TextIOWrapper = None):

    if file is not None:

        nunmberOfCategoriesLines = int(categorie.strip())

        for _ in range(nunmberOfCategoriesLines):

            line = file.readline()
            line = list(filter(None, line.strip().split('|')))

            for categorieItem in line:
                m = match(r"(\w+.*)(\[\d+\])", categorieItem)
                if m is not None:
                    categorieItemMatched = m.group(1)
                    if (categorieItemMatched not in entry.mCategories):
                        global_categories.add(categorieItemMatched)
                        entry.addCategorie(categorieItemMatched)


def reviewKey(entry: Entry, statistic: str, file: TextIOWrapper = None):

    s = statistic.replace('  ', ':')
    splitedLine = list(filter(None, s.strip().split(':')))

    keys[splitedLine[Constants.DOWNLOADED]](
        entry, splitedLine[Constants.DOWNLOADED_VALUE])
    keys[splitedLine[Constants.AVR_RATING]](
        entry, splitedLine[Constants.AVR_RATING_VALUE])

    reviewKeyInternal(entry, splitedLine[Constants.DOWNLOADED_VALUE], file)


def reviewKeyInternal(entry: Entry, totalLines: str, file: TextIOWrapper = None):

    totalLines = int(totalLines.strip())

    for _ in range(totalLines):

        line = file.readline()

        line = line.replace(" ", ":")
        line = list(filter(None, line.strip().split(':')))

        entry.addReview(reviewDict(*line[0::2]))


def downloadedKey(entry: Entry, downloaded: str, file: TextIOWrapper = None):
    entry.setDownloaded(int(downloaded.strip()))


def avgratingKey(entry: Entry, avrRating: str, file: TextIOWrapper = None):
    entry.setAvrRating(float(avrRating.strip()))



keys = {"id": idKey, "asin": asinKey, "title": titleKey, "group": groupKey, "salesrank": salesrankKey,"similar": similarKey, "categories": categorieKey, "reviews": reviewKey, "downloaded": downloadedKey, "avg rating": avgratingKey}


def readEntry(entry: Entry, file: TextIOWrapper):
    line = file.readline()

    if not line:
        return False

    while line != '\n':

        if line.strip() == 'discontinued product':
            entry.mDiscontinued = True
            line = file.readline()
            continue

        key, value = line.split(':', maxsplit=1)

        key = key.lower().strip()
        try:
            keys[key](entry, value, file)
        except KeyError as e:
            print("There is not key named: ", e)

        line = file.readline()

    return True

def load_dataset_and_transform(filename, outputPath):
    entries = []

    # https://snap.stanford.edu/data/amazon-meta.html
    amazon_test_dataset = open(filename, encoding='utf-8')

    for _ in range(3):
        amazon_test_dataset.readline()
        
    fileNumber = 0
    entriesCount = 0

    while (True):
        entry = Entry()
        if not readEntry(entry, amazon_test_dataset):
            break

        entry.jsonInit()
        entries.append(entry.mJsonDict)

        if not entry.mDiscontinued:
            global_products[entry.mAsin] = 1

        entriesCount += 1

        if (entriesCount == Constants.MAX_ENTRIES_PER_BLOCK):

            fp = open(f"%s%d.json" %
                    (outputPath, fileNumber), "w", encoding="utf-8")
            print(f"Dumping entries [%d] into file..." % (fileNumber))
            json.dump(entries, fp, ensure_ascii=False)
            fp.close()

            entries = []
            fileNumber += 1
            entriesCount = 0

    fp = open(f"%s%d.json" %
            (outputPath, fileNumber), "w", encoding="utf-8")
    print(f"Dumping entries [%d] into file..." % (fileNumber))
    json.dump(entries, fp, ensure_ascii=False)
    fp.close()

    return fileNumber

def get_connection():
    return connect("dbname=postgres user=postgres password=postgres host=0.0.0.0 port=5432")

def create_database():
    conn = get_connection()
    cursor = conn.cursor()
    crate_products_table = """
        CREATE TABLE IF NOT EXISTS PRODUCTS (
            ID INT NOT NULL,
            ASIN VARCHAR(10) NOT NULL,
            TITLE VARCHAR(500),
            PRODUCT_GROUP VARCHAR(200),
            DOWNLOADED INT NOT NULL,
            AVRRATING REAL NOT NULL,
            SALESRANK INT NOT NULL,
            PRIMARY KEY(ASIN)
        );
        """
    cursor.execute(crate_products_table)

    create_similars_table = """
        CREATE TABLE IF NOT EXISTS SIMILARS (
        ID SERIAL PRIMARY KEY,
        ASIN_PRODUCT_1 VARCHAR(10) NOT NULL,  
        ASIN_PRODUCT_2 VARCHAR(10) NOT NULL,
        FOREIGN KEY(ASIN_PRODUCT_1) REFERENCES PRODUCTS(ASIN),
        FOREIGN KEY(ASIN_PRODUCT_2) REFERENCES PRODUCTS(ASIN)
    );
    """
    cursor.execute(create_similars_table)

    create_categories_table = """
        CREATE TABLE IF NOT EXISTS CATEGORIES (
        ID SERIAL PRIMARY KEY,
        TITLE VARCHAR(100) NOT NULL
    );
    """
    cursor.execute(create_categories_table)

    create_prod_categ_table = """
        CREATE TABLE IF NOT EXISTS PRODUCT_CATEGORIES (
        ID SERIAL PRIMARY KEY,
        ASIN_PRODUCT VARCHAR(10) NOT NULL,
        ID_CATEGORY INT NOT NULL,
        FOREIGN KEY(ASIN_PRODUCT) REFERENCES PRODUCTS(ASIN),
        FOREIGN KEY(ID_CATEGORY) REFERENCES CATEGORIES(ID)
    );
    """
    cursor.execute(create_prod_categ_table)

    create_reviews_table = """
        CREATE TABLE IF NOT EXISTS REVIEWS (
        ID SERIAL PRIMARY KEY,
        CREATED_AT DATE NOT NULL,
        CUSTOMER VARCHAR(20) NOT NULL,
        RATING INT NOT NULL,
        VOTES INT NOT NULL,
        HELPFULL INT NOT NULL,
        ASIN_PRODUCT VARCHAR(10) NOT NULL,
        FOREIGN KEY(ASIN_PRODUCT) REFERENCES PRODUCTS(ASIN)
    );
    """
    cursor.execute(create_reviews_table)
    

    conn.commit()
    conn.close()
    cursor.close()


def insert_batch(cur, sql, template, args):
    argslist = list(args)
    sql_full = sql + ','.join([template] * len(argslist))
    cur.execute(sql_full, reduce(operator.add, argslist))

def populate_products(filename):
    data = json.load(open(filename))

    conn = get_connection()
    cursor = conn.cursor()

    lst_to_insert = []
    sql = "INSERT INTO PRODUCTS (id, asin, title, product_group, downloaded, avrrating, salesrank) VALUES "
    params = "(%s, %s, %s, %s, %s, %s, %s)"

    for item in data:
        if item["discontinued"]:
            continue

        lst_to_insert.append((item["id"], item["asin"], item["title"], item["group"], item["downloaded"], item["avrRating"], item["salesrank"]))

        if len(lst_to_insert) > 500:
            insert_batch(cursor, sql, params, lst_to_insert)
            lst_to_insert = []
    
    if lst_to_insert:
        insert_batch(cursor, sql, params, lst_to_insert)
    
    conn.commit()
    conn.close()
    cursor.close()

def populate_similars(filename):
    data = json.load(open(filename))

    conn = get_connection()
    cursor = conn.cursor()

    lst_to_insert = []
    sql = "INSERT INTO SIMILARS (asin_product_1, asin_product_2) VALUES "
    params = "(%s, %s)"

    for item in data:
        if item["discontinued"]:
            continue

        similars = item["similar"]
        for similar in similars:

            if similar in global_products:
                lst_to_insert.append((item["asin"], similar))

                if len(lst_to_insert) > 500:
                    insert_batch(cursor, sql, params, lst_to_insert)
                    lst_to_insert = []

    if lst_to_insert:
        insert_batch(cursor, sql, params, lst_to_insert)

    conn.commit()
    conn.close()
    cursor.close()

def populate_categories():
    conn = get_connection()
    cursor = conn.cursor()

    lst_to_insert = []
    for category in global_categories:
        lst_to_insert.append((category,))

    sql = "INSERT INTO CATEGORIES (title) VALUES "
    params = "(%s)"

    insert_batch(cursor, sql, params, lst_to_insert)

    conn.commit()
    conn.close()
    cursor.close()


def get_all_categories_in_db():
    conn = get_connection()
    cur = conn.cursor()
    sql = "SELECT ID, TITLE FROM CATEGORIES"
    cur.execute(sql)

    data = cur.fetchall()
    cur.close()
    conn.close()

    map_category = dict()
    for item in data:
        map_category[item[1]] = item[0]

    return map_category

def populate_product_categories(filename, map_categories):
    data = json.load(open(filename))

    conn = get_connection()
    cursor = conn.cursor()

    # inserir usando o map_categories
    lst_to_insert = []
    sql = "INSERT INTO PRODUCT_CATEGORIES (asin_product, id_category) VALUES "
    params = "(%s, %s)"

    for item in data:
        if item["discontinued"]:
            continue

        categories = item["categories"]
        for category in categories:
            lst_to_insert.append((item["asin"], map_categories[category]))

            if len(lst_to_insert) > 500:
                insert_batch(cursor, sql, params, lst_to_insert)
                lst_to_insert = []

    if lst_to_insert:
        insert_batch(cursor, sql, params, lst_to_insert)
    
    conn.commit()
    conn.close()
    cursor.close()

def populate_reviews(filename):
    data = json.load(open(filename))

    conn = get_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO REVIEWS (created_at, customer, rating, votes, helpfull, asin_product) VALUES "
    params = "(%s, %s, %s, %s, %s, %s)"

    lst_to_insert = []

    for item in data:
        if item["discontinued"]:
            continue

        reviews = item["reviews"]
        for review in reviews:
            lst_to_insert.append((review["date"], review["customer"], review["rating"], review["votes"], review["helpfull"], item["asin"]))

            if len(lst_to_insert) > 500:
                insert_batch(cursor, sql, params, lst_to_insert)
                lst_to_insert = []

    if lst_to_insert:
        insert_batch(cursor, sql, params, lst_to_insert)
    
    conn.commit()
    conn.close()
    cursor.close()

def populate_database(file_path, n_files):
    print("Inserindo produtos")
    for i in range(n_files):
        populate_products(f"{file_path}{i}.json")

    print("Inserindo similares")
    for i in range(n_files):
        populate_similars(f"{file_path}{i}.json")

    print("Inserindo categorias")
    populate_categories()
    categories = get_all_categories_in_db()

    print("Inserindo produto-categorias")
    for i in range(n_files):
        populate_product_categories(f"{file_path}{i}.json", categories)
    
    print("Inserindo avaliações")
    for i in range(n_files):
        populate_reviews(f"{file_path}{i}.json")

    
if __name__ == "__main__":
    print("criando as tabelas...")
    create_database()
    print("tabelas criadas...")

    output_path = "out/"
    number_of_files = load_dataset_and_transform('amazon-meta.txt', output_path)

    populate_database(output_path, number_of_files)
    
    print("finalizando...")
