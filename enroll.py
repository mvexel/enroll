from bs4 import BeautifulSoup
import urllib2
import sqlite3
import datetime
import time
import os
import config
import requests

hot_courses = [4230]  # courses that need email slag
hot_emails = ['m@rtijn.org', 'jessen.kelly@utah.edu']
depts = ['ARTH', 'GEOG']
term = '1148'  # fall 2014
baseurl = 'http://www.acs.utah.edu/uofu/stu/'\
    'scheduling/crse-info?term=%s&subj=' % (term,)

datapath = "/home/ubuntu/enroll"
dbfilename = "enroll-fall2014.db"
fieldtypes = "isiisiii"


def send_email(catnumber, old, new):
    print 'sending email about %s' % catnumber
    if new - old > 0:
        subject = 'More enrollment!'
    else:
        subject = 'Dropped :('
    return requests.post(
        "https://api.mailgun.net/v2/maproulette.org/messages",
        auth=("api", config.mailgun_api_key),
        data={"from": "Boni <m@rtijn.org>",
              "to": hot_emails,
              "subject": subject,
              "text": "Enrollment for %s changed, "
                      "it was %s and now it is %s."
                      "\n\nLove - Mannetje" % (catnumber, old, new)})


def adapt_datetime(ts):
    return time.mktime(ts.timetuple())

if not os.path.exists(os.path.join(datapath, dbfilename)):
# CREATE DATABASE
    conn = sqlite3.connect(os.path.join(datapath, dbfilename))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS enrollment
    (date text, classindex integer, subject text, catnumber integer,
    section integer, title text, cap integer, enrolled integer,
    available integer, department text)
    ''')
    conn.commit()
    c.close()
    print 'table created'

try:
    conn = sqlite3.connect(os.path.join(datapath, dbfilename))
except NameError:
    print "database was open"

sqlite3.register_adapter(datetime.datetime, adapt_datetime)

for dept in depts:
    print "parsing %s" % dept
    url = baseurl + dept
    print url
    soup = BeautifulSoup(urllib2.urlopen(url))
    t = soup('table')[0]
    rowcnt = 0
    for row in t('tr'):
        cellcnt = 0
        vals = [datetime.datetime.now()]
        if len(row('td')) != 8:
            # print 'skipping weird row'
            continue
        rowcnt += 1
        for cell in row('td'):
            # print 'parsing row %i, cell %i, should be be %s, content %s' %\
            #    (rowcnt, cellcnt, fieldtypes[cellcnt], cell.string)
            if cell.string is not None:
                if fieldtypes[cellcnt] == 's':
                    vals.append(cell.string.strip())
                else:
                    vals.append(int(cell.string.strip()))
            else:
                    vals.append(None)
            cellcnt += 1
        vals.append(dept)
        # print len(vals)
        if len(vals) != 10:
            continue
        c = conn.cursor()
        c.execute('''INSERT INTO enrollment VALUES (?,?,?,?,?,?,?,?,?,?)''',
                  tuple(vals))
        conn.commit()
    print "%i records added" % rowcnt

# now check the hot courses

for hot_course in hot_courses:
    q = c.execute("select enrolled from enrollment "
                  "where catnumber = %i order by date desc limit 2;" %
                  hot_course).fetchall()
    results = [res[0] for res in q]
    if len(results) == 2 and results[0] != results[1]:
        send_email(hot_course, results[1], results[0])

c.close()
conn.close()
