import math
import np

# Spatial definitions
worldUp = [0.0, 1.0, 0.0];
worldCross = [0.0, 0.0, 1.0];
worldThrough = [1.0, 0.0, 0.0];

def t(theta):
    return 1-math.cos(theta)

def a1(angle,  axis, tr, cos):
    return (tr * axis[0] * axis[0]) + cos;
    
def a2(angle,  axis, tr, sin):
    return (tr * axis[0] * axis[1]) - (sin * axis[2])
    
def a3(angle,  axis, tr, sin):
    return (tr * axis[0] * axis[2]) + (sin * axis[1])

def b1(angle,  axis, tr, sin):
    return (tr * axis[0] * axis[1]) + (sin * axis[2])

def b2(angle,  axis, tr, cos):
    return (tr * axis[1] * axis[1]) + cos

def b3(angle,  axis, tr, sin):
    return (tr * axis[1] * axis[2]) - (sin * axis[0])

def c1(angle,  axis, tr, sin):
    return (tr * axis[0] * axis[2]) - (sin * axis[1])

def c2(angle,  axis, tr, sin):
    return (tr * axis[1] * axis[2]) + (sin * axis[0])

def c3(angle,  axis, tr, cos):
    return (tr * axis[2] * axis[2]) + cos

def RotateAroundAxis( v, axis, angle):
   
    result = [0.0,0.0,0.0]
    tr = t(angle);
    cos = math.cos(angle);
    sin = math.sin(angle);

    result[0] = a1(angle, axis, tr, cos) * v[0] + a2(angle, axis, tr, sin) * v[1] + a3(angle, axis, tr, sin) * v[2];
    result[1] = b1(angle, axis, tr, sin) * v[0] + b2(angle, axis, tr, cos) * v[1] + b3(angle, axis, tr, sin) * v[2];
    result[2] = c1(angle, axis, tr, sin) * v[0] + c2(angle, axis, tr, sin) * v[1] + c3(angle, axis, tr, cos) * v[2]; 

    return result;
    
def halfPI():
    result=math.pi/2.0
    return result

def quarterPI():
    result=math.pi/4.0
    return result

def twoPI():
    result = math.pi + math.pi
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
        self._phaseAngle = PhaseAngle
        self._isClockwise = IsClockwise
        
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

class VectorPhoton:
        def __init__(self):
            _spinAxis = worldCross
            # phase zero vector: The intersection between planes defined by normal
            # to analyzer face (worldThrough), and the plane of spin (i.e. the plane normal
            # to the spin axis) of the polarized beam.
            _phaseZeroVector = worldUp
            # The phaseVector is the actual instantaneous phase of the particular photon
            _phaseVec = worldUp         

        def MakeCircular(self, phaseAngle = 0.0, bSense= True):
            _phaseVec = RotateAroundAxis( worldUp, _spinAxis, phaseAngle)
            
class Photon:
    def __init__(self):
        _spinAxis = worldCross

        self._phasors = []

    def AddPhasor(self, phaseAngle=0.0, bSense=True):
        self._phasors.append(PhotonPhasor(LimitPi(phaseAngle),bSense))

    def MakeCircular(self, PhaseAngle, bSense = True):
        self._phasors = []
        if (bSense):
            _spinAxis = worldThrough
        else:
            _spinAxis = worldThrough*-1;
        
    def MakeLinear(self, LinearAxis, LinearPhase):
        self._phasors = []
        self.AddPhasor(LinearAxis + LinearPhase, True)
        self.AddPhasor(LinearAxis - LinearPhase, False)

    def MakeLinearDegrees(self, AxisDeg, PhaseDeg):
        self.MakeLinear((AxisDeg*math.pi)/180.0,(PhaseDeg*math.pi)/180.0)
 
    @property
    def Phasors(self):
        """Phasors: List of phasors 1=Circular 2=Linear"""
        return self._phasors
        
    def Analyze(self, AnalyzerAxis = 0.0):
        '''
        First step is to convert each phasor into an axis and a phase
        angle with respect to that axis.
        
        In the case of a linearly polarized photon, the 'photon axis'
        is identified as the angle of the mid point between the pair
        of phasors, such that each phasor is at the same phase angle
        with respect to that axis.
        
        In the case of a single phasor, the opposing phasor is to be
        supplied by the analyzer. In this case a circularly porlrized
        photon is always treated as being at phase angle zero, with
        the axis aligned with the phasor.
        '''
        if (len(self._phasors) == 0):
            return None # empty photon returns null result

        # The software step for calculating the photn axis is acieved
        # by calculating the arithmetic mean of the phase angle.
        mappedAxis = 0
        for phasor in self._phasors:
           mappedAxis += LimitPi(phasor.PhaseAngle)
        mappedAxis = mappedAxis/len(self._phasors)
        mappedAxis = LimitHalfPi(mappedAxis)
        
        # Calculate the acute angle  between the photon Axis and the
        # Analyzer Axis
        axisDelta = LimitHalfPi(mappedAxis - AnalyzerAxis)
        shiftSineSq = ExtendedSineSq(axisDelta)*math.pi
        nResult = 1

        # Iterate: calculating the result for each phasor independently
        # of the other
        for phasor in self._phasors:
            # Photon's Phasor Orientation is transformed into Analyzer Phase

            # Calculate in range ±180° WRT Photon's projected Axis 
            analyzerPhase = LimitPi(mappedAxis - phasor.PhaseAngle)

            # Now Transform Phase, Axis, Sense into Phasor Gate 'Phasor'
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
    
      
        
    
