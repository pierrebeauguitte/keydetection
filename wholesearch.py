from representations import * 
from key import Key
from getKeyProfiles import *
import json
import csv
import sys
import argparse
import warnings
from latexmatrix import *

reload(sys)
sys.setdefaultencoding('utf8')

warnings.filterwarnings("ignore")

def topKeys(sortedKeys):
    return [ k[0] for k in sortedKeys if k[1] == sortedKeys[0][1] ]

def wrapScores(histograms, target, profiles):
    results = []
    for hist in histograms:
        scores = getScores(hist, profiles)
        results.append({
            'true key': target,
            'PartCadence': topKeys(scores['PartCadence']),
            'PartCadenceMod': topKeys(scores['PartCadenceMod']),
        })
    return results

def processScores(lScores, t):
    worstScore = -1
    predKey = None
    for s in lScores:
        if s.similar(t):
            point = 0
        elif s.fifth(t):
            point = 1
        elif s.relative(t):
            point = 2
        elif s.parallel(t):
            point = 3
        elif s.neighbour(t):
            point = 4
        else:
            point = 5
        if point > worstScore:
            worstScore = point
            predKey = s.simplified()
    return worstScore, predKey

def loadGroundTruth():
    gt = {}
    with open('FS.csv', 'r') as csvfile:
        reader=csv.reader(csvfile)
        for row in reader:
            if int(row[0][:3]) ==  218:
                continue
            gt['FS_%s' % row[0][:3]] = row[1]
    with open('GL.csv', 'r') as csvfile:
        reader=csv.reader(csvfile)
        for row in reader:
            gt['GL_%s' % row[0][:3]] = row[1]
    print len(gt), 'tunes'
    return gt

def run(gt, dired, rep, weights = [1, 1, 1]):
    profiles = getAllProfiles(weights = weights, onlyCad = True)
    results = {}
    confusion = {}
    resultssymb = {}
    confusionsymb = {}
    n_examples = 0
    for pType in profiles:
        results[pType] = [0, 0, 0, 0, 0, 0] # correct / fifth / relative / parallel / neighbour / wrong
        confusion[pType] = {}
        resultssymb[pType] = [0, 0, 0, 0, 0, 0]
        confusionsymb[pType] = {}
    for audioindex in gt:

        h = readPCP(audioindex[:2], int(audioindex[3:]))['deep']
        t = Key(strRep = gt[audioindex])

        keys = wrapScores([h], t, profiles)
        for res in keys:
            n_examples += 1
            for pType in profiles:
                wScore, predK = processScores(res[pType], t)
                results[pType][wScore] += 1
                trueK = t.simplified()
                if trueK not in confusion[pType]:
                    confusion[pType][trueK] = {}
                if predK not in confusion[pType][trueK]:
                    confusion[pType][trueK][predK] = []
                confusion[pType][trueK][predK].append(audioindex)

    sumup = {}
    mirex = {}
    for r, v in results.iteritems():
        mirexEval = v[0] + 0.5*v[1] + 0.3*v[2] + 0.2*v[3]
        mirexEval /= float(n_examples)
        mirex[r] = mirexEval

    sumup = [
        # mirex['PartCadence'],
        mirex['PartCadenceMod']
    ]


    if True:
        # print 'Tonal:'
        # print 'eval score: %.3f' % mirex['PartCadence']

        print 'Modal:', weights
        print 'eval score: %.3f' % mirex['PartCadenceMod']
        return mirex['PartCadenceMod']  # [ results['PartCadenceMod']]

    return sumup

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Grid search for triad weights')
    parser.add_argument('-dir')
    parser.add_argument('-gt')
    parser.add_argument('-degree', type=int)
    parser.add_argument('-rep')
    args = parser.parse_args()

    gt = loadGroundTruth()
    print len(gt)

    degrees = range(1, args.degree + 1)

    print '\nSearch starting with degree %d' % args.degree

    # matsTonal = [0 for _ in range(10)]
    matsModal = [0 for _ in range(10)]

    bestWeightsAudioModal = [0, None]
    for w1 in degrees:
        for w2 in degrees:
            for w3 in degrees:
                if w1 + w2 + w3 == 0:
                    continue
                r = run(gt, args.dir, args.rep, weights = [w1, w2, w3])

                if r > bestWeightsAudioModal[0]:
                    bestWeightsAudioModal = [r, [w1, w2, w3]]

    print 'Modal:', bestWeightsAudioModal
    # res = run(gt, args.dir, splits, s, args.rep, weights = bestWeightsAudioModal[1], eval = True)
    # matsModal[s] = res[1]
    # print 'Modal:', matsModal[s]

    sys.stdout.flush()

    # finalTonal = [ sum([m[i] for m in matsTonal]) for i in range(6) ]
    # print 'Tonal:', finalTonal
    # mirexEval = finalTonal[0] + 0.5*finalTonal[1] + 0.3*finalTonal[2] + 0.2*finalTonal[3]
    # print '>>>>> Final score Tonal: %.3f' % (mirexEval / len(gt)) 

    # finalModal = [ sum([m[i] for m in matsModal]) for i in range(6) ]
    # print 'Modal:', finalModal
    # mirexEval = finalModal[0] + 0.5*finalModal[1] + 0.3*finalModal[2] + 0.2*finalModal[3]
    # print '>>>>> Final score Modal: %.3f' % (mirexEval / len(gt)) 
