"""Resume limit_stats.csv: uso de cada tabla del motor y año en que se llenaría a este ritmo."""
import sys

filas = {}
with open(sys.argv[1], encoding='utf-8') as f:
    for linea in f:
        ano, tabla, usadas, tope = linea.strip().split(';')
        filas.setdefault(tabla, []).append((int(ano), int(usadas), int(tope)))

salida = []
for tabla, serie in filas.items():
    ano, usadas, tope = serie[-1]
    # ritmo de los últimos 10 años registrados
    ano0, usadas0, _ = serie[max(0, len(serie) - 11)]
    ritmo = (usadas - usadas0) / max(ano - ano0, 1)
    pico = max(u for _, u, _ in serie)
    lleno = int(ano + (tope - usadas) / ritmo) if ritmo > 0 else None
    salida.append((pico / tope, tabla, usadas, pico, tope, ritmo, lleno))

print('tabla;último;pico;tope;% pico;filas/año;año lleno')
for parte, tabla, usadas, pico, tope, ritmo, lleno in sorted(salida, reverse=True):
    print(f'{tabla};{usadas};{pico};{tope};{parte * 100:.1f};{ritmo:.1f};{lleno or "-"}')
