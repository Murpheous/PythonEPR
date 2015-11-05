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

class Analyzer:
    def __init__(self, Axis = 0.0):
        self._axis = 0.0
        
    @property
    def Axis(self):
        """Axis: the acute angle between the A Axis and world 'up' vector (±90 degrees)"""
        return _axis
    
    @Axis.setter
    def Axis(self,value):
        self._axis = Limit90(value)

class Phasor:
    def __init__(self, PhaseAngle = 0, IsClockwise = True):
        self._phaseAngle = PhaseAngle;
        self._isClockwise = IsClockWise;
        
    @property
    def Sense(self):
        if self._isClockwise:
            return 1
        else:
            return -1

    @property
    def IsClockWise(self):
        return _isClockwise

    @property
    def PhaseAngle(self):
        return _phaseAngle
    
    
class Photon:
    def __init__(self):
        self._phasors = []

    def AddPhasor(self, phaseAngle, bSense):
        _phasors.Add(Phasor(Limit180(phaseAngle),bSense)))

    def makeCircular(self, PhaseAngle, bSense = true)
        self._phasors = []
        self.AddPhasor(PhaseAngle,bSense)
        
    def makeLinear(self, LinearAxis, LinearPhase):
        self._phasors = []
        self.AddPhasor(LinearAxis + LinearPhase, True)
        self.AddPhasor(LinearAxis - LinearPhase, False)

    @property
        """Phasors: List of phasors 1=Circular 2=Linear"""
    def Phasors(self):
        return self._phasors

    # Analyze with respect to a particular analyzer axis   
    def Analyze(self, AnalyzerAxis = 0.0):
        if (Len(self._phasors) == 0):
            return None
        photonAxis = 0
        for phasor in self._phasors:
           photonAxis += Limit90(phasor.PhaseAngle)
        photonAxis = photonAxis/Len(self._phasors)
        MappedPhasors = []
        for phasor in self._phasors:
            NewPhasor = Phasor(phasor.PhaseAngle - photonAxis,phasor.IsClockWise)
            mappedPhasors.Add(photonAxis += Limit90(phasor.PhaseAngle)
        
        return True

    
      
        
    
