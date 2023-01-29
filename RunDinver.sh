#!/bin/bash

export PATH=/home/gVwave/Opsy/bin:$PATH


dinver -optimization -i DispersionCurve -param $1.param -target $2.target -f -max-misfit 0.3 -ns $3 -o temp.report
gpdcreport temp.report -best 200 > $4.txt
rm temp.report
