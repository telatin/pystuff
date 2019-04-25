# Samtools Depth 2 Coverage (BED)

A tool to produce a bed file from the output of 'samtools depth [-a]'

```
usage: depth2bed.py [-h] [-r REF] -i INPUT [-m MINCOV] [-x MAXCOV] [-l MINLEN]
                    [--skiperrors] [-v]

"samtools depth" to bed

optional arguments:
  -h, --help            show this help message and exit
  -r REF, --ref REF     Reference FASTA
  -i INPUT, --input INPUT
                        "samtools depth" output file
  -m MINCOV, --mincov MINCOV
                        Minimum coverage [1]
  -x MAXCOV, --maxcov MAXCOV
                        Maximum coverage [10000]
  -l MINLEN, --minlen MINLEN
                        Minimum feature length [1]
  --skiperrors          Skip bad formatted lines, without exiting
  -v, --verbose         Increase output verbosity

```
Example input (generated with _samtools depth -a BAMFILE_):
```
#Comment
A00011	1	0
A00011	2	0
A00011	3	0
A00011	4	10
A00011	5	20
A00011	6	30
A00011	7	0
A00011	8	0
A00011	9	0
A00011	10	17
A00011	11	17
A00011	12	17
A00011	13	17
A00011	14	17
A00011	15	17
A00011	16	17
U00096	4	20
U00096	5	25
U00096	6	30
U00096	7	0
U00096	8	0
U00096	9	0
U00096	10	17
U00096	11	17
U00096	12	17
U00096	13	17
U00096	14	17
U00096	15	17
U00096	16	17
```

Example output (depth2cov.py --mincov 10 --maxcov 100 --len 5 -i INPUTFILE)
```
A00011	3	6	AVG=20.00000
A00011	9	16	AVG=17.00000
U00096	3	6	AVG=25.00000
U00096	9	16	AVG=17.00000
```
