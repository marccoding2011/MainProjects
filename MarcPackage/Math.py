from math import *
def DegresToRadians(Degres):
    return Degres/radian
radian=1/radians(1)
def TurnMove(Move,Radians):
    return (cos(Radians)*Move[0]-sin(Radians)*Move[1],sin(Radians)*Move[0]+cos(Radians)*Move[1])
def Primes(N):
    List=set()
    ListReturn=set()
    for i in range(2,N+1):
        if not i in List:
            ListReturn.add(i)
            k=0
            while k<=N:
                k+=i
                List.add(k)
    Running=False
    return ListReturn
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
