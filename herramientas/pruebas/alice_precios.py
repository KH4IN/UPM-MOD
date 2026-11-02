"""Evolucion de precios por mercancia a partir de commodity_stats.csv."""
import collections
import sys

ruta = sys.argv[1]
d = collections.defaultdict(dict)
with open(ruta, encoding='utf-8') as f:
    for l in f:
        c = l.rstrip('\n').split(';')
        if len(c) == 4:
            d[c[1]][int(c[0])] = (float(c[2]), float(c[3]))
anos = sorted({a for v in d.values() for a in v})
print('años', anos[0], anos[-1], 'mercancias', len(d))
marcas = [a for a in anos if (a - anos[0]) % 20 == 0] + [anos[-1]]
fil = []
for k, v in d.items():
    maxim = max(x[1] for x in v.values())
    fil.append((maxim, k, v))
fil.sort(key=lambda x: x[0], reverse=True)
print('mayor precio maximo (mercado mas caro); media por mercado en', marcas)
for maxim, k, v in fil[:18]:
    medias = ' '.join(f'{v[a][0]:.1f}' if a in v else '-' for a in marcas)
    an = max(v, key=lambda a: v[a][1])
    print(f'{k:24} max {maxim:12.1f} ({an}) | {medias}')
# indice medio de precios (media simple de las medias)
print('indice medio:')
for a in marcas:
    x = [v[a][0] for v in d.values() if a in v]
    print(a, round(sum(x) / len(x), 2))
