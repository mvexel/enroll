#!/bin/bash -l
START=$(date +%s)
python /home/ubuntu/enroll/enroll.py >> /home/ubuntu/enroll/enroll.log
python /home/ubuntu/enroll/charts.py >> /home/ubuntu/enroll/enroll.log
python /home/ubuntu/pygal/PyGallery.py --Gui=0 --Style=Gallery --Title=EnrollmentARTH --WritePictureName=1 --PicsPerGallery=100 /home/ubuntu/www/ARTH /home/ubuntu/www/enrollment/ARTH > /dev/null 2>&1
#python /home/ubuntu/pygal/PyGallery.py --Gui=0 --Style=Gallery --InputDir=/home/ubuntu/www/GEOG/ --Title=EnrollmentGEOG --WritePictureName=1 --PicsPerGallery=100 --OutputDir=/home/ubuntu/www/enrollment/GEOG > /dev/null 2>&1
END=$(date +%s)
DIFF=$(( $END - $START ))
echo "`date`: new galleries created. done. took $DIFF secs" >> /home/ubuntu/enroll/enroll.log
