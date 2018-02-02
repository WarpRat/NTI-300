#!/bin/bash

for x in $(ls *.conf);do
	cp $x $x.$(date +%s)
done
