import numpy
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        self.matrixHeader = None
        self.signalBuffer = list()
        self.bol = True

        self.simID = 0
        self.simDate = 0
        self.simDuration = 0

        self.X = []
        self.y_labels = []

        self.X_matrix = []
        self.y_label_matrix = []
        self.toggleLDA = True

    def readConfigFilterValue(self):
        pass

    def initialize(self):
        self.filteConfigFile = self.setting['tmp_filter_config_file']
        self.filterConfig = numpy.genfromtxt(self.filteConfigFile)
        print "init"
        print self.filterConfig

        self.cuTime = self.getCurrentTime()

        self.numberOfInputs = len(self.input)
        print "Number of inputs: " + str(self.numberOfInputs)

        for i in range(0, (self.numberOfInputs - 1) / 2):
            self.X_matrix.append([])
            self.y_label_matrix.append([])

        print "Evaluating filters. PLEASE WAIT...."

        self.dot = "."

    def process(self):

        # last input is always stimulation
        for chunkIndex in range(len(self.input[self.numberOfInputs - 1])):
            chunk = self.input[self.numberOfInputs - 1].pop()
            if (type(chunk) == OVStimulationSet):
                for stimIdx in range(len(chunk)):
                    stim = chunk.pop();
                    self.simID = stim.identifier
                    self.simDate = stim.date
                    self.simDuration = stim.duration
                    # print 'Received stim', stim.identifier, 'stamped at', stim.date, 's'

        # for each input
        i = 0

        if (self.getCurrentTime() - self.cuTime) == 30.0:
            print self.dot
            self.dot = self.dot + "."
            self.cuTime = self.getCurrentTime()
        while (i <= self.numberOfInputs - 2):

            # matrix A

            for chunkIndex in range(len(self.input[i])):

                if type(self.input[i][chunkIndex]) == OVStreamedMatrixHeader:
                    self.matrixHeaderA = self.input[i].pop()
                elif type(self.input[i][chunkIndex]) == OVStreamedMatrixBuffer:
                    chunk = self.input[i].pop()

                    # Add value to the array
                    self.X_matrix[i / 2].append(chunk)

                    # Add label (i mod 2)
                    self.y_label_matrix[i / 2].append(0)

                elif (type(self.input[i][chunkIndex]) == OVStreamedMatrixEnd):
                    self.input[i].pop()  # just take the value from the buffer
            # next input (always in pairs)

            # matrix B
            for chunkIndex in range(len(self.input[i + 1])):

                if type(self.input[i + 1][chunkIndex]) == OVStreamedMatrixHeader:
                    self.matrixHeaderA = self.input[i + 1].pop()
                elif type(self.input[i + 1][chunkIndex]) == OVStreamedMatrixBuffer:
                    chunk = self.input[i + 1].pop()

                    # Add value to the array
                    self.X_matrix[i / 2].append(chunk)

                    # Add label (i mod 2)
                    self.y_label_matrix[i / 2].append(1)

                elif (type(self.input[i + 1][chunkIndex]) == OVStreamedMatrixEnd):
                    self.input[i + 1].pop()  # just take the value from the buffer
            i = i + 2

        if (self.simID == 33281 or self.simID == 1010) and self.toggleLDA:
            print "ENDE"

            for i in range(0, (self.numberOfInputs - 1) / 2):
                self.X = self.X_matrix[i]
                self.y_labels = self.y_label_matrix[i]
                clf = LinearDiscriminantAnalysis(n_components=None, priors=None, shrinkage=None, solver='svd',
                                                 store_covariance=False, tol=0.0001)
                try:
                    clf.fit(self.X, self.y_labels)
                except:
                    pass
                self.filterConfig[i][3] = clf.score(self.X, self.y_labels)
            print self.filterConfig
            numpy.savetxt(self.filteConfigFile, self.filterConfig, fmt='%f %f %f %f')
            self.toggleLDA = False

            # send stimulation to stop openvibe
            stimulationOutput = OVStimulationSet(chunk.startTime, chunk.endTime)
            stimEnd = OVStimulation(0x00008207, self.getCurrentTime(), 0)
            stimulationOutput.append(stimEnd)
            self.output[0].append(stimulationOutput)


box = MyOVBox()
