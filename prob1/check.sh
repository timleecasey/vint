

python print_tree_2.py > log


N=10
for i in $(seq 2 8) ; do
    echo "N: $N M: $i"
    grep -A${N} "N:${N} M:${i}" log | grep -v '^#' | grep -v -e '->' | sort | uniq -c
done
