#!/usr/bin/env python3
import argparse
import pprint
import sys


def eprint(*args, **kwargs):
	"""print to STDERR"""
	print(*args, file=sys.stderr, **kwargs)	


def print_buffer(chrname, start, end, covarray):
    if not chrname == None and (end-start)>=opt.minlen:
        avg = mean(covarray)
        print('{}\t{}\t{}\tAVG={:0.5f}'.format(chrname, start, end, avg))
 
    
    
opt_parser = argparse.ArgumentParser(description='"MGnify query tools')

subparsers = opt_parser.add_subparsers()
subparsers.required = True
subparsers.dest = 'command'
subparser = subparsers.add_parser("studies", help="retrieve a list of studies")
subparser = subparsers.add_parser("samples", help="retrieve a list of samples given some studies")

opt_parser.add_argument('-a', '--ref',
                        help='Reference FASTA',
                        required=False)


opt_parser.add_argument('-m', '--mincov',
                        help='Minimum coverage [1]',
                        type=int,
                        default=1)


opt_parser.add_argument('-v', '--verbose',
                        help='Increase output verbosity',
                        action='store_true')


opt = opt_parser.parse_args()

pprint.pprint(subparsers)


exit();
line_no   = 0
chr_start = None
pos_start = None
pos_end   = None
cov_array = []

if opt.ref:
    chromosomes = get_fasta_chromosomes(opt.ref)
    if len(chromosomes)<1:
        eprint("Error: {} file has no FASTA sequences".format(opt.ref))
        exit(1)

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

    if opt.ref and not cols[0] in chromosomes:
        eprint("Line {} error: {} was not found in (--ref) {}".format(line_no, cols[0], opt.ref))
        exit(2) 
        
    if chr_start != None and cols[0] != chr_start:
        print_buffer(chr_start, pos_start, pos_end, cov_array)
        chr_start = None
        pos_start = None
        pos_end = None
        cov_array = []
        
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
