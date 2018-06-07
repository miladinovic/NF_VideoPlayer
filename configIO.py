import ConfigParser
from ast import literal_eval as make_tuple

class configWriter:

    def __init__(self,cfgReader):
        if isinstance(cfgReader,configReader):
            self.configFilename = cfgReader.configFilename

            self.language=cfgReader.getLanguage()
            self.number_of_trials =cfgReader.getNumberOfTrials()
            self.buffer_size =cfgReader.getBufferSize()
            self.threshold_value =cfgReader.getThresholdValue()
            self.video_speed =cfgReader.getVideoSpeed()
            self.video_filename =cfgReader.getVideoFilename()
            self.video_subsequence_to_display =cfgReader.getVideoSubsequenceToDisplay()
            self.openvibe_designer_ip =cfgReader.getOpenVibeDesignerIP()
            self.openvibe_designer_port =cfgReader.getOpenVibeDesignerPort()
            self.openvibe_aq_ser_ip =cfgReader.getOpenVibeAqusitionServerIP()
            self.openvibe_aq_ser_port =cfgReader.getOpenVibeAqusitionServerPort()

            self.experimentPath=cfgReader.getLastExperimentPath()
            self.serverPath=cfgReader.getServerPath()
            self.designerPath=cfgReader.getDesignerPath()
            self.acquisitionScenarioPath=cfgReader.getAcquisitionScenarionPath()
            self.trainingScenarioPath=cfgReader.getTrainingScenarioPath()
            self.onlineScenarioPath=cfgReader.getOnlineScenarioPath()
        else:
            raise ValueError("Argument not type of configReader")

    def write(self):
        print "write " + self.configFilename
        configManualWriter(self.configFilename, self.language, self.number_of_trials, self.buffer_size,
                           self.threshold_value,
                           self.video_speed,self.video_filename,self.video_subsequence_to_display,self.openvibe_designer_ip,
                           str(self.openvibe_designer_port),self.openvibe_aq_ser_ip,str(self.openvibe_aq_ser_port),self.experimentPath,self.serverPath,self.designerPath,self.acquisitionScenarioPath,
                           self.trainingScenarioPath,self.onlineScenarioPath)




class configManualWriter:
    def __init__(self, configFilename, language, number_of_trials, buffer_size, threshold_value, video_speed,
                 video_filename, video_subsequence_to_display,
                 openvibe_designer_ip="localhost", openvibe_designer_port="5678", openvibe_aq_ser_ip="localhost", openvibe_aq_ser_port="15361", experimentPath="",
                 serverPath="PLEASE SELECT", designerPath="PLEASE SELECT", acqScePath="PLEASE SELECT", trainScePath="PLEASE SELECT", onlineScePath="PLEASE SELECT"):
        cfgfile = open(configFilename, 'w')
        Config=ConfigParser.ConfigParser()
        # add the settings to the structure of the file, and lets write it out...

        section="Player"
        Config.add_section(section)
        Config.set(section,'Language',language)
        Config.set(section,'Number of trials', number_of_trials)
        Config.set(section,'Buffer size', buffer_size)
        Config.set(section,'Threshold value', threshold_value)
        Config.set(section,'Video speed', video_speed)
        Config.set(section,'Video filename', video_filename)
        Config.set(section,'Video subsequence to display', video_subsequence_to_display)


        section2="Connection"
        Config.add_section(section2)
        Config.set(section2,'OpenVibe Designer IP',openvibe_designer_ip)
        Config.set(section2,'OpenVibe Designer port',openvibe_designer_port)
        Config.set(section2,'OpenVibe Aq. Ser IP (TCP Tagging)',openvibe_aq_ser_ip)
        Config.set(section2,'OpenVibe Aq. Ser port (TCP Tagging)',openvibe_aq_ser_port)

        section3="Player"
        Config.set(section3,'experiment path',experimentPath)
        Config.set(section3,'server path',serverPath)
        Config.set(section3,'designer path',designerPath)
        Config.set(section3,'acquisition scenario path',acqScePath)
        Config.set(section3,'training scenario path',trainScePath)
        Config.set(section3,'online scenario path',onlineScePath)

        Config.write(cfgfile)
        cfgfile.close()



