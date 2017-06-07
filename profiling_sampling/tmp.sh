# MAX
awk '{if(a[FILENAME]<$2)a[FILENAME]=$2}END{for(i in a)print i,a[i]}' p_0.*/ml_*insert* | sort -k2 -n
# MIN
awk '{if(a[FILENAME]>$2)a[FILENAME]=$2}END{for(i in a)print i,a[i]}' p_0.*/ml_*insert* | sort -k2 -n
