#---------- SOME FUNCTIONS ----------

def strToCoor(str_vec):
    ab_rep_split = str_vec.replace('[', '').replace(']', '').split(',')
    print(ab_rep_split)
    return [float(ab_rep_split[0]), float(ab_rep_split[1])]


def strToCoorBig(full_str):
    a = full_str.split(',')
    # print(a)
    gg = []
    otvet = []
    for i in a:
        gg.append(float(i.replace('[', '').replace(']', '').replace(',', '')))
    for i in range(0, len(gg)):
        if (i % 2) == 0:
            otvet.append([gg[i], gg[i + 1]])
    return otvet


def strToNameVec(str_vec):
    ab_rep_split = str_vec.replace('[', '').replace(']', '').replace(' ', '').replace('\'', '').split(',')
    return ab_rep_split


def createUlrForYandex(coorFrom, coorTo):
    url = f"https://yandex.ru/maps/213/moscow/?mode=routes&rtext={coorFrom[0]}%2C{coorFrom[1]}~{coorTo[0]}%2C{coorTo[1]}&rtt=auto"
    return url







# a = '[[56.94091937142843,39.302723071369385],[55.82834407,37.770358],[56.50650442111945,38.63897583037276]]'
#
# b = strToCoorBig(a)
# print(b)
#
# del b[0]
#
# print(b)
#
# a = ['Asb', 'Cd', 'Ef', 'Gsch']
#
# print (a)
#
#
# b = str(a)
#
# print(b)
#
# c = b.replace('[', '').replace(']', '').replace(' ', '').split(',')
#
# print(c)
# print(c[0])


#
# e=strToNameVec(b)
# print(e)
#
# del e[0]
#
# c = str(e)
#
# print(c)
#
# f = strToNameVec(c)
#
# print(f)