import matplotlib.pyplot as plt

with open('NG-1400-100SK-27BTDC.TXT', 'r') as file:
    # file = file.read().split('\n')[:-1]
    file = file.read().split('\n')
file = [[float(x) for x in i.split()] for i in file]

stlpce = [[] for _ in range(5)]
for row in file:
    for i in range(len(row)):
        stlpce[i].append(row[i])

fig, ax = plt.subplots()

pom3 = [i for i in range(len(stlpce[1])) if stlpce[1][i] < -1.8]

pom4 = []
for i in range(len(pom3) - 1):
    if pom3[i + 1] - pom3[i] > 10:
        pom4.append(pom3[i])

cyklus = []
for i in range(1, len(pom4) - 2, 2):
    cyklus.append(stlpce[2][pom4[i]:pom4[i + 2]+1])

pom5 = min([len(row) for row in cyklus])
pom6 = [row[:pom5] for row in cyklus]

priemernehodnotydruhystlpec = [sum([row[i] for row in pom6]) / len(pom6) for i in range(pom5)]

cyklus3 = [stlpce[2][pom4[i]:pom4[i + 2]+1] for i in range(1, len(pom4) - 2, 2)]
cyklus4 = [stlpce[3][pom4[i]:pom4[i + 2]+1] for i in range(1, len(pom4) - 2, 2)]
cyklus5 = [stlpce[4][pom4[i]:pom4[i + 2]+1] for i in range(1, len(pom4) - 2, 2)]

pom5 = min([len(row) for row in cyklus3])

cyklus3orezany = [cyklus3[i][:pom5] for i in range(len(cyklus3))]
cyklus4orezany = [cyklus4[i][:pom5] for i in range(len(cyklus3))]
cyklus5orezany = [cyklus5[i][:pom5] for i in range(len(cyklus3))]

priemernehodnoty3stlpec = [sum([row[i] for row in cyklus3orezany]) / len(pom6) for i in range(pom5)]
priemernehodnoty4stlpec = [sum([row[i] for row in cyklus4orezany]) / len(pom6) + 1.1335 for i in range(pom5)]
priemernehodnoty5stlpec = [sum([row[i] for row in cyklus5orezany]) / len(pom6) for i in range(pom5)]

k = 0
x = []
for i in range(len(priemernehodnoty4stlpec)):
    k += 720 / priemernehodnoty4stlpec[i]
    x.append(k)

ax.plot(priemernehodnoty3stlpec)
ax.plot(priemernehodnoty4stlpec)
ax.plot(priemernehodnoty5stlpec)
plt.xlabel('crank angle')
plt.ylabel('pressure')
plt.ylim([0.8, 1.5])
# plt.show()
plt.savefig('test.jpg')
