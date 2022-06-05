
class Product:
    def __init__(self,id,asin):
        self.id = id
        self.asin = asin
        self.title = ""
        self.group = ""
        self.salesrank = 0

    def toDB(self):
        return 

class Similar:
    def __init__(self):
        self.product_id = 0
        self.product_tog_id = 0

class Subcat:
    def __init__(self):
        self.cat_id = 0
        self.cat_name = ""
        self.subcat_id = 0
        self.subcat_name = ""

class Cat_prod:
    def __init__(self):
        self.catid = 0
        self.product_asin = ""

class Reviews:
    def __init__(self):
        self.product_asin = ""
        self.date = ""
        self.customer_id = 0
        self.rating = 0
        self.votes = 0
        self.helpf = 0

def splitBySpace(dataText):
    dataLines = dataText.split('  ', -1)
    print(dataLines)
    return dataLines

def splitByLine(dataText):
    dataLines = dataText.split('\n', -1)
    for i in range(len(dataLines)):
        splitBySpace(dataLines[i])



def parser():
    with open('ptest.txt') as file:
        file_contents = file.read()
        file_split_by_id = file_contents.split('Id: ',-1)
    
    for i in range(len(file_split_by_id)):
        splitByLine(file_split_by_id[i])


    fr = "|Books[283155]|Subjects[1000]|Religion & Spirituality[22]|Christianity[12290]|Clergy[12360]|Preaching[12368]"
    fd = fr.split('|',-1)

    
    cd = fd[1].split('[',1)
    
    catID = int(''.join(filter(str.isdigit,fd[1])))




parser()