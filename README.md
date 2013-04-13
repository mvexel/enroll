enroll
======

Gets enrollment figures from utah.edu, sticks them in an SQLite database, and creates nice-ish charts from them.

Requirements
------------
ubuntu / debian packages (`apt-get install`):  

    apache2 sqlite3 python-pip, python-numpy, g++ python-dev, libfreetype6-dev libpng-dev  

python modules (`pip install`)  

    sqlite3 mathplotlib beautifulsoup4 pillow  

That is all, I think..

Oh you will need to create:

    ~/www
    ~/www/ARTH
    ~/www/enrollment/ARTH

And have PyGallery in ~/pygal, get it here: http://pygallery.sourceforge.net/
