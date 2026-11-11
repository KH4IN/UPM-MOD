"""Resume el mundo del UPM en una fecha de inicio: dueños, provincias, población y avisos.

Uso: python -I upm_fecha.py <carpeta del juego con mod/UPM> <fecha, p. ej. 1492.1.1> [n paises]
     python -I upm_fecha.py <carpeta del juego con mod/UPM> comparar <fecha del base> <fecha del UPM>
Lee el mod encima del juego base, como hace el juego: un archivo del mod tapa al del base con la misma ruta.
"""
import collections
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
TOKEN = re.compile(r'"[^"]*"|[{}=]|[^\s{}=#"]+')


def analizar(texto):
    """Devuelve una lista de pares (clave, valor); un valor es texto o otra lista."""
    fichas = TOKEN.findall(re.sub(r'#[^\r\n]*', '', texto))
    pos = 0

    def bloque():
        nonlocal pos
        pares = []
        while pos < len(fichas):
            f = fichas[pos]
            pos += 1
            if f == '}':
                break
            if pos < len(fichas) and fichas[pos] == '=':
                pos += 1
                if pos < len(fichas) and fichas[pos] == '{':
                    pos += 1
                    pares.append((f, bloque()))
                elif pos < len(fichas):
                    pares.append((f, fichas[pos].strip('"')))
                    pos += 1
            elif f == '{':
                pares.append(('', bloque()))
            else:
                pares.append((f.strip('"'), None))
        return pares

    return bloque()


def leer(ruta):
    with open(ruta, 'rb') as f:
        return f.read().decode('cp1252', 'replace')


def fecha(texto):
    m = re.fullmatch(r'(\d{1,4})\.(\d{1,2})\.(\d{1,2})', texto)
    return tuple(int(x) for x in m.groups()) if m else None


def raices(juego, con_mod):
    return (juego, os.path.join(juego, 'mod', 'UPM')) if con_mod else (juego,)


def capas(juego, rel, con_mod=True):
    """Archivos .txt de una carpeta, con los del mod tapando a los del juego base."""
    vistos = {}
    for raiz in raices(juego, con_mod):
        base = os.path.join(raiz, *rel.split('/'))
        for d, _, fs in os.walk(base):
            for f in fs:
                if f.lower().endswith('.txt'):
                    p = os.path.join(d, f)
                    vistos[os.path.relpath(p, raiz).lower()] = p
    return sorted(vistos.values())


def estado(pares, hasta):
    """Aplica el bloque base y despues los bloques con fecha hasta la pedida, en orden."""
    datos = collections.defaultdict(list)

    def aplicar(lista):
        for k, v in lista:
            if isinstance(v, str):
                datos[k.lower()].append(v)

    aplicar(pares)
    fechados = sorted((fecha(k), v) for k, v in pares if isinstance(v, list) and fecha(k))
    for d, v in fechados:
        if d <= hasta:
            aplicar(v)
    return datos


class Mundo:
    def __init__(self, juego, hasta, con_mod=True):
        self.hasta = hasta
        self.etiquetas = {}
        for p in capas(juego, 'common', con_mod):
            if os.path.basename(p).lower() == 'countries.txt':
                for k, v in analizar(leer(p)):
                    if isinstance(v, str) and re.fullmatch(r'[A-Z][A-Z0-9]{2}', k):
                        self.etiquetas[k] = v

        self.paises = {}
        for p in capas(juego, 'history/countries', con_mod):
            self.paises[os.path.basename(p)[:3].upper()] = estado(analizar(leer(p)), hasta)

        self.provincias = {}
        self.repetidas = []
        for p in capas(juego, 'history/provinces', con_mod):
            m = re.match(r'\s*(\d+)', os.path.basename(p))
            if not m:
                continue
            n = int(m.group(1))
            if n in self.provincias:
                self.repetidas.append(n)
            self.provincias[n] = estado(analizar(leer(p)), hasta)

        self.carpeta = None
        for raiz in reversed(raices(juego, con_mod)):
            base = os.path.join(raiz, 'history', 'pops')
            if not os.path.isdir(base):
                continue
            exacta = os.path.join(base, '%d.%d.%d' % hasta)
            if os.path.isdir(exacta):
                self.carpeta = exacta
                break
            for d in sorted(os.listdir(base)):
                if d.startswith(str(hasta[0]) + '.'):
                    self.carpeta = os.path.join(base, d)
                    break
            if self.carpeta:
                break

        self.pob = collections.Counter()
        self.por_cultura = collections.defaultdict(collections.Counter)
        self.por_religion = collections.defaultdict(collections.Counter)
        for f in sorted(os.listdir(self.carpeta)) if self.carpeta else []:
            if not f.lower().endswith('.txt'):
                continue
            for k, v in analizar(leer(os.path.join(self.carpeta, f))):
                if not (k.isdigit() and isinstance(v, list)):
                    continue
                for _, pop in v:
                    if not isinstance(pop, list):
                        continue
                    d = dict((a, b) for a, b in pop if isinstance(b, str))
                    try:
                        t = int(float(d.get('size', '0')))
                    except ValueError:
                        t = 0
                    self.pob[int(k)] += t
                    self.por_cultura[int(k)][d.get('culture', '?')] += t
                    self.por_religion[int(k)][d.get('religion', '?')] += t

        self.dueno = {n: (d['owner'][-1].upper() if d['owner'] else None) for n, d in self.provincias.items()}
        self.suyas = collections.defaultdict(list)
        for n, t in self.dueno.items():
            if t:
                self.suyas[t].append(n)
        self.total = collections.Counter()
        self.cultura = collections.defaultdict(collections.Counter)
        self.religion = collections.defaultdict(collections.Counter)
        for n, t in self.pob.items():
            d = self.dueno.get(n)
            if d:
                self.total[d] += t
                self.cultura[d].update(self.por_cultura[n])
                self.religion[d].update(self.por_religion[n])


