"""Guerras de history/wars del UPM que siguen abiertas en una fecha de inicio.

Uso: python -I upm_guerras.py <carpeta del juego con mod/UPM> <fecha, p. ej. 1836.1.2>
Una guerra empieza con add_attacker y add_defender en un bloque con fecha y acaba cuando un bloque
posterior quita a todos los de un bando con rem_attacker o rem_defender.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import upm_fecha  # noqa: E402

juego, hasta = sys.argv[1], upm_fecha.fecha(sys.argv[2])
carpeta = os.path.join(juego, 'mod', 'UPM', 'history', 'wars')
abiertas = 0
for f in sorted(os.listdir(carpeta)):
    if not f.lower().endswith('.txt'):
        continue
    pares = upm_fecha.analizar(upm_fecha.leer(os.path.join(carpeta, f)))
    nombre = next((v for k, v in pares if k == 'name' and isinstance(v, str)), f)
    atacan, defienden, objetivos, inicio = [], [], 0, None
    for d, bloque in sorted((upm_fecha.fecha(k), v) for k, v in pares if isinstance(v, list) and upm_fecha.fecha(k)):
        if d > hasta:
            break
        for k, v in bloque:
            if k == 'add_attacker':
                atacan.append(v)
                inicio = inicio or d
            elif k == 'add_defender':
                defienden.append(v)
            elif k == 'rem_attacker' and v in atacan:
                atacan.remove(v)
            elif k == 'rem_defender' and v in defienden:
                defienden.remove(v)
            elif k == 'war_goal':
                objetivos += 1
    if atacan and defienden:
        abiertas += 1
        print('%s | %s | desde %s | atacan %s | defienden %s | objetivos %d' % (
            f, nombre, '.'.join(str(x) for x in inicio), ' '.join(atacan), ' '.join(defienden), objetivos))
print('guerras abiertas el %s: %d' % (sys.argv[2], abiertas))
