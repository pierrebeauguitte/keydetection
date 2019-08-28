# quick script to look into thesession.org json dump

import json
import sys
from os import listdir

with open('tunes.json', 'r') as data:
    tunes = json.load(data)

# print len(tunes), 'tunes loaded'

def findName(query, byName = True):
    # print 'Searching for %s' % query
    for tune in tunes:
        try:
            if byName and query.lower() in tune['name'].lower():
                print '\ttune %d\t%d\t%s,\t%s' % (tune['tune'],
                                                  tune['setting'],
                                                  tune['name'],
                                                  tune['mode'])
            elif query == int(tune['setting']):
                # print tune['abc']
                print 'X:%d\nT:%s\nM:%s\nK:%s\n%s\n' % (tune['setting'],
                                                        tune['name'],
                                                        tune['meter'],
                                                        tune['mode'],
                                                        tune['abc']
                                                        .replace('\r', '\r\n')
                                                        .replace('\n\n', '\n'))
        except:
            continue

if sys.argv[1] == 'dir':
        
    names = [f for f in listdir('audio')]

    print '%d tunes to find...' % len(names)

    for n in names:
        query = n[5:-4]
        findName(query)
elif sys.argv[1] == 'name':
    findName(sys.argv[2], byName = True)

elif sys.argv[1] == 'setting':
    findName(int(sys.argv[2]), byName = False)
