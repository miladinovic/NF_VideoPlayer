# -*- coding: utf-8 -*-
import numpy


class feedback:
    @staticmethod
    def new_round_press_space_to_continue_or_wait_or_q_to_quit(langID):
        textENG = "> NEW ROUND\n> PRESS SPACE TO CONTINUE OR WAIT FOR THE NEW ROUND\n"
        textIT = "> NOVO ROUND\n> PER CONTINUARE PREMI 'SPACE' O ASPETTA IL TIMEOUT\n"
        textSLO="> NEW ROUND\n> PRESS SPACE TO CONTINUE OR WAIT FOR THE NEW ROUND\n"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def summary_display(langID, runTrace, runTraceBuffer, positive, negative, total):

        avgRvalue=numpy.mean(runTraceBuffer)
        avgRvalue=str(avgRvalue)

        perPositive=(0.0+positive)/total*100
        perPositive=" ("+str(perPositive)+"%)"
        perNegative=(0.0+negative)/total*100
        perNegative=" ("+str(perNegative)+"%)"
        negative=str(negative)
        total=str(total)

        runTrace=str(runTrace)

        runTraceBufferStr="[ "+','.join([str(round(x,2)) for x in runTraceBuffer])+ " ]"

        textENG = "> SUMMARY\n\n> POSITIVE: "+str(positive)+" / "+str(total)+perPositive+"\n> NEGATIVE: "+negative+" / "+total+perNegative+"\n> TRACE: [ "+runTrace+" ]"+"\n> BUFFER: [ "+runTraceBufferStr+" ]\n> AVG-r: "+avgRvalue
        textIT = "> RISULTATI\n\n> POSITIVI: "+str(positive)+" / "+str(total)+perPositive+"\n> NEGATIVI: "+negative+" / "+total+perNegative+"\n> TRACCIA: [ "+runTrace+" ]"+"\n> TRACCIA VAL. R: [ "+runTraceBufferStr+" ]\n> MEDIO-r: "+avgRvalue
        textSLO= "> SUMMARY\n\n> POSITIVE: "+str(positive)+" / "+str(total)+perPositive+"\n> NEGATIVE: "+negative+" / "+total+perNegative+"\n> TRACE: [ "+runTrace+" ]"+"\n> BUFFER: [ "+runTraceBufferStr+" ]\n> AVG-r: "+avgRvalue
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)


    @staticmethod
    def ready(langID):
        textENG = "Ready"
        textIT = "Pronto"
        textSLO="Ready"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def go(langID):
        textENG = "GO!"
        textIT = "VIA!"
        textSLO="GO!"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def success(langID):
        textENG = "SUCCESS!"
        textIT = "COMPLETTATO!"
        textSLO="SUCCESS!"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def fail(langID):
        textENG = "FAIL!"
        textIT = "ERRORE!"
        textSLO="FAIL!"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def num_run(langID):
        textENG = "RUN.:"
        textIT = "#"
        textSLO="RUN.:"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def num_hits(langID):
        textENG = "POS.:"
        textIT = "+"
        textSLO="POS.:"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def num_fails(langID):
        textENG = "NEG.:"
        textIT = "-"
        textSLO="NEG.:"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)








class intro:
    @staticmethod
    def drag_the_window_and_press_f_for_fullscreen(langID):
        textENG = "> Drag the window to the stimuli \n> presentation display and press f key \n> for fullscreen ot ESC/q to continue"
        textIT = "> Drag the window to the stimuli \n> presentation display and press f key \n> for fullscreen ot ESC/q to continue"
        textSLO="> Drag the window to the stimuli \n> presentation display and press f key \n> for fullscreen ot ESC/q to continue"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def fullscreen_mode_activated_press_space_when_ready(langID):
        textENG = "> Fullscreen mode activated! \n> PRESS SPACE WHEN READY!"
        textIT = "> Fullscreen mode activated! \n> PRESS SPACE WHEN READY!"
        textSLO="> Fullscreen mode activated! \n> PRESS SPACE WHEN READY!"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def continue_without_fulscreen_press_space_when_ready(langID):
        textENG = "> Continue without fullscreen mode!\n> PRESS SPACE WHEN READY!"
        textIT = "> Continue without fullscreen mode!\n> PRESS SPACE WHEN READY!"
        textSLO="> Continue without fullscreen mode!\n> PRESS SPACE WHEN READY!"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def tcp_connection_ok__received_value(langID):
        textENG = ">TCP Connection OK\n>Received value  :"
        textIT = ">TCP Connection OK\n>Received value  :"
        textSLO=">TCP Connection OK\n>Received value  :"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def press_space_to_continue(langID):
        textENG = '\n> PRESS SPACE TO CONTINUE!'
        textIT = '\n> PRESS SPACE TO CONTINUE!'
        textSLO='\n> PRESS SPACE TO CONTINUE!'
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)





