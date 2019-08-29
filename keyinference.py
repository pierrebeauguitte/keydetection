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
            'triad': topKeys(scores['triad']),
            'KK': topKeys(scores['KK']),
            'Lerdahl': topKeys(scores['Lerdahl']),
            'LerdahlModal': topKeys(scores['LerdahlModal']),
            'Leman': topKeys(scores['Leman']),
            'PartCadence': topKeys(scores['PartCadence']),
            'PartCadenceMod': topKeys(scores['PartCadenceMod'])
        })
    return results

def loadGroundTruth(filename):
    gt = {}
    with open(filename, 'r') as csvfile:
        reader=csv.reader(csvfile)
        for row in reader:
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

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Infer key from a tune')
    parser.add_argument('-dir')
    parser.add_argument('-gt')
    parser.add_argument('-pcp')
    args = parser.parse_args()

    if args.dir:
        gt = loadGroundTruth(args.gt)
        profiles = getAllProfiles() # for Exp A.
        # profiles = getAllProfiles(weights = [3,1,2]) # for final parametric results
        results = {}
        confusion = {}
        resultssymb = {}
        confusionsymb = {}
        n_examples = 0
        n_examples_symb = 0
        for pType in profiles:
            results[pType] = [0, 0, 0, 0, 0, 0] # correct / fifth / relative / parallel / neighbour / wrong
            confusion[pType] = {}
            resultssymb[pType] = [0, 0, 0, 0, 0, 0]
            confusionsymb[pType] = {}
    
        for audioindex in gt:
            if args.dir == 'FS' and audioindex ==  218:
                #print 'skipping %s %s' % (args.dir, audioindex)
                continue
            #print 'inferring key from %s %s' % (args.dir, audioindex)
            # h, t = inferTune(tune, rep, profiles, length = length)
            # h = getPCPHistogram('%s/%s' % (args.dir, audio), fs = args.framesize)

            h = readPCP(args.dir, audioindex)[args.pcp]

            hsymb = getRepresentation(args.dir, audioindex, 'wpch')
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

            if args.dir == 'FS' and audioindex in [238, 239, 240, 319]:
                continue

            keys = wrapScores([hsymb], t, profiles)
            for res in keys:
                n_examples_symb += 1
                for pType in profiles:
                    wScore, predK = processScores(res[pType], t)
                    resultssymb[pType][wScore] += 1
                    trueK = t.simplified()
                    if trueK not in confusionsymb[pType]:
                        confusionsymb[pType][trueK] = {}
                    if predK not in confusionsymb[pType][trueK]:
                        confusionsymb[pType][trueK][predK] = []
                    confusionsymb[pType][trueK][predK].append(audioindex)

        mirex = {}
        for r, v in results.iteritems():
            mirexEval = v[0] + 0.5*v[1] + 0.3*v[2] + 0.2*v[3]
            mirexEval /= float(n_examples)
            mirex[r] = mirexEval

        for r in results:
            results[r] = map(lambda x: 100*x/float(n_examples), results[r])

        print 'results on %d audio examples:' % n_examples
        for r, v in results.iteritems():
            print '%s\tMIREX score: %.3f' % (r, mirex[r])
            # print '%2.2f / %2.2f / %2.2f / %2.2f / %2.2f / %2.2f' % (v[0], v[1], v[2], v[3], v[4], v[5])


        mirex = {}
        for r, v in resultssymb.iteritems():
            mirexEval = v[0] + 0.5*v[1] + 0.3*v[2] + 0.2*v[3]
            mirexEval /= float(n_examples_symb)
            mirex[r] = mirexEval

        print '\nresults on %d symbolic examples:' % n_examples_symb
        for r, v in resultssymb.iteritems():
            print '%s\tMIREX score: %.3f' % (r, mirex[r])

        # comment next line to get final confusion matrices
        sys.exit(0)
            
        if args.dir == 'FS':
            order = ['D', 'G', 'Am', 'Em', 'A', 'Bm', 'C']
        else:
            order = ['D', 'G', 'Am', 'Em', 'A', 'C', 'Dm', 'Bm', 'Gm', 'F']

        print '\nConfusion (audio):'
        print generateMatrix(confusion['PartCadenceMod'], order)

        print '\nConfusion (symb):'
        print generateMatrix(confusionsymb['LerdahlModal'], order)
