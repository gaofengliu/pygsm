
"""
update mobile phone numbers to  mysql database
"""

from __future__ import print_function

# import pymysql.cursors
import time
import numpy as np


'''
connection= pymysql.connect(host='114.55.224.65',
                            user='so',
                            password='ybkmysql123123',
                            db='ybk',
                            charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
'''
def main():
    print('reading sim number,iccid,imsi...')
    #  read sim number file
    sim=np.loadtxt('simno.txt', delimiter=',',usecols=(0,1,3), dtype=str) # int narray
    ndim=sim.shape()

    for i in ndim[1]:
       print(u'no.= {0} iccid= {1} imsi={2}\n'.format(sim[i][0],sim[i][1],sim[i][2]))

#    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

#    with connection.cursor() as cursor:
#    sql = '''INSERT INTO `sms` (`PhoneNo`,`OrgAddr`, `SmsTime`,`UserData`,`UpdateTime`) VALUES (%s, %s, %s, %s, %s)
#                ON DUPLICATE KEY UPDATE PhoneNo=VALUES(PhoneNo),OrgAddr=VALUES(OrgAddr),UserData=VALUES(UserData),SmsTime=VALUES(SmsTime),UpdateTime=VALUES(UpdateTime)'''
#    cursor.execute(sql,(sms.number,sms.number,sms.text,sms.time,nowtime))
#    connection.commit()

 #       connection.close()

if __name__ == '__main__':
    main()
