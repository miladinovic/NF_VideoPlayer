from belfrywidgets.wizard import *
from Tkinter import *
import Local as l
import configIO as io
import OpenPype

class configReader():
    def __init__(self, configFilename):
        self.reader = io.configReader(configFilename)
        self.reader.setNewConfigFilename(configFilename)


    def readNumberOfTrials(self):
        return self.reader.getNumberOfTrials()

    def readBufferSize(self):
        return self.reader.getBufferSize()

    def readThersholdValue(self):
        #TODO
        return self.reader.getThresholdValue()

    def readLanguageSetting(self):
        #TODO Insert Config Reader
        # 1 - English
        # 2 - Italian
        # 3 - Slovenian
        # n>4 - English
        return self.reader.getLanguage()

    def readVideoSpeed(self):
        #TODO Insert Config Reader
        return self.reader.getVideoSpeed()

    def readVideoSequenceToDisplay(self):
        #TODo
        start=0
        stop=100
        return str(self.reader.getVideoSubsequenceToDisplay())+" ms"
    def readVideoFilename(self):
        #TODo
        return self.reader.getVideoFilename()

    def readOpenVibeDesignerConfig(self):
        return self.reader.getOpenVibeDesignerIP(), self.reader.getOpenVibeDesignerPort()

    def readOpenVibeServerConfig(self):
        return self.reader.getOpenVibeAqusitionServerIP(), self.reader.getOpenVibeAqusitionServerPort()


    def toString(self):
        langID=self.readLanguageSetting()


        labels=l.gui.confLanguage(langID)+":\n"+\
            l.gui.numberOfTrials(langID)+":\n"+\
            l.gui.bufferSize(langID)+":\n"+\
            l.gui.thresholdValue(langID)+":\n"+\
            l.gui.videoSpeed(langID)+":\n"+\
            l.gui.displayVideoFileName(langID)+":\n"+\
            l.gui.displayVideoSubSequence(langID)+":"

        values=l.gui.language(langID)+"\n"+\
            str(self.readNumberOfTrials())+"\n"+\
            self.readBufferSize()+"\n"+\
            self.readThersholdValue()+"\n"+\
            self.readVideoSpeed()+"\n"+\
            self.readVideoFilename()+"\n"+\
            self.readVideoSequenceToDisplay()


        return labels,values





def pt(string):
    print string

