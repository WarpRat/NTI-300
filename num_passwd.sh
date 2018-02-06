#!/bin/bash

while read line; do
	echo -e "$((count ++)) $line"; done < /etc/passwd
