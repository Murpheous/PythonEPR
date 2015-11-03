import math
# Vector definitions
worldUp = (0.0, 1.0, 0.0);
worldCross = (0.0, 0.0, 1.0);
worldThrough = (1.0, 0.0, 0.0);
sense={'Clockwise':True,'AntiClockwise':False}

def twoPI():
    result=math.pi*2.0
    return result

def halfPI():
    result=math.pi/2.0
    return result

def quarterPI():
    result=math.pi/4.0
    return result

def Limit180(theta): # Flip large angles back into base range +- 180
    nPi = 0
    if (theta >= math.pi):
        nPi = math.trunc(theta/math.pi)
        nPi = math.trunc((nPi + 1)/2.0)
        theta = theta - (nPi*twoPI())
    else:
        if (theta <= -math.pi):
            nPi = math.trunc(theta/math.pi)
            nPi = (nPi - 1)/2
            theta = theta - (nPi*twoPI())
    return theta

def Limit90(theta):
    theta = Limit180(theta)
    if (theta > halfPI()):
        theta = theta-math.pi
    else:
        if (theta < -halfPI()):
            theta = theta+math.pi
    return theta

def ExtendedAsin(value):
    nOffset = 0
    integerPart = math.trunc(value)
    if (integerPart >= 1):
        nOffset = math.trunc((integerPart + 1)/2)
    else:
        if (integerPart <= -1):
            nOffset = math.trunc((integerPart - 1)/2)
    nOffset *= 2
    fractionPart = value - nOffset
    result = math.asin(fractionPart) + ((nOffset/2)*math.pi)
    return result

def ExtendedSine(theta):
    thetaNormalised = (theta + halfPI())/math.pi
    integerPart = math.trunc(thetaNormalised)
    if (thetaNormalised < 0):
        integerPart -= 1
    fractionPart = theta - (integerPart*math.pi)
    result = math.sin(fractionPart) + integerPart*2
    return result


def ExtendedArcSinSq(value):
    intpart = math.floor(value)
    fracpart = value - intpart
    return math.asin(math.sqrt(fracpart)) + halfPI()*intpart

def ExtendedArcCosSq(value):
    return ExtendedArcSinSq(value + 0.5) - quarterPI()

def ExtendedSineSq(theta):
    nSineSign = 1
    integerPart = math.trunc(theta/halfPI())
    nOffset = 0
    if (integerPart >= 1):
        nOffset = math.trunc((integerPart + 1)/2)
    else:
        if (integerPart <= -1):
            nOffset = math.trunc((integerPart - 1)/2)
    nOffset *= 2
    dOffset = nOffset*halfPI()
    fractionPart = theta - dOffset
    dSine = math.sin(fractionPart)
    if (dSine < 0):
        nSineSign = -1
    dSine *= (dSine*nSineSign)
    return dSine + nOffset

class clPhasor:
    def __init__(self, phase = 0, sense = 1):
        self._phase = 0;
        self._isClockwise = True;
        self._initialized=False;
            
class clPhoton:
    def __init__(self):
        self.phasors = []
    
    def makeCircular(self, phase = 0, sense = 1):
        self.phasors = []
        self.phasors.Add(self, phase, sense)
        #tmp = clPhasor()
        #self.phasors.append(clPhasor
