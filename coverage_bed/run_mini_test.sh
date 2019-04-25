PASS=0
ERR=0

echo "# Will perform 5 tests"
if [ ! -e "test/mini-test.depth" ]; then
	echo "<<Run from script dir>>"
	exit
fi
grep -v '#' test/mini-test.depth | ./depth2bed.pl -min 10 -max 100 -len 3 > test/mini.perl.bed
./depth2bed.py -i test/mini-test.depth -m 10 -x 100 -l 3 > test/mini.py.bed

if [ $? -eq 0 ]; then
	echo "OK: Python script executed"
	PASS=$((PASS+1))
else
	echo "NOT OK: Program failed"
fi
./depth2bed.py --ref test/mini-test.fa -i test/mini-test.depth -m 10 -x 100 -l 3 > test/mini.py.bed
if [ $? -eq 0 ]; then
	echo "OK: Python script executed with reference check"
fi

./depth2bed.py --ref test/mini-test-wrong.fa -i test/mini-test.depth -m 10 -x 100 -l 3 > /dev/null
EXIT=$?
if [ $EXIT -gt 0 ]; then
	PASS=$((PASS+1))
	echo "OK: Python script executed with WRONG reference check ($EXIT: should be A00011 not found)"
else
	echo "NOT OK: Expected fail"
fi


WC1=$(cat test/mini.perl.bed|wc -l)
WC2=$(cat test/mini.py.bed |wc -l)
if [[ "$WC1" -eq "4" ]]; then
	PASS=$((PASS+1))
	echo "OK: Perl printed 4 features"
fi
if [[ "$WC2" -eq "4" ]]; then
	PASS=$((PASS+1))
	echo "OK: Python Script printed 4 features"
else
	echo "NOT OK: Python printed $WC2 lines, 4 expected"
fi


diff  <(cut -f 1-4 test/mini.perl.bed) <(cut -f 1-4 test/mini.py.bed)
EXIT=$?
if [ $? -eq 0 ]; then
	PASS=$((PASS+1))
	echo "OK: Perl and Python print same output"
else
	echo "NOT OK: Perl and Python do not print same output"
fi

echo "$PASS/5 test passed"
rm  test/mini.perl.bed test/mini.py.bed 
if [[ $PASS -lt 5 ]];then
	exit 1
fi

