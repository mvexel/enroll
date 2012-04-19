import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import sqlite3
import os
from datetime import datetime

departments = ['ARTH', 'GEOG']
datapath = "/home/mvexel/enroll/"
dbfilename = "enroll.db"
figbasedir = "/home/mvexel/www/"

conn = sqlite3.connect(os.path.join(datapath,dbfilename))

print "start creating new charts"
for dept in departments:
    chartcnt=0
    classindices = conn.execute('SELECT DISTINCT(classindex) FROM enrollment WHERE department = ?;',(dept,)).fetchall()
    figdir = os.path.join(figbasedir,dept)
    for classindex in classindices:
        (name,cap, mindate, maxdate) = conn.execute('SELECT subject || catnumber, cap, min(date), max(date) FROM enrollment WHERE classindex = ?',classindex).fetchone()
#        print maxdate
        curenrol = conn.execute('SELECT enrolled FROM enrollment WHERE classindex = ? AND date = ?',(classindex[0],maxdate)).fetchone()
        mindate = datetime.fromtimestamp(float(mindate))
        maxdate = datetime.fromtimestamp(float(maxdate))
#        print name, cap, mindate, maxdate
        enrollment = conn.execute('SELECT date, enrolled FROM enrollment WHERE classindex = ?',classindex).fetchall()
        dates = []
        enrolled = []
        for record in enrollment:
            dates.append(datetime.fromtimestamp(float(record[0])))
            enrolled.append(record[1])
#        print dates,enrolled
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111,autoscale_on=False, xlim=(mindate,maxdate), ylim=(0,cap))
        plt.ylabel('Enrollment')
        plt.xlabel('Date')
        lines = ax.plot(dates,enrolled)
        plt.setp(lines, linewidth=3.0)
        ax.annotate('current enrollment: %i' % curenrol, xy=(0.95,0.95), xycoords='figure fraction', xytext=(0.95,0.95), textcoords='axes fraction', horizontalalignment='right', verticalalignment='top')
        plt.title(name + ' Enrollment as of ' + datetime.now().strftime("%d %B %Y, %I%p"))
        fig.autofmt_xdate(rotation=45)
        fig.savefig(os.path.join(figdir,name+'.png'), dpi=96)
        chartcnt+=1
    print "%i new charts created for %s" % (chartcnt, dept)
