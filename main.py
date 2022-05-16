import matplotlib.pyplot as plt
import numpy

with open('data.TXT', 'r') as file:
    # file = file.read().split('\n')[:-1]
    file = file.read().split('\n')
file = [[float(x) for x in i.split()] for i in file]

stlpce = [[] for _ in range(4)]
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
for i in range(0, len(pom4) - 2, 2):
    cyklus.append(stlpce[2][pom4[i]:pom4[i + 2]+1])

pom5 = min([len(row) for row in cyklus])
pom6 = [row[:pom5] for row in cyklus]

priemernehodnotydruhystlpec = [sum([row[i] for row in pom6]) / len(pom6) for i in range(pom5)]

cyklus3 = [stlpce[2][pom4[i]:pom4[i + 2]+1] for i in range(0, len(pom4) - 2, 2)]
cyklus4 = [stlpce[3][pom4[i]:pom4[i + 2]+1] for i in range(0, len(pom4) - 2, 2)]

pom5 = min([len(row) for row in cyklus3])

cyklus3orezany = [cyklus3[i][:pom5] for i in range(len(cyklus3))]
cyklus4orezany = [cyklus4[i][:pom5] for i in range(len(cyklus3))]

priemernehodnoty3stlpec = [sum([row[i] for row in cyklus3orezany]) / len(pom6) + 1.1335 for i in range(pom5)]
priemernehodnoty4stlpec = [sum([row[i] for row in cyklus4orezany]) / len(pom6) for i in range(pom5)]

k = 0
x = []
for i in range(len(priemernehodnoty3stlpec)):
    k += 720 / len(priemernehodnoty3stlpec)
    x.append(k)

a = numpy.array(list(zip(priemernehodnoty3stlpec, x)))
xd = numpy.matrix.transpose(a).tolist()
# ax.plot(priemernehodnotydruhystlpec)
ax.plot(xd[1], xd[0])

avg = sum(priemernehodnoty3stlpec[1155:1292]) / (1292-1155)

# ax.plot(priemernehodnoty4stlpec)
# plt.xlabel('crank angle')
# plt.ylabel('pressure')
# plt.ylim([0.8, 1.5])
# plt.show()
plt.vlines(216, 0, 7, colors=['red'], label='SZ')
plt.vlines(360, 0, 7, colors=['black'], label='HÚ')
plt.vlines(507, 0, 7, colors=['yellow'], label='VO')
plt.legend()
plt.savefig('test.jpg')
