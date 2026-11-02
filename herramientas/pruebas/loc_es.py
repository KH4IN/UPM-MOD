"""Compara alice.csv en ingles y en espanol: vacias, ausentes y variables distintas."""
import re
import sys

base = sys.argv[1]


def leer(ruta):
    d = {}
    with open(ruta, 'rb') as f:
        t = f.read().decode('utf-8-sig', 'replace').replace('\r', '')
    for n, l in enumerate(t.split('\n'), 1):
        if ';' in l and not l.startswith('#'):
            k, v = l.split(';', 1)
            d[k] = (v, n)
    return d


en = leer(base + r'\en-US\alice.csv')
es = leer(base + r'\es-ES\alice.csv')
var = re.compile(r'\$\w+\$')
vacias = [k for k, (v, _) in es.items() if not v.strip() and en.get(k, ('', 0))[0].strip()]
ausentes = [k for k in en if k not in es and en[k][0].strip()]
distintas = []
for k, (v, _) in es.items():
    if k in en and v.strip() and sorted(var.findall(v)) != sorted(var.findall(en[k][0])):
        distintas.append(k)
print(len(en), 'en;', len(es), 'es')
print('vacias', len(vacias))
for k in vacias[:60]:
    print('  ', k, '|', en[k][0][:70])
print('ausentes', len(ausentes), ausentes[:10])
print('variables distintas', len(distintas))
for k in distintas[:40]:
    print('  ', k, '| en', sorted(var.findall(en[k][0])), '| es', sorted(var.findall(es[k][0])))
