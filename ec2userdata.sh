#!/bin/bash

#Pull down the latest bootstrap script from github, make it executable, and run it.
curl https://raw.githubusercontent.com/WarpRat/NTI-300/master/nti300bootstrap.sh > /tmp/bootstrap.sh
chmod +x /tmp/bootstrap.sh
/tmp/bootstrap.sh
