import csv
from key import Key

tunes = {}
nr = -1
with open('abc/FS.abc') as abcfile:
    for line in abcfile:
        if line.startswith('X: '):
            nr = int(line[3:])
        elif line.startswith('K: '):
            key = line[3:-1]
        elif line.startswith('F: '):
            url = line[3:-1]
            try:
                seshnr = int(url[29:].split('#', 1)[0])
            except:
                seshnr = -1
            tunes[nr] = [seshnr, key]
            nr = -1

lasttune = max(tunes.keys())
if tunes.keys() != range(lasttune + 1):
    print 'missing tunes!'
else:
    print 'all tunes there'

sessionidsFS = {}

with open('FS.csv') as inputfile:
    reader = csv.reader(inputfile)
    for row in reader:
        if row[2] == '':
            continue
        try:
            tuneid = int(row[2])
        except:
            tuneid = -1
        if tuneid not in sessionidsFS:
            sessionidsFS[tuneid] = row[0]
        else:
            print 'tune %d already here' % tuneid
            print '\t', sessionidsFS[tuneid]
            print '\t', row[0]

        tuneindex = int(row[0][:3])
        if tunes[tuneindex][0] != tuneid:
            print 'mismatch:', row, tunes[tuneindex]

        try:
            kabc = Key(strRep = tunes[tuneindex][1])
            kcsv = Key(strRep = row[1])
            if not kabc.similar(kcsv):
                print 'key mismatch for %d' % tuneindex
        except:
            print 'Could not read', row, tunes[tuneindex]

print 'done\n\n'

tunes = {}
nr = -1
with open('abc/GL.abc') as abcfile:
    for line in abcfile:
        if line.startswith('X: '):
            nr = int(line[3:])
        elif line.startswith('K: '):
            key = line[3:-1]
        elif line.startswith('F: '):
            url = line[3:-1]
            try:
                seshnr = int(url[29:].split('#', 1)[0])
            except:
                seshnr = -1
            tunes[nr] = [seshnr, key]
            nr = -1

lasttune = max(tunes.keys())
if tunes.keys() != range(1, lasttune + 1):
    print 'missing tunes!'
else:
    print 'all tunes there'

sessionidsGL = {}

with open('GL.csv') as inputfile:
    reader = csv.reader(inputfile)
    for row in reader:
        if row[3] == '':
            continue
        try:
            tuneid = int(row[3])
        except:
            tuneid = -1
            continue
        if tuneid not in sessionidsGL:
            sessionidsGL[tuneid] = row[0]
        else:
            print 'tune %d already here' % tuneid
            print '\t', sessionidsGL[tuneid]
            print '\t', row[0]

        tuneindex = int(row[0][:3])
        if tunes[tuneindex][0] != tuneid:
            print 'mismatch:', row, tunes[tuneindex]

        try:
            kabc = Key(strRep = tunes[tuneindex][1])
            kcsv = Key(strRep = row[1])
            if not kabc.similar(kcsv):
                print 'key mismatch for %d' % tuneindex
        except:
            print 'Could not read', row, tunes[tuneindex]

print 'done'

sFS = set(sessionidsFS.keys())
sGL = set(sessionidsGL.keys())
inter = sFS.intersection(sGL)

