# Samtools Depth 2 Coverabe (BED)

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
