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

def ShiftToPlusMinusOne(arg):
    nCycles = math.trunc(arg)
    if arg >= 1.0:
        nCycles = math.trunc((nCycles +1.0)/2.0)
        arg = arg - (2 * nCycles)
    elif (arg <= -1.0):
        nCycles = math.trunc((nCycles -1.0)/2.0)
        arg = arg - (2 * nCycles)
    return arg
    
def LimitPi(theta): # Flip large angles back into base range +- 180
    nPi = 0
    if (theta >= math.pi):
        nPi = math.trunc(theta/math.pi)
        nPi = math.trunc((nPi + 1)/2.0)
        theta = theta - (nPi*twoPI())
    elif (theta <= -math.pi):
        nPi = math.trunc(theta/math.pi)
        nPi = (nPi - 1)/2
        theta = theta - (nPi*twoPI())
    return theta

def LimitHalfPi(theta):
    theta = LimitPi(theta)
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


def ExtendedArcSineSq(value):
    intpart = math.floor(value)
    fracpart = value - intpart
    return math.asin(math.sqrt(fracpart)) + halfPI()*intpart

def ExtendedArcCosSq(value):
    return ExtendedArcSineSq(value + 0.5) - quarterPI()

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
        self._axis = LimitHalfPi(value)

class PhotonPhasor:
    def __init__(self, PhaseAngle = 0, IsClockwise = True):
        self._phaseAngle = PhaseAngle;
        self._isClockwise = IsClockwise;
        
    @property
    def Sense(self):
        if self._isClockwise:
            return 1
        else:
            return -1

    @property
    def IsClockWise(self):
        return self._isClockwise

    @property
    def PhaseAngle(self):
        return self._phaseAngle

class AnalyzerPhasor:
    def __init__(self, Axis= 0, PhaseAngle = 0, Sense = 1):
        self._phaseAngle = LimitPi(PhaseAngle)
        self._isClockwise = (Sense >= 0)
        self._axis = Axis    

    @property
    def Sense(self):
        if self._isClockwise:
            return 1
        else:
            return -1

    @property
    def IsClockWise(self):
        return self._isClockwise

    @property
    def Phase(self):
        return self._phaseAngle

    @property
    def Axis(self):
        return self._axis
    
    
class Photon:
    def __init__(self):
        self._phasors = []

    def AddPhasor(self, phaseAngle=0.0, bSense=True):
        self._phasors.append(PhotonPhasor(LimitPi(phaseAngle),bSense))

    def MakeCircular(self, PhaseAngle, bSense = True):
        self._phasors = []
        self.AddPhasor(PhaseAngle,bSense)
        
    def MakeLinear(self, LinearAxis, LinearPhase):
        self._phasors = []
        self.AddPhasor(LinearAxis + LinearPhase, True)
        self.AddPhasor(LinearAxis - LinearPhase, False)

    @property
    def Phasors(self):
        """Phasors: List of phasors 1=Circular 2=Linear"""
        return self._phasors
        
    '''
    First step is to convert each phasor into an axis and a phase
    angle with respect to that axis.
    In the case of a linearly polarized photon, the 'photon axis'
    is identified as the angle of the mid point between the pair
    of phasors. Each phasor is at the same phase angle with respect to the axis.
    
    In the case of a single phasor, the opposing phasor is to be
    supplied by the analyzer. In this case a circularly porlrized
    photon is always treated as being at phase angle zero, with
    the axis aligned with the phasor. '''
    def Analyze(self, AnalyzerAxis = 0.0):
        if (len(self._phasors) == 0):
            return None # empty photon returns null result
        # In software this is done by calculating the artihmetic mean of the phase angle
        mappedAxis = 0
        for phasor in self._phasors:
           mappedAxis += LimitHalfPi(phasor.PhaseAngle)
        mappedAxis = mappedAxis/len(self._phasors)
        # Calculate the acute angle  between the photon Axis and the Analyzer Axis
        axisDelta = LimitHalfPi(mappedAxis - AnalyzerAxis)
        shiftSineSq = ExtendedSineSq(axisDelta)*math.pi
        nResult = 1
        # Iterate through phasors
        for phasor in self._phasors:
            # Photon's Phase angle onto Analyzer
            # Calculate phase in range ±180° from Mapped Axis 
            analyzerPhase = LimitPi(mappedAxis - phasor.PhaseAngle)
            # mappedPhasor = AnalyzerPhasor(mappedAxis, analyzerPhase, phasor.Sense)

            # Now Calculate Results
            phaseOffset = (shiftSineSq - shiftSineSq * phasor.Sense)/4.0
            effectivePhase = analyzerPhase + phaseOffset
            mappedResult = ShiftToPlusMinusOne(ExtendedSineSq(effectivePhase))
            mappedPi = mappedResult*math.pi
            if (mappedResult < -0.5) or (mappedResult >= 0.5):
                nResult *= -1
        if nResult >= 0:
            return True
        else:
            return False
    
      
        
    
