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

for dept in departments:
    classindices = conn.execute('SELECT DISTINCT(classindex) FROM enrollment WHERE department = ?;',(dept,)).fetchall()
    figdir = os.path.join(figbasedir,dept)
    for classindex in classindices:
        print classindex
        (name,cap) = conn.execute('SELECT subject || catnumber, cap FROM enrollment WHERE classindex = ?',classindex).fetchone()
        print name
        print cap
        enrollment = conn.execute('SELECT date, enrolled FROM enrollment WHERE classindex = ?',classindex).fetchall()
        dates = []
        enrolled = []
        for record in enrollment:
            dates.append(datetime.fromtimestamp(float(record[0])))
            enrolled.append(record[1])
        print dates,enrolled
        fig = plt.figure(figsize=(8,6))
        plt.plot(dates,enrolled)
        fig.autofmt_xdate(rotation=30)
        plt.ylabel('Enrollment')
        plt.xlabel('Date')
        plt.title(name + ' Enrollment as of ' + datetime.now().strftime("%d %B %Y, %I%p"))
        fig.savefig(os.path.join(figdir,name+'.png'), dpi=96)
#chart = SimpleLineChart(200, 125, y_range=[0, max_y])

