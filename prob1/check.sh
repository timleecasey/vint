

echo "RUN"
python print_tree_2.py > log

rm check_out

echo "CHECK"
for N in $(seq 5 100) ; do
    echo "N: ${N}"
    for i in $(seq 4 10) ; do
        echo "N: $N M: $i" >> check_out
        grep -A${N} "N:${N} M:${i}" log | grep -v '^#' | grep -v -e '->' | sort | uniq -c >> check_out
    done
done

echo "Check errors"

grep -v -e '--' check_out  | grep -v '^N: '
