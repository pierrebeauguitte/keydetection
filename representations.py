import json
import os
import sys
from key import Key

def getFilename(corpus, tuneNumber):
    filename = '%03d.json' % tuneNumber
    return 'abc/%s/%s' % (corpus, filename)

def readFile(corpus, tuneNumber):
    with open(getFilename(corpus, tuneNumber), 'r') as tune:
        data = json.load(tune)
    return data

def readPCP(corpus, tuneNumber, transposition = 0):
    filename = '%03d.json' % tuneNumber
    with open('audio/%s_chromas/%s' % (corpus, filename), 'r') as pcp:
        data = json.load(pcp)
    if transposition == 0:
        return data
    else:
        res = {}
        for method, h in data.iteritems():
            l = len(h)
            res[method] = [ h[i-transposition] for i in range(l) ]
        return res

def pitchSequence(notes, transposition = 0):
    seq = []
    for n in notes:
        if n[0] > 0:
            seq.append(n[0] + transposition)
    return seq

def chromaSequence(pitchSeq):
    seq = []
    for p in pitchSeq:
        seq.append(p % 12)
    return seq

def intervalSequence(pitchSeq, chroma = False):
    seq = []
    previous = -1
    for p in pitchSeq:
        if previous > 0:
            seq.append((p-previous) % 12 if chroma else (p-previous))
        previous = p
    return seq

def normalize(histo):
    if type(histo) is list:
        w = float(sum(histo))
        if w > 0:
            histo = map(lambda x: x / w, histo)
        return histo
    elif type(histo) is dict:
        w = float(sum(histo.values()))
        if w > 0:
            for k in histo:
                histo[k] /= w
        return histo
    else:
        return None

def pitchClassHistogram(notes,
                        weighted = False,
                        length = 0,
                        transposition = 0,
                        normalized = True):
    if length == 0:
        histo = dict.fromkeys(range(12), 0)
        for n in notes:
            if n[0] == 0:
                continue
            w = n[1] / float(n[2]) if weighted else 1
            histo[ (n[0] + transposition) % 12 ] += w
        if normalized:
            histo = normalize(histo)
        return histo
    else:
        actualNotes = [n for n in notes if n[0] > 0]
        nHisto = len(actualNotes) - length
        histos = []
        for h in range(nHisto):
            histo = dict.fromkeys(range(12), 0)
            for n in range(length):
                note = actualNotes[h + n]
                w = note[1] / float(note[2]) if weighted else 1
                histo[ (note[0] + transposition) % 12 ] += w
            if normalized:
                histo = normalize(histo)
            histos.append(histo)
        return histos

def repHistogram(pitchSeq, length = 0, normalized = True):
    if length == 0:
        histo = dict.fromkeys(range(12), 0)
        previous = -1
        for p in pitchSeq:
            if p == previous:
                histo[p % 12] += 1
            previous = p
        if normalized:
            histo = normalize(histo)
        return histo
    else:
        histos = []
        nHisto = len(pitchSeq) - length
        for h in range(nHisto):
            histo = dict.fromkeys(range(12), 0)
            previous = -1
            for n in pitchSeq[h:h+length]:
                if n == previous:
                    histo[ n % 12 ] += 1
                previous = n
            if normalized:
                histo = normalize(histo)
            histos.append(histo)
        return histos

def getSubsequences(seq, length):
    subs = []
    starts = range(len(seq) - length + 1)
    for start in starts:
        subs.append(seq[start : start + length])
    return subs

def getRepresentations(corpus,
                       tuneNumber,
                       reps = None,
                       length = 0,
                       transposition = 0):
    res = {}
    data = readFile(corpus, tuneNumber)

    if reps is None or 'key' in reps:
        res['key'] = Key(strRep = data['key'], transposition = transposition)

    pitchSeq = pitchSequence(data['notes'], transposition = transposition)

    if reps is None or 'pitch' in reps:
        res['pitch'] = pitchSeq if length == 0 else getSubsequences(pitchSeq, length)

    if reps is None or 'chroma' in reps:
        seq = chromaSequence(pitchSeq)
        if length == 0:
            res['chroma'] = seq
        else:
            res['chroma'] = getSubsequences(seq, length)

    if reps is None or 'int' in reps:
        seq = intervalSequence(pitchSeq)
        if length == 0:
            res['int'] = seq
        else:
            res['int'] = getSubsequences(seq, length - 1)

    if reps is None or 'chrint' in reps:
        seq = intervalSequence(pitchSeq, chroma = True)
        if length == 0:
            res['chrint'] = seq
        else:
            res['chrint'] = getSubsequences(seq, length - 1)

    if reps is None or 'pch' in reps:
        res['pch'] = pitchClassHistogram(data['notes'],
                                         length = length,
                                         transposition = transposition)

    if reps is None or 'wpch' in reps:
        res['wpch'] = pitchClassHistogram(data['notes'],
                                          weighted = True,
                                          length = length,
                                          transposition = transposition)

    if reps is None or 'rh' in reps:
        res['rh'] = repHistogram(pitchSeq, length = length)

    return res

def getRepresentation(corpus, tuneNumber, rep, length = 0, transposition = 0):
    reps = getRepresentations(corpus, tuneNumber, [rep], length = length, transposition = transposition)
    return reps[rep]

if __name__ == '__main__':

    print getRepresentations(sys.argv[1],
                             int(sys.argv[2]),
                             ['key', 'rh'],
                             transposition = int(sys.argv[3]))

    print readPCP(sys.argv[1], int(sys.argv[2]))
