import math
from math import log, e
import os
import matplotlib.pyplot as plt
import numpy
from math import sin, cos, sqrt, pi, floor, radians as rad


fig = plt.figure()
ax = fig.add_subplot(111)


def get_data(filename):
    with open(filename, 'r') as input_:
        input_ = input_.read().split('\n')
    if len(input_[-1]) == 0:
        input_ = input_[:-1]
    return [[float(val) for val in row.split()] for row in input_]


def get_cycle(lst, hu):
    return [lst[hu[i]:hu[i + 2]+1] for i in range(0, len(hu) - 2, 2)]


def get_cycle_starts(cols):
    pom3 = [i for i in range(len(cols[1])) if cols[1][i] < -1.8]

    hu = []
    for i in range(len(pom3) - 1):
        if pom3[i + 1] - pom3[i] > 10:
            hu.append(pom3[i])
    return hu


def slice_(lst, length):
    return [lst[i][:length] for i in range(len(lst))]


def get_avg(lst, length, correction=0.):
    return [sum([row[i] for row in lst]) / len(lst) + correction for i in range(length)]


def get_delta(lst):
    d = []
    items_per_deg = len(lst[0]) / 720
    items = 111
    angles = numpy.linspace(310, 410, num=items)
    for cycle in lst:
        tmp = []
        for i in range(len(angles) - 1):
            x1 = cycle[int(items_per_deg * angles[i])]
            x2 = cycle[int(items_per_deg * angles[i + 1])]
            tmp.append((x2 - x1) / (100 / items))
        d.append(max(tmp))
    return d


def get_constant(lst):
    p = []
    for row in lst:
        start = int((len(row) / 720) * 170)
        end = 1 + int((len(row) / 720) * 190)
        p_atm = 0.101325
        p.append((sum(row[start:end]) / (end - start)) - p_atm)
    return sum(p) / len(p)


def graph(lst):
    v_alpha = []
    p_alpha = []
    D = 0.075
    r = 0.0388
    l = 0.1265
    angles = numpy.linspace(0, 719, num=720)
    for alpha in angles:
        p_alpha.append(lst[floor((len(lst) / 720) * alpha)])
        v_alpha.append(((pi * pow(D, 2)) / 4) *
                       ((r * (1 - cos(rad(alpha)))) + l *
                        (1 - sqrt(1 - pow(r / l, 2) * pow(sin(rad(alpha)), 2)))) + 0.000029809)
    p_i = (1 / 0.000343) * sum(((p_alpha[i + 1] + p_alpha[i]) / 2) * (v_alpha[i + 1] - v_alpha[i]) for i in range(719))
    n = []
    for i in range(451, 490):
        n.append(log(p_alpha[i] / p_alpha[i + 1]) / log(v_alpha[i + 1] / v_alpha[i]))
    filtered = list(filter(lambda x: 1.2 <= x <= 1.3, n))
    n = sum(filtered) / len(filtered)
    print("n =", n)
    print("p_i =", p_i)
    # ax.set_yscale('log')
    # ax.set_xscale('log')
    # ax.plot(v_alpha, p_alpha)
    # plt.savefig('graph2.jpg')
    KH = []
    for i in range(449,500):
        KH.append(p_alpha[i] * pow(v_alpha[i], 1.15))
    print(max(KH))

    indices = []
    while not len(indices):
        e = 0.00000001
        for dec in reversed(range(4, 8)):
            for item in v_alpha:    
                if item - e <= round(max(KH), dec) <= item + e:
                    indices.append(v_alpha.index(item))
            e *= 10
    indices = sorted(list(filter(lambda x: 360 <= x <= 390, indices)))
    print(indices)
    ppi = []
    for i in range(719):
        ppi.append(p_alpha[i + 1] - (p_alpha[i] * pow((v_alpha[i] / v_alpha[i + 1]), n)))
    delta_pci = []
    for i in range(719):
        delta_pci.append(ppi[i] * (v_alpha[i] / v_alpha[359]))
    x_a = []
    start_comb = 340
    with open('values.txt', 'w') as file:
        for i in range(start_comb, 401):
            x_a.append((sum(delta_pci[j] for j in range(start_comb, i))) / (sum(delta_pci[j] for j in range(start_comb, indices[0]))))
            file.write(str(x_a[-1]) + '\n')
    for num in [359, 719]:
        print(v_alpha[num])
    ax.plot(angles[start_comb:401], x_a)


