from MarcPackage import Filter,AI
import os
import numpy as np
def LoadImages(Path):
    global BatchSize
    BatchSize=0
    Images=[]
    for FileName in os.listdir(os.getcwd()+'/'+Path):
        if FileName.endswith(".png") or FileName.endswith(".jpg"):
            Images.append(Filter.Load(os.getcwd()+'/'+Path+'/'+FileName))  
            BatchSize+=1
    return np.array([np.array([i.GetArray1D()]) for i in Images])
ImagesSize=(10,10)#Noise
InputImagesSize=(10,10)#ImagesSize
Images=LoadImages('SpaceInvadersImages')
Epochs=int(input('Combien de fois entraîner le réseau? '))
NumberGeneratedImages=int(input('Combien d\'images voulez-vous? '))
print('Création du générateur...')
Generator=AI.Network()
Generator.Use(AI.Mse,AI.MsePrime)
Generator.Add(AI.FCLayer((ImagesSize[0]*ImagesSize[1]),(ImagesSize[0]*ImagesSize[1])//2))
Generator.Add(AI.ActivationLayer(AI.Tanh,AI.TanhPrime))
Generator.Add(AI.FCLayer((ImagesSize[0]*ImagesSize[1])//2,(ImagesSize[0]*ImagesSize[1])//2))
Generator.Add(AI.ActivationLayer(AI.Tanh,AI.TanhPrime))
Generator.Add(AI.FCLayer((ImagesSize[0]*ImagesSize[1])//2,(ImagesSize[0]*ImagesSize[1])//4))
Generator.Add(AI.ActivationLayer(AI.Tanh,AI.TanhPrime))
Generator.Add(AI.FCLayer((ImagesSize[0]*ImagesSize[1])//4,(ImagesSize[0]*ImagesSize[1])//8))
Generator.Add(AI.ActivationLayer(AI.Tanh,AI.TanhPrime))
Generator.Add(AI.FCLayer((ImagesSize[0]*ImagesSize[1])//8,(ImagesSize[0]*ImagesSize[1])//10))
Generator.Add(AI.ActivationLayer(AI.Tanh,AI.TanhPrime))
Generator.Add(AI.FCLayer((ImagesSize[0]*ImagesSize[1])//10,(ImagesSize[0]*ImagesSize[1])//10))
Generator.Add(AI.ActivationLayer(AI.Tanh,AI.TanhPrime))
Generator.Add(AI.FCLayer((ImagesSize[0]*ImagesSize[1])//10,(ImagesSize[0]*ImagesSize[1])//10))
Generator.Add(AI.ActivationLayer(AI.Tanh,AI.TanhPrime))
Generator.Add(AI.FCLayer((ImagesSize[0]*ImagesSize[1])//10,(ImagesSize[0]*ImagesSize[1])//10))
Generator.Add(AI.ActivationLayer(AI.Tanh,AI.TanhPrime))
Generator.Add(AI.FCLayer((ImagesSize[0]*ImagesSize[1])//10,(ImagesSize[0]*ImagesSize[1])//10))
Generator.Add(AI.ActivationLayer(AI.Tanh,AI.TanhPrime))
Generator.Add(AI.FCLayer((ImagesSize[0]*ImagesSize[1])//10,InputImagesSize[0]*InputImagesSize[1]*3))
Generator.Add(AI.ActivationLayer(AI.Tanh,AI.TanhPrime))
print('Création du générateur: terminé.')
print('Entraînement du générateur...')
for Epoch in range(Epochs):
    Noise=np.random.randint(0,256,size=(ImagesSize[0]*ImagesSize[1]))
    Generator.Fit(InputTrain=Noise,OutputTrain=Images,Epochs=1,LearningRate=0.001)
print('Entraînement du générateur: terminé')
print('Génération des images...')
GeneratedImages=[]
for GenerateImage in range(NumberGeneratedImages):
    Noise=np.random.randint(0,256,size=(1,ImagesSize[0]*ImagesSize[1]))
    GeneratedImages.append(Generator.Predict(Noise))
print('Génération des images: terminé.')
print('Transformation des tenseurs en images...')
Filters=[]
for GeneratedImage in GeneratedImages:
    GeneratedImage=np.array()
    GeneratedImage=np.reshape(GeneratedImage,(ImagesSize[0]*3,ImagesSize[1]))
    FilterToAdd=Filter.Filter(ImagesSize,None)
    for X in range(ImagesSize[0]):
        for Y in range(ImagesSize[1]):
            FilterToAdd.Pixels.update({(X*3,Y):(GeneratedImage[X*3,Y],GeneratedImage[X*3+1,Y],GeneratedImage[X*3+2,Y],255)})
print('Transformation des tenseurs en images: terminé.')
print('Création du fichier...')
Folder=0
while True:
    try:
        os.mkdir(os.getcwd()+'/GeneratedImages'+str(Folder),)
        break
    except FileExistsError:
        Folder+=1
print('Création du fichier: terminé.')
print('Enregistrement des images')
ID=0
for LoopFilter in Filters:
    LoopFilter.Save(f'{os.getcwd()}/GeneratedImages{Folder}/Image{ID}')
    ID+=1
print('Enregistrement des images: terminé')
print(f'Les images ont été stockées dans le fichier: GeneratedImages{Folder}')
