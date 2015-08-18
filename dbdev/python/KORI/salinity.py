'''
Created on Jul 23, 2015
This script calculates the salinity values in PSU for the falmouth meters.
The calculate_salinity() function was written by Zexuan Xu.
The rest of this code is a implimentation of that function by Seth Bassett

@author: Seth Bassett, Zexuan Xu

'''
import psycopg2
import psycopg2.extras
import decimal
import datetime

def calculate_salinity(cond, temp):
    '''Calculate the salinity given a conductivity and temperature value
    cond (float): Conductivity in mmho/cm
    temp (float): Temperature in degrees centigrade
    returns salinity (float): total salinity in PSU
    Function written by Zexuan Xu, implimented by Seth Bassett'''
    a0 = 0.0080
    a1 = -0.1692
    a2 = 25.3851
    a3 = 14.0941
    a4 = -7.0261
    a5 = 2.7081
    b0 = 0.0005
    b1 = -0.0056
    b2 = -0.0066
    b3 = -0.0375
    b4 = 0.0636
    b5 = -0.0144
    rtkcl = -0.0267243 * (temp ** 3) + 4.6636947 * (temp ** 2) + 861.3027640 * temp + 29035.1640851    
    rt = (cond * 1000) / rtkcl    
    deltaS = (b0 + b1 * (rt ** 0.5) + b2 * rt + b3 * (rt ** 1.5) + b4 * (rt ** 2) + b5 *(rt ** 2.5)) * (temp - 15.0)/ (1 + 0.0162 * (temp - 15.0))    
    salinity = a0 + a1 * (rt ** 0.5) + a2 * rt + a3 * (rt ** 1.5) + a4 * (rt ** 2) + a5 * (rt ** 2.5) + deltaS    
    return salinity

if __name__ == '__main__':
    
    #establish connection using credentials
    pw = raw_input()
    conn = psycopg2.connect(dsn=None, host="fgs-usrv", user="wkp_user",password=pw,database="wkp_hrdb")
    
    #get data from database
    print "Fetching Data"
    sql = 'SELECT falmouth_id, cond, temp FROM falmouth ORDER BY falmouth_id;'
    cursor =  conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    #build a dictionary table
    print "Building dict-table"
    cInfo = cursor.description
    header = [i[0] for i in cInfo]
    data = [{c:val for c,val in zip(header, row)} for row in rows]
    
    #calculate salinity
    print "Calculating Salinity Values"
    for row in data[:]:
        try:
            row['salt'] = calculate_salinity(float(row['cond']),float(row['temp']))
        except Exception, e:
            print row
            print e
            row['salt'] = None
    
    #execute INSERT statement
    print "Executing Insert Statement"
    for row in data:
        cursor.execute("""INSERT INTO falmouth_salt (falmouth_id, salt) VALUES (%(falmouth_id)s, %(salt)s);""",
                       {'falmouth_id':row['falmouth_id'], 'salt':row['salt']})
    #commit changes
    print "Commiting Changes"
    conn.commit()
    
    print "Removing Cursors and Connections"
    cursor.close()
    conn.close()
    del cursor
    del conn
    
    print "Finished"
    #sql = '''CREATE VIEW 
    
    
             
    
    
    
    
    
    
    