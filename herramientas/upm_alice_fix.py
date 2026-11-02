"""Corrige erratas de los scripts de UPM que Project Alice detecta al cargar el mod.

Uso: python -I upm_alice_fix.py <carpeta mod/UPM>
Se puede repetir: una regla ya aplicada no vuelve a encontrar nada.
"""
import glob
import os
import re
import shutil
import sys

REGLAS = [
    ('events/**/*.txt', rb'\bexist(\s*=)', rb'exists\1'),
    ('history/provinces/**/*.txt', rb'\bremove_croe\b', b'remove_core'),
    ('history/provinces/**/*.txt', rb'\bdelete_core\b', b'remove_core'),
    ('history/provinces/**/*.txt', rb'\bcontrollar\b', b'controller'),
    ('history/provinces/**/*.txt', rb'\bcontoller\b', b'controller'),
    ('history/provinces/**/*.txt', rb'\bownter\b', b'owner'),
    ('history/provinces/**/*.txt', rb'\bbase_naval\b', b'naval_base'),
    ('history/provinces/**/*.txt', rb'(?m)^(\s*)core(\s*=)', rb'\1add_core\2'),
    ('history/provinces/soviet/968 - Odessa.txt', rb'remove_core = LT\b', b'remove_core = LIT'),
    ('history/countries/URR - Soviet Union.txt', rb'(?m)^religion =\s*$', b'religion = orthodox\r'),
    ('history/wars/AdraWar1579.txt', rb'casus_belli = acquire state', b'casus_belli = acquire_state'),
    ('decisions/arabian formation.txt', rb'\bannex = FROM', b'inherit = FROM'),
    # La cultura noculture no existe; dummy, su pareja en cada condicion, sigue activa.
    ('events/**/*.txt', rb'\b(?:remove_accepted_culture|accepted_culture|primary_culture|has_pop_culture)\s*=\s*noculture\b', b''),
    # Con coma decimal, Alice lee 0 y deja el resto suelto.
    ('history/countries/**/*.txt', rb'(?m)^(\s*\w+\s*=\s*\d+),(\d+)', rb'\1.\2'),
    # Una fecha necesita año, mes y dia.
    ('history/provinces/**/*.txt', rb'(?m)^(\s*\d{3,4})(\s*=\s*\{)', rb'\1.1.1\2'),
    # Paises que no existen: quitar o dar su reclamacion no hace nada.
    ('history/provinces/**/*.txt', rb'[ \t]*remove_core = (?:LET|SAY)\b', b''),
    ('history/provinces/**/*.txt', rb'[ \t]*add_core = (?:WIR|SJA)\b', b''),
    ('history/countries/**/*.txt', rb'(?m)^post_napoleonic_army_doctrine = (?:no|yes)[ \t]*', b''),
    ('units/*.txt', rb'\btelephone\b', b'telephones'),
    ('events/converterEvents.txt', rb'\bis_year\s*=', b'year ='),
    ('events/Eventos1492.txt', rb'\bis_uncivilized = yes', b'civilized = no'),
    ('events/DissolutionKUK.txt', rb'\bis_empty\s*=', b'empty ='),
    ('events/DissolutionKUK.txt', rb'\bai_will_do\b', b'ai_chance'),
    ('events/guerracivilinca.txt', rb'(?m)^(\s*)set_global_flag = charca_inde', rb'\1immediate = { set_global_flag = charca_inde }'),
    # La etiqueta AND de Andhra choca con la condicion AND, y su nombre con la palabra "and".
    ('common/countries.txt', rb'(?m)^AND = "countries/Andhra.txt"', b'ADH = "countries/Andhra.txt"'),
    ('history/provinces/india/*.txt', rb'\badd_core = AND\b', b'add_core = ADH'),
    ('history/units/MLD_OOB.txt', rb'(?m)^AND = \{', b'ADH = {'),
    ('localisation/pasies.csv', rb'(?m)^AND_', b'ADH_'),
]


def renombrar_andhra(raiz):
    """Lo que las reglas de texto no alcanzan: archivos y el nombre del pais."""
    historia = os.path.join(raiz, 'history', 'countries', 'AND - Andhra.txt')
    if os.path.exists(historia):
        os.replace(historia, historia.replace('AND - Andhra', 'ADH - Andhra'))
    for p in glob.glob(os.path.join(raiz, 'gfx', 'flags', 'AND*.tga')):
        nuevo = os.path.join(os.path.dirname(p), 'ADH' + os.path.basename(p)[3:])
        if not os.path.exists(nuevo):
            shutil.copyfile(p, nuevo)
    csv = os.path.join(raiz, 'localisation', 'pasies.csv')
    with open(csv, 'rb') as f:
        a = f.read()
    if not re.search(rb'(?m)^ADH;', a):
        with open(csv, 'ab') as f:
            f.write(b'ADH;Andhra;Andhra;Andhra;;Andhra;;;;;;;;;x\r\n')


def fecha(texto):
    return tuple(int(x) for x in texto.split(b'.'))[:3]


def alargar_partidos(raiz):
    """El ultimo partido de una ideologia que caduca en 2000 sigue hasta 2300, como los demas."""
    n = 0
    with open(os.path.join(raiz, 'common', 'countries.txt'), 'rb') as f:
        listado = re.findall(rb'(?m)^\s*[A-Z][A-Z0-9]{2}\s*=\s*"?countries/([^"\r\n]+?)"?\s*$', f.read())
    for nombre in listado:
        p = os.path.join(raiz, 'common', 'countries', nombre.decode('cp1252'))
        with open(p, 'rb') as f:
            a = f.read()
        # los comentarios se tapan sin mover nada, para que las posiciones valgan en el original
        limpio = re.sub(rb'#[^\r\n]*', lambda m: b' ' * len(m.group()), a)
        partidos = []
        for m in re.finditer(rb'party\s*=\s*\{.*?\}', limpio, re.S):
            ini = re.search(rb'start_date\s*=\s*([\d.]+)', m.group())
            fin = re.search(rb'end_date\s*=\s*([\d.]+)', m.group())
            ide = re.search(rb'ideology\s*=\s*(\w+)', m.group())
            if ini and fin and ide:
                partidos.append((fecha(ini.group(1)), fecha(fin.group(1)), ide.group(1), m.start() + fin.start(1), m.start() + fin.end(1)))
        despues = {x[2] for x in partidos if x[0] <= (2001, 6, 1) < x[1]}
        ultimos = {}
        for x in partidos:
            if x[0] <= (1999, 6, 1) < x[1] and x[2] not in despues and (x[2] not in ultimos or x[1] > ultimos[x[2]][1]):
                ultimos[x[2]] = x
        b = a
        for x in sorted(ultimos.values(), key=lambda v: -v[3]):
            b = b[:x[3]] + b'2300.1.1' + b[x[4]:]
            n += 1
        if b != a:
            with open(p, 'wb') as f:
                f.write(b)
    print(n, 'partidos alargados hasta 2300')
    return n


def main():
    raiz = sys.argv[1]
    total = alargar_partidos(raiz)
    renombrar_andhra(raiz)
    for patron, buscar, poner in REGLAS:
        n = 0
        for p in glob.glob(os.path.join(raiz, patron), recursive=True):
            with open(p, 'rb') as f:
                a = f.read()
            b, k = re.subn(buscar, poner, a)
            if k:
                with open(p, 'wb') as f:
                    f.write(b)
                n += k
        print(n, buscar.decode())
        total += n
    print('total', total)


if __name__ == '__main__':
    main()
