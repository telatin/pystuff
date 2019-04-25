#!/usr/bin/env python3
import vcf
import pprint
import argparse
from pathlib import Path
import sys
import os.path

opt_parser = argparse.ArgumentParser(description='Create a BED file from coverage')

opt_parser.add_argument('-r', '--ref',
                        help='Reference VCF',
                        required=True)
opt_parser.add_argument('vcffiles',
                        type=str,
                        nargs='+',
                        help='VCF files to parse')
opt_parser.add_argument('--minqual',
                        help='Minimum quality for variant',
                        type=float,
                        default=0)
opt_parser.add_argument('--mincov',
                        help='Minimum coverage for variant',
                        type=int,
                        default=0)
opt_parser.add_argument('--maxcov',
                        help='Maximum coverage for variant',
                        type=int,
                        default=1000)
opt_parser.add_argument('-v', '--verbose',
                        help='Increase output verbosity',
                        action='store_true')


opt = opt_parser.parse_args()
stats = {}
variants = {}
samples = []

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def check_files(filenames):
    errors = 0
    for file in filenames:
        file = Path(file)
        if not file.is_file():
            eprint("ERROR: File <{}> is not a file.".format(file))
            errors += 1
    if errors > 0:
        return 0
    else:
        return 1


def counter(stats, key, label):
    if key in stats:
        if label in stats[key]:
            stats[key][label] += 1
        else:
            stats[key][label] = 0
    else:
        stats[key] = {label: 0}


def add_variant(variants, sample, variant):
    if not variant.CHROM in variants:
        variants[variant.CHROM] = { variant.POS :   {'_reference': variant.REF, 'count': 0 } }

    if not variant.POS in variants[variant.CHROM]:
        variants[variant.CHROM][variant.POS] = {'_reference': variant.REF, 'count': 0 }


    if not sample in variants[variant.CHROM][variant.POS]:
        variants[variant.CHROM][variant.POS][sample] = variant.ALT[0]
        variants[variant.CHROM][variant.POS]['count'] += 1


def parse_vcf(vcf_reader, variants, stats, label):
    if not isinstance(variants, dict):
        eprint('[parse_vcf] expects a "variants" dictionary')
        return 0
    if not isinstance(stats, dict):
        eprint('[parse_vcf] expects a "stats" dictionary')
        return 0

    for record in vcf_reader:
        if record.QUAL < opt.minqual:
            counter(stats, label, 'low_qual')
            continue
        if 'DP' in record.INFO:
            if record.INFO['DP'] < opt.mincov or record.INFO['DP'] > opt.maxcov:
                counter(stats, label, 'bad_cov')
                continue
        else:
            eprint('DP not found in {} [{}]'.format(label, record.INFO['DP']))

        #print('{}\t{}:{}\t{}^{} '.format(label,record.CHROM, record.POS, record.REF, record.ALT))
        #pprint.pprint(record.samples[0]['GT'])
        add_variant(variants, label, record)


# Check VCF files are found
if not check_files([opt.ref]+ opt.vcffiles):
    eprint('Exiting: one or more files were not found (see above)')
    exit(1)


# Parse Reference
try:
    vcf_reader = vcf.Reader(open(opt.ref, 'r'))
    parse_vcf(vcf_reader, variants, stats, 'ref')
except Exception as e:
    pprint.pprint(e)
    eprint('ERROR: Reference VCF "{}" is not readable or is a valid VCF file:\n > {}'.format(opt.ref, e))
    exit(2)


for vcf_file in opt.vcffiles:
    base = os.path.splitext(os.path.basename(vcf_file))
    samples.append(base[0])
    try:
        vcf_reader = vcf.Reader(open(vcf_file, 'r'))
        parse_vcf(vcf_reader, variants, stats, base[0])
    except Exception as e:
        eprint('ERROR: input VCF "{}" is not readable or is a valid VCF file:\n > {}'.format(vcf_file, e))
        exit(3)

for chr in variants:
    for pos in sorted(variants[chr]):
        var = variants[chr][pos]
        diff=0
        vars = ''

        if not 'ref' in var:
            counter(stats, 'global','no_in_ref')
            vars += '[?]\t'
            var['ref'] = var['_reference']
        else:
            vars += '[{}]\t'.format(var['ref'])
        for sample in samples:
            if sample in var:
                vars += '{}[{}] '.format(sample, var[sample])
                if var[sample] != var['ref']:
                    diff += 1

        if diff > 0:
            counter(stats, 'global', 'passed_vars')
            print("*{}:{}:{}\t{}\t{}".format(chr, pos, var['_reference'], var['count'], vars))
        else:
            counter(stats, 'global', 'children_like_ref')
            print("={}:{}:{}\t{}\t{}".format(chr, pos, var['_reference'], var['count'], vars))
            #pprint.pprint(var)