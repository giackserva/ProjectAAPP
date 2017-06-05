# Arguments
# - insert/search/delete
# - type of skiplist (0/1/2)
# - max level of the skiplist
# - data folder
# - lines/points
# - y/n to choose if to export to png
# Example of call inside gnuplot
# call "plotting.gp" "insert" "1" "7" "samples2"


reset
if (ARG5 eq 'y') {
  set terminal png enhanced;
  set output "data/images/n_'ARG1/ml_'ARG2_ns_10000_'ARG0.png";
}
else {
  set output
}
set xlabel "N"
set ylabel "t[s]"
set title "Average 'ARG0 time with skiplist of max level = 'ARG2 with various number of nodes and p"
set grid

f1 = sprintf("data/%s/n_%s/p_0.10/ml_%s_ns_10000_%s_vs2.csv", ARG4, ARG2, ARG3, ARG1)
f2 = sprintf("data/%s/n_%s/p_0.30/ml_%s_ns_10000_%s_vs2.csv", ARG4, ARG2, ARG3, ARG1)
f3 = sprintf("data/%s/n_%s/p_0.50/ml_%s_ns_10000_%s_vs2.csv", ARG4, ARG2, ARG3, ARG1)
f4 = sprintf("data/%s/n_%s/p_0.70/ml_%s_ns_10000_%s_vs2.csv", ARG4, ARG2, ARG3, ARG1)
plot f1 with points, f2 with points, f3 with points, f4 with points



#plot 'data/', ARG3, '/n_', ARG1, '/p_0.10/ml_', ARG2', '_ns_10000_', ARG0, '_vs2.csv'
#using 1:2 with 'ARG4 title "p=0.10", 'data/'ARG3/n_'ARG1/p_0.30/ml_'ARG2_ns_10000_'ARG0_vs2.csv' using 1:2 with 'ARG4 title "p=0.30", 'data/'ARG3/n_'ARG1/p_0.50/ml_'ARG2_ns_10000_'ARG0_vs2.csv' using 1:2 with 'ARG4 title "p=0.50", 'data/'ARG3/n_'ARG1/p_0.70/ml_'ARG2_ns_10000_'ARG0_vs2.csv' using 1:2 with 'ARG4 title "p=0.70", 'data/'ARG3/n_'ARG1/p_0.90/ml_'ARG2_ns_10000_'ARG0_vs2.csv' using 1:2 with 'ARG4 title "p=0.90"
#plot 'data/'ARG3/n_'ARG1/p_0.10/ml_'ARG2_ns_10000_'ARG0_vs2.csv' with 'ARG4 title "p=0.10", 'data/'ARG3/n_'ARG1/p_0.30/ml_'ARG2_ns_10000_'ARG0_vs2.csv' with 'ARG4 title "p=0.30", 'data/'ARG3/n_'ARG1/p_0.50/ml_'ARG2_ns_10000_'ARG0_vs2.csv' with 'ARG4 title "p=0.50", 'data/'ARG3/n_'ARG1/p_0.70/ml_'ARG2_ns_10000_'ARG0_vs2.csv' with 'ARG4 title "p=0.70"
#, 'data/'ARG3/n_'ARG1/p_0.90/ml_'ARG2_ns_10000_'ARG0_vs2.csv' with 'ARG4 title "p=0.90"
