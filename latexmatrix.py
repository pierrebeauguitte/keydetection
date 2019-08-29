from key import Key

def generateMatrix(confusion, order):
    truKeys = list(order)
    estKeys = list(order)
    for trueKey, wrongKeys in confusion.iteritems():
        for wKey, l in wrongKeys.iteritems():
            if wKey not in estKeys:
                estKeys.append(wKey)

    summary = [0, 0, 0, 0, 0, 0]
    totalM = 0
    totalm = 0
    correctM = 0
    correctm = 0

    latex = '\\begin{tabular}{cc}\n'

    latex += '\\begin{tabular}{C|'
    for _ in estKeys:
        latex += 'C'
    latex += '}\n'
    for k in estKeys:
        latex += '& %s ' % k
    latex += '\\\\\n\\hline\n'
    for k in truKeys:
        latex += '%s ' % k
        for e in estKeys:
            n = len(confusion[k][e]) if k in confusion and e in confusion[k] else 0
            if Key(strRep = k).major:
                totalM += n
            else:
                totalm += n
            latex += '& '
            if k == e:
                latex += '\\correctColor '
                summary[0] += n
                if Key(strRep = k).major:
                    correctM += n
                else:
                    correctm += n
            elif Key(strRep = e).fifth(Key(strRep = k)):
                latex += '\\fifthColor '
                summary[1] += n
            elif Key(strRep = e).relative(Key(strRep = k)):
                latex += '\\relativeColor '
                summary[2] += n
            elif Key(strRep = e).parallel(Key(strRep = k)):
                latex += '\\parallelColor '
                summary[3] += n
            elif Key(strRep = e).neighbour(Key(strRep = k)):
                latex += '\\neighbourColor '
                summary[4] += n
            else:
                summary[5] += n
            latex += '%d ' % n
        latex += '\\\\\n'
    latex += '\\end{tabular}\n&\n'

    latex += '\\begin{tabular}{ll}\n'
    latex += 'Correct & \\correctColor %d\\\\\n' % summary[0]
    latex += 'Fifth & \\fifthColor %d\\\\\n' % summary[1]
    latex += 'Relative & \\relativeColor %d\\\\\n' % summary[2]
    latex += 'Parallel & \\parallelColor %d\\\\\n' % summary[3]
    latex += 'Neighbour & \\neighbourColor %d\\\\\n' % summary[4]
    latex += 'Other & %d\n' % summary[5]

    latex += '\\end{tabular}\n'

    latex += '\\end{tabular}'

    print 'CorrectM: %.1f' % (100 * correctM / float(totalM))
    print 'Correctm: %.1f' % (100 * correctm / float(totalm))
    
    return latex
