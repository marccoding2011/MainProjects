from pygame import *
import Math as mth
import Filter as fltr
init()
class Window:
    def __init__(self,Size,BackgroundColor=(255,255,255),Resizable=False,Tick=None,Running=None,Checking=None,Items=[],Initialisation=None,Exit=None,Bonus=False):
        global Screen
        self.Run=True
        self.Exit=Exit
        self.Clock=time.Clock()
        self.Running=Running
        self.Checking=Checking
        self.Items=Items
        self.BackgroundColor=BackgroundColor
        if Resizable:
            self.Screen=display.set_mode(Size,RESIZABLE)
        else:
            self.Screen=display.set_mode(Size)
        if Initialisation:
            Initialisation(self)
        while self.Run:
            for Event in event.get():
                if Event.type == QUIT:
                    self.Run=False
                if self.Checking:
                    self.Checking(self,Event)
                if Bonus:
                    if Event.type==MOUSEBUTTONDOWN:
                        if Event.button in (0,1):
                            for I in self.Items:
                                if IsIn(Event.pos,I):
                                    if I.Click:
                                        I.Clicked=True
                                        if I.ClickFunctionDown:
                                            I.ClickFunctionDown(I,self)
                                    if I.ButtonFunction:
                                        I.ButtonFunction(I,self)
                    if Event.type==MOUSEBUTTONUP:
                        for I in self.Items:
                            if I.Clicked:
                                I.Clicked=False
                                if I.ClickFunctionUp:
                                    I.ClickFunctionUp(I,self)
                    if Event.type==MOUSEMOTION:
                        for I in self.Items:
                            if I.Clicked:
                                I.Position=(Event.pos[0]-I.Size[0]/2,Event.pos[1]-I.Size[1]/2)
            if self.Running:
                self.Running(self)
            self.Screen.fill(self.BackgroundColor)
            for I in self.Items:
                self.Screen.blit(I.Surface,I.Position)
            display.update()
            if Tick:
                self.Clock.tick(Tick)
        else:
            if self.Exit:
                self.Exit(self)
            display.quit()
def IsIn(Position,Sprite):
    return Sprite.Position[0]+Sprite.Size[0]>=Position[0] and Sprite.Position[0]<=Position[0] and Sprite.Position[1]+Sprite.Size[1]>=Position[1] and Sprite.Position[1]<=Position[1]
def Touch(Sprite1,Sprite2):
    return Sprite1.Position[0]+Sprite1.Size[0]>=Sprite2.Position[0] and Sprite1.Position[0]<=Sprite2.Position[0]+Sprite2.Size[0] and Sprite1.Position[1]+Sprite1.Size[1]>=Sprite2.Position[1] and Sprite1.Position[1]<=Sprite2.Position[1]+Sprite2.Size[1]
def Collide(Sprite1,Sprite2):
    return Sprite1.Position[0]+Sprite1.Size[0]>Sprite2.Position[0] and Sprite1.Position[0]<Sprite2.Position[0]+Sprite2.Size[0] and Sprite1.Position[1]+Sprite1.Size[1]>Sprite2.Position[1] and Sprite1.Position[1]<Sprite2.Position[1]+Sprite2.Size[1]
def Gravity(Time,Gravity,Vector):
    return (Time**2/2*Gravity[0]+Vector[0]*Time,Time**2/2*Gravity[1]+Vector[1]*Time)
class Sprite:
    def __init__(self,Filter,Position=(0,0),ButtonFunction=None,Click=False,ClickFunctionUp=None,ClickFunctionDown=None,Type=''):
        self.Type=Type
        self.Filter=Filter
        self.Surface=fltr.FilterToSurface(self.Filter)
        self.Position=Position
        self.Size=self.Filter.Size
        self.ButtonFunction=ButtonFunction
        self.Click=Click
        self.Clicked=False
        self.ClickFunctionUp=ClickFunctionUp
        self.ClickFunctionDown=ClickFunctionDown
    def ChangeImage(self,NewFilter):
        self.Filter=NewFilter
        self.Update()
    def Update(self):
        self.Surface=fltr.FilterToSurface(self.Filter)
        self.Size=self.Filter.Size
    def Move(self,Move:tuple,Radians=0):
        Move=mth.MoveTurn()
        self.Position=(self.Position[0]+Move[0],self.Position[1]+Move[1])
    def Copy(self):
        Result=Sprite(self.Filter.Copy(),self.Position,self.ButtonFunction,self.Click,self.ClickFunctionUp,self.ClickFunctionDown,self.Type)
        return Result
class Text:
    def __init__(self,Text:str,Size:int,Position=(0,0),Color=(0,0,0),Font='',Bold=False,Italic=False,ButtonFunction=None,Click=False,ClickFunctionDown=None,ClickFunctionUp=None,Type=''):
        self.Type=Type
        self.Text=Text
        self.Color=Color
        self.FontSize=Size
        self.FontName=Font
        self.Font=font.SysFont(self.FontName,self.FontSize,Bold,Italic)
        self.Surface=self.Font.render(Text,1,Color)
        self.Size=self.Surface.get_size()
        self.Bold=Bold
        self.Italic=Italic
        self.ButtonFunction=ButtonFunction
        self.Position=Position
        self.Click=Click
        self.Clicked=False
        self.ClickFunctionDown=ClickFunctionDown
        self.ClickFunctionUp=ClickFunctionUp
    def ChangeText(self,Text:str='',Color:tuple=(0,0,0)):
        self.Text=Text
        self.Color=Color
        self.Surface=self.Font.render(self.Text,1,self.Color)
        self.UpdateAroundSurface()
    def ChangeFont(self,Font='',Bold=False,Italic=False,Size:int=0):
        self.FontSize=Size
        self.Bold=Bold
        self.Italic=Italic
        self.FontName=Font
        self.Font=font.SysFont(self.FontName,self.FontSize,Bold,Italic)
        self.Surface=self.Font.render(self.Text,True,self.Color)
        self.UpdateAroundSurface()
    def UpdateAroundSurface(self):
        self.Filter=fltr.SurfaceToFilter(self.Surface)
        self.Size=self.Surface.get_size()
    def UpdateAroundFilter(self):
        self.Surface=fltr.FilterToSurface(self.Filter)
        self.Size=self.Filter.Size
    def Move(self,Move:tuple,Radians=0):
        Move=mth.MoveTurn()
        self.Position=(self.Position[0]+Move[0],self.Position[1]+Move[1])
    def Copy(self):
        Result=Text(self.Text,self.FontSize,self.Position,self.Color,self.FontName,self.Bold,self.Italic,self.ButtonFunction,self.Click,self.ClickFunctionUp,self.ClickFunctionDown,self.Type)
        return Result