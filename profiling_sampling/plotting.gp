# Arguments
# - insert/search/delete
# - type of skiplist (0/1/2)
# - max level of the skiplist
# - data folder
# - lines/points
# - y/n to choose if to export to png
# Example of call inside gnuplot
# call "plotting.gp" "samples2" "1" "insert"

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
set title "Average ARG1 time with skiplist with various number of nodes and p"
set grid

f1 = sprintf("data/%s/n_%s/p_0.10/%s_vs2.csv", ARG1, ARG2, ARG3)
f2 = sprintf("data/%s/n_%s/p_0.20/%s_vs2.csv", ARG1, ARG2, ARG3)
f3 = sprintf("data/%s/n_%s/p_0.30/%s_vs2.csv", ARG1, ARG2, ARG3)
f4 = sprintf("data/%s/n_%s/p_0.40/%s_vs2.csv", ARG1, ARG2, ARG3)
f5 = sprintf("data/%s/n_%s/p_0.50/%s_vs2.csv", ARG1, ARG2, ARG3)
f6 = sprintf("data/%s/n_%s/p_0.60/%s_vs2.csv", ARG1, ARG2, ARG3)
f7 = sprintf("data/%s/n_%s/p_0.70/%s_vs2.csv", ARG1, ARG2, ARG3)
f8 = sprintf("data/%s/n_%s/p_0.80/%s_vs2.csv", ARG1, ARG2, ARG3)
f9 = sprintf("data/%s/n_%s/p_0.90/%s_vs2.csv", ARG1, ARG2, ARG3)

plot f1 with lines, f2 with lines, f3 with lines, f4 with lines, f5 with lines, f6 with lines, f7 with lines, f8 with lines, f8 with lines, f9 with lines

#plot 'data/', ARG3, '/n_', ARG1, '/p_0.10/ml_', ARG2', '_ns_10000_', ARG0, '_vs2.csv'
#using 1:2 with 'ARG4 title "p=0.10", 'data/'ARG3/n_'ARG1/p_0.30/ml_'ARG2_ns_10000_'ARG0_vs2.csv' using 1:2 with 'ARG4 title "p=0.30", 'data/'ARG3/n_'ARG1/p_0.50/ml_'ARG2_ns_10000_'ARG0_vs2.csv' using 1:2 with 'ARG4 title "p=0.50", 'data/'ARG3/n_'ARG1/p_0.70/ml_'ARG2_ns_10000_'ARG0_vs2.csv' using 1:2 with 'ARG4 title "p=0.70", 'data/'ARG3/n_'ARG1/p_0.90/ml_'ARG2_ns_10000_'ARG0_vs2.csv' using 1:2 with 'ARG4 title "p=0.90"
#plot 'data/'ARG3/n_'ARG1/p_0.10/ml_'ARG2_ns_10000_'ARG0_vs2.csv' with 'ARG4 title "p=0.10", 'data/'ARG3/n_'ARG1/p_0.30/ml_'ARG2_ns_10000_'ARG0_vs2.csv' with 'ARG4 title "p=0.30", 'data/'ARG3/n_'ARG1/p_0.50/ml_'ARG2_ns_10000_'ARG0_vs2.csv' with 'ARG4 title "p=0.50", 'data/'ARG3/n_'ARG1/p_0.70/ml_'ARG2_ns_10000_'ARG0_vs2.csv' with 'ARG4 title "p=0.70"
#, 'data/'ARG3/n_'ARG1/p_0.90/ml_'ARG2_ns_10000_'ARG0_vs2.csv' with 'ARG4 title "p=0.90"