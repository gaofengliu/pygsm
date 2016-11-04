
"""
update mobile phone numbers to  mysql database
"""

from __future__ import print_function
import pymysql.cursors
import time
import numpy as np

def main():

    print('reading sim number,iccid,imsi...')
    #  read sim number file
    sim=np.loadtxt('phone.txt',delimiter=',',usecols=(0,1,2), dtype=str)
    ndim=sim.shape

    connection= pymysql.connect(host='114.55.224.65',
                                user='so',
                                password='ybkmysql123123',
                                db='ybk',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    sql = '''INSERT INTO `sim` (`PhoneNo`,`iccid`, `imsi`) VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE PhoneNo=VALUES(PhoneNo),iccid=VALUES(iccid),imsi=VALUES(imsi)'''
    for i in range(ndim[0]):
       print(u'len={0} no.= {1} iccid= {2} imsi={3}\n'.format(ndim[0],sim[i][0],sim[i][1],sim[i][2]))
       with connection.cursor() as cursor:
           cursor.execute(sql,(sim[i][0],sim[i][2],sim[i][1]))
           connection.commit()
    connection.close()

if __name__ == '__main__':
    main()
