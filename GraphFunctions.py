
import math
import EprMath

def makecsv(filename):
    csvfile = open(filename+".csv", "w")
    csvfile.write('"Theta";"ExtendedSin";"ExtendedSinSq";"ExtArcSin";"ExtArcSinSq"\n')
    for angle in range(-360,360):
        theta = angle*(EprMath.halfPI()/90)
        eSinSq = EprMath.ExtendedSineSq(theta)
        eSin = EprMath.ExtendedSine(theta)
        frac = angle/180.0
        eAsin = EprMath.ExtendedAsin(frac)
        eAsinSq = EprMath.ExtendedArcSinSq(frac)
        csvfile.write('{0};{1};{2};{3};{4}\n'.format(angle,eSin,eSinSq,eAsin,eAsinSq))
    csvfile.close()
    

def makeMalus():
    csvfile = open("Malus.csv", "w")
    csvfile.write('"Theta";"Rate"\n')
    for AxisDelta in range(0,90):
        Alice = 0
        Bob = 0
        AxisRadians = (AxisDelta*math.pi)/180.0
        for PhaseDecimalDeg in range(0,3600):
            PhaseRadians = (PhaseDecimalDeg*math.pi)/1800.0
            photon = EprMath.Photon()
            photon.MakeLinear(AxisRadians,PhaseRadians)
            nResult = photon.Analyze(0.0)
            if nResult != None:
                if nResult == True:
                    Alice += 1
                else:
                    Bob += 1
        fracAlice = float(Alice)/float(Alice + Bob)
        csvfile.write('{0};{1}\n'.format(AxisDelta,fracAlice))
    csvfile.close()

def vecMalus():
    csvfile = open("VecMalus.csv", "w")
    csvfile.write('"Theta";"Rate"\n')
    for AxisDelta in range(0,91):
        Alice = 0
        Bob = 0
        AxisRadians = (AxisDelta*math.pi)/180.0
        for PhaseDecimalDeg in range(0,3600):
            PhaseRadians = (PhaseDecimalDeg*math.pi)/1800.0
            photon = EprMath.VectorPhoton()
            photon.MakeLinear(AxisRadians,PhaseRadians)
            nResult = photon.Analyze(0.0)
            if nResult != None:
                if nResult == True:
                    Alice += 1
                else:
                    Bob += 1
        fracAlice = float(Alice)/float(Alice + Bob)
        csvfile.write('{0};{1}\n'.format(AxisDelta,fracAlice))
    csvfile.close()
    
def vecCorrelate():
    csvfile = open("VecCorrelate.csv", "w")
    csvfile.write('"Theta";"Rate"\n')
    for AxisDelta in range(0,91):
        SameCount = 0.0
        DifferCount = 0.0
        Total = 0.0
        for pairOrientation in range(-1800,1800):
            photonAlice = EprMath.VectorPhoton()
            photonBob = EprMath.VectorPhoton()
            PhaseAngle = (pairOrientation*math.pi)/1800.0
            photonAlice.MakeCircular(PhaseAngle,True)
            photonBob.MakeCircular(PhaseAngle,False)
            resultAlice = photonAlice.Analyze(0)
            resultBob = photonBob.Analyze(AxisDelta)
            if (resultBob == resultAlice):
                SameCount += 1.0
            else:
                DifferCount += -1.0
            Total = Total + 1
        correlation = (SameCount + DifferCount)/Total        
        csvfile.write('{0};{1}\n'.format(AxisDelta,correlation))
    csvfile.close()

def correlate():
    csvfile = open("Correlate.csv", "w")
    csvfile.write('"Theta";"Rate"\n')
    for AxisDelta in range(0,90):
        SameCount = 0.0
        DifferCount = 0.0
        Total = 0.0
        for pairOrientation in range(-1799,1800):
            photonAlice = EprMath.Photon()
            photonBob = EprMath.Photon()
            PhaseAngle = (pairOrientation*math.pi)/1800.0
            photonAlice.MakeCircular(PhaseAngle,True)
            photonBob.MakeCircular(PhaseAngle,False)
            resultAlice = photonAlice.Analyze(0)
            resultBob = photonBob.Analyze(AxisDelta)
            if (resultBob == resultAlice):
                SameCount += 1.0
            else:
                DifferCount += -1.0
            Total = Total + 1
        correlation = (SameCount + DifferCount)/Total        
        csvfile.write('{0};{1}\n'.format(AxisDelta,correlation))
    csvfile.close()
