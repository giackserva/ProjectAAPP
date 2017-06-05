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
if ('$5' eq 'y') {
  set terminal png enhanced;
  set output "data/images/n_$1/ml_$2_ns_10000_$0.png";
}
set xlabel "N"
set ylabel "t"
set title "Average $0 time at various number of nodes and p with 10'000 samples"
set grid

plot '$3/n_$1/p_0.10/ml_$2_ns_10000_$0_vs2.csv' using 1:2 with $4 title "p=0.10", '$3/n_$1/p_0.30/ml_$2_ns_10000_$0_vs2.csv' using 1:2 with $4 title "p=0.30", '$3/n_$1/p_0.50/ml_$2_ns_10000_$0_vs2.csv' using 1:2 with $4 title "p=0.50", '$3/n_$1/p_0.70/ml_$2_ns_10000_$0_vs2.csv' using 1:2 with $4 title "p=0.70", '$3/n_$1/p_0.90/ml_$2_ns_10000_$0_vs2.csv' using 1:2 with $4 title "p=0.90"
