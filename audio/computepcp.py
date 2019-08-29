from madmom.audio.signal import Signal, FramedSignal
from madmom.audio.stft import ShortTimeFourierTransform
from madmom.audio.spectrogram import Spectrogram
from madmom.audio.chroma import PitchClassProfile, HarmonicPitchClassProfile, DeepChromaProcessor
from madmom.audio.hpss import HarmonicPercussiveSourceSeparation
from math import log, exp, sqrt
import matplotlib.pyplot as plt
import sys
import json

reload(sys)  
sys.setdefaultencoding('utf8')

# def getFlatness(spec, show = False):
#     flatness = []
#     for frame in spec:
#         try:
#             nInv = 1 / float(len(frame))
#             sumLog = sum(map(log, frame))
#             num = exp(nInv * sumLog)
#             den = nInv * sum(frame)
#             flatness.append(1 - pow(num / den, 0.5))
#         except:
#             flatness.append(0)
#     if show:
#         plt.plot(flatness)
#         plt.show()
#     return flatness

def flatness(hist):
    product = reduce(lambda x, y: x * y, hist)
    if sum(hist) < 1:
        return 0
    flat = pow(product, 1./len(hist)) / (sum(hist) / float(len(hist)))
    return 1 - pow(flat, 2)

def getPCPHistogram(filename, fs = 8192, show = False):

    res = {}

    sig = Signal(filename, num_channels = 1)
    fsig = FramedSignal(sig, frame_size = fs)
    stft = ShortTimeFourierTransform(fsig)
    spec = Spectrogram(stft)
    chroma = PitchClassProfile(spec, num_classes=12)

    hist = [0 for i in range(12)]
    hist_f = [0 for i in range(12)]
    for f in range(len(chroma)):
        wf = chroma[f]
        hist = map(sum, zip(hist, wf))
        f = flatness(wf)
        hist_f = map(sum, zip(hist_f, [w * f for w in wf]))

    s = sum(hist)
    hist = map(lambda x: x / s, hist)
    C_hist = [hist[i-9] for i in range(12)]
    res['standard'] = C_hist

    s_f = sum(hist_f)
    hist_f = map(lambda x: x / s_f, hist_f)
    C_hist_f = [hist_f[i-9] for i in range(12)]
    res['standard_f'] = C_hist_f

    hpss = HarmonicPercussiveSourceSeparation()
    h, _ = hpss.process(spec)
    chroma = PitchClassProfile(h, num_classes=12)

    hist = [0 for i in range(12)]
    hist_f = [0 for i in range(12)]
    for f in range(len(chroma)):
        wf = chroma[f]
        hist = map(sum, zip(hist, wf))
        f = flatness(wf)
        hist_f = map(sum, zip(hist_f, [w * f for w in wf]))

    s = sum(hist)
    hist = map(lambda x: x / s, hist)
    C_hist = [hist[i-9] for i in range(12)]
    res['hpss'] = C_hist

    s_f = sum(hist_f)
    hist_f = map(lambda x: x / s_f, hist_f)
    C_hist_f = [hist_f[i-9] for i in range(12)]
    res['hpss_f'] = C_hist_f

    dcp = DeepChromaProcessor()
    deepchroma = dcp(filename)

    hist = [0 for i in range(12)]
    hist_f = [0 for i in range(12)]
    for f in range(len(deepchroma)):
        wf = deepchroma[f]
        hist = map(sum, zip(hist, wf))
        f = flatness(wf)
        hist_f = map(sum, zip(hist_f, [w * f for w in wf]))

    s = sum(hist)
    hist = map(lambda x: x / s, hist)
    res['deep'] = hist

    s_f = sum(hist_f)
    hist_f = map(lambda x: x / s_f, hist_f)
    res['deep_f'] = hist_f

    if show:
        plt.subplot(131)
        plt.barh(range(12), res['standard'])
        plt.subplot(132)
        plt.barh(range(12), res['hpss'])
        plt.subplot(133)
        plt.barh(range(12), res['deep'])
        plt.show()
    return res

    # return C_hist

if __name__ == '__main__':
    filename = sys.argv[1]
    outdir = sys.argv[2]
    show = True if len(sys.argv) > 2 and sys.argv[2] == 'plot' else False

    h = getPCPHistogram(filename, fs = 2048, show = show)

    outfile = '%s/%s.json' % (outdir, filename.split('/')[-1][:3])
    with open(outfile, 'w') as jsonout:
        json.dump(h, jsonout)

    print '%s done' % filename
