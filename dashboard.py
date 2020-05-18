import sys
import time
from daemon3 import Daemon
import sysv_ipc as ipc
import TM1638
import time
import os

class Dashboard(Daemon):   
    def run(self):
        # Configure IPC
        path = "/tmp"
        text = ""
        leds = 0
        buttons = 0
        try:           
            key = ipc.ftok(path, 2333)
            shm = ipc.SharedMemory(key, ipc.IPC_CREAT, 0600, 1024)
        except:
            print("Error")
        
        # Init board
        board = self.initialize()
        while True:
            # Text
            textBuf = shm.read(8, 0)
            if text != textBuf:
                text = textBuf
                board.set_text(text)
                
            # LEDS
            ledsBuf = shm.read(8, 8)
            if leds != ledsBuf:
                leds = ledsBuf
                for i in range(0, 8):
                    if leds[i] == "1":
                        board.set_led(i, 255)
                    else:
                        board.set_led(i, 0)
            
            # Buttons
            buttonsBuf = board.get_buttons();
            if buttonsBuf != buttons:
                buttons = buttonsBuf
                shm.write('{0:08b}'.format(buttons), 16)
            
    def initialize(self):
        #I found if we do not attach ourselves
        #it will attach as ReadOnly.
        #shm.attach(0,0)  
        #buf = shm.read(19)
        #print(buf)
        #shm.detach()
        
        # These are the pins the display is connected to. Adjust accordingly.
        # In addition to these you need to connect to 5V and ground.

        DIO = 17
        CLK = 27
        STB = 22

        board = TM1638.TM1638(DIO, CLK, STB)
        board.enable(1)
        return board
    
    # CPU temp
    def showCPUTemp(self, board):        
        res = os.popen('cat /sys/class/thermal/thermal_zone0/temp').readline()
        res = res.replace('\n', '')
        board.set_text("CPU %0.1fc" % (float(res)/1000))
    
    # Load Average
    def showCPULoad(self, board):
        res = os.popen('uptime').readline()
        res = res.replace('\n', '')
        pos = res.index('age:')
        load = res[pos+5:pos+9]
        board.set_text("load %s" % (load))
        
if __name__ == "__main__":
    daemon = Dashboard('/tmp/daemon-tm1638.pid')

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
