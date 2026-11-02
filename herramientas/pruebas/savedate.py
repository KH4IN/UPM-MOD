import datetime, glob, os, struct, sys
# Lee la fecha de cada partida guardada de Alice desde su cabecera.
carpeta, inicio = sys.argv[1], datetime.date(*map(int, sys.argv[2].split('-')))
desde = float(sys.argv[3]) if len(sys.argv) > 3 else 0
fs = sorted((f for f in glob.glob(os.path.join(carpeta, '*.bin')) if os.path.getmtime(f) >= desde), key=os.path.getmtime)
for f in fs[-int(sys.argv[4]) if len(sys.argv) > 4 else 0:]:
    with open(f, 'rb') as h:
        b = h.read(128)
    ver = struct.unpack_from('<I', b, 4)[0]
    d = struct.unpack_from('<i', b, 88)[0]
    # La cuenta juliana evita el limite de datetime en fechas lejanas
    ord_ = inicio.toordinal() + d - 1
    fecha = datetime.date.fromordinal(ord_) if 0 < ord_ < datetime.date.max.toordinal() else d
    print(os.path.basename(f), 'ver', ver, 'fecha', fecha, os.path.getsize(f) // 1024, 'KB', datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime('%H:%M:%S'))
