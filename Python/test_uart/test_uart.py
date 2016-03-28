#! /usr/bin/env python3


import array
import binascii
import sys 
import serial
import serial.tools.list_ports


def sendData(port, data):
    print("Trans Binary: ", data)
    transmit = array.array('B', data).tostring()
    print("Transmit", transmit)
    crc32 = (binascii.crc32(transmit) & 0xFFFFFFFF)
    print(type(crc32))
    print("CRC32 = 0x%x \n" % crc32)
    transmit_crc32 = crc32.to_bytes(4, byteorder=sys.byteorder)
    print(transmit_crc32)
    port.write(transmit)
    port.write(transmit_crc32)
    return

if __name__ == "__main__":
    com_port_list = list(serial.tools.list_ports.comports())
    ports = [x[0] for x in com_port_list]
    print(ports)

    SerialPort = serial.Serial()
    #SerialPort.setPort('COM4')
    SerialPort.setPort('/dev/ttyUSB0')
    SerialPort.setBaudrate(115200)
    SerialPort.setByteSize(serial.EIGHTBITS)
    SerialPort.setParity(serial.PARITY_NONE)
    SerialPort.setStopbits(serial.STOPBITS_ONE)

    SerialPort.open()
    sendData(SerialPort, [0x31, 0x32, 0x33, 0x34])
