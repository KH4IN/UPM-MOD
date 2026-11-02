"""Corrige, linea a linea, lo que Project Alice anota en scenario_errors.txt.

Uso: python -I upm_alice_avisos.py <scenario_errors.txt> <carpeta mod/UPM>

El registro debe ser el de la ultima creacion del escenario y aplicarse una sola
vez, antes de otros cambios, porque manda por numero de linea. Ningun cambio
mueve lineas: al borrar una clausula, la linea queda en su sitio.

Una condicion sobre algo que no existe (una cultura, un pais) siempre es falsa.
Alice la tira, y entonces la condicion de alrededor pasa a cumplirse siempre, asi
que se cambia por `always = no`, que dice lo mismo dentro de OR y de NOT.
"""
import collections
import os
import re
import sys

# Etiquetas usadas como grupo cultural: su grupo real.
GRUPO_DE_ETIQUETA = {b'USA': b'american_cultures', b'FRA': b'french', b'GER': b'germanic'}

CONDICION = re.compile(r'(\w+) trigger supplied with an invalid (?:\w+ )*"(\w+)" \((.+?), line (\d+)\)')
REGION = re.compile(r'region trigger not supplied with a state name \((.+?), line (\d+)\)')
EFECTO = re.compile(r'\w+ effect supplied with invalid \w+ name (\w+) \((.+?), line (\d+)\)')
ETIQUETA = re.compile(r'(add_core|change_tag) effect given an invalid tag \((.+?), line (\d+)\)')
RELIGION_POP = re.compile(r'pop_majority_religion trigger used in an incorrect scope type pop \((.+?), line (\d+)\)')


class Mod:
    def __init__(self, raiz):
        self.raiz = raiz
        self.lineas = {}
        with open(os.path.join(raiz, 'common', 'countries.txt'), 'rb') as f:
            self.etiquetas = set(re.findall(rb'(?m)^\s*(\w{3})\s*=', f.read()))
        with open(os.path.join(raiz, 'map', 'region.txt'), 'rb') as f:
            self.regiones = set(re.findall(rb'(?m)^\s*(\w+)\s*=\s*\{', f.read()))

    def ruta(self, nombre):
        nombre = nombre.replace(' [pending]', '')
        if nombre.startswith('.\\mod\\UPM\\'):
            return os.path.join(self.raiz, nombre[len('.\\mod\\UPM\\'):])
        return os.path.join(self.raiz, 'common', nombre)

    def linea(self, nombre, n):
        p = self.ruta(nombre)
        if p not in self.lineas:
            with open(p, 'rb') as f:
                self.lineas[p] = f.read().split(b'\n')
        return self.lineas[p], n - 1

    def guardar(self):
        for p, ls in self.lineas.items():
            with open(p, 'wb') as f:
                f.write(b'\n'.join(ls))


def clausula(valor):
    return rb'\b\w+\s*=\s*"?' + re.escape(valor) + rb'"?(?=\s|\}|$)'


def aplicar(mod, cuenta, nombre, n, patron, poner, tipo):
    ls, i = mod.linea(nombre, n)
    nueva, k = re.subn(patron, poner, ls[i], count=1)
    if k:
        ls[i] = nueva
        cuenta[tipo] += 1
    else:
        cuenta['sin aplicar: ' + tipo] += 1
        print('sin aplicar', tipo, nombre, n, ls[i][:60])


def main():
    registro, raiz = sys.argv[1], sys.argv[2]
    with open(registro, 'rb') as f:
        texto = f.read().decode('utf-8', 'replace').replace('\r', '')
    errores = texto[:texto.find('\nWarnings:\n')]
    mod = Mod(raiz)
    cuenta = collections.Counter()
    for m in CONDICION.finditer(errores):
        valor = m.group(2).encode()
        poner = b'always = no'
        if m.group(1) == 'culture_group' and valor in GRUPO_DE_ETIQUETA:
            poner = b'is_culture_group = ' + GRUPO_DE_ETIQUETA[valor]
        aplicar(mod, cuenta, m.group(3), int(m.group(4)), clausula(valor), poner, 'condicion')
    for m in REGION.finditer(errores):
        ls, i = mod.linea(m.group(1), int(m.group(2)))
        malas = [v for v in re.findall(rb'\bregion\s*=\s*(\S+)', ls[i]) if v not in mod.regiones]
        for v in malas:
            aplicar(mod, cuenta, m.group(1), int(m.group(2)), clausula(v), b'always = no', 'region')
    for m in EFECTO.finditer(errores):
        aplicar(mod, cuenta, m.group(2), int(m.group(3)), clausula(m.group(1).encode()), b'', 'efecto')
    for m in ETIQUETA.finditer(errores):
        ls, i = mod.linea(m.group(2), int(m.group(3)))
        for v in re.findall(m.group(1).encode() + rb'\s*=\s*(\w+)', ls[i]):
            if v not in mod.etiquetas:
                aplicar(mod, cuenta, m.group(2), int(m.group(3)), clausula(v), b'', 'etiqueta')
    for m in RELIGION_POP.finditer(errores):
        aplicar(mod, cuenta, m.group(1), int(m.group(2)), rb'\bpop_majority_religion\b', b'has_pop_religion', 'religion del pop')
    mod.guardar()
    for k, v in sorted(cuenta.items()):
        print(v, k)


if __name__ == '__main__':
    main()
