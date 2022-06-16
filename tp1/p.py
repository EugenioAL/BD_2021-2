import re

texto = "   |Music[5174]|Styles[301668]|Classical[85]|Featured Performers, A-Z[38472]|( W )[62549]|Williams, John        [guitar][63054]"
res = '[[0-9]+]'
ab = []
def af(texto):
    ar = texto.split(r"|",-1)
    for i in range(len(ar)):
        ab.append(re.sub(res,'',ar[i]))
    print(ar)
    print(ab)

af(texto)