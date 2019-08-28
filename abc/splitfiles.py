import sys

filename = sys.argv[1]
destname = sys.argv[2]

abcs = open(filename, 'r')

tune = ''
nr = -1
for line in abcs:
    if line == '\n':
        with open('%s/%03d.abc' % (destname, nr), 'w') as outfile:
            outfile.write(tune)        
        tune = ''
        continue
    elif line.startswith('X: '):
        nr = int(line[3:-1])
    elif line.startswith('F: '):
        continue
    tune += line

print 'Done!'
