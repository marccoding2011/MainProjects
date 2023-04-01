from math import *
def DegresToRadians(Degres):
    return Degres/radian
radian=1/radians(1)
def TurnMove(Move,Radians):
    return (cos(Radians)*Move[0]-sin(Radians)*Move[1],sin(Radians)*Move[0]+cos(Radians)*Move[1])
def Primes(Limit):
    List=[True]*Limit
    List[0]=False
    List[1]=False
    for i in range(2,int(sqrt(Limit))+1):
        if List[i]:
            t=2
            while t*i<Limit:
                List[t*i]=False
                t+=1
    Result=[]
    t=0
    for i in List:
        if i:
            Result.append(t)
        t+=1
    return Result
def IsPrime(Number):
    if Number<2:
        return False
    for Divisor in range(2,int(sqrt(Number))+1):
        if Number%Divisor==0:
            return False
    return True
def GetDivisors(Number):
    if Number<1:
        raise ArithmeticError
    Divisors=[]
    for Divisor in range(1,int(sqrt(Number))+1):
        if Number%Divisor==0:
            Divisors.append(Divisor)
    return Divisors
