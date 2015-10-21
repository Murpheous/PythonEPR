
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
    