class gui:

    @staticmethod
    def connetionToOpenVibeDesigner(langID):
        textENG = "Connection to OpenVibe Designer "
        textIT = "Connection to OpenVibe Designer "
        textSLO="Connection to OpenVibe Designer "
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def connetionToOpenVibeServer(langID):
        textENG = "Connection to OpenVibe Server "
        textIT = "Connection to OpenVibe Server "
        textSLO="Connection to OpenVibe Server "
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)


    @staticmethod
    def currentConfiguration(langID):
        textENG = "Current Configuration"
        textIT = "Current Configuration"
        textSLO="Current Configuration"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)
    @staticmethod
    def language(langID):
        textENG = "English"
        textIT = "Italiano"
        textSLO="Sloven\xc5\xa1\xc4\x8dina"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)
    @staticmethod
    def confLanguage(langID):
        textENG = "Language"
        textIT = "Lingua"
        textSLO="Jezik"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def getLangueges():
        textENG = "English"
        textIT = "Italiano"
        textSLO="Sloven\xc5\xa1\xc4\x8dina"
        return [textENG,textIT,textSLO]

    @staticmethod
    def numberOfTrials(langID):
        textENG = "Number of Trials"
        textIT = "Number of Trials"
        textSLO="Number of Trials"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def bufferSize(langID):
        textENG = "Buffer Size"
        textIT = "Buffer Size"
        textSLO="Buffer Size"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def thresholdValue(langID):
        textENG = "Threshold Value"
        textIT = "Threshold Value"
        textSLO="SThreshold Value"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def videoSpeed(langID):
        textENG = "Video Speed"
        textIT = "Video Speed"
        textSLO="Video Speed"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def displayVideoSubSequence(langID):
        textENG = "Video Subsequence to Display"
        textIT = "Video Subsequence to Display"
        textSLO="Video Subsequence to Display"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def displayVideoFileName(langID):
        textENG = "Video Filename"
        textIT = "Video Filename"
        textSLO="Video Filename"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def langasaasduage(langID):
        textENG = "English"
        textIT = "Italiano"
        textSLO="Sloven\xc5\xa1\xc4\x8dina"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)


    @staticmethod
    def run(langID):
        textENG = "Run"
        textIT = "Run"
        textSLO="Run"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def nextItem(langID):
        textENG = "Next"
        textIT = "Next"
        textSLO="Next"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)
    @staticmethod
    def previousItem(langID):
        textENG = "Prev"
        textIT = "Prev"
        textSLO="Prev"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)
    @staticmethod
    def cancel(langID):
        textENG = "Cancel"
        textIT = "Cancel"
        textSLO="Cancel"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)

    @staticmethod
    def quit(langID):
        textENG = "Quit"
        textIT = "Esci"
        textSLO="Esci"
        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)





    @staticmethod
    def wizardWindowTitle(langID):
        textENG = "Video Feedback Configuration Wizard"
        textIT = "Video Feedback Configuration Wizard"
        textSLO="Video Feedback Configuration Wizard"

        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)
    @staticmethod
    def wizardWelcomeText(langID):
        textENG = "Welcome to the configuration Wizard Lorem \n\n" \
                  "Ipsum is simply dummy text of the printing and typesetting industry. \n" \
                  "Lorem Ipsum has been the industry's standard dummy text ever since the \n" \
                  "1500s, when an unknown printer took a galley of type and scrambled it \n" \
                  "to make a type specimen book. It has survived not only five centuries, \n" \
                  "but also the leap into electronic typesetting, remaining essentially \n" \
                  "unchanged. It was popularised in the 1960s with the release of Letraset \n" \
                  "sheets containing Lorem Ipsum passages, and more recently with desktop \n" \
                  "publishing software like Aldus PageMaker including versions of Lorem Ipsum"
        textENG="Welcome to the configuration Wizard"

        textIT = "Welcome to the configuration Wizard Lorem \n\n" \
                  "Ipsum is simply dummy text of the printing and typesetting industry. \n" \
                  "Lorem Ipsum has been the industry's standard dummy text ever since the \n" \
                  "1500s, when an unknown printer took a galley of type and scrambled it \n" \
                  "to make a type specimen book. It has survived not only five centuries, \n" \
                  "but also the leap into electronic typesetting, remaining essentially \n" \
                  "unchanged. It was popularised in the 1960s with the release of Letraset \n" \
                  "sheets containing Lorem Ipsum passages, and more recently with desktop \n" \
                  "publishing software like Aldus PageMaker including versions of Lorem Ipsum"
        textSLO="Welcome to the configuration Wizard Lorem \n\n" \
                  "Ipsum is simply dummy text of the printing and typesetting industry. \n" \
                  "Lorem Ipsum has been the industry's standard dummy text ever since the \n" \
                  "1500s, when an unknown printer took a galley of type and scrambled it \n" \
                  "to make a type specimen book. It has survived not only five centuries, \n" \
                  "but also the leap into electronic typesetting, remaining essentially \n" \
                  "unchanged. It was popularised in the 1960s with the release of Letraset \n" \
                  "sheets containing Lorem Ipsum passages, and more recently with desktop \n" \
                  "publishing software like Aldus PageMaker including versions of Lorem Ipsum"

        return {1:textENG,2:textIT, 3:textSLO}.get(langID,textENG)


if __name__=="__main__":
    print ("TEST")
    print(gui.wizardWelcomeText(2))
