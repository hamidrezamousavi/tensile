
from time import sleep
from serial import Serial
from util import range_lookup_table, TensileOutput

class Tensile:
    def __init__(self,port = 'COM1', sampling_rate = 10 , baudrate = 19200):
        self.active = False
        self.sampling_rate = sampling_rate
        self.port = port
        self.baudrate = baudrate
        try:
            self.serial_port = self.connect_to_port(self.port, self.baudrate)
            self.range = self.get_load_cell_range()
        except Exception as e :
            raise e
        self.speed = 10

    def connect_to_port(self, port, baudrate):
        self.active = True
        return Serial(self.port, self.baudrate,timeout = 0.1)
   
    def get_load_cell_range(self):
        self.serial_port.write(b'RC\r')
        loadcell_type = self.serial_port.read(100)
        loadcell_type = self.bytes_to_num_list(loadcell_type)
        loadcell_type = str(int(loadcell_type[0]))
        return range_lookup_table[loadcell_type]

    def read_data(self):

        #for _ in range(100):
        #while self.active:
        self.serial_port.write(b'WX091\r')
        self.serial_port.write(b'#\r')
        raw_data = self.serial_port.read(100)
            
        raw_data = self.bytes_to_num_list(raw_data)
        tensile_output = TensileOutput( 
                    self.force_to_newton(raw_data[0]),
                    self.position_to_mm(raw_data[1]),
                    self.extenso_to_mm(raw_data[2])
                     )
         
        
        return tensile_output           
        
    
    def move_up(self):
        self.serial_port.write(b'WF\r')
    
    def move_down(self):
        self.serial_port.write(b'WR\r')
    
    def stop(self):
        self.serial_port.write(b'WS\r')
    
    def zero_position(self):
        self.serial_port.write(b'WP\r')

    def zero_force(self):
        self.serial_port.write(b'WZ\r')
    def zero_extensometer(self):
        self.serial_port.write(b'WN1\r')
    
    def set_speed(self, speed):
        self.speed = speed
        speed = str(speed)
        speed = bytes(speed, 'utf8')
        
        command = b'WV'+speed+b'\r'
      #  print(command)
        self.serial_port.write(command)

    def close(self):
        self.serial_port.close()
    
    def force_to_newton(self, num):
        return round(num * self.range / 30000,1)
    
    def extenso_to_mm(self, num):
        return round(num * 0.009,3)
    
    def position_to_mm(self, num):
        return num/1000
    @staticmethod
    def bytes_to_num_list(b):
        b = str(b,'utf8')
        b = b.split('\r')
        b = list(filter(lambda item: item != '\x04', b))
        b = list(filter(lambda item: item != '', b))
        b = list(filter(lambda item: item != '?', b))
        
        b = [float(item) for item in b]
        return b

if __name__ == '__main__':
    sleep(10)
    t = Tensile()
    sleep(1)
    t.set_speed(150)
    sleep(1)
    t.zero_force()
    sleep(1)
    t.zero_position()
    sleep(1)
    t.zero_extensometer()
    sleep(1)
    t.move_up()
    t.read_data()
    t.stop()
    sleep(1)
    t.set_speed(10)
    sleep(1)
    t.move_down()
    t.read_data()
    t.stop()

    #print(t.get_load_cell_range())
    t.close_connection()
