import os
import matplotlib.pyplot as plt
import numpy


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
    delta_angle = 720 / len(lst[0])
    for cycle in lst:
        start = int((len(cycle) / 720) * 310)
        end = 1 + int((len(cycle) / 720) * 410)
        d.append(max(((cycle[i + 1] - cycle[i]) / delta_angle) for i in range(start, end)))
    return sum(d) / len(d)


def get_constant(lst):
    p = []
    for row in lst:
        start = int((len(row) / 720) * 170)
        end = 1 + int((len(row) / 720) * 190)
        p_atm = 0.101325
        p.append((sum(row[start:end]) / (end - start)) - p_atm)
    return sum(p) / len(p)


def run():
    for filename in os.listdir('files'):
        file = get_data('files/' + filename)
        cols = list(zip(*file))
        pom4 = get_cycle_starts(cols)
        if not (-1 <= cols[2][pom4[0]] <= 1):
            pom4 = pom4[1:]
        min_length = min([pom4[i + 2] - pom4[i] for i in range(0, len(pom4) - 2, 2)]) + 1

        cyklus2orezany = slice_(get_cycle(cols[2], pom4), min_length)
        cyklus3orezany = slice_(get_cycle(cols[2], pom4), min_length)
        cyklus4orezany = slice_(get_cycle(cols[3], pom4), min_length)
        delta = get_delta(cyklus3orezany)

        c = abs(get_constant(cyklus3orezany))

        priemernehodnoty2stlpec = get_avg(cyklus2orezany, min_length)
        priemernehodnoty3stlpec = get_avg(cyklus3orezany, min_length, c)
        priemernehodnoty4stlpec = get_avg(cyklus4orezany, min_length)

        x = numpy.linspace(0, 720, num=len(priemernehodnoty3stlpec))
        a = numpy.array(list(zip(x, priemernehodnoty3stlpec)))
        a = numpy.matrix.transpose(a).tolist()
        ax.plot(*a, label=filename)
        print(filename, delta)


if __name__ == '__main__':
    run()
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
    plt.savefig('output.jpg', bbox_extra_artists=(legend, ), bbox_inches='tight')

    # avg = sum(priemernehodnoty3stlpec[1255:1402]) / (1402-1255)
