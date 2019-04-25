#!/usr/bin/env python3
import argparse
import pprint
import sys
from statistics import mean 

def eprint(*args, **kwargs):
	"""print to STDERR"""
	print(*args, file=sys.stderr, **kwargs)	


def print_buffer(chrname, start, end, covarray):
    if not chrname == None and (end-start)>=opt.minlen:
        avg = mean(covarray)
        print('{}\t{}\t{}\tAVG={:0.5f}'.format(chrname, start, end, avg))
    
opt_parser = argparse.ArgumentParser(description='"samtools depth" to bed')

opt_parser.add_argument('-r', '--ref',
                        help='Reference FASTA',
                        required=False)
opt_parser.add_argument('-i', '--input',
                        type=argparse.FileType('r'),
                        help='"samtools depth" output file',
                        required=True)
opt_parser.add_argument('-m', '--mincov',
                        help='Minimum coverage [1]',
                        type=int,
                        default=1)
opt_parser.add_argument('-x', '--maxcov',
                        help='Maximum coverage [10000]',
                        type=int,
                        default=10000)
opt_parser.add_argument('-l', '--minlen',
                        help='Minimum feature length [1]',
                        type=int,
                        default=1)
opt_parser.add_argument('--skiperrors',
                        help='Skip bad formatted lines, without exiting',
                        action='store_true'   )                    
opt_parser.add_argument('-v', '--verbose',
                        help='Increase output verbosity',
                        action='store_true')


opt = opt_parser.parse_args()

line_no   = 0
chr_start = None
pos_start = None
pos_end   = None
cov_array = []
for line in opt.input.readlines():
    #$chromosome_name, $position, $coverage
    line_no += 1
    if line[0]=='#':
        continue
    cols = line.rstrip().split('\t')

    if len(cols) < 3:
        eprint('Line {} error: less than 3 cols and no #comment:\n{}'.format(line_no,line))
        if not opt.skiperrors:
            exit(1)
        continue

    try:
        pos = int(cols[1])
        cov = int(cols[2])
    except Exception as e:
        print('Line {} error: Columns 2 and 3 (Position and coverage) must be INT:\n{}'.format(line_no,line))
        if not opt.skiperrors:
            exit(2)
        continue

    if chr_start != None and cols[0] != chr_start:
        print_buffer(chr_start, pos_start, pos_end, cov_array)
        chr_start = None
        pos_start = None
        pos_end = None
        
    if cov >= opt.mincov and cov < opt.maxcov:
        
        if chr_start == None:
            chr_start = cols[0]
            pos_start = pos-1
        pos_end = pos
        cov_array.append(cov)     
    else:
        print_buffer(chr_start, pos_start, pos_end, cov_array)
        chr_start = None
        pos_start = None
        pos_end = None
        cov_array = []
        
print_buffer(chr_start, pos_start, pos_end, cov_array)
