#!/usr/bin/env python
"""\
Demo: handle incoming SMS messages by replying to them
Simple demo app that listens for incoming SMS messages, displays the sender's number
and the messages, then replies to the SMS by saying "thank you"
"""
from __future__ import print_function
import logging
import pymysql.cursors
import time

from gsmmodem.modem import GsmModem

#PORTS =('COM36','COM37','COM38','COM39','COM40','COM41','COM42','COM43','COM44','COM45','COM46','COM47','COM48','COM49','COM50','COM51','COM262','COM263','COM264','COM265','COM286','COM287',
#'COM288','COM289','COM290','COM291','COM292','COM293','COM294','COM295','COM296','COM297','COM298','COM299','COM300','COM302','COM303','COM304','COM305','COM306','COM307','COM308','COM309')

PORTS =('COM36','COM37','COM38')

modem = []

BAUDRATE = 115200
PIN = None # SIM card PIN (if any)

connection= pymysql.connect(host='114.55.224.65',
                            user='so',
                            password='ybkmysql123123',
                            db='ybk',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

sql = '''INSERT INTO `sms` (`iccid`,`OrgAddr`,`UserData`,`SmsTime`,`UpdateTime`) VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE iccid=VALUES(iccid),OrgAddr=VALUES(OrgAddr),UserData=VALUES(UserData),SmsTime=VALUES(SmsTime),UpdateTime=VALUES(UpdateTime)'''

def handleSms(sms):
    print(u'== SMS message received ==\nFrom: {0} SMSC: {1} Sim ICCID: {2}\nTime: {3}\nMessage:\n{4}\n'.format(sms.number,sms.smsc,sms.iccid, sms.time, sms.text))
    # Create a new record
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with connection.cursor() as cursor:
        cursor.execute(sql,(sms.iccid,sms.number,sms.text,sms.time,nowtime))
        connection.commit()

def main():
    print('Initializing modem...')
    # Uncomment the following line to see what the modem is doing:
  #  logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s][%(process)d:%(thread)d][%(levelname)s] %(message)s',
        filename="main.log",
        filemode='a+')
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
    _logger.debug('aaa')
    for i in range(len(PORTS)):
        modem.append(GsmModem(PORTS[i], BAUDRATE, smsReceivedCallbackFunc=handleSms))
        modem[i].smsTextMode = False
        modem[i].connect(PIN)
        print(u' {0} is opened\n'.format(PORTS[i]))
        print('Waiting for SMS message...')
    try:
        for i in range(len(PORTS)):
            modem[i].rxThread.join(2**31) # Specify a (huge) timeout so that it essentially blocks indefinitely, but still receives CTRL+C interrupt signal
    finally:
        for i in range(len(PORTS)):
            modem[i].close();
    connection.close()

if __name__ == '__main__':
    main()
