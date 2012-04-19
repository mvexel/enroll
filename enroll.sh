#!/bin/bash
python /home/mvexel/enroll/enroll.py >> /home/mvexel/enroll/enroll.log
python /home/mvexel/enroll/charts.py >> /home/mvexel/enroll/enroll.log
python /home/mvexel/pygal/PyGallery.yp --Gui=0 --Style=Gallery --InputDir=/home/mvexel/www/ARTH/ --Title=EnrollmentARTH --WritePictureName=1 --PicsPerGallery=100 --OutputDir=/home/mvexel/www/enrollment/ARTH > /dev/null 2>&1
python /home/mvexel/pygal/PyGallery.py --Gui=0 --Style=Gallery --InputDir=/home/mvexel/www/GEOG/ --Title=EnrollmentGEOG --WritePictureName=1 --PicsPerGallery=100 --OutputDir=/home/mvexel/www/enrollment/GEOG >> /dev/null 2>&1
echo "`date`: new galleries created. done." >> /home/mvexel/enroll/enroll.log
