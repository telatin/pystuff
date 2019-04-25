SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
TEST="$SCRIPTPATH/test/long-test.depth"

if [ -e "${TEST}.gz" ]; then
	gunzip "${TEST}.gz"
fi

echo "= Python script"
time ./depth2bed.py -i "$TEST" -m 10 -x 1000 -l 5 > "$SCRIPTPATH/test/py_test.bed"
echo "= Perl script"
time cat "$TEST"| ./depth2bed.pl -min 10 -max 1000 -len 5 > "$SCRIPTPATH/test/pl_test.bed"

echo "= Output lines"
wc -l "$SCRIPTPATH/test/py_test.bed" "$SCRIPTPATH/test/pl_test.bed"

echo "= Different _regions_ (cov not tested)"
diff <(cut -f 1-3 "$SCRIPTPATH/test/py_test.bed") <(cut -f 1-3 "$SCRIPTPATH/test/pl_test.bed")

gzip "${TEST}"
rm  "$SCRIPTPATH/test/py_test.bed" "$SCRIPTPATH/test/pl_test.bed"

