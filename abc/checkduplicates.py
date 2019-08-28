import csv
import sys
from key import Key

if sys.argv[1] == 'FS':
    corpus = 'FS.abc'
    gt = 'keys.csv'
    index = 2
    first = 0
elif sys.argv[1] == 'GL':
    corpus = 'GL.abc'
    gt = 'greys.csv'
    index = 3
    first = 1
else:
    print 'invalid corpus'
    sys.exit(1)

tunes = {}
nr = -1
with open(corpus) as abcfile:
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
if tunes.keys() != range(first, lasttune + 1):
    print 'missing tunes!'
else:
    print 'all tunes there'

sessionids = {}
    
with open(gt) as inputfile:
    reader = csv.reader(inputfile)
    for row in reader:
        if row[index] == '':
            continue
        try:
            tuneid = int(row[index])
        except:
            tuneid = -1
            continue
        if tuneid not in sessionids:
            sessionids[tuneid] = row[0]
        else:
            print 'tune %d already here' % tuneid
            print '\t', sessionids[tuneid]
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

