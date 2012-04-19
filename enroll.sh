#!/bin/bash
python /home/mvexel/enroll/enroll.py
python /home/mvexel/enroll/charts.py
python /home/mvexel/pygal/PyGallery.py --Gui=0 --Style=Gallery --InputDir=/home/mvexel/www/ARTH/ --Title=EnrollmentARTH --WritePictureName=1 --PicsPerGallery=100 --OutputDir=/home/mvexel/www/enrollment/ARTH
python /home/mvexel/pygal/PyGallery.py --Gui=0 --Style=Gallery --InputDir=/home/mvexel/www/GEOG/ --Title=EnrollmentGEOG --WritePictureName=1 --PicsPerGallery=100 --OutputDir=/home/mvexel/www/enrollment/GEOG
