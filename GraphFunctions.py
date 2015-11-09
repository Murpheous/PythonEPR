
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
            if photon.Analyze(0.0) == True:
                Alice += 1
            else:
                Bob += 1
        fracAlice = float(Alice)/float(Alice + Bob)
        csvfile.write('{0};{1}\n'.format(AxisDelta,fracAlice))
    csvfile.close()
        
