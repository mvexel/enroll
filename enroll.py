from bs4 import BeautifulSoup
import urllib2
import sqlite3
import datetime
import time
import os

depts = ['ARTH','GEOG']
baseurl = 'http://www.acs.utah.edu/uofu/stu/scheduling/crse-info?term=1128&subj='

datapath = "/home/mvexel/enroll/"
dbfilename = "enroll.db"
fieldtypes = "isiisiii"

def adapt_datetime(ts):
    return time.mktime(ts.timetuple())

if not os.path.exists(os.path.join(datapath, dbfilename)):
# CREATE DATABASE
    conn = sqlite3.connect(os.path.join(datapath,dbfilename))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS enrollment 
    (date text, classindex integer, subject text, catnumber integer, section integer, title text, cap integer, enrolled integer, available integer, department text)
    ''')
    conn.commit()
    c.close()
    print 'table created'

try:
    conn = sqlite3.connect(os.path.join(datapath,dbfilename))
except NameError:
    print "database was open"

sqlite3.register_adapter(datetime.datetime, adapt_datetime)

for dept in depts:
    print "parsing %s" % dept
    url = baseurl + dept
    print url
    soup = BeautifulSoup(urllib2.urlopen(url))
    t = soup('table')[2]
    rowcnt = 0
    for row in t('tr'):
        print "row!"
        vals = [datetime.datetime.now()]
        if len(row('td')) != 8:
                continue
        rowcnt+=1
        for cell in row('td'):
            if cell.string is not None:
                if fieldtypes[len(vals)-1] == 's':
                    vals.append(cell.string.strip())
                else:
                    vals.append(int(cell.string.strip()))
        vals.append(dept)
        if len(vals) != 10: 
            continue
        c = conn.cursor()
        c.execute('''INSERT INTO enrollment VALUES (?,?,?,?,?,?,?,?,?,?)''', tuple(vals))
        conn.commit()
        c.close()
        print "%i records added" % rowcnt
conn.close()
