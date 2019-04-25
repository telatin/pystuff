if [ ! -e "test/mini-test.depth" ]; then
	echo "<<Run from script dir>>"
	exit
fi
echo "=Input"
cat test/mini-test.depth
echo "=Perl"
grep -v '#' test/mini-test.depth | ./depth2bed.pl -min 10 -max 100 -len 3 > test/mini.perl.bed
echo "=Python"
./depth2bed.py -i test/mini-test.depth -m 10 -x 100 -l 3 > test/mini.py.bed

wc -l test/mini.perl.bed test/mini.py.bed 
diff  <(cut -f 1-4 test/mini.perl.bed) <(cut -f 1-4 test/mini.py.bed)

rm  test/mini.perl.bed test/mini.py.bed 