def resumen(juego, hasta, cuantos):
    m = Mundo(juego, hasta)
    print('fecha', '%d.%d.%d' % hasta, '| carpeta de pops:', m.carpeta)
    print('provincias con historia', len(m.provincias), '| con dueño', sum(1 for t in m.dueno.values() if t),
          '| paises con provincias', len(m.suyas), '| poblacion en archivos', sum(m.pob.values()),
          '| de ella, con dueño', sum(m.total.values()))
    print()
    print('pais;provincias;poblacion;capital;gobierno;religion;cultura;mayor cultura real;mayor religion real')
    for t, _ in sorted(m.suyas.items(), key=lambda x: -m.total[x[0]])[:cuantos]:
        h = m.paises.get(t, {})

        def u(k):
            return h[k][-1] if h and h[k] else '-'

        mc = m.cultura[t].most_common(1)
        mr = m.religion[t].most_common(1)
        print(';'.join(str(x) for x in (
            t, len(m.suyas[t]), m.total[t], u('capital'), u('government'), u('religion'), u('primary_culture'),
            '%s %d%%' % (mc[0][0], 100 * mc[0][1] // max(m.total[t], 1)) if mc else '-',
            '%s %d%%' % (mr[0][0], 100 * mr[0][1] // max(m.total[t], 1)) if mr else '-')))

    print()
    avisos = collections.OrderedDict()
    avisos['dueños que no estan en countries.txt'] = sorted(t for t in m.suyas if t not in m.etiquetas)
    avisos['dueños sin archivo en history/countries'] = sorted(t for t in m.suyas if t not in m.paises)
    # pais:capital>dueño real de esa provincia
    avisos['paises cuya capital no es suya'] = sorted(
        '%s:%s>%s' % (t, m.paises[t]['capital'][-1], m.dueno.get(int(m.paises[t]['capital'][-1])) or 'nadie')
        for t in m.suyas if m.paises.get(t) and m.paises[t]['capital'] and m.paises[t]['capital'][-1].isdigit()
        and m.dueno.get(int(m.paises[t]['capital'][-1])) != t)
    avisos['provincias con dueño y sin poblacion'] = sorted(n for n, t in m.dueno.items() if t and not m.pob.get(n))
    avisos['provincias con poblacion y sin dueño'] = sorted(n for n in m.pob if m.pob[n] and not m.dueno.get(n))
    avisos['provincias con poblacion y sin historia'] = sorted(n for n in m.pob if n not in m.provincias)
    avisos['numeros de provincia con dos archivos'] = sorted(set(m.repetidas))
    for k, v in avisos.items():
        print('%s: %d %s' % (k, len(v), v[:25]))


def comparar(juego, fecha_base, fecha_mod):
    """Diferencias entre el juego base y el UPM en una misma epoca."""
    a, b = Mundo(juego, fecha_base, con_mod=False), Mundo(juego, fecha_mod)
    print('base %d.%d.%d' % fecha_base, '| provincias con dueño', sum(1 for t in a.dueno.values() if t),
          '| paises', len(a.suyas), '| poblacion', sum(a.pob.values()))
    print('UPM  %d.%d.%d' % fecha_mod, '| provincias con dueño', sum(1 for t in b.dueno.values() if t),
          '| paises', len(b.suyas), '| poblacion', sum(b.pob.values()))
    cambios = collections.Counter()
    for n in sorted(set(a.dueno) | set(b.dueno)):
        x, y = a.dueno.get(n), b.dueno.get(n)
        if x != y:
            cambios[(x or 'nadie', y or 'nadie')] += 1
    print('provincias con otro dueño:', sum(cambios.values()), '| solo en el UPM:', len(set(b.dueno) - set(a.dueno)))
    print('cambio de dueño (base>UPM): provincias')
    for (x, y), n in cambios.most_common(60):
        print('  %s>%s: %d' % (x, y, n))
    print('poblacion por pais, base y UPM, donde difiere mas de un 10 %:')
    filas = []
    for t in set(a.total) | set(b.total):
        x, y = a.total.get(t, 0), b.total.get(t, 0)
        if abs(x - y) > 0.1 * max(x, y, 1) and max(x, y) > 400000:
            filas.append((max(x, y), t, x, y))
    for _, t, x, y in sorted(filas, reverse=True)[:45]:
        print('  %s;%d;%d;%+d%%' % (t, x, y, 100 * (y - x) // max(x, 1)))
    print('paises con provincias en los dos y algun dato distinto (pais;dato;base;UPM), por poblacion en el UPM:')
    for t in sorted(set(a.suyas) & set(b.suyas), key=lambda t: -b.total[t]):
        x, y = a.paises.get(t, {}), b.paises.get(t, {})
        for k in ('government', 'religion', 'primary_culture', 'capital', 'civilized', 'nationalvalue'):
            u = x[k][-1] if x and x[k] else '-'
            v = y[k][-1] if y and y[k] else '-'
            if u != v:
                print('  %s;%s;%s;%s' % (t, k, u, v))


if __name__ == '__main__':
    if sys.argv[2] == 'comparar':
        comparar(sys.argv[1], fecha(sys.argv[3]), fecha(sys.argv[4]))
    else:
        resumen(sys.argv[1], fecha(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 40)
