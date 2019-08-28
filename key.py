import sys

class Key:

    chromas = ['C','C#','D','D#','E','F','F#','G','G#','A','Bb','B']

    modes = {
        '': True,
        'maj': True,
        'dor': False,
        'phr': False,
        'lyd': True,
        'mix': True,
        'm': False, 'ael': False, 'min': False, # two names, standard minor mode 
        'loc': False
    }

    def __init__(self,
                 strRep = None,
                 chrMod = None,
                 transposition = 0):

        try:
            # instantiate from string representation
            if strRep:
                self.fund = strRep[0]
                if len(strRep) > 1 and strRep[1] in ['b', '#']:
                    self.fund += strRep[1]
                stemlen = len(self.fund)
                self.chrFund = Key.chromas.index(self.fund)
                if transposition != 0:
                    self.chrFund = (self.chrFund + transposition) % 12
                    self.fund = Key.chromas[self.chrFund]
                self.mode = strRep[stemlen:]
                self.major = Key.modes[self.mode]

            # instantiate from 2array (only C/A modes, for triads)
            elif chrMod:
                self.fund = Key.chromas[chrMod[0]]
                self.chrFund = chrMod[0]
                self.major = chrMod[1]
                self.mode = '' if self.major else 'm'

            else:
                raise Exception
        except:
            e = sys.exc_info()[0]
            print e
            raise ValueError

    def __str__(self):
        return '%s%s (%s, chroma %d)' % (self.fund,
                                         self.mode,
                                         'major' if self.major else 'minor',
                                         self.chrFund)
    def __repr__(self):
        return self.__str__()

    def simplified(self):
        if self.mode == 'loc':
            raise ValueError
        return self.fund + ('' if self.major else 'm')

    def triad(self):
        if self.major:
            third = (self.chrFund + 4) % 12
            fifth = (self.chrFund + 7) % 12
        else:
            third = (self.chrFund + 3) % 12
            if self.mode == 'loc':
                fifth = (self.chrFund + 6) % 12
            else:
                fifth = (self.chrFund + 7) % 12
        t = [0 for c in range(12)]
        t [ self.chrFund ] = 1
        t [ third ] = 1
        t [ fifth ] = 1
        return t

    def similar(self, other):
        return self.triad() == other.triad()

    def relative(self, other = None, fund = None):
        if other:
            if self.major and not other.major and (self.chrFund - other.chrFund) % 12 == 3:
                return True
            if other.major and not self.major and (other.chrFund - self.chrFund) % 12 == 3:
                return True
            return False
            # return sum(map(lambda d: d[0] * d[1],
            #                zip(self.triad(), other.triad()))) == 2
        if fund:
            if self.major and (self.chrFund - fund) % 12 == 3:
                return True
            if not self.major and (fund - self.chrFund) % 12 == 3:
                return True
            return False

    def fifth(self, other):
        if self.major and (self.chrFund - other.chrFund) % 12 == 7:
            return True
        if not other.major and not self.major and (other.chrFund - self.chrFund) % 12 == 7:
            return True
        # self.major and other.minor is not possible with church modes
        return False

    def parallel(self, other):
        if self.chrFund == other.chrFund and self.major != other.major:
            return True
        return False

    def neighbour(self, other):
        if self.major and not other.major:
            if (other.chrFund - self.chrFund) % 12 == 2:
                return True
        elif not self.major and other.major:
            if (self.chrFund - other.chrFund) % 12 == 2:
                return True
        return False

if __name__ == '__main__':
    k1 = Key(strRep = 'Cm')
    k2 = Key(strRep = 'C')
    print k1
    print k2
    print k1.parallel(k2)
    print k2.parallel(k1)
