#!/usr/bin/python
import cv2
import random
import time
import numpy
import OpenPype as tcp
import Local as l
import GUI as guiWizard
import configIO as io
import logging
import threading
from OpenPype import stimulation as Stm


#Sound
try:
    import winsound
except ImportError:
    import os
    def playsound(frequency,duration):
        #apt-get install beep
        #os.system('beep -f %s -l %s' % (frequency,duration))
        print ('beep -f %s -l %s' % (frequency,duration))

    def playSuccess():
        pass
    def playFail():
        pass

else:
    def playsound(frequency,duration):
        winsound.Beep(frequency,duration)

    def playSuccess():
        winsound.PlaySound("audio/success.wav",winsound.SND_ASYNC)

    def playFail():
        winsound.PlaySound("audio/fail.wav",winsound.SND_ASYNC)



#FULLSCREEN=0

#Monitor/Display Configuration
#SCREEN_RESOLUTION_WIDTH=1920
#SCREEN_RESOLUTION_HIGTH=1080

#Video Clip Configuration
#ASPECT_RATIO=float(4)/3
#START_FRAME=0
#RESTART_FRAME=100

#Fullscreen
#FULLSCREEN=0



class VideoPlayer():



    def __init__(self,generateData=True,loggingPath="",subjectInfo=""):

        #config
        self.fullscreen=0 #0 - windowed, 1-fullscreen
        self.startFrame=0
        self.restartFrame=100
        self.filename=None
        self.openvibe_designer_ip=None
        self.openvibe_designer_port="L"
        self.openvibe_aq_ser_ip="localhost"
        self.openvibe_aq_ser_port=15361
        self.feedbackFrameName="Video Feedback"
        self.enableResize=False
        self.resolutionW=800
        self.resolutionH=600
        self.subjectID="Subject"
        self.subjectInfo=subjectInfo
        self.TCPTagging=True



        #feedback related config
        self.langID=1
        self.number_of_trials=10
        self.buffer_size="MAX"
        self.threshold_value="default"
        self.video_speed="normal"
        self.newRoundWaiting=10000
        self.loggingPath=loggingPath





        self.generateData=generateData

        # if generateData is set to false, the connection to openVibe TCP Writer will be established
        if not generateData:
            #self.tcpReader=tcp.OpenVibeClient()
            self.lslReader=tcp.OpenVibeLSLClient()
            self.tagger=tcp.OpenVibeTCPTagger()
            if self.TCPTagging:
                self.tagger.connect(self.openvibe_aq_ser_ip,self.openvibe_aq_ser_port)

        else:
            self.lslReader=None
            #self.tcpReader=None
        self.FULSCREEN=0

        #Logging
        timestr = time.strftime("%Y%m%d-%H%M%S")
        if len(self.loggingPath)<=0:
            logFilename="logs/"+self.subjectID+'_video_player_log-'+timestr+".txt"
        else:
            logFilename=self.loggingPath+"/"+self.subjectID+'video_player_log-'+timestr+".txt"

        logging.basicConfig(filename=logFilename, level=logging.INFO, format='%(asctime)s %(message)s')
        #playsound(800,2000)

        #add information
        logging.info("Information: * "+self.subjectInfo+" *")
        logging.info('Video Neurofeedback Started')
        logging.info('Real-time data: '+ 'NO' if generateData else 'YES')

    def sendMarker(self,EVEN_ID):
        if not self.generateData and self.TCPTagging:
            self.tagger.sendTag(EVEN_ID)
        else:
            print "Marker "+str(EVEN_ID)








    def loadVideoFile(self,filename):
        self.filename=filename
        logging.info('Video file: '+self.filename)

        #Test if file exists
        tmpFile=open(filename, 'r')
        tmpFile.close()

        self.cap = cv2.VideoCapture(filename)
        if (self.cap.isOpened() == False):
            print("Error opening video stream or file")
            self.height=0
            self.width=0

        else:
            self.height=int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.width=int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))



        return self.cap

    def displayInitialInformation(self):
        self.fullscreen
        #Read the first frame to get inormation about video size
        ret, initFrame = self.cap.read()
        #Restart reading
        self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.startFrame)

        self.overlayColor(initFrame,(0,0,0),1)

        simulation=""
        if self.generateData:
            simulation ="\n\n> !!!!! SIMULATION - NO REALTIME DATA!!!!"


        while(1):
            frame=initFrame.copy()
            cv2.namedWindow(self.feedbackFrameName, cv2.WND_PROP_FULLSCREEN | cv2.WND_PROP_ASPECT_RATIO)
            cv2.setWindowProperty(self.feedbackFrameName, cv2.WND_PROP_FULLSCREEN,self.fullscreen)
            """> Drag the window to the stimuli \n> presentation display and press f key \n> for fullscreen ot ESC/q to continue"""
            self.display_text(frame,l.intro.drag_the_window_and_press_f_for_fullscreen(self.langID)+simulation,(255,255,255),1,1,True)
            cv2.imshow(self.feedbackFrameName,frame)
            key=cv2.waitKey(0)

            if key & 0xFF==ord('f'):
                self.fullscreen=1
                cv2.setWindowProperty(self.feedbackFrameName, cv2.WND_PROP_FULLSCREEN,self.fullscreen)
                self.overlayColor(frame,(0,0,0),1)
                """> Fullscreen mode activated! \n> PRESS SPACE WHEN READY!"""
                self.display_text(frame,l.intro.fullscreen_mode_activated_press_space_when_ready(self.langID),(255,255,255),1,1,True)
                cv2.imshow(self.feedbackFrameName,frame)
                if cv2.waitKey(0) ==32:
                    return self.fullscreen;
            elif key ==ord('\x1b') or key==32:
                self.fullscreen=0
                cv2.setWindowProperty(self.feedbackFrameName, cv2.WND_PROP_FULLSCREEN,self.fullscreen)
                self.overlayColor(frame,(0,0,0),1)

                """> Continue without fullscreen mode!\n> PRESS SPACE WHEN READY!"""
                self.display_text(frame,l.intro.continue_without_fulscreen_press_space_when_ready(self.langID),(255,255,255),1,1,True)
                cv2.imshow(self.feedbackFrameName,frame)
                if cv2.waitKey(0) ==32:
                    return self.fullscreen;

            elif key & 0xFF==ord('q'):
                exit(0)


        return 0

    def validateOpenVibeLSLConnection(self,lslReader):
        if lslReader==None:
            print "No connection, continue with generated data!"
            return


        lslReader.resolveStream()

        #Read the first frame to get inormation about video size
        ret, frame = self.cap.read()
        #Restart reading
        self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.startFrame)
        self.overlayColor(frame,(0,0,0),1)

        while(1):
            displayFrame=frame.copy()
            cv2.namedWindow(self.feedbackFrameName, cv2.WND_PROP_FULLSCREEN | cv2.WND_PROP_ASPECT_RATIO)
            cv2.setWindowProperty(self.feedbackFrameName, cv2.WND_PROP_FULLSCREEN,0)

            """LSL Connection OK\n>Received value  .... \n> PRESS SPACE TO CONTINUE!"""
            self.display_text(displayFrame,l.intro.tcp_connection_ok__received_value(self.langID)+str(lslReader.getControlValue(True))+l.intro.press_space_to_continue(self.langID),(255,255,255),1,1,True)
            cv2.imshow(self.feedbackFrameName, displayFrame)
            if cv2.waitKey(25) ==32:
                #lslReader.disconnect()
                return










    # def validateOpenVibeConnection(self,tcpReader):
    #     if tcpReader==None:
    #         print "No connection, continue with generated data!"
    #         return
    #
    #     tcpReader.connect()
    #     tcpReader.readheader(False)
    #
    #
    #     #Read the first frame to get inormation about video size
    #     ret, frame = self.cap.read()
    #     #Restart reading
    #     self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.startFrame)
    #     self.overlayColor(frame,(0,0,0),1)
    #
    #
    #     while(1):
    #         displayFrame=frame.copy()
    #         cv2.namedWindow(self.feedbackFrameName, cv2.WND_PROP_FULLSCREEN | cv2.WND_PROP_ASPECT_RATIO)
    #         cv2.setWindowProperty(self.feedbackFrameName, cv2.WND_PROP_FULLSCREEN,0)
    #
    #         """>TCP Connection OK\n>Received value  .... \n> PRESS SPACE TO CONTINUE!"""
    #         self.display_text(displayFrame,l.intro.tcp_connection_ok__received_value(self.langID)+str(tcpReader.getTCPcontrolvalue(True))+l.intro.press_space_to_continue(self.langID),(255,255,255),1,1,True)
    #         cv2.imshow(self.feedbackFrameName, displayFrame)
    #         if cv2.waitKey(80) ==32:
    #             tcpReader.disconnect()
    #             return

    def resynchBuffer(self):

        for x in range(0, 10):
            self.lslReader.getControlValue()

        pass


        #if not self.generateData:
        #    while(1):
        #        rc=self.tcpReader.sock.recv(4096)
        #        if len(rc)<=16:
        #            return
        #        print "buffer resynch: received ", len(rc)

    def playVideoFile(self):
        # Read until video is completed

        logging.info("--> Playing started")
        self.sendMarker(Stm.ExperimentStart)

        frame_counter=0

        genSim=0.0
        genTrial=0

        inputSim=0


        step=0;
        start = time.clock()

        restartPosition=0


        trialStart=True
        experimentStart=False
        trialCount=3
        genSimBuffer=[]
        self.fullscreen=self.displayInitialInformation()

        #Check OpenVibe Connection
        if not self.generateData:

            self.validateOpenVibeLSLConnection(self.lslReader)


            #self.validateOpenVibeConnection(self.tcpReader)
            #self.tcpReader.connect()
            #self.tcpReader.readheader(False)
            #self.tcpReader.readheader(False)


        start = time.clock()

        self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.startFrame)
        ret, tmpFrame = self.cap.read()
        restFrameLocation=self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        tmpFrameCounter=self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        negativeSequence=False
        alphaNegative=0

        positiveRuns=0
        negativeRuns=0
        runTrace=""
        runTraceBuffer=[]

        #Marker
        transition=False
        recovery=False
        fail=False

        while (1):


            if not self.generateData:
                receivedControlValue=self.lslReader.getControlValue(True)
                #receivedControlValue=self.tcpReader.getTCPcontrolvalue(True)
            else:
                #Simulation of the received value
                receivedControlValue=random.uniform(-1,1)


            # Capture frame-by-frame
            ret, frame = self.cap.read()
            frame_counter+=1

            #Restart of the video
            if frame_counter==self.restartFrame:
            #if frame_counter==self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
                frame_counter=0 #restart if reaches the end
                self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.startFrame)
                experimentStart=False
                genSimBuffer=[]
                genSim=0
                transition=False
                fail=False
                recovery=False

                #log
                logging.info('-----> NEW RUN <-----')
                self.sendMarker(Stm.Reset)
                #playsound(800,2000)




            hul=cv2.getTrackbarPos('Video Speed', 'Configuration')



            #cv2.putText(frame, "test! " + str(random.randint(1, 101)), (400, 105), cv2.FONT_HERSHEY_COMPLEX_SMALL, 5,
                          #  (225, 0, 0))
            #cv2.line(frame, (500, 400), (640, 480),(0,255,0), 100)

            #arrowedLine(Mat& img, Point pt1, Point pt2, const Scalar& color, int thickness=1, int line_type=8, int shift=0, double tipLength=0.1)

            #cv2.arrowedLine(frame, (500, 400), (640, 480), (0,0,255), 40,4,0,0.5 )

            if trialCount>=self.number_of_trials:
                trialStart=True
                start=time.clock()

            if trialStart:

                frame_counter,trialStart=self.generateInfo(frame,start,frame_counter)

                if ~trialStart:
                    trialCount=0
                else:
                    start=time.clock()
                    pass

            else:

                if experimentStart==False:
                    frame_counter,experimentStart=self.generateArrow(frame,start,frame_counter)
                    tmpFrame=frame.copy()
                    tmpFrameCounter=frame_counter
                    self.resynchBuffer()




                else:

                    if time.clock() - start > 1:
                        start=time.clock()


                        #get previous position of the bar
                        oldPos=genSim

                        #take new input

                        inputSim=receivedControlValue


                        #calculate the step
                        step=(inputSim-oldPos)/(60)

                        #set the first step
                        genSim=oldPos+step
                        genSimBuffer.append(genSim)

                        if(genTrial>1 or genTrial<-1):
                            genTrial=0




                    else:
                        if genSim!=inputSim:
                            genSim+=step
                            genSimBuffer.append(genSim)

                    genTrial=numpy.mean(genSimBuffer)



                    #NEGATIVE INPUTS

                    if genTrial<=0:
                        #print frame_counter % 10

                        #play beep at every fift 10th frame
                        if frame_counter % 10 == 5:
                            playsound(int(2000+abs(genTrial)*100),50)


                        if frame_counter<100:
                            if frame_counter % 10 < 5:

                                    alphaNegative+=1
                            else:

                                    alphaNegative-=1


                        #freeze by copping the frame
                        frame=tmpFrame.copy()

                        #set overlay
                        self.overlayColor(frame,(0,0,255-abs(alphaNegative)*10),abs(genTrial)*3)
                        #threading.Thread(target=playsound, args=(1500, 100)).start()

                        #first frame with negative control value
                        if not negativeSequence:

                            #skip first 2 frames
                            if frame_counter>2:
                                logging.info("-> Fail at frame: "+str(frame_counter)+" time: "+str(start))
                                transition=True
                            self.sendMarker(Stm.ThresholdPassed_Negative)
                            fail=True

                            #save the frame location to tmp var
                            restFrameLocation=self.cap.get(cv2.CAP_PROP_POS_FRAMES)

                            #save the counter
                            tmpFrameCounter=frame_counter



                            #beep sound
                            #threading.Thread(target=playsound, args=(1500, 500)).start()


                        negativeSequence=True

                    #If possitive
                    else:
                        #tmpFrame=frame.copy()
                        #tmpFrameCounter=frame_counter
                        #restFrameLocation=self.cap.get(cv2.CAP_PROP_POS_FRAMES)



                        if negativeSequence:
                            logging.info("-> Recovery at frame: "+str(frame_counter)+" time: "+str(start))
                            self.sendMarker(Stm.ThresholdPassed_Positive)
                            recovery=True
                            transition=True
                            #threading.Thread(target=playsound, args=(800, 500)).start()

                            frame_counter=tmpFrameCounter
                            self.cap.set(cv2.CAP_PROP_POS_FRAMES,restFrameLocation)
                            negativeSequence=False
                            tmpFrame=frame.copy()
                            continue
                        else:
                            tmpFrame=frame.copy()
                            #tmpFrameCounter=frame_counter
                            #restFrameLocation=self.cap.get(cv2.CAP_PROP_POS_FRAMES)









                    self.draw_current_bar(frame,genSim,0.8)
                    self.draw_trial_bar(frame,genTrial,0.8)
            self.draw_pointers(frame)

            #Insert marker
            if frame_counter==self.restartFrame-10:
                self.sendMarker(Stm.VisualStimulationStop)

            if frame_counter==self.restartFrame-1:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.startFrame)
                    restFrameLocation=self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                    tmpFrameCounter=self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                    negativeSequence=False
                    print "var cleared---"


            # If between last 10 frames i.e. 90 to 100
            if frame_counter >self.restartFrame-10 and frame_counter<=self.restartFrame-5:

                #normalize for overlay alpha to 0-100
                norm_frame_counter=100*(frame_counter-self.startFrame)/(self.restartFrame-self.startFrame)



                #If bigger then threshold "0" TODO CHANGE TO TH
                if numpy.mean(genSimBuffer)>0:
                    self.overlayColor(frame,(0,255,0),0.08*(norm_frame_counter)-7.1)
                    """SUCCESS"""

                    if frame_counter==self.restartFrame-9:
                        #beep
                        threading.Thread(target=playSuccess(), args=()).start()

                    self.display_text(frame,l.feedback.success(self.langID),(0,255,50),0.7)
                else:
                    """FAIL"""
                    self.overlayColor(frame,(0,0,255),0.08*norm_frame_counter-7.1)
                    self.display_text(frame,l.feedback.fail(self.langID),(0,50,255),0.7)

                    if frame_counter==self.restartFrame-9:
                        #beep
                        threading.Thread(target=playFail(), args=()).start()

            #between last file -5 to -0
            if frame_counter >self.restartFrame-5 and frame_counter<=self.restartFrame:
                if numpy.mean(genSimBuffer)>0:
                    self.overlayColor(frame,(0,255,0),8.1-norm_frame_counter*0.08)
                    """SUCCESS"""
                    self.display_text(frame,l.feedback.success(self.langID),(0,255,50),0.7)

                    #last frame, signle operation
                    if frame_counter==self.restartFrame-1:
                        trialCount+=1
                        positiveRuns+=1
                        runTrace+=" P"
                        runTraceBuffer.append(numpy.mean(genSimBuffer))
                        #log
                        logging.info("-> Run finished successfully after : "+str(start))
                        logging.info("-> Average control value (r-value) : "+str(numpy.mean(genSimBuffer)))
                        logging.info("-> Buffer : "+','.join([str(x) for x in genSimBuffer]))
                        self.sendMarker(Stm.Label_01)

                        #send marker dependig on transition

                        #No transition POSITIVE marker
                        if not transition:
                            self.sendMarker(Stm.OVTK_StimulationId_Number_01)
                            self.sendMarker(Stm.OVTK_StimulationId_Number_11)
                        elif recovery:
                            self.sendMarker(Stm.OVTK_StimulationId_Number_01)
                            self.sendMarker(Stm.OVTK_StimulationId_Number_1B)







                else:
                    """FAIL"""
                    self.overlayColor(frame,(0,0,255),8.1-norm_frame_counter*0.08)
                    self.display_text(frame,l.feedback.fail(self.langID),(0,50,255),0.7)

                    #last frame, signle operation
                    if frame_counter==self.restartFrame-1:
                        trialCount+=1
                        negativeRuns+=1
                        runTrace+=" N "
                        runTraceBuffer.append(numpy.mean(genSimBuffer))
                        #log
                        logging.info("-> Run failed after : "+str(start))
                        logging.info("-> Average control value (r-value) : "+str(numpy.mean(genSimBuffer)))
                        logging.info("-> Buffer : "+','.join([str(x) for x in genSimBuffer]))
                        self.sendMarker(Stm.Label_00)

                        #No transition POSITIVE negative
                        if not transition:
                            self.sendMarker(Stm.OVTK_StimulationId_Number_00)
                            self.sendMarker(Stm.OVTK_StimulationId_Number_10)
                        elif fail:
                            self.sendMarker(Stm.OVTK_StimulationId_Number_00)
                            self.sendMarker(Stm.OVTK_StimulationId_Number_1A)












            # Display the resulting frame
            #cv2.namedWindow(self.feedbackFrameName, cv2.WINDOW_NORMAL)
            #cv2.setWindowProperty(self.feedbackFrameName, cv2.WINDOW_AUTOSIZE, cv2.WINDOW_AUTOSIZE)
            #cv2.namedWindow( self.feedbackFrameName, cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO)
            #cv2.moveWindow("Frame", int(SCREEN_RESOLUTION_WIDTH*0.5-SCREEN_RESOLUTION_HIGTH * ASPECT_RATIO *0.5),0);

            #cv2.setWindowProperty(self.feedbackFrameName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.namedWindow(self.feedbackFrameName, cv2.WND_PROP_FULLSCREEN | cv2.WND_PROP_ASPECT_RATIO)
            #cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)



            cv2.setWindowProperty(self.feedbackFrameName, cv2.WND_PROP_FULLSCREEN,self.fullscreen)



            """DISPLAY: Number of runs/trials"""
            self.displayPerformance(frame,l.feedback.num_run(self.langID)+" "+str((trialCount))+" / "+str(self.number_of_trials),
                                    l.feedback.num_hits(self.langID)+" "+str((positiveRuns))+" / "+str(self.number_of_trials),
                                    l.feedback.num_fails(self.langID)+" "+str((negativeRuns))+" / "+str(self.number_of_trials))

            #resize to fit display resolution
            if self.enableResize:
                frame=cv2.resize(frame, (self.resolutionW,self.resolutionH))


            cv2.imshow(self.feedbackFrameName, frame)

            # Press Q on keyboard to  exit
            if frame_counter==self.restartFrame-1:
                cv2.waitKey(hul+500)
                if trialCount==self.number_of_trials:
                    self.overlayColor(frame,(0,0,0),1)
                    """display_summary"""
                    self.display_text(frame,l.feedback.summary_display(self.langID,runTrace,runTraceBuffer,positiveRuns,negativeRuns,self.number_of_trials),(255,255,255),1,1,True)
                    cv2.imshow(self.feedbackFrameName, frame)
                    #logging
                    logging.info("\n"+l.feedback.summary_display(self.langID,runTrace,runTraceBuffer,positiveRuns,negativeRuns,self.number_of_trials))

                    #clear variables
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.startFrame)
                    ret, tmpFrame = self.cap.read()
                    restFrameLocation=self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                    tmpFrameCounter=self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                    negativeSequence=False
                    alphaNegative=0

                    positiveRuns=0
                    negativeRuns=0
                    runTrace=""
                    runTraceBuffer=[]
                    print "VAR cleared"

                    key=cv2.waitKey(self.newRoundWaiting)
                    if key ==32:#& 0xFF == ord('s'):
                        pass
                    elif key & 0xFF == ord('q'):
                        self.sendMarker(Stm.ExperimentStop)
                        break;
                    self.sendMarker(Stm.ExperimentStop)
                    self.overlayColor(frame,(0,0,0),1)
                    """> NEW ROUND\n> PRESS SPACE TO CONTINUE OR WAIT FOR THE NEW ROUND\n\n> TO QUIT PRESS Q"""
                    self.display_text(frame,l.feedback.new_round_press_space_to_continue_or_wait_or_q_to_quit(self.langID),(255,255,255),1,1,True)
                    cv2.imshow(self.feedbackFrameName, frame)
                    key=cv2.waitKey(self.newRoundWaiting)
                    if key ==32:#& 0xFF == ord('s'):
                        #log
                        logging.info("NEW ROUND STARTED")
                        #threading.Thread(target=playsound, args=(800, 1000)).start()

                        pass
                    elif key & 0xFF == ord('q'):
                        break;

                    self.resynchBuffer()
            else:
                if cv2.waitKey(hul) & 0xFF == ord('q'):
                    self.sendMarker(Stm.ExperimentStop)
                    logging.info("QUIT (INTERRUPTED)")
                    break

    def generateInfo(self,frame,start,frame_counter):
        if time.clock()-start<2:
            self.display_text(frame,l.feedback.ready(self.langID))
        elif time.clock()-start<3:
            self.display_text(frame,"3")
        elif time.clock()-start<4:
            self.display_text(frame,"2")
        elif time.clock()-start<5:
            self.display_text(frame,"1")
        elif time.clock()-start<6:
            self.display_text(frame,l.feedback.go(self.langID))
        if frame_counter>2:
            frame_counter=0 #restart if reaches the end
            self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.startFrame)

        if time.clock()-start>7:
            trialStart=False
            logging.info("-> "+l.feedback.go(self.langID))
        else:
            trialStart=True

        return frame_counter,trialStart


    def generateArrow(self,frame,start,frame_counter):

        if time.clock()-start<9:
            #self.display_text(frame,"ARROW?")
            #LINE
            #cv2.arrowedLine(frame, (500, 400), (640, 480), (0,0,255), 40,4,0,0.5 )
            cv2.line(frame, (self.width/2,self.height-60 ), (self.width/2,self.height-10),(155,0,255), 5)
            cv2.arrowedLine(frame, (self.width/2+2, self.height-35), (self.width/2+50,self.height-35),(155,0,255), 10,4,0,0.8 )


        if frame_counter>2:
            frame_counter=0 #restart if reaches the end
            self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.startFrame)

        if time.clock()-start<9.5:
            experimentStart=False
        else:
            experimentStart=True
            self.resynchBuffer()
            logging.info("-> EEG starts")
            self.sendMarker(Stm.VisualStimulationStart)

            #beep
            #playsound(1000,500)
            threading.Thread(target=playsound, args=(800, 400)).start()

        return frame_counter,experimentStart



    def displayPerformance(self,frame,text,text2,text3,(R,G,B)=(255,255,255),alpha=0.6):
        size=0.8
        overlay=frame.copy()
        cv2.putText(overlay, text, (20, 30), cv2.FONT_HERSHEY_COMPLEX, size,  (R, G, B),1)
        cv2.putText(overlay, text2, (20, 60), cv2.FONT_HERSHEY_COMPLEX, size,  (R, G, B),1)
        cv2.putText(overlay, text3, (20, 90), cv2.FONT_HERSHEY_COMPLEX, size,  (R, G, B),1)


        cv2.addWeighted(overlay, alpha, frame, 1 - alpha,0, frame)


    def display_text(self,frame,text,(R,G,B)=(0,255,0),alpha=1,size=5,multiline=False):
        pos= self.width/2-len(text)*size*10
        overlay=frame.copy()

        #For Multiline display
        if multiline:
            y0, dy = int(self.height/2), 50
            for i, line in enumerate(text.split('\n')):
                y = y0 + i*dy
                cv2.putText(overlay, line, (50, y ), cv2.FONT_HERSHEY_DUPLEX, size, (R, G, B),2,cv2.LINE_AA)
                cv2.addWeighted(overlay, alpha, frame, 1 - alpha,0, frame)
            return

        cv2.putText(overlay, text, (int(pos), self.height/2), cv2.FONT_HERSHEY_COMPLEX_SMALL, size,  (R, G, B),5)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha,0, frame)


    def draw_trial_bar(self,frame,value,alpha=1):
        #value from -1 to +1
        pos=(self.width/2)*value*0.95+self.width/2
        overlay=frame.copy()
        cv2.rectangle(overlay, (self.width/2, self.height-60), (int(pos),self.height-40),(0,255,255), -1)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha,0, frame)


    def draw_current_bar(self,frame,value,alpha=1):
        #value from -1 to +1
        pos=(self.width/2)*value*0.95+self.width/2
        overlay=frame.copy()
        cv2.rectangle(overlay, (self.width/2, self.height-30), (int(pos),self.height-10),(155,0,255), -1)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha,0, frame)




    def draw_pointers(self,frame):

        cv2.line(frame, (self.width/2,self.height-60 ), (self.width/2,self.height-10),(255,255,255), 5)


    def overlayColor(self,frame,(R,G,B),alpha=0.5):
        overlay=frame.copy()
        cv2.rectangle(overlay, (0, 0), (self.width,self.height),(R, G, B), -1)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha,0, frame)


        return frame





    def closeALl(self):
        # When everything done, release the video capture object
        self.cap.release()

        # Closes all the frames
        cv2.destroyAllWindows()

    def retreiveControlValue(self):
        return random.random(0, -1)


    def createBarTrackers(self):

        def action(value):
            pass


        cv2.namedWindow('Configuration')
        # assign strings for ease of coding
        videoSpeed = 'Video Speed'
        wnd = 'Configuration'

        # Begin Creating trackbars for each
        cv2.createTrackbar(videoSpeed, wnd, 25, 100, action)





def runVideoPlayer(loggingPath="",subjectInfo="Subject info not provided"):
    gui=guiWizard.GUI()
    gui.displayWizard()

    #Configuration
    cfg=io.configReader()
    cfg.getVideoFilename()

    vPlayer=VideoPlayer(False,loggingPath,subjectInfo)


    #congigure
    vPlayer.number_of_trials=cfg.getNumberOfTrials()
    vPlayer.filename=cfg.getVideoFilename()
    vPlayer.startFrame,vPlayer.restartFrame= cfg.getVideoSubsequenceToDisplay()
    vPlayer.langID=cfg.getLanguage()

    vPlayer.createBarTrackers()
    #vPlayer.loadVideoFile("C:\\Users\\aleks\\Documents\\video_stimuli\\sample_converted.mp4")
    vPlayer.loadVideoFile(cfg.getVideoFilename())
    vPlayer.playVideoFile()
    vPlayer.closeALl()

if __name__ == "__main__":
    import sys
#    path=str(sys.argv[1])
#    info=str(sys.argv[2])

    runVideoPlayer()


