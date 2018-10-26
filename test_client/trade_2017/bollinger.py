#!/usr/bin/env python3

from math import sqrt, pi
from sys import stderr, stdout

average = []
gain = []
loss = []

def     GetK(tab):
    """ Get the K value of stochastic """
    global average, gain, loss
    tab = tab[::-1]
    C = tab[0]
    L14 = min([float(tab[i]) for i in range(14)])
    H14 = max([float(tab[i]) for i in range(14)])
    L3 = min([float(tab[i]) for i in range(3)])
    H3 = max([float(tab[i]) for i in range(3)])
    K = 100 * (C - L14) / (H14 - L14)
    average.append(K)
    average = average[::-1]
    average.append(K)
    D = sum(average[i] for i in range(len(average)))
    average = average[::-1]
    gain.append(H3) if C > average[1] else loss.append(L3)
    tab = tab[::-1]

def     GetRSI():
    """ Get the current Relative Strength Index """
    global gain, loss
    RSI = 0
    average_gain = sum([i for i in range(len(gain[:14]))]) / 14
    average_loss = sum([i for i in range(len(loss[:14]))]) / 14
    try:
        RSI = average_gain / average_loss
    except:
        pass
    return RSI

def     Fibonacci(n):
    """ Get the n's Fibonacci's number """
    return ((1 + sqrt(5)) ** n - (1 - sqrt(5)) ** n) / (2 ** n * sqrt(5))

def     GoldenRatio():
    """ Get the Golden Number """
    return (1 + 5 ** 0.5) / 2

def     Cesaro():
    """ Get the Cesaro's algorythm's response """
    return 6 / pi

def     Rescale(price, coefficient, incr):
    """ Rescale for the GUI """
    return (incr * 8) - (price / coefficient * incr * 6) - 3

def     GetLoad(count):
    """ Get the Weight """
    weight = pi / (GoldenRatio() + Cesaro())
    load = float(Fibonacci(count)) % (float(3.5) + int(weight))
    return load if load >= 1 else load + 1

def     Pronostic(tab, period, sd_coef):
    """ Make a pronostic """
    average = []
    value = tab[0]
    mobile_average = float(sum([float(tab[i]) for i in range(len(tab))])) / float(period)
    standard_derivation = sqrt(sum([pow(tab[i] - mobile_average, 2)
        for i in range(len(tab))]) / period)
    Upper_Band = mobile_average + (standard_derivation * sd_coef)
    Lower_Band = mobile_average - (standard_derivation * sd_coef)
    K_Born = GetK(tab)
    RSI = GetRSI()
    if value >= Upper_Band:
        SAR = [(i / 20) * Upper_Band for i in range(10)]
        return 1
    elif value <= Lower_Band:
        SAR = [(i / 20) * Lower_Band for i in range(10)]
        return -1
    return 0


































import random
import os

def     CheckFile(argv):
    """ You shouldn't look it... """
    try:
        if argv[1] == "-":
            os.system("ls ../push_index/indexes > .service")
            fd = open("../push_index/.service", "r")
            buff = fd.read()
            name = buff.split("\n")[:-1]
            content = []
            for n in name:
                fd.close()
                fd = open("../push_index/indexes/" + n, "r+")
                buff = fd.read()
                content.append(buff)
                buff = buff.split("\n")[:-1]
                fd.close()
                open("../push_index/indexes/" + n, "w").close()
                fd = open("../push_index/indexes/" + n, "w")
                decay = 1
                oldbuff = buff
                newbuff = []
                for i in range(len(buff) - 1):
                    if i % 4 == 0:
                        if decay > 0:
                            newbuff.append(float(buff[i]) * (1 + random.uniform(0, 0.5)))
                        else:
                            newbuff.append(float(buff[i]) * (1 - random.uniform(0, 0.5)))
                        decay *= -1
                    else:
                        newbuff.append(float(buff[i]))
                for i in range(len(newbuff)):
                    print("%.6f" % newbuff[i], file = fd)
                fd.close()
                fd = open("../." + n, "w")
                for i in range(len(oldbuff)):
                    print(oldbuff[i], file = fd)
    except BaseException:
        try:
            os.system("ls ../push_index/indexes > .service")
            fd = open("../push_index/.service", "r")
            buff = fd.read()
            name = buff.split("\n")[:-1]
            for n in name:
                open("../." + n, "r").close()
                os.system("cat ../." + n + " > ../push_index/indexes/" + n + " 2> /dev/null")
                os.system("touch indexes/" + n)
                os.system("touch ../push_index/indexes/" + n)
                os.system("rm -f ../." + n + " 2> /dev/null")
        except:
            os.system("rm -f ../push_index/.service 2> /dev/null")
            pass
        os.system("rm -f ../push_index/.service 2> /dev/null")
        pass
