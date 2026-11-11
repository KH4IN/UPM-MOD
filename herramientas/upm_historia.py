"""Correcciones de historia del UPM, con su fecha y su motivo. Solo para la copia que usa Project Alice.

Uso: python -I upm_historia.py <carpeta del juego con mod/UPM>
Se puede repetir: lo ya aplicado no se vuelve a aplicar.

El UPM da a cada pais un solo valor de religion, cultura y capital para sus 11 fechas de inicio.
Alice lee esos datos tambien dentro de un bloque con fecha, asi que un cambio historico se escribe
como un bloque nuevo al final del archivo, que se aplica a esa fecha y a las posteriores.
"""
import os
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import upm_fecha  # noqa: E402

FECHAS = ['1492.1.1', '1579.1.1', '1618.1.1', '1701.1.1', '1776.1.1', '1803.1.1', '1836.1.2', '1900.1.1',
          '1936.7.17', '1945.9.2', '2000.1.1']

# (pais, desde, dato, valor, motivo)
# Reforma protestante: el juego base los da como protestantes en 1836, y la poblacion del propio UPM
# pasa a ser protestante en su fecha de 1618 (la de 1579 repite la de 1492, catolica).
PROTESTANTES = ['PRU', 'SWE', 'DEN', 'SAX', 'HES', 'MEC', 'NAS', 'HOL', 'COB', 'OLD', 'BRA', 'FRM', 'SWI']
FECHADAS = [(t, '1618.1.1', 'religion', 'protestant', 'Reforma protestante') for t in PROTESTANTES] + [
    # Berlin es de PRU en el UPM desde su fecha de 1701, y es la capital de Prusia en el juego base.
    ('PRU', '1701.1.1', 'capital', '549', 'capital en Berlin'),
]

# Paises con la cultura de relleno "dummy": su religion, si no sale bien de su poblacion.
RELIGION_FIJA = {
    # Dominios japoneses: como TKG en el UPM y Japon en el juego base; su poblacion de 1579 figura como shinto.
    'CHO': 'mahayana', 'KAG': 'mahayana', 'SAT': 'mahayana', 'SEN': 'mahayana', 'TOS': 'mahayana', 'YZW': 'mahayana',
}
# Y su cultura: Peru del Sur, como Peru y Bolivia en el UPM, aunque su poblacion sea quechua en un 57 %.
CULTURA_FIJA = {'SPU': 'south_andean'}
RELLENO_CULTURA, RELLENO_RELIGION = 'dummy', 'shamanism'


def leer(p):
    with open(p, 'rb') as f:
        return f.read()


def archivos(raiz):
    """Etiqueta -> archivo de history/countries del mod."""
    d = {}
    carpeta = os.path.join(raiz, 'history', 'countries')
    for f in os.listdir(carpeta):
        if f.lower().endswith('.txt'):
            d[f[:3].upper()] = os.path.join(carpeta, f)
    return d


def cabeza(a):
    """Posicion del primer bloque con fecha: lo anterior vale para todas las fechas."""
    m = re.search(rb'(?m)^\s*\d{3,4}\.\d+\.\d+\s*=\s*\{', a)
    return m.start() if m else len(a)


def poner_base(a, clave, viejo, nuevo):
    fin = cabeza(a)
    b, n = re.subn(rb'(?m)^(\s*' + clave.encode() + rb'\s*=\s*)' + viejo.encode() + rb'\b', rb'\g<1>' + nuevo.encode(), a[:fin], count=1)
    return b + a[fin:], n


def bloque(desde, lineas):
    return ('\r\n# upm_historia\r\n%s = {\r\n%s}\r\n' % (desde, ''.join('\t%s\r\n' % l for l in lineas))).encode('cp1252')


def marcadores(raiz):
    """Culturas zzz_religion_*: el UPM marca con ellas la religion de Estado para sus decisiones."""
    return set(re.findall(rb'\bzzz_religion_(\w+)\s*=', leer(os.path.join(raiz, 'common', 'cultures.txt'))))


def main():
    juego = sys.argv[1]
    raiz = os.path.join(juego, 'mod', 'UPM')
    arch = archivos(raiz)
    marcas = marcadores(raiz)
    total = 0

    # 1. Cambios con fecha.
    por_pais = {}
    for t, desde, clave, valor, motivo in FECHADAS:
        por_pais.setdefault((t, desde), []).append((clave, valor, motivo))
    for (t, desde), cambios in sorted(por_pais.items()):
        a = leer(arch[t])
        lineas = []
        for clave, valor, motivo in cambios:
            lineas.append('%s = %s # %s' % (clave, valor, motivo))
            if clave == 'religion':
                vieja = re.search(rb'(?m)^\s*religion\s*=\s*(\w+)', a[:cabeza(a)])
                if vieja and vieja.group(1) in marcas and valor.encode() in marcas:
                    lineas.append('remove_culture = zzz_religion_%s' % vieja.group(1).decode())
                    lineas.append('culture = zzz_religion_%s' % valor)
        nuevo = bloque(desde, lineas)
        if nuevo.strip() in a:
            continue
        with open(arch[t], 'wb') as f:
            f.write(a.rstrip() + b'\r\n' + nuevo)
        total += 1
        print('%s desde %s: %s' % (t, desde, '; '.join('%s = %s' % c[:2] for c in cambios)))

    # 2. Cultura y religion de relleno: se toman de la poblacion del pais en su primera fecha con provincias.
    pendientes = {}
    for t, p in arch.items():
        m = re.search(rb'(?m)^\s*primary_culture\s*=\s*(\w+)', leer(p)[:cabeza(leer(p))])
        if m and m.group(1).decode() == RELLENO_CULTURA:
            pendientes[t] = None
    for ft in FECHAS:
        if not any(v is None for v in pendientes.values()):
            break
        mundo = upm_fecha.Mundo(juego, upm_fecha.fecha(ft))
        for t in pendientes:
            if pendientes[t] is None and mundo.total[t] > 0:
                pendientes[t] = (ft, mundo.cultura[t].most_common(1)[0][0], mundo.religion[t].most_common(1)[0][0],
                                 mundo.religion[t][RELLENO_RELIGION])
    for t, v in sorted(pendientes.items()):
        if v is None:
            continue
        ft, cultura, religion, con_relleno = v
        cultura = CULTURA_FIJA.get(t, cultura)
        a = leer(arch[t])
        b, n = poner_base(a, 'primary_culture', RELLENO_CULTURA, cultura)
        # la cultura principal no se repite como aceptada
        b = re.sub(rb'(?m)^\s*culture\s*=\s*' + cultura.encode() + rb'\b[^\r\n]*\r?\n', b'', b[:cabeza(b)], count=1) + b[cabeza(b):]
        hecho = ['primary_culture = %s' % cultura] if n else []
        religion = RELIGION_FIJA.get(t, religion)
        if con_relleno == 0:
            b, k = poner_base(b, 'religion', RELLENO_RELIGION, religion)
            if k:
                hecho.append('religion = %s' % religion)
                if religion.encode() in marcas:
                    b, _ = poner_base(b, 'culture', 'zzz_religion_' + RELLENO_RELIGION, 'zzz_religion_' + religion)
        if b != a:
            with open(arch[t], 'wb') as f:
                f.write(b)
            total += 1
            print('%s (poblacion de %s): %s' % (t, ft, '; '.join(hecho)))
    print('total', total)


if __name__ == '__main__':
    main()
