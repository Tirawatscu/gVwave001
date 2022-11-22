set local
set "PATH=D:\Program Files\geopsypack-win64-3.4.1\bin;%PATH%"
Dinver -optimization -i DispersionCurve -param %1.param -target %2.target -f -max-misfit 0.3 -ns %3 -o temp.report
gpdcreport temp.report -best 200 > %4.txt
del temp.report