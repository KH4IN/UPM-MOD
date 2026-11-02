import collections, re, sys
t = open(sys.argv[1], 'rb').read().decode('utf-8', 'replace').replace('\r', '')
i = t.find('\nWarnings:\n')
ls = [x for x in t[:i].split('\n')[4:] if x.strip()]
ign = ('Tried to remove a non-existent core', 'invalid culture "noculture"', 'Event given too many', 'unknown key: exist')
rest = [x for x in ls if not any(k in x for k in ign)]
print(len(ls), 'total;', len(rest), 'tras quitar los grupos conocidos')
g = collections.defaultdict(list)
for x in rest:
    k = re.sub(r'\d+', 'N', re.sub(r'\(.*$', '', x))[:46]
    g[k].append(x)
for k, v in sorted(g.items(), key=lambda a: -len(a[1])):
    print(f'{len(v):4} {v[0][:125]}')
    if len(sys.argv) > 2:
        for y in v[1:int(sys.argv[2])]:
            print('       ', y[:125])
