"""Serie por paises: PIB, poblacion, tesoro, provincias y guerra cada N años."""
import collections
import sys

ruta, cada = sys.argv[1], int(sys.argv[2])
tags = sys.argv[3:]
d = collections.defaultdict(dict)
total = collections.defaultdict(float)
with open(ruta, encoding='utf-8') as f:
    for l in f:
        c = l.rstrip('\n').split(';')
        if len(c) < 10 or c[1] == '---':
            continue
        a = int(c[0])
        d[c[1]][a] = c
        total[a] += float(c[3])
anos = sorted(total)
print('año   PIB mundial')
for a in anos[::cada]:
    print(a, round(total[a]))
for t in tags:
    print('---', t, '(año pob_M pib pib/hab tesoro prov guerra)')
    for a in anos[::cada]:
        c = d[t].get(a)
        if c:
            pob, pib = float(c[2]), float(c[3])
            print(a, round(pob / 1e6, 1), round(pib), round(pib / max(pob, 1) * 1e6, 1), round(float(c[7])), c[8], c[9])
