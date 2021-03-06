import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import dates
import sqlite3
import os
import string
from datetime import datetime

departments = ['ARTH', 'GEOG']
datapath = "/home/ubuntu/enroll/"
dbfilename = "enroll-fall2014.db"
figbasedir = "/home/ubuntu/www/"
valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
conn = sqlite3.connect(os.path.join(datapath, dbfilename))

print "start creating new charts"
for dept in departments:
    chartcnt = 0
    figdir = os.path.join(figbasedir, dept)
    for row in conn.execute('SELECT DISTINCT(classindex) FROM '
                            'enrollment WHERE department = ?;', (dept,)):
        if row[0] is None:
            continue
        classindex = int(row[0])
        print 'processing class index %s' % (classindex)
        (name, cap, mindate, maxdate) =\
            conn.execute('SELECT title || catnumber, cap, min(date),'
                         ' max(date) FROM enrollment WHERE classindex'
                         ' = ?', (classindex,)).fetchone()
        if name is None:
            continue
        #normalize name
        name = ''.join(c for c in name if c in valid_chars)
#        print maxdate
        curenrol = conn.execute('SELECT enrolled FROM enrollment'
                                ' WHERE classindex = ? AND date = ?',
                                (classindex, maxdate,)).fetchone()
        mindate = datetime.fromtimestamp(float(mindate))
        maxdate = datetime.fromtimestamp(float(maxdate))
        #print name, cap, mindate, maxdate
        enrollment = conn.execute('SELECT date, enrolled FROM enrollment'
                                  ' WHERE classindex = ?',
                                  (classindex,)).fetchall()
        dts = []
        enrolled = []
        for record in enrollment:
            dts.append(datetime.fromtimestamp(float(record[0])))
            enrolled.append(record[1])
        #print dates,enrolled
        hfmt = dates.DateFormatter('%m/%d %H:%M')
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111,
                             autoscale_on=False,
                             xlim=(mindate, maxdate),
                             ylim=(0, cap))
#        ax.xaxis.set_major_locator(dates.HourLocator())
        ax.xaxis.set_major_formatter(hfmt)
        locator = dates.AutoDateLocator()
        ax.xaxis.set_major_locator(locator)
        plt.ylabel('Enrollment')
        plt.xlabel('Date')
        lines = ax.plot(dts, enrolled)
        plt.setp(lines, linewidth=3.0)
        ax.annotate('current enrollment: %i' %
                    curenrol,
                    xy=(0.95, 0.95),
                    xycoords='figure fraction',
                    xytext=(0.95, 0.95),
                    textcoords='axes fraction',
                    horizontalalignment='right',
                    verticalalignment='top')
        plt.title(name +
                  ' Enrollment as of ' +
                  datetime.now().strftime("%d %B %Y, %I%p"))
        fig.autofmt_xdate(rotation=45)
        fig.savefig(os.path.join(figdir, name + '.png'), dpi=96)
        chartcnt += 1
    print "%i new charts created for %s" % (chartcnt, dept)
