#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""\
Demo: handle incoming SMS messages by replying to them
Simple demo app that listens for incoming SMS messages, displays the sender's number
and the messages, then replies to the SMS by saying "thank you"
"""
from __future__ import print_function
import logging
import MySQLdb.cursors
import time
from gsmmodem.modem import GsmModem
import serial
import serial.tools.list_ports

port_list = list(serial.tools.list_ports.comports())

if len(port_list) <= 0:
    print(u'No any serial port can be find!')
else:
    PORTS = [port[0] for port in port_list]
   # serlist = [serial.Serial(port_serial, 115200, timeout=60) for port_serial in port_list_coms]
   # PORTS = [ser.name for ser in serlist]
   # for ser in serlist:
   #     print(u'The name of port is  > {0}\n'.format( ser.name))
   #     ser.close()

modem = []

BAUDRATE = 115200
PIN = '1234' # SIM card PIN (if any)

connection= MySQLdb.connect('114.55.224.65',
                            user='so',
                            passwd='ybkmysql123123',
                            db='ybk',
                            charset='utf8',
                            cursorclass=MySQLdb.cursors.DictCursor)

sql = '''INSERT INTO `sms` (`iccid`,`OrgAddr`,`UserData`,`SmsTime`,`UpdateTime`) VALUES (%s, %s, %s, %s, %s)
       ON DUPLICATE KEY UPDATE iccid=VALUES(iccid),OrgAddr=VALUES(OrgAddr),UserData=VALUES(UserData),SmsTime=VALUES(SmsTime),UpdateTime=VALUES(UpdateTime)'''

def handleSms(sms):
    print(u'== SMS message received ==\nFrom: {0} SMSC: {1} Sim ICCID: {2}\nTime: {3}\nMessage:\n{4}\n'.format(sms.number,sms.smsc,sms.iccid[:len(sms.iccid)-1], sms.time, sms.text))
    # Create a new record
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    smstime = str(sms.time)[:len(str(sms.time))-6]

    try:
        cursor=connection.cursor()
        n=cursor.execute(sql,(sms.iccid[:len(sms.iccid)-1],
                              sms.number,
                              sms.text,
                              smstime,
                              nowtime))
        connection.commit()
    except MySQLdb.Error, e:
        print("Could not insert data into MySQLdb.")
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))


def main():
    print('Initializing modem...')
    # Uncomment the following line to see what the modem is doing:
  #  logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s][%(process)d:%(thread)d][%(levelname)s] %(message)s',
        filename="main.log",
        filemode='w')
    _logger = logging.getLogger('another.log')
    fh = logging.FileHandler('another.log')
    fh.setLevel(logging.DEBUG)
    formatter1 = logging.Formatter('[%(asctime)s][%(process)d:%(thread)d][%(levelname)s] %(message)s')
    fh.setFormatter(formatter1)
    _logger.addHandler(fh)

    #################################################################################################
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    #################################################################################################
   # _logger.debug('aaa')

#  open all modems
    IDopened = -1
    PORTSNOTOPEND =[]
    PORTSOPENED=[]
    for i in range(len(PORTS)):
        modem.append(GsmModem(PORTS[i], BAUDRATE, smsReceivedCallbackFunc=handleSms))
        modem[i].smsTextMode = False
        try:
            modem[i].connect(PIN)
            IDopened +=1
            print(u' {0} is opened\n'.format(PORTS[i]))
            PORTSOPENED.append(PORTS[i])
        except:
            PORTSNOTOPEND.append(PORTS[i])
            print(u' {0} can not be opened\n'.format(PORTS[i]))
            pass
    if IDopened>-1:
        if len(PORTSNOTOPEND)>0:
            print(u'{} Ports have not been opened!'.format(len(PORTSNOTOPEND)))
            for p in PORTSNOTOPEND:
               print(p)
        print('='*40)
        try:
            print(u'{} Ports have  been opened!'.format(len(PORTSOPENED)))
            for p in PORTSOPENED:
                print(p)
            print('are waiting for SMS message...')
            modem[IDopened].rxThread.join(2**31) # Specify a (huge) timeout so that it essentially blocks indefinitely, but still receives CTRL+C interrupt signal

        finally:
            modem[IDopened].close();
    else:
        print('No any Ports have been opened, check the Port !')

    connection.close()

if __name__ == '__main__':
    main()
