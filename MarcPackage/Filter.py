from pygame import Surface,SRCALPHA
import PIL.Image
def Load(File):
    Image=PIL.Image.open(File)
    Result=Filter((0,0),None)
    Result.Size=Image.size
    Result.Pixels={}
    ImagePixels=Image.load()
    for X in range(Image.size[0]):
        for Y in range(Image.size[1]):
            Result.Pixels.update({(X,Y):ImagePixels[X,Y]})
    return Result
def SurfaceToFilter(SurfaceToConvert):
    Result=Filter((0,0),None)
    Result.Size=SurfaceToConvert.get_size()
    for X in range(Result.Size[0]):
        for Y in range(Result.Size[1]):
            Result.Pixels.update({(X,Y):SurfaceToConvert.get_at((X,Y))})
    return Result
def FilterToSurface(FilterToConvert):
    Result=Surface(FilterToConvert.Size,SRCALPHA)
    for X in range(Result.get_size()[0]):
        for Y in range(Result.get_size()[1]):
            Result.set_at((X,Y),FilterToConvert.Pixels[X,Y])
    return Result
def RGBA(Color):
    Result=Color
    for T in range(4-len(Color)):
        Result=Result.__add__((255,))
    return Result
class Filter:
    def __init__(self,Size,Color):
        self.Size=Size
        self.Pixels={}
        try:
            self.Fill(RGBA(Color))
        except:
            pass
    def Replace(self,OldColor,NewColor):
        try:
            for X in range(self.Size[0]):
                for Y in range(self.Size[1]):
                    if self.Pixels[X,Y]==OldColor:
                        self.Pixels.update({(X,Y):NewColor})
        except:
            pass
    def Fill(self,Color):
        for X in range(self.Size[0]):
            for Y in range(self.Size[1]):
                self.Pixels.update({(X,Y):Color})
    
    def Bigger(self,Bigger):
        Result=Filter((0,0),None)
        Result.Size=(int(Bigger[0]*self.Size[0]),int(Bigger[1]*self.Size[1]))
        for X in range(int(Bigger[0]*self.Size[0])):
            for Y in range(int(Bigger[1]*self.Size[1])):
                Result.Pixels.update({(X,Y):self.Pixels[int(X/Bigger[0]),int(Y/Bigger[1])]})
        self.Size=Result.Size
        self.Pixels=Result.Pixels
    def Pixelisation(self,Pixelisation):
        Result=Filter((0,0),None)
        Result.Size=self.Size
        for X in range(self.Size[0]):
            for Y in range(self.Size[1]):
                Result.Pixels.update({(X,Y):self.Pixels[int(X-X%Pixelisation[0]),int(Y-Y%Pixelisation[1])]})
        self.Size=Result.Size
        self.Pixels=Result.Pixels
    def Copy(self):
        Result=Filter((0,0),None)
        Result.Size=self.Size
        for X in range(self.Size[0]):
            for Y in range(self.Size[1]):
                Result.Pixels.update({(X,Y):self.Pixels[X,Y]})
        return Result   
    def Blit(self,FilterToBlit,PositionToBlit):
        for X in range(FilterToBlit.Size[0]):
            for Y in range(FilterToBlit.Size[1]):
                try:
                    self.Pixels[(X+PositionToBlit[0],Y+PositionToBlit[1])]=FilterToBlit.Pixels[X,Y]
                except:
                    pass
    def Gray(self):
        for X in range(self.Size[0]):
            for Y in range(self.Size[1]):
                Color=self.Pixels[X,Y]
                self.Pixels[(X,Y)]=(((Color[0]+Color[1]+Color[2])/3,)*3).__add__((255,))
    def GetArray1D(self,Alpha=False):
        Result=np.array([])
        for X in range(self.Size[0]):
            for Y in range(self.Size[1]):
                Color=self.Pixels[X,Y]
                if not Alpha:
                    Color=Color[:-1]
                Result=np.append(Color,Result)
        return Result
    def Save(self,FileName):
        ImageToSave=FilterToPILImage(self)
        ImageToSave.save(FileName)
