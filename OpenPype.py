"""
OpenPype
========
OpenPype is missing open source module for
streaming EEG data or matrixes from OpenVibe
box TCPWrite.

Version: 0.1b
"""
import numpy
import socket
from pylsl import StreamInlet, resolve_stream, resolve_byprop


class OpenVibeLSLClient:
    # first resolve an EEG stream on the lab network
    #print("looking for an EEG stream...")

    def __init__(self):
        self.streams=None
        self.inlet=None


    def resolveStream(self,type="OpenVibe"):
        # first resolve an EEG stream on the lab network
        print("looking for an EEG stream...")
        self.streams = resolve_stream('type', type)
        # create a new inlet to read from the stream
        self.inlet = StreamInlet(self.streams[0])
        if self.inlet!=None and self.streams!=None:
            print "Success! Stream Resolved"
            return True
        print "Could not resolve LSL stream..."
        return False

    def getControlValue(self,printValue=False):
        if self.streams==None or self.inlet==None:
            print "No stream and/or inlet initialized!"
            return None
        chunk, timestamps = self.inlet.pull_sample()

        return chunk[0]
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        #while(1):
        #    chunk, timestamps = self.inlet.pull_chunk()
        #    if timestamps:
        #        value= chunk[0][0]
        #        print "Received control value: "+str(value)
        #        return value
        #        break;

    def disconnect(self):
        if self.inlet!=None:
            self.inlet.close_stream()
            return True

        return False

    def closeStream(self):
        self.inlet.close_stream()









class ConnectionTest:

    @staticmethod
    def testLSL(type="OpenVibe"):
        print "Searching for LSL stream... "+type
        stream=resolve_byprop('type', type,1,2)
        if len(stream)>0:
            return True;
        return False;



    @staticmethod
    def pingServer((tcp_ip,tcp_port)):
        try:
            address=(tcp_ip,tcp_port)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(address)
            sock.close()
            return True
        except:
            return False



    @staticmethod
    def ping(host):
        try:
            from platform   import system as system_name  # Returns the system/OS name
            from subprocess import call   as system_call  # Execute a shell command
        except ImportError:
            print "ERROR IMPORTING PING TOOLS"
            return False


        # Ping command count option as function of OS
        param = '-n 1' if system_name().lower()=='windows' else '-c 1'

        # Building the command. Ex: "ping -c 1 google.com"
        command = ['ping', param, host]

        # Pinging
        return system_call(command) == 0