def draw_p_alpha_graph(lst, filename):
    x = numpy.linspace(0, 720, num=len(lst))
    a = numpy.array(list(zip(x, lst)))
    a = numpy.matrix.transpose(a).tolist()
    ax.plot(*a, label=filename)


def add_p_alpha_graph_legend():
    # plt.ylim([0.8, 1.5])
    plt.vlines(216, 0, 7, colors=['blue'])
    plt.vlines(360, 0, 7, colors=['black'])
    plt.vlines(507, 0, 7, colors=['red'])
    plt.vlines(720, 0, 7, colors=['black'], label='Horná úvrať')
    plt.vlines(180, 0, 7, colors=['green'])
    plt.vlines(540, 0, 7, colors=['green'], label='Dolná úvrať')
    plt.vlines(22, 0, 7, colors=['red'], label='Výfukový ventil')
    plt.vlines(704, 0, 7, colors=['blue'], label='Sací ventil')
    plt.xlabel('Uhol natočenia KH (º)')
    plt.ylabel('Tlak (MPa)')
    plt.title('p - α diagram')
    plt.xticks([*range(90, 721, 90)] + [22, 216, 507], fontsize=7.5)
    legend = ax.legend(loc='upper center', bbox_to_anchor=(1.35, 0.9))
    plt.savefig('output.jpg', bbox_extra_artists=(legend,), bbox_inches='tight')


def get_p_data(filename):
    file = get_data('files/' + filename)
    cols = list(zip(*file))
    pom4 = get_cycle_starts(cols)
    if not (-1 <= cols[2][pom4[0]] <= 1):
        pom4 = pom4[1:]
    min_length = min([pom4[i + 2] - pom4[i] for i in range(0, len(pom4) - 2, 2)]) + 1

    cyklus2orezany = slice_(get_cycle(cols[2], pom4), min_length)
    cyklus3orezany = slice_(get_cycle(cols[2], pom4), min_length)
    cyklus4orezany = slice_(get_cycle(cols[3], pom4), min_length)

    c = abs(get_constant(cyklus3orezany))

    priemernehodnoty2stlpec = get_avg(cyklus2orezany, min_length)
    priemernehodnoty3stlpec = get_avg(cyklus3orezany, min_length, c)
    priemernehodnoty4stlpec = get_avg(cyklus4orezany, min_length)
    return priemernehodnoty3stlpec, cyklus3orezany


if __name__ == '__main__':
    for file in os.listdir('files'):
        print(file)
        # file = 'N2NG50-1500-100SK-27BTDC (1).txt'
        priemernehodnoty3stlpec, cyklus3orezany = get_p_data(file)

        # max_angle = priemernehodnoty3stlpec.index(max(priemernehodnoty3stlpec)) * (720 / len(priemernehodnoty3stlpec))

        # draw_p_alpha_graph(priemernehodnoty3stlpec, filename)
        graph(priemernehodnoty3stlpec)
        print(len(priemernehodnoty3stlpec))
#        for cycle in cyklus3orezany:
 #           graph(cycle)
        delta = get_delta(cyklus3orezany)
        print(file, max(delta))
        print(sum(delta) / len(delta))
    plt.savefig('hihi.jpg')
    # add_p_alpha_graph_legend()

    # avg = sum(priemernehodnoty3stlpec[1255:1402]) / (1402-1255)
