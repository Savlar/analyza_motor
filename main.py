import matplotlib.pyplot as plt

with open('data.TXT', 'r') as file:
    file = file.read().split('\n')[:-1]
file = [[float(x) for x in i.split()] for i in file]

stlpce = [[] for _ in range(4)]
for row in file:
    for i in range(len(row)):
        stlpce[i].append(row[i])

fig, ax = plt.subplots()
#
# ax.plot([row[3] for row in file[:2000]])
#
# plt.show()

pom3 = [i for i in range(len(file)) if file[i][1] < -1.8]
print(pom3)

pom4 = []
for i in range(len(pom3) - 1):
    if pom3[i + 1] - pom3[i] > 10:
        pom4.append(pom3[i])

print(pom4)

cyklus = []
for i in range(0, len(pom4) - 3, 4):
    cyklus.append(stlpce[2][pom4[i]:pom4[i+4]])
print('cyklus', cyklus)

pom5 = min([len(row) for row in cyklus])
pom6 = [row[:pom5] for row in cyklus]

mean = [sum(row) / pom5 for row in pom6]
ax.plot(pom6[0])
plt.show()
priemernehodnotydruhystlpec = 0
