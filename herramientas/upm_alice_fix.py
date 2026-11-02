"""Corrige erratas de los scripts de UPM que Project Alice detecta al cargar el mod.

Uso: python -I upm_alice_fix.py <carpeta mod/UPM>
Se puede repetir: una regla ya aplicada no vuelve a encontrar nada.
"""
import glob
import os
import re
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
]


def main():
    raiz = sys.argv[1]
    total = 0
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