class configReader:
    def __init__(self, configFilename):
        self.config=ConfigParser.ConfigParser()
        self.setNewConfigFilename(configFilename)

    def setNewConfigFilename(self, filepath="x.ini"):
        self.config.read(filepath)
        self.configFilename = filepath
        self.playerSection="Player"
        self.connectionSection="Connection"
        self.tmp="TMP"

    def getLanguage(self):
        return int(self.configSectionMap(self.playerSection)['language'])

    def getNumberOfTrials(self):
        return int(self.configSectionMap(self.playerSection)['number of trials'])

    def getBufferSize(self):
        return self.configSectionMap(self.playerSection)['buffer size']

    def getThresholdValue(self):
        return self.configSectionMap(self.playerSection)['threshold value']

    def getVideoSpeed(self):
        return self.configSectionMap(self.playerSection)['video speed']

    def getVideoFilename(self):
        return self.configSectionMap(self.playerSection)['video filename']

    def getVideoSubsequenceToDisplay(self):
        return make_tuple(self.configSectionMap(self.playerSection)['video subsequence to display'])

    def getOpenVibeDesignerIP(self):
        return self.configSectionMap(self.connectionSection)['openvibe designer ip']

    def getOpenVibeDesignerPort(self):
        return int(self.configSectionMap(self.connectionSection)['openvibe designer port'])

    def getOpenVibeAqusitionServerIP(self):
        return self.configSectionMap(self.connectionSection)['openvibe aq. ser ip (tcp tagging)']

    def getOpenVibeAqusitionServerPort(self):
        return int(self.configSectionMap(self.connectionSection)['openvibe aq. ser port (tcp tagging)'])

    #addional

    def getLastExperimentPath(self):
        return self.configSectionMap(self.playerSection)["experiment path"]

    def getServerPath(self):
        return self.configSectionMap(self.playerSection)["server path"]
    def getDesignerPath(self):
        return self.configSectionMap(self.playerSection)["designer path"]

    def getAcquisitionScenarionPath(self):
        return self.configSectionMap(self.playerSection)["acquisition scenario path"]
    def getTrainingScenarioPath(self):
        return self.configSectionMap(self.playerSection)["training scenario path"]
    def getOnlineScenarioPath(self):
        return self.configSectionMap(self.playerSection)["online scenario path"]




    def configSectionMap(self,section):
        dict1 = {}
        options = self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1



if __name__=="__main__":
    print "hi"
    """instance=configReader()
    instance2=configWriter(instance)
    instance2.number_of_trials=10

    instance2.write()"""

    """cfgfile = open("config.ini",'w')
    Config=ConfigParser.ConfigParser()
    # add the settings to the structure of the file, and lets write it out...
    section="Player"
    Config.add_section(section)
    Config.set(section,'Language',1)
    Config.set(section,'Number of trials', 10)
    Config.set(section,'Buffer size', "MAX")
    Config.set(section,'Threshold value', "default")
    Config.set(section,'Video speed', "normal")
    Config.set(section,'Video filename', "/usr/share/test.mp4")
    Config.set(section,'Video subsequence to display', "(0,10)")
    section2="Connection"
    Config.add_section(section2)
    Config.set(section2,'OpenVibe Designer IP',"localhost")
    Config.set(section2,'OpenVibe Designer port',"1111")
    Config.set(section2,'OpenVibe Aq. Ser IP (TCP Tagging)',"localhost")
    Config.set(section2,'OpenVibe Aq. Ser port (TCP Tagging)',"localhost")










    Config.write(cfgfile)
    cfgfile.close()"""

