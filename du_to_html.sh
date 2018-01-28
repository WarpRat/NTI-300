#!/bin/bash

#Insert html headers and other info
echo -e '<html>\n  <head>\n    <title>home du as of' $(date) '</title>\n  <body>\n    <h1>Disk Use Statistics</h1>\n    <br><br>\n    <h2>Disk use for host<em>' $(hostname) '</em></h2>\n    <br>\n    <h3>Last updated: ' $(date) '</h3>\n    <br>\n    <ul>' | sudo tee /var/www/html/du.html

#Find everyone home folder disk use and append the proper html file
find /home -maxdepth 1 -mindepth 1 -type d -exec du -sh {} \; 2> /dev/null | awk '{print "      <li>"$2" contains "$1" of files.</li>"}' | sudo tee -a /var/www/html/du.html

#Close up the html
echo -e '    </ul>\n  </body>\n</html>' | sudo tee -a /var/www/html/du.html