class OpenVibeClient:
    """
    Client for OpenVibe TCPWritter box.
    Requires address to connect, e.g. IP and
    port. When running on same computer it
    should be 'localhost'
    
    Methods:
        connect() - Connects to intialized address
        disconnect() - Disconnects from socket
        readheader() - Read first 16 bytes as header
        readstream() - Read streamed data from TCPWritter
    """
    def __init__(self, tcp_ip = "localhost", tcp_port = 5678):
        """
        Constructor of OpenVibeClient for reading TCPWritter
        box from OpenVibe. Default address is localhost:5678.
        """
        # Import socket
        try:
            import socket
        except:
            print("Cannot load socket module")
        # Constructor    
        self.address = (tcp_ip, tcp_port)
        self.buffer_size = 32
        self.number_of_channels = None
        self.sampling_frequency = None
        self.samples_per_chunk = None
        self.is_connected = False
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print("No OpenVibe client created because " + 
                  "socket cannot be initialized.")
        
    def connect(self):
        """
        Main method of OpenVibeClient. It connects
        to a socket specified in constructor.
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(self.address)
            self.is_connected = True
            print("Connected to OpenVibe")
        except:
            print("Cannot connect to initialized socket.")
    
    def disconnect(self):
        """
        Disconnects from opened socket. It is 
        highly recommend to close connection
        after you finish streming from server
        to prevent disconnection in future.
        """
        if self.is_connected:
            try:
                # Clear the connection variables
                self.sock.close()
               # self.number_of_channels = None
               # self.sampling_frequency = None
               # self.samples_per_chunk = None
               #self.is_connected = False
               # self.header_readed = False
            except:
                print("Cannot disconnect from connected socket.")
        else:
            print("Socket was not connected. No need to disconnect.")

    
    def readheader(self, info = True):
        """
        After establishing the connection to OpenVibe
        user can try to read datastream header which
        is in int32 format from bytes. It contains
        information about:
            - number of channels
            - samples per chunk
            - sampling frequency
           
        Optional argument info switch output of
        header information.
        """

        # Read header from stream 
        header = []
        if self.is_connected:
            for i in range(5):
                header.append(numpy.frombuffer(self.sock.recv(4), 
                                               dtype = "int32", 
                                               count = -1))
            try:
                self.number_of_channels = int(header[3])
                self.sampling_frequency = int(header[2])
                self.samples_per_chunk = int(header[4])
            except:
                self.number_of_channels = None
                self.sampling_frequency = None
                self.samples_per_chunk = None
                print("Cannot parse data from header")
                
            self.header_readed = True
            
            if info:
                print("END: ", str(header[2]))
                print("Number of channels: ", str(self.number_of_channels))
                print("Sampling frequency: ", str(self.sampling_frequency))
                print("Samples per chunk:  ", str(self.samples_per_chunk))
        else:
            print("Cannot read header if there is no socekt connected.")

    def getTCPcontrolvalue(self,showControlValue=False):

        stream=self.readstream(False)
        if stream!=None:
            controlValue=stream[1]-stream[0]
            if showControlValue: print ("Received control value: "+str(controlValue))
            return controlValue
        else:
            print ("Something went wrong, NO CONTROL VALUE RECEIVED!")
        return 0


                
    def readstream(self, info = True):
        """
        TODO!!!!!
        """
        # Import numpy
        try:
            import numpy
        except:
            print("Cannot import numpy module")
        # Read TCPWritter datastream
        if self.header_readed:
            #print("Reading the TCPWritter stream...")
            stream = []
            rcv=self.sock.recv(8)
            rcv2=self.sock.recv(8)

            if len(rcv)-len(rcv2)==0:
                is_streaming = True
            else:
                is_streaming = False


            while is_streaming:

                stream.append(numpy.frombuffer(rcv, dtype = numpy.float64, count = -1)[0])
                stream.append(numpy.frombuffer(rcv2, dtype = numpy.float64, count = -1)[0])


                if numpy.size(stream) != 0:
                    #eeg_data.append(stream)
                    if info:
                        print(stream)
                    return stream                    
                else:
                    is_streaming = False
                    #self.disconnect()
                    print("No data in buffer, socket is closed.")
        else:
            pass#print("No header was read. Cannot recieve datastream.")

class OpenVibeTCPTagger:

    def __init__(self):
        self.s=None
        self.isConnected=False


    # transform a value into an array of byte values in little-endian order.
    def to_byte(self, value, length):
        for x in range(length):
            yield value%256
            value//=256
    def connect(self,HOST = '127.0.0.1',PORT = 15361):
        # TODO add TRY catch statement to handle if there is not connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        self.s=s
        self.isConnected=True

    def disconnect(self):
        if self.isConnected:
            self.s.close
            self.isConnected=False


    def sendTag(self,EVENT_ID=5+0x8100):
        # Artificial delay (ms). It may need to be increased if the time to send the tag is too long and causes tag loss.
        DELAY=0
        # create the three pieces of the tag, padding, event_id and timestamp
        padding=[0]*8
        event_id=list(self.to_byte(EVENT_ID, 8))

        # timestamp can be either the posix time in ms, or 0 to let the acquisition server timestamp the tag itself.
        timestamp=list(self.to_byte(int(0)+DELAY, 8))
        # send tag and sleep
        self.s.sendall(bytearray(padding+event_id+timestamp))


class stimulation():
    ExperimentStart  = 0x00008001
    ExperimentStop  = 0x00008002
    SegmentStart  =0x00008003
    SegmentStop  = 0x00008004
    TrialStart  = 0x00008005
    TrialStop  = 0x00008006
    VisualStimulationStart  = 0x0000800b
    VisualStimulationStop  = 0x0000800c
    Label_00  = 0x00008100
    Label_01  = 0x00008101
    Label_02  = 0x00008102
    Label_03  = 0x00008103
    Label_04  = 0x00008104
    Label_05  = 0x00008105
    Label_06  = 0x00008106
    Label_07  = 0x00008107
    Label_08  = 0x00008108
    Train  = 0x00008201
    Beep  = 0x00008202
    DoubleBeep  = 0x00008203
    EndOfFile  = 0x00008204
    Target  = 0x00008205
    NonTarget  = 0x00008206
    TrainCompleted  = 0x00008207
    Reset  = 0x00008208
    ThresholdPassed_Positive  = 0x00008209
    ThresholdPassed_Negative  = 0x00008210
    NoArtifact  = 0x00008301
    Artifact  = 0x00008302
    RemovedSamples  = 0x00008310
    AddedSamplesBegin  = 0x00008311
    AddedSamplesEnd  = 0x00008312

    OVTK_StimulationId_Number_00 = 0
    OVTK_StimulationId_Number_01 = 1
    OVTK_StimulationId_Number_10 = 10
    OVTK_StimulationId_Number_11 = 11
    OVTK_StimulationId_Number_1A = 20
    OVTK_StimulationId_Number_1B = 21

    OVTK_GDF_Right  =0x302




if __name__ == "__main__":

    tcpReader=OpenVibeClient()
    tcpReader.connect()
    tcpReader.readheader()
    while 1:
        tcpReader.readstream()

