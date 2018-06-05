import numpy
import math
from datetime import datetime, time


class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        self.signalHeader = None
        self.m_vAmplitude=[0.0,0.0]
        self.m_PredictionsToIntegrate=5
        self.m_f64BarScale=0.0
        self.maxNumElements=10
        self.countTime=True
        self.numberOfSamplesPerSecond=0
        self.startTime= datetime.now()

    def aggregatePredictions(self,bIncludeAll=False):
        voteAggregate = 0



        #Do we have enough elements for predictions 
        if len(self.m_vAmplitude)>=self.m_PredictionsToIntegrate:


            if not bIncludeAll:
                #take last m_PredictionsToIntegrate elements
                lastElements=self.m_vAmplitude[-self.m_PredictionsToIntegrate:]
            else:
                lastElements=self.m_vAmplitude



            voteAggregate=numpy.sum(lastElements)
            m_maxAmplitude=numpy.amax(numpy.absolute(lastElements))


            voteAggregate /= m_maxAmplitude
            voteAggregate /= len(lastElements)

            return voteAggregate






    def setMatrixBuffer(self,p_buffer):

        #if prediction needed test, based on stimulation

        #if two values received

        value0 = abs(p_buffer[0])
        value1 = abs(p_buffer[1])
        l_Sum = value0 + value1
        if(l_Sum!=0):
            value0 = value0 / l_Sum
            value1 = value1 / l_Sum

        else:
            value0 = 0.5
            value1 = 0.5

        l_PredictedAmplitude = value1 - value0
        
        #add value to array

        self.m_vAmplitude.append(l_PredictedAmplitude)
        if(len(self.m_vAmplitude)>self.maxNumElements):
            self.m_vAmplitude.pop(0)
        self.m_f64BarScale = self.aggregatePredictions(False)


    def process(self):
        for chunkIndex in range(len(self.input[0])):

            if(type(self.input[0][chunkIndex]) == OVStreamedMatrixHeader):
                self.signalHeader = self.input[0].pop()
                outputHeader=OVSignalHeader(
                    self.signalHeader.startTime,
                    self.signalHeader.endTime,
                    [1, 1],
                    ['control_value'] + 1 * [''],
                    0)

                self.output[0].append(outputHeader)

                outputHeader2=OVSignalHeader(
                    self.signalHeader.startTime,
                    self.signalHeader.endTime,
                    [1, 1],
                    ['sampl_per_sec'] + 1 * [''],
                    0)
                self.output[1].append(outputHeader2)


            elif type(self.input[0][chunkIndex]) == OVStreamedMatrixBuffer:
                chunk = self.input[0].pop()


                # original signal shape
                shape = numpy.array(chunk).shape

                numpy_buffer = numpy.array(chunk)
                num_of_sampls_buff= numpy.array(chunk)


                self.setMatrixBuffer(numpy_buffer)


                numpy_buffer[0]=self.m_f64BarScale

                num_of_sampls_buff[0]=self.numberOfSamplesPerSecond


                #Count
                if self.countTime:

                    now = datetime.now()
                    time=(now-self.startTime).seconds

                    #Count the number of samples in a second
                    if time==3:
                        self.numberOfSamplesPerSecond+=1
                    #Turn Off the time counting, to save power
                    if time==4:
                        print "Number of samples in the block "+str(self.numberOfSamplesPerSecond)
                        self.countTime=False


                chunk = OVSignalBuffer(chunk.startTime, chunk.endTime, numpy_buffer.tolist())
                chunk2 = OVSignalBuffer(chunk.startTime, chunk.endTime, num_of_sampls_buff.tolist())
                self.output[0].append(chunk)
                self.output[1].append(chunk2)



            elif (type(self.input[0][chunkIndex]) == OVStreamedMatrixEnd):
                self.output[0].append(OVSignalEnd(self.input[0].pop()))
                self.output[1].append(OVSignalEnd(self.input[0].pop()))







            # if (type(self.input[0][chunkIndex]) == OVSignalHeader):
            #     self.signalHeader = self.input[0].pop()
            #
            #     outputHeader = OVSignalHeader(
            #         self.signalHeader.startTime,
            #         self.signalHeader.endTime,
            #         [1, self.signalHeader.dimensionSizes[1]],
            #         ['Mean'] + self.signalHeader.dimensionSizes[1] * [''],
            #         self.signalHeader.samplingRate)
            #
            #     self.output[0].append(outputHeader)
            #
            # elif (type(self.input[0][chunkIndex]) == OVSignalBuffer):
            #     chunk = self.input[0].pop()
            #     numpyBuffer = numpy.array(chunk).reshape(tuple(self.signalHeader.dimensionSizes))
            #     numpyBuffer = numpyBuffer. mean(axis=0)
            #     chunk = OVSignalBuffer(chunk.startTime, chunk.endTime, chunk.)
            #     self.output[0].append(chunk)
            #
            # elif (type(self.input[0][chunkIndex]) == OVSignalEnd):
            #     self.output[0].append(self.input[0].pop())


box = MyOVBox()
