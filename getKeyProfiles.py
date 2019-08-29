from key import Key
from representations import *

def listAllkeys():
    return keys

# Krumhansl-Kessler profiles
KKM = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
KKm = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]

sKKM = sum(KKM)
sKKm = sum(KKm)
KKMnorm = [x / sKKM for x in KKM]
KKmnorm = [x / sKKm for x in KKm]

# # C_Do
lerdahlBasicSpaceM = [5, 1, 2, 1, 3, 2, 1, 4, 1, 2, 1, 2]
# # C_La
lerdahlBasicSpacem = [5, 1, 2, 3, 1, 2, 1, 4, 2, 1, 2, 1]

# C_Do/Sol
lerdahlBasicSpaceMModal = [5, 1, 2, 1, 3, 2, 1, 4, 1, 2, 2, 2]
# C_La/Re
lerdahlBasicSpacemModal = [5, 1, 2, 3, 1, 2, 1, 4, 2, 2, 2, 1]

# from (Leman, 1995) p. 85
lemanToneCenterM = [0.36, 0.05, 0.21, 0.08, 0.24, 0.21, 0.05, 0.31, 0.07, 0.24, 0.09, 0.10]
lemanToneCenterm = [0.34, 0.11, 0.15, 0.25, 0.11, 0.25, 0.02, 0.31, 0.24, 0.09, 0.12, 0.14]

def getPartialCadence(major = True, modal = True, weights = [1,1,1]):
    if major:
        scale = [[0], [2], [4], [5], [7], [9], [10, 11] if modal else [11]]
    else:
        scale = [[0], [2], [3], [5], [7], [8, 9] if modal else [8], [10]]
    I  = [scale[i] for i in (0, 2, 4)]
    IV = [scale[i] for i in (3, 5, 0)]
    V  = [scale[i] for i in (4, 6, 1)]
    VII = [scale[i] for i in (6, 1, 3)]

    allCadences = [0 for i in range(12)]

    factor = 2 if major else 4

    for degree in range(3):
        for d in I[degree]:
            allCadences[d] += factor * weights[degree]
    for degree in range(3):
        for d in V[degree]:
            allCadences[d] += 1 * weights[degree]
    for degree in range(3):
        for d in IV[degree]:
            allCadences[d] += 1 * weights[degree]
    if not major:
        for degree in range(3):
            for d in VII[degree]:
                allCadences[d] += 2 * weights[degree]
    # print allCadences
    s = float(sum(allCadences))
    return [x/s for x in allCadences]


def getAllProfiles(weights = [1,1,1], onlyCad = False):

    allKeys = []
    for k in range(12):
        allKeys.append(Key(chrMod = [k, True]))
        allKeys.append(Key(chrMod = [k, False]))
        
    allProfiles = {
        'PartCadenceMod': {},
        'PartCadence': {}
    }

    if not onlyCad:
        allProfiles['triad'] = {}
        allProfiles['KK'] = {}
        allProfiles['Lerdahl'] = {}
        allProfiles['LerdahlModal'] = {}
        allProfiles['Leman'] = {}

    partCadenceMtonal = getPartialCadence(major=True, modal=False, weights = weights)
    partCadenceMmodal = getPartialCadence(major=True, modal=True, weights = weights)
    partCadencemtonal = getPartialCadence(major=False, modal=False, weights = weights)
    partCadencemmodal = getPartialCadence(major=False, modal=True, weights = weights)

    for k in allKeys:
        if not onlyCad:
            allProfiles['triad'][k] = k.triad()
        if k.major:
            if not onlyCad:
                allProfiles['KK'][k] = [KKMnorm[i - k.chrFund] for i in range(12)]
                allProfiles['Lerdahl'][k] = [lerdahlBasicSpaceM[i - k.chrFund] for i in range(12)]
                allProfiles['LerdahlModal'][k] = [lerdahlBasicSpaceMModal[i - k.chrFund] for i in range(12)]
                allProfiles['Leman'][k] = [lemanToneCenterM[i - k.chrFund] for i in range(12)]
            allProfiles['PartCadence'][k] = [partCadenceMtonal[i - k.chrFund] for i in range(12)]
            allProfiles['PartCadenceMod'][k] = [partCadenceMmodal[i - k.chrFund] for i in range(12)]
        else:
            if not onlyCad:
                allProfiles['KK'][k] = [KKmnorm[i - k.chrFund] for i in range(12)]
                allProfiles['Lerdahl'][k] = [lerdahlBasicSpacem[i - k.chrFund] for i in range(12)]
                allProfiles['LerdahlModal'][k] = [lerdahlBasicSpacemModal[i - k.chrFund] for i in range(12)]
                allProfiles['Leman'][k] = [lemanToneCenterm[i - k.chrFund] for i in range(12)]
            allProfiles['PartCadence'][k] = [partCadencemtonal[i - k.chrFund] for i in range(12)]
            allProfiles['PartCadenceMod'][k] = [partCadencemmodal[i - k.chrFund] for i in range(12)]
    return allProfiles

def getScores(histogram, profiles):
    res = {}
    for pType in profiles:
        tmp = []
        for k, p in profiles[pType].iteritems():
            score = sum([histogram[c] * p[c] for c in range(12)])
            tmp.append((k, score))
        res[pType] = sorted(tmp, key = lambda x: x[1], reverse = True)
    return res

if __name__ == '__main__':

    # partCadenceMtonal = getPartialCadence(major=True, modal=False)
    getPartialCadence(major=True, modal=True, weights = [3,1,2])
    # partCadencemtonal = getPartialCadence(major=False, modal=
    getPartialCadence(major=False, modal=True, weights = [3,1,2])
