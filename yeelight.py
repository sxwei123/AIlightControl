import socket
from Queue import Queue
import threading
from time import sleep

class yeelight(threading.Thread):
    def __init__(self, address):
        threading.Thread.__init__(self)
        self.buf = Queue()
        self.backCommand = ''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((address, 10003))
        self.running = True
        self.daemon = True

    def run(self):
        while self.running:
            res = self.sock.recv(1024)
            self.buf.put(res)
            sleep(0.2)

    def readBuf(self):
        while not self.buf.empty():
            self.backCommand += self.buf.get()
        cmdPos = self.backCommand.find('\n')
        if cmdPos >= 0:
            cmd = self.backCommand[:cmdPos].strip()
            self.backCommand = self.backCommand[cmdPos+1:]
            return cmd
        return ''

    def close(self):
        self.sock.close()

    def sendCommand(self, method, parameters):
        message = method + ' ' + ','.join(parameters) + '\r\n'
        print "message : ", message
        self.sock.send(message)

    def heartBeat(self):
        self.sendCommand('HB',[])

    def getList(self):
        self.sendCommand('GL',[])

    def control(self, id, red, green, blue,brightness):
        self.sendCommand('C',[id, str(red), str(green), str(blue), str(brightness),''])

    def turn_on(self, id):
        self.control(id,'','','',100)

    def turn_off(self, id):
        self.control(id,'','','',0)

    def changeColor(self, id, red, green, blue):
        self.control(id, red, green, blue, '')

    def changeBrightness(self, id, brightness):
        self.control(id, '', '', '', brightness)

    def turn_on_all(self):
        self.turn_on('G000')

    def turn_off_all(self):
        self.turn_off('G000')

    def delay_on(self, id, minutes):
        self.sendCommand('T',[id,str(minutes),1])

    def delay_off(self, id, minutes):
        self.sendCommand('T',[id,str(minutes),0])
