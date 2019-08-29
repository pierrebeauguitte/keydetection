from representations import * 
from key import Key
from getKeyProfiles import *
import json
import csv
import sys
import argparse
import warnings
import random
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

def loadGroundTruth(filename, rep):
    gt = {}
    with open(filename, 'r') as csvfile:
        reader=csv.reader(csvfile)
        for row in reader:
            if filename == 'FS.csv' and int(row[0][:3]) ==  218:
                continue
            if filename == 'FS.csv' and rep == 'symb' and int(row[0][:3]) in [238, 239, 240, 319]:
                continue
            gt[int(row[0][:3])] = row[1]
    return gt

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

def run(gt, dired, splits, s, rep, weights = [1, 1, 1], eval = False):
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
        if not eval and audioindex in splits[s]:
            continue
        if eval and audioindex not in splits[s]:
            continue

        if args.rep == 'audio':
            h = readPCP(dired, audioindex)['deep']
        else:
            h = getRepresentation(dired, audioindex, 'wpch')
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
        mirex['PartCadence'],
        mirex['PartCadenceMod']
    ]

    if eval:
        print 'Tonal:'
        print 'eval score: %.3f' % mirex['PartCadence']

        print 'Modal:'
        print 'eval score: %.3f' % mirex['PartCadenceMod']
        return [ results['PartCadence'], results['PartCadenceMod']]
    
    return sumup

def makeSplits(nfolds, nseq, sequences):
    random.seed(2376)

    splitIndices = [int(i * float(nfolds) / nseq) for i in range(nseq)]
    random.shuffle(splitIndices)

    splitX = dict.fromkeys(range(nfolds))
    for s in range(nfolds):
        splitX[s] = []

    for i in range(nseq):
        splitX[splitIndices[i]].append(sequences[i])

    return splitX

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Grid search for triad weights')
    parser.add_argument('-dir')
    parser.add_argument('-gt')
    parser.add_argument('-degree', type=int)
    parser.add_argument('-rep')
    args = parser.parse_args()

    gt = loadGroundTruth(args.gt, args.rep)

    splits =  makeSplits(10, len(gt), gt.keys())
    
    degrees = range(1, args.degree)

    print 'Search starting with degree %d' % args.degree

    matsTonal = [0 for _ in range(10)]
    matsModal = [0 for _ in range(10)]

    # find max
    for s in range(10):
        bestWeightsAudioTonal = [0, None]
        bestWeightsAudioModal = [0, None]
        print '----------Split %d----------' % s
        for w1 in degrees:
            for w2 in degrees:
                for w3 in degrees:
                    if w1 + w2 + w3 == 0:
                        continue
                    r = run(gt, args.dir, splits, s, args.rep, weights = [w1, w2, w3])

                    if r[0] > bestWeightsAudioTonal[0]:
                        bestWeightsAudioTonal = [r[0], [w1, w2, w3]]

                    if r[1] > bestWeightsAudioModal[0]:
                        bestWeightsAudioModal = [r[1], [w1, w2, w3]]

        print 'Tonal:', bestWeightsAudioTonal
        res = run(gt, args.dir, splits, s, args.rep, weights = bestWeightsAudioTonal[1], eval = True)
        matsTonal[s] = res[0]
        print 'Tonal:', matsTonal[s]

        print 'Modal:', bestWeightsAudioModal
        res = run(gt, args.dir, splits, s, args.rep, weights = bestWeightsAudioModal[1], eval = True)
        matsModal[s] = res[1]
        print 'Modal:', matsModal[s]

        sys.stdout.flush()

    finalTonal = [ sum([m[i] for m in matsTonal]) for i in range(6) ]
    print 'Tonal:', finalTonal
    mirexEval = finalTonal[0] + 0.5*finalTonal[1] + 0.3*finalTonal[2] + 0.2*finalTonal[3]
    print '>>>>> Final score Tonal: %.3f' % (mirexEval / len(gt)) 

    finalModal = [ sum([m[i] for m in matsModal]) for i in range(6) ]
    print 'Modal:', finalModal
    mirexEval = finalModal[0] + 0.5*finalModal[1] + 0.3*finalModal[2] + 0.2*finalModal[3]
    print '>>>>> Final score Modal: %.3f' % (mirexEval / len(gt)) 
