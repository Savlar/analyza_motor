import matplotlib.pyplot as plt

with open('NG-1400-100SK-27BTDC.TXT', 'r') as file:
    # file = file.read().split('\n')[:-1]
    file = file.read().split('\n')[:9500]
file = [[float(x) for x in i.split()] for i in file]

stlpce = [[] for _ in range(5)]
for row in file:
    for i in range(len(row)):
        stlpce[i].append(row[i])

fig, ax = plt.subplots()

pom3 = [i for i in range(len(file)) if file[i][1] < -1.8]
# print(pom3)

pom4 = []
for i in range(len(pom3) - 1):
    if pom3[i + 1] - pom3[i] > 10:
        pom4.append(pom3[i])

# print(pom4)

cyklus = []
for i in range(1, len(pom4) - 1, 2):
    cyklus.append(stlpce[2][pom4[i]:pom4[i + 2]])
# print('cyklus', cyklus)
#

pom5 = min([len(row) for row in cyklus])
pom6 = [row[:pom5] for row in cyklus]

priemernehodnotydruhystlpec = [sum(row) / len(row) for row in pom6[0]]

print(pom4)
cyklus3 = [stlpce[2][pom4[i]:pom4[i + 2]] for i in range(1, len(pom4) - 1, 2)]
cyklus4 = [stlpce[3][pom4[i]:pom4[i + 2]] for i in range(1, len(pom4) - 1, 2)]
cyklus5 = [stlpce[4][pom4[i]:pom4[i + 2]] for i in range(1, len(pom4) - 1, 2)]

pom5 = min([len(row) for row in cyklus3])

cyklus3orezany = [cyklus3[i][:pom5] for i in range(len(cyklus3))]
cyklus4orezany = [cyklus4[i][:pom5] for i in range(len(cyklus3))]
cyklus5orezany = [cyklus5[i][:pom5] for i in range(len(cyklus3))]

priemernehodnoty3stlpec = [sum(row) / len(row) for row in cyklus3orezany]
priemernehodnoty4stlpec = [sum(row) / len(row) for row in cyklus4orezany]
priemernehodnoty5stlpec = [sum(row) / len(row) for row in cyklus5orezany]

k = 0
x = []
for i in range(len(priemernehodnoty4stlpec)):
    k += 720 / priemernehodnoty4stlpec[i]
    x.append(k)

dataobr3 = zip(x, priemernehodnoty3stlpec)

ax.plot(*dataobr3)
plt.show()
