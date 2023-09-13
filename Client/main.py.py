from usocket import socket
from machine import Pin,SPI,ADC
import network
import time

# GPIO 핀 설정
button_pin1 = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)
button_pin2 = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP)
button_pin3 = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)
button_pin4 = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)
adc = machine.ADC(28)
#machine.sleep(100)  # 0.1초 대기
            
#W5x00 chip init
def w5x00_init():
    spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
    nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
    nic.active(True)
    
    #None DHCP
    nic.ifconfig(('192.168.0.20','255.255.255.0','192.168.0.1','8.8.8.8'))
    
    #DHCP
    #nic.ifconfig('dhcp')
    
    print('IP address :', nic.ifconfig())
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())

def client_loop(query):
    s = socket()
    s.connect(('192.168.0.4', 5000))  # Destination IP Address
    #data = query.encode('utf-8')
    query_str = str(query)
    query_bytes = query_str.encode('utf-8')
    s.send(query_bytes)
    s.close()

def main():
    w5x00_init()
###TCP SERVER###
    #server_loop()
###TCP CLIENT###
    print("Ready")
    try:
        while True:
            # 클라이언트와의 통신 코드
            if button_pin1.value() == 0:
                analog_value = adc.read_u16()
                print("Button 1 pressed. Sending data: %d" % analog_value)
                client_loop(analog_value)
                time.sleep(3)
            elif button_pin3.value() == 0:
                analog_value = adc.read_u16()
                print("Button 3 pressed. Sending data: %d" % analog_value)
                client_loop(analog_value)
                time.sleep(3)
            elif button_pin2.value() == 0:
                analog_value = adc.read_u16()
                print("Button 2 pressed. Sending data: %d" % analog_value)
                client_loop(analog_value)
                time.sleep(3)
    except ConnectionResetError:
        print("클라이언트 연결이 닫혔습니다.")
    except Exception as e:
        print("오류 발생:", e)
    finally:
        # 클라이언트 종료 또는 기타 마무리 작업을 수행할 수 있음
        pass
if __name__ == "__main__":
    main()