class GUI:
    def __init__(self, configFilename):
        self.configFilename = configFilename
        self.cfg = configReader(configFilename)
        self.langID=self.cfg.readLanguageSetting()
        pass


    def center(self,toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def displayWizard(self):

        root = Tk()
        root.title(l.gui.wizardWindowTitle(self.langID))

        wiz = Wizard(
            width=640,
            height=480,
            cancelcommand=lambda: exit(0),
            finishcommand=lambda: pt("Run"),
        )

        self.center(wiz)

        def disable_finish():
            #Change the name to "RUN"
            wiz.set_finish_text(l.gui.run(self.langID))
            wiz.set_cancel_text(l.gui.quit(self.langID))

            wiz.set_finish_enabled(False)

        def enable_finish():
            wiz.set_finish_enabled(True)



        wiz.set_default_button('next')

        ##########PANE 1 ############
        pane1 = wiz.add_pane('one', 'First',entrycommand=disable_finish)

        lbl1 = Label(pane1, text=l.gui.wizardWelcomeText(self.langID))
        lbl1.pack(side=TOP, fill=Y, expand=1)

        #Connection Test
        midGroupP1=Frame(pane1)
        midGroupP1.pack(side=TOP, anchor="c", expand=1)

        if OpenPype.ConnectionTest.testLSL():
            color="green"
        else:
            color="red"

        connectionOpenVibeDesigner = Label(midGroupP1, text=l.gui.connetionToOpenVibeDesigner(self.langID),justify=LEFT)
        connectionOpenVibeDesigner.pack(side=LEFT, fill=Y, expand=0)

        connectionOpenVibeServer= Label(midGroupP1, text="   ",bg=color,justify=LEFT)
        connectionOpenVibeServer.pack(side=LEFT, fill=Y, expand=0)

        #Connection Test
        midGroupP1=Frame(pane1)
        midGroupP1.pack(side=TOP, anchor="c", expand=1)



        if OpenPype.ConnectionTest.pingServer(self.cfg.readOpenVibeServerConfig()):
            color="green"
        else:
            color="red"

        connectionOpenVibeDesigner = Label(midGroupP1, text=l.gui.connetionToOpenVibeServer(self.langID),justify=LEFT)
        connectionOpenVibeDesigner.pack(side=LEFT, fill=Y, expand=0)

        connectionOpenVibeServer= Label(midGroupP1, text="   ",bg=color,justify=LEFT)
        connectionOpenVibeServer.pack(side=LEFT, fill=Y, expand=0)










        #LOGOS

        photo = PhotoImage(file="logoB.pbm")
        logoBioing = Label(pane1, image=photo)
        logoBioing.pack(side=RIGHT, fill=BOTH, expand=1)

        photo2 = PhotoImage(file="logoA.pbm")
        logoBrainNew = Label(pane1, image=photo2)
        logoBrainNew.pack(side=RIGHT, fill=BOTH, expand=1)

        ##########PANE 2 ############


        pane2 = wiz.add_pane( 'two', 'Second')

        lbl2 = Label(pane2, text=l.gui.currentConfiguration(self.langID))
        lbl2.pack(side=TOP, fill=BOTH, expand=1)

        labels,values=self.cfg.toString()

        midGroup=Frame(pane2)
        midGroup.pack(side=TOP, anchor="c", expand=1)

        lbl3 = Label(midGroup,text=values,justify=LEFT)
        lbl3.pack(side=RIGHT, fill=BOTH, expand=0)

        lbl4 = Label(midGroup, text=labels,justify=RIGHT)
        lbl4.pack(side=RIGHT, fill=BOTH, expand=0)



        #LOGOS

        logoBioing = Label(pane2, image=photo)
        logoBioing.pack(side=RIGHT, fill=BOTH, expand=1)

        logoBrainNew = Label(pane2, image=photo2)
        logoBrainNew.pack(side=RIGHT, fill=BOTH, expand=1)

        pane3 = wiz.add_pane(
            'three', 'Third',
            entrycommand=enable_finish,
            prevcommand=disable_finish
        )

        lcfgTitle = Label(pane3, text=l.gui.currentConfiguration(self.langID))
        lcfgTitle.pack(side=TOP, fill=BOTH, expand=0)

        #Language
        midGroup3=Frame(pane3)
        midGroup3.pack(side=TOP, anchor="c", expand=1)

        lg = Label(midGroup3, text=l.gui.confLanguage(self.langID),justify=LEFT)
        lg.pack(side=LEFT, fill=Y, expand=0)

        LG_OPTIONS = l.gui.getLangueges()

        lGvariable = StringVar(root)
        lGvariable.set(LG_OPTIONS[self.langID-1]) # default value

        w = apply(OptionMenu, (midGroup3, lGvariable) + tuple(LG_OPTIONS))
        w.pack(side=LEFT)





        #No of Trials

        numberOfTrialsGroup=Frame(pane3)
        numberOfTrialsGroup.pack(side=TOP, anchor="c", expand=1)
        lNumberOfTrials = Label(numberOfTrialsGroup, text=l.gui.numberOfTrials(self.langID),justify=LEFT)
        lNumberOfTrials.pack(side=LEFT, fill=Y, expand=0)
        OPTIONS = range(1,31)
        noTrialsvariable = IntVar(root)
        noTrialsvariable.set(OPTIONS[self.cfg.readNumberOfTrials()-1]) # default value
        w = apply(OptionMenu, (numberOfTrialsGroup, noTrialsvariable) + tuple(OPTIONS))
        w.pack(side=LEFT)

        #Buffer size

        bufferSizeGroup=Frame(pane3)
        bufferSizeGroup.pack(side=TOP, anchor="c", expand=1)
        lbufferSize = Label(bufferSizeGroup, text=l.gui.numberOfTrials(self.langID), justify=LEFT)
        lbufferSize.pack(side=LEFT, fill=Y, expand=0)
        OPTIONS = ["MAX"]
        bufferSizevariable = StringVar(root)
        bufferSizevariable.set(OPTIONS[0]) # default value
        w = apply(OptionMenu, (bufferSizeGroup, bufferSizevariable) + tuple(OPTIONS))
        w.pack(side=LEFT)


        #Logos
        logoBioing = Label(pane3, image=photo)
        logoBioing.pack(side=RIGHT, fill=BOTH, expand=1)

        logoBrainNew = Label(pane3, image=photo2)
        logoBrainNew.pack(side=RIGHT, fill=BOTH, expand=1)








        # wiz.show_pane('two')
        # wiz.del_pane('two')
        # wiz.set_prev_enabled(True)
        # wiz.set_next_enabled(True)

        root.wm_withdraw()
        root.wait_window(wiz)


        #self.langID=LG_OPTIONS.index(lGvariable.get())
        i=0
        for lg in LG_OPTIONS:
            i+=1
            if lg.decode("utf-8")==lGvariable.get():
                self.langID=i

        cfgWriter=io.configWriter(self.cfg.reader)
        cfgWriter.language=self.langID
        cfgWriter.number_of_trials=noTrialsvariable.get()
        cfgWriter.buffer_size=bufferSizevariable.get()
        cfgWriter.configFilename = self.configFilename
        cfgWriter.write()




if __name__ == "__main__":
    def main():
        gui=GUI()
        gui.displayWizard()

    main()
