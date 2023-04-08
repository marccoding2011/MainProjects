import os
def IsBissecstile(Year):
    return Year%4==0
def GetMonthsSize(Year):
    if IsBissecstile(Year):
        return [31,29,31,30,31,30,31,31,30,31,30,31]
    else:
        return [31,28,31,30,31,30,31,31,30,31,30,31]
def GetDay(Year,Month,Day):
    if Month<3:
        return ((23*Month)//9+Day+4+Year+(Year-1)//4-(Year-1)//100+(Year-1)//400)%7
    else:
        return ((23*Month)//9+Day+2+Year+Year//4-Year//100+Year//400)%7
def PrintReturn(Item):
    print(Item)
    return Item
def PrintLoad(Finished,Of):
    os.system('cls|clear')
    print(Finished*'#'+(Of-Finished)*'-')
