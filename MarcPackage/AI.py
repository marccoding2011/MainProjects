import random
import numpy as np
from scipy import signal
class QTable():
    def __init__(self,Get,Pos,Gamma,Epsilon,Alpha,Play,Start,Rew):
        self.Get=Get
        self.Pos=Pos
        self.Gamma=Gamma
        self.Epsilon=Epsilon
        self.Alpha=Alpha
        self.Play=Play
        self.Start=Start
        self.Rew=Rew
        self.Update()
    def Update(self):
        self.QTable={}
        for QItem in self.Pos:
            QPos={}
            for QGet in self.Get(QPos):
                QPos.update({QGet:0})
            self.QTable.update(QPos)
    def Choose(self,Pos):
        QMax=self.QTable[Pos].values()[0]
        QList=self.QTable[Pos].keys()[0]
        for QValue,QPath in self.QTable[Pos].values()[1:]:
            if QValue==QMax:
                QList.append(QPath)
            elif QValue>QMax:
                QMax=QValue
                QList=[QPath]
        return (QMax,random.choice(QList))
    def Run(self):
        Best=random.Random()<self.Epsilon
        QPos=self.Start
        while len(self.Get(QPos))>0:
            for QPath in QTable[QPos]:
                self.QTable[QPos][QPath]+=self.Aplha*(self.Rew(QPos)+self.Epsilon*self.Choose(self.Play(QPos,QPath))[0]-self.Choose(QPos)[0])
            if Best:
                QPath=self.Choose(QPos)[1]
            else:
                QPath=random.choice(self.QTable[QPos].values())
            QPos=self.Play(QPos,QPath)
class Layer:
    def __init__(self):
        self.Input = None
        self.Output = None
    def ForwardPropagation(self,Input):
        raise NotImplementedError
    def BackwardPropagation(self,OutputError,LearningRate):
        raise NotImplementedError
class FCLayer(Layer):
    def __init__(self,InputSize,OutputSize):
        self.Weights = np.random.rand(InputSize,OutputSize)-0.5
        self.Bias = np.random.rand(1,OutputSize)-0.5
    def ForwardPropagation(self,InputData):
        self.Input = InputData
        self.Output = np.dot(self.Input,self.Weights)+self.Bias
        return self.Output
    def BackwardPropagation(self, OutputError, LearningRate):
        InputError = np.dot(OutputError, self.Weights.T)
        WeightsError = np.dot(self.Input.T, OutputError)
        self.Weights -= LearningRate * WeightsError
        self.Bias -= LearningRate * OutputError
        return InputError
class ActivationLayer(Layer):
    def __init__(self,Activation,ActivationPrime):
        self.Activation=Activation
        self.ActivationPrime=ActivationPrime
    def ForwardPropagation(self,InputData):
        self.Input=InputData
        self.Output=self.Activation(self.Input)
        return self.Output
    def BackwardPropagation(self,OutputError,LearningRate):
        return self.ActivationPrime(self.Input)*OutputError
class ConvLayer(Layer):
    def __init__(self,InputShape,KernelShape,LayerDepth):
        self.InputShape=InputShape
        self.InputDepth=InputShape[2]
        self.KernelShape=KernelShape
        self.LayerDepth=LayerDepth
        self.OutputShape=(InputShape[0]-KernelShape[0]+1,InputShape[1]-KernelShape[1]+1,LayerDepth)
        self.Weights=np.random.rand(KernelShape[0],KernelShape[1],self.InputDepth,LayerDepth)-0.5
        self.Bias=np.random.rand(LayerDepth)-0.5
    def ForwardPropagation(self,Input):
        self.Input=Input
        self.Output=np.zeros(self.OutputShape)
        for LoopLayerDepth in range(self.LayerDepth):
            for LoopInputDepth in range(self.InputDepth):
                self.Output[:,:,LoopLayerDepth]+=signal.correlate2d(self.Input[:,:,LoopInputDepth],self.Weights[:,:,LoopInputDepth,LoopLayerDepth],'valid')+self.Bias[LoopLayerDepth]
        return self.Output
    def BackwardPropagation(self,OutputError,LearningRate):
        InError=np.zeros(self.InputShape)
        dWeights=np.zeros((self.KernelShape[0],self.KernelShape[1],self.InputDepth,self.LayerDepth))
        dBias=np.zeros(self.LayerDepth)
        for LoopLayerDepth in range(self.layer_depth):
            for LoopInputDepth in range(self.input_depth):
                InError[:,:,LoopInputDepth]+=signal.convolve2d(OutputError[:,:,LoopLayerDepth],self.Weights[:,:,LoopInputDepth,LoopLayerDepth],'full')
                dWeights[:,:,LoopInputDepth,LoopLayerDepth]=signal.correlate2d(self.input[:,:,LoopInputDepth],OutputError[:,:,LoopLayerDepth],'valid')
            dBias[LoopLayerDepth]=self.LayerDepth*np.sum(OutputError[:,:,LoopLayerDepth])
        self.Weights-=LearningRate*dWeights
        self.Bias-=LearningRate*dBias
        return InError
class FlattenLayer(Layer):
    def ForwardPropagation(self,InputData):
        self.Input=InputData
        self.Output=InputData.flatten().reshape((1,-1))
        return self.Output
    def BackwardPropagation(self,OutputError,LearningRate):
        return OutputError.reshape(self.Input.shape)
def Tanh(Number):
    return np.tanh(Number)
def TanhPrime(Number):
    return 1-np.tanh(Number)**2
def Mse(Result,Desired):
    return np.mean(np.power(Result-Desired, 2))
def MsePrime(Result,Desired):
    return 2*(Desired-Result)/Result.size
class Network:
    def __init__(self):
        self.Layers=[]
        self.Loss=None
        self.LossPrime=None
    def Add(self,LayerToAdd):
        self.Layers.append(LayerToAdd)
    def Use(self,Loss,LossPrime):
        self.Loss=Loss
        self.LossPrime=LossPrime
    def Predict(self,InputData):
        Samples=len(InputData)
        Result=[]
        for Loop in range(Samples):
            Output = InputData[Loop]
            for LoopLayer in self.Layers:
                output = LoopLayer.ForwardPropagation(Output)
            Result.append(output)
        return Result
    def Fit(self,InputTrain,OutputTrain,Epochs,LearningRate):
        Samples=len(InputTrain)
        for Loop in range(Epochs):
            Err=0
            for Sample in range(Samples):
                Output=OutputTrain[Sample]
                for LoopLayer in self.Layers:
                    Output=LoopLayer.ForwardPropagation(Output)
                Err+=self.Loss(OutputTrain[Sample],Output)
                Error=self.LossPrime(OutputTrain[Sample],Output)
                for LoopLayer in reversed(self.Layers):
                    Error=LoopLayer.BackwardPropagation(Error,LearningRate)
            Err/=Samples
