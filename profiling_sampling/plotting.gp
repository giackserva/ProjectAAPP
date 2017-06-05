# Arguments
# - insert/search/delete
# - type of skiplist (0/1/2)
# - max level of the skiplist
# - data folder
# - y/n to choose if to export to png
# Example of call inside gnuplot
# call "plotting.gp" "insert" "1" "7" "samples2"

reset
if (ARG5 eq 'y') {
  set terminal png enhanced;
  out = sprintf("data/images/n_%s/ml_%s_ns_10000_%s.png", ARG2, ARG3, ARG1);
  set output out;
}
else {
  #set terminal x11 reset
}
set xlabel "N"
set ylabel "t[s]"
title = sprintf("Average %s time with skiplist of max level = %s with various number of nodes and p", ARG0, ARG2)
set title title
set grid

f1 = sprintf("data/%s/n_%s/p_0.10/ml_%s_ns_10000_%s_vs2.csv", ARG4, ARG2, ARG3, ARG1)
f2 = sprintf("data/%s/n_%s/p_0.30/ml_%s_ns_10000_%s_vs2.csv", ARG4, ARG2, ARG3, ARG1)
f3 = sprintf("data/%s/n_%s/p_0.50/ml_%s_ns_10000_%s_vs2.csv", ARG4, ARG2, ARG3, ARG1)
f4 = sprintf("data/%s/n_%s/p_0.70/ml_%s_ns_10000_%s_vs2.csv", ARG4, ARG2, ARG3, ARG1)
plot f1 with points title "p=0.1" lt rgb "red", \
    f2 with points title "p=0.3" lt rgb "dark-green", \
    f3 with points title "p=0.5" lt rgb "blue", \
    f4 with points title "p=0.7"
