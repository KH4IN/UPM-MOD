"""Resume las guerras de una partida con -stats: guerras a la vez, batallas, paises en guerra y paises que desaparecen.

Uso: python -I alice_guerras.py <carpeta con nation_stats.csv y limit_stats.csv> [cada cuantos anos] [sufijo, p. ej. _g1]
"""
import collections
import sys

carpeta = sys.argv[1]
cada = int(sys.argv[2]) if len(sys.argv) > 2 else 25
suf = sys.argv[3] if len(sys.argv) > 3 else ''

tablas = collections.defaultdict(dict)
with open(carpeta + '\\limit_stats%s.csv' % suf, encoding='utf-8') as f:
    for l in f:
        a, t, u, _ = l.strip().split(';')
        tablas[int(a)][t] = int(u)

paises = collections.defaultdict(dict)   # ano -> etiqueta -> (provincias, en guerra)
with open(carpeta + '\\nation_stats%s.csv' % suf, encoding='utf-8') as f:
    for l in f:
        c = l.rstrip('\n').split(';')
        if len(c) >= 10 and c[1] != '---':
            paises[int(c[0])][c[1]] = (int(c[8]), c[9] == '1')

anos = sorted(paises)
print('anos', anos[0], 'a', anos[-1])
print('ano;paises;en guerra;guerras;participantes;batallas de tierra;regimientos;rebeldes;movilizados')
for a in anos:
    if a != anos[0] and a != anos[-1] and a % cada:
        continue
    t = tablas.get(a, {})
    print(';'.join(str(x) for x in (
        a, len(paises[a]), sum(1 for p in paises[a].values() if p[1]), t.get('war'), t.get('war_participant'),
        t.get('land_battle'), t.get('regiment'), t.get('rebel_regiment'), t.get('mobilized_regiment'))))

for clave, nombre in (('war', 'guerras a la vez'), ('war_participant', 'participantes'), ('wargoal', 'objetivos de guerra'),
                      ('land_battle', 'batallas de tierra a la vez'), ('naval_battle', 'batallas navales a la vez')):
    serie = [(tablas[a].get(clave, 0), a) for a in anos if a in tablas]
    if serie:
        print('%s: media %.1f, pico %d en %d' % (nombre, sum(v for v, _ in serie) / len(serie), *max(serie)))
print('paises en guerra, media por ano: %.1f' % (sum(sum(1 for p in paises[a].values() if p[1]) for a in anos) / len(anos)))

primero, ultimo = paises[anos[0]], paises[anos[-1]]
print('paises al principio', len(primero), '| al final', len(ultimo),
      '| desaparecen', len(set(primero) - set(ultimo)), '| aparecen', len(set(ultimo) - set(primero)))
cambios = sorted(((ultimo.get(t, (0,))[0] - primero.get(t, (0,))[0], t) for t in set(primero) | set(ultimo)))
print('mas provincias perdidas:', ', '.join('%s %+d' % (t, d) for d, t in cambios[:10]))
print('mas provincias ganadas:', ', '.join('%s %+d' % (t, d) for d, t in cambios[::-1][:10]))
