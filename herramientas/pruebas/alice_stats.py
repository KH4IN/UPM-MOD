"""Resume nation_stats.csv: mundo por año y clasificacion por poblacion y PIB."""
import collections
import math
import sys

ruta = sys.argv[1]
cada = int(sys.argv[2]) if len(sys.argv) > 2 else 20
tops = int(sys.argv[3]) if len(sys.argv) > 3 else 8
anos = collections.defaultdict(list)
guerras = {}
raros = []
with open(ruta, encoding='utf-8') as f:
    for linea in f:
        c = linea.rstrip('\n').split(';')
        if len(c) < 10:
            continue
        a = int(c[0])
        if c[1] == '---':
            guerras[a] = int(c[9])
            continue
        v = [float(x) if x not in ('nan', '-nan(ind)', 'inf', '-inf') else math.nan for x in c[2:8]]
        if any(math.isnan(x) or math.isinf(x) for x in v):
            raros.append((a, c[1], c[2:8]))
        anos[a].append((c[1], v))
for a in sorted(anos):
    if (a - min(anos)) % cada and a != max(anos):
        continue
    d = anos[a]
    pob = sum(x[1][0] for x in d if not math.isnan(x[1][0]))
    pib = sum(x[1][1] for x in d if not math.isnan(x[1][1]))
    neg = sum(1 for x in d if x[1][1] < 0)
    print(f'{a}: {len(d)} paises, {pob / 1e6:.0f} M hab., PIB {pib / 1e6:.1f} M, {neg} con PIB negativo, {guerras.get(a, "?")} guerras')
    orden = sorted(d, key=lambda x: -x[1][0])[:tops]
    print('   pob:', ', '.join(f'{x[0]} {x[1][0] / 1e6:.0f}' for x in orden))
    orden = sorted(d, key=lambda x: -x[1][1])[:tops]
    print('   pib:', ', '.join(f'{x[0]} {x[1][1] / 1e6:.1f}' for x in orden))
print('valores no numericos:', len(raros), raros[:5])
