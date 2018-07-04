import subprocess
import numpy
from shutil import copyfile


class runCspTraining:
    def __init__(self, designerPath, filterBankScenario="x",
                 testScenarioPath="x"):
        self.designerPath = designerPath
        self.filterBankScenario = filterBankScenario
        self.testScenarioPath = testScenarioPath
        self.filterConfig = []
        pass

    def runTesting(self, experimentPath, subjectID, session):

        argumentsVar = " --define Experiment_Path " + experimentPath + " --define SubjectID " + subjectID + " --define Session " + str(
            session)
        # p = subprocess.Popen(self.designerPath +" --run-bg --no-pause --no-session-management --open " + self.testScenarioPath + argumentsVar, shell=False, stdout = subprocess.PIPE)
        p = subprocess.Popen(
            self.designerPath + " --run-bg --no-gui --play-fast " + self.testScenarioPath + argumentsVar, shell=False,
            stdout=subprocess.PIPE)
        (output, err) = p.communicate()

        # This makes the wait possible
        p_status = p.wait()

    def runTraining(self, experimentPath, subjectID, session, lF, hF, filename):

        argumentsVar = " --define Experiment_Path " + experimentPath + " --define SubjectID " + subjectID + " --define Session " + str(
            session) + " --define low_freq " + str(lF) + " --define high_freq " + str(
            hF) + " --define filename " + filename
        # p = subprocess.Popen(self.designerPath +" --run-bg --no-pause --no-session-management --open " + self.trainingScenarioPath + argumentsVar, shell=False, stdout = subprocess.PIPE)

        p = subprocess.Popen(
            self.designerPath + " --run-bg --no-gui --no-pause --play-fast " + self.filterBankScenario + argumentsVar,
            shell=False, stdout=subprocess.PIPE)
        (output, err) = p.communicate()

        # This makes the wait possible
        p_status = p.wait()

    def batchTraining(self, experimentPath, subjectID, session, initialFreq=6, filterBW=4, overlap=2):

        print "Training filter: 8 - 24 Hz"
        self.runTraining(experimentPath, subjectID, session, 8, 24, "8-24-csp-filter.cfg")
        self.filterConfig.append(["1", "8", "24", "0"])
        print("training done!")

        print "Training filter: 12 - 24 Hz"
        self.runTraining(experimentPath, subjectID, session, 12, 24, "12-24-csp-filter.cfg")
        self.filterConfig.append(["2", "12", "24", "0"])
        print("training done!")

        for i in range(1, 12):
            lF = initialFreq
            hF = initialFreq + filterBW
            print "Training filter: " + str(lF) + "-" + str(hF) + " Hz"
            self.runTraining(experimentPath, subjectID, session, lF, hF, str(lF) + "-" + str(hF) + "-csp-filter.cfg")
            self.filterConfig.append([str(i + 2), str(lF), str(hF), "0"])
            print("training done!")
            initialFreq = initialFreq + overlap

        self.filterConfig = numpy.asanyarray(self.filterConfig)
        numpy.savetxt(experimentPath + "/" + subjectID + "/" + session + "/tmp_filter_config.csv", self.filterConfig,
                      fmt='%s %s %s %s')

    def readTmpFilterConfiguration(self, experimentPath, subjectID, session, filterConffigFile="tmp_filter_config.csv"):
        filterConfig = numpy.genfromtxt(experimentPath + "/" + subjectID + "/" + session + "/" + filterConffigFile)
        return filterConfig

    def readAndSortFilterConfiguration(self, experimentPath, subjectID, session,
                                       filterConffigFile="tmp_filter_config.csv"):
        filterConfig = self.readTmpFilterConfiguration(experimentPath, subjectID, session, filterConffigFile)
        return numpy.array(sorted(filterConfig, key=lambda x: x[3], reverse=True))

    def inputToXml(self, experimentPath, subjectID, session, filename, lf, hf):

        outputFile = experimentPath + "/" + subjectID + "/" + session + "/" + filename

        outputXML = "<OpenViBE-SettingsOverride>\n" \
                    "\t<SettingValue>Butterworth</SettingValue>\n" \
                    "\t<SettingValue>Band pass</SettingValue>\n" \
                    "\t<SettingValue>4</SettingValue>\n" \
                    "\t<SettingValue>" + str(lf) + "</SettingValue>\n" \
                                                   "\t<SettingValue>" + str(hf) + "</SettingValue>\n" \
                                                                                  "\t<SettingValue>0.500000</SettingValue>\n" \
                                                                                  "</OpenViBE-SettingsOverride>"
        try:
            text_file = open(outputFile, "w+")
            text_file.write(outputXML)
            text_file.close()
        except:
            "Unable to write to file, please try Again!"

    def selectCSPconf(self, experimentPath, subjectID, session, lf, hf, outputFile):

        path = experimentPath + "/" + subjectID + "/" + session
        try:
            print "Copying: " + path + "/" + str(int(lf)) + "-" + str(
                int(hf)) + "-csp-filter.cfg to " + path + "/" + outputFile
            copyfile(path + "/" + str(int(lf)) + "-" + str(int(hf)) + "-csp-filter.cfg", path + "/" + outputFile)
        except:
            print "Unable to copy, please try again"

    def seletFilters(self, experimentPath, subjectID, session, numberOfFilters=4,
                     filterConffigFile="tmp_filter_config.csv", log=True):

        logPath = experimentPath + "/" + subjectID + "/" + session + "/filter_log.txt"
        try:
            logfile = open(logPath, "w+")
            logfile.write("LOG " + logPath + "\n")

        except:
            log = False

        sortedFilterConfig = self.readAndSortFilterConfiguration(experimentPath, subjectID, session, filterConffigFile)

        control = 0.0
        for i in range(1, numberOfFilters + 1):
            control += sortedFilterConfig[i][3]

        if control == 0:
            print "ERROR: Something went wrong! No coefficients."
            return

        for i in range(1, numberOfFilters + 1):

            lf = sortedFilterConfig[i][1]
            hf = sortedFilterConfig[i][2]
            fisherScore = sortedFilterConfig[i][3]
            printString = "Filter no. " + str(i) + " " + str(lf) + "Hz-" + str(hf) + "Hz with the score: " + str(
                fisherScore)
            print (printString)
            if log:
                logfile.write(printString + "\n")

            self.inputToXml(experimentPath, subjectID, session, "tmpFilter" + str(i) + ".xml", lf, hf)
            self.selectCSPconf(experimentPath, subjectID, session, lf, hf, "cspFilter" + str(i) + ".cfg")

        if log:
            logfile.close()


if __name__ == "__main__":
    csp = runCspTraining("C:\Program Files\openvibe-2.0.1\openvibe-designer.cmd")
    csp.batchTraining("C:/Users/aleks/Desktop/MyExperiment", "1", "1")
    csp.runTesting("C:/Users/aleks/Desktop/MyExperiment", "1", "1")
    csp.seletFilters("C:/Users/aleks/Desktop/MyExperiment", "1", "1", 4)
