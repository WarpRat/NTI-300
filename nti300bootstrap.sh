#!/bin/bash

mkdir /root/bin
echo WAAASSSSUPPP > /root/bin/test.txt
for i in {0..5}; do
	touch /root/bin/touch_test$i
done
