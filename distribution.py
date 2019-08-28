import matplotlib.pyplot as plt
import operator
import csv

FSkeys = {}
with open('FS.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        key = row[1]
        if key[-1] != 'm':
            key += 'M'
            # key = key[:-1].lower()
        if key not in FSkeys:
            FSkeys[key] = 0
        FSkeys[key] += 1

sFSkeys = sorted(FSkeys.items(), key=operator.itemgetter(1), reverse = True)

print sFSkeys

GLkeys = {}
with open('GL.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        key = row[1]
        if key[-1] != 'm':
            key += 'M'
            # key = key[:-1].lower()
        if key not in GLkeys:
            GLkeys[key] = 0
        GLkeys[key] += 1

sGLkeys = sorted(GLkeys.items(), key=operator.itemgetter(1), reverse = True)

print sGLkeys

plt.figure(figsize=(4,4))
plt.bar(range(len(FSkeys)), [v[1] for v in sFSkeys], align='center')
plt.xticks(range(len(FSkeys)), [v[0] for v in sFSkeys])
plt.xlim(-1,len(FSkeys))
plt.savefig('distFS.pdf', bbox_inches='tight')


plt.figure(figsize=(4,4))
plt.bar(range(len(GLkeys)), [v[1] for v in sGLkeys], align='center')
plt.xticks(range(len(GLkeys)), [v[0] for v in sGLkeys])
plt.xlim(-1,len(GLkeys))
plt.savefig('distGL.pdf', bbox_inches='tight')


# plt.tight_layout()
# plt.savefig('dists.pdf')
