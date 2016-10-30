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

connection= pymysql.connect(host='114.55.224.65',
                            user='so',
                            password='ybkmysql123123',
                            db='ybk',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

PORT = 'COM5'
BAUDRATE = 115200
PIN = None # SIM card PIN (if any)

from gsmmodem.modem import GsmModem

def handleSms(sms):
    print(u'== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\nSMSC: {3}\n'.format(sms.number, sms.time, sms.text,sms.smsc))
    # Create a new record
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with connection.cursor() as cursor:
      sql = '''INSERT INTO `sms` (`PhoneNo`,`OrgAddr`, `SmsTime`,`UserData`,`UpdateTime`) VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE PhoneNo=VALUES(PhoneNo),OrgAddr=VALUES(OrgAddr),UserData=VALUES(UserData),SmsTime=VALUES(SmsTime),UpdateTime=VALUES(UpdateTime)'''
      cursor.execute(sql,(sms.number,sms.number,sms.text,sms.time,nowtime))
      connection.commit()

   # print('Replying to SMS...')
   # sms.reply(u'SMS received: "{0}{1}"'.format(sms.text[:20], '...' if len(sms.text) > 20 else ''))
   # print('SMS sent.\n')
    
def main():
    print('Initializing modem...')
    # Uncomment the following line to see what the modem is doing:
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
    modem.smsTextMode = False 
    modem.connect(PIN)
    print('Waiting for SMS message...')

    try:    
        modem.rxThread.join(2**31) # Specify a (huge) timeout so that it essentially blocks indefinitely, but still receives CTRL+C interrupt signal
    finally:
        modem.close();
        connection.close()

if __name__ == '__main__':
    main()
