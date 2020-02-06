#!/usr/bin/env python3


import sys
import argparse
import pprint
import csv

def eprint(*args, **kwargs):
    """print to STDERR"""
    print(*args, file=sys.stderr, **kwargs)

def vprint(*args, **kwargs):
    if not opt.verbose:
        return 0 
    eprint(*args, **kwargs)

def check_header(ini_array, header_array):
	if not len(ini_array) == 1:
		vprint("Header line should be [Data], but is a CSV line:\n{}".format(ini_array))
		return 0

	if not ini_array[0] == '[Data]':
		vprint("Header line should be [Data]: {} found".format(ini_array[0]))
		return 0

	if (header_array[0] != 'Sample_Name') or (header_array[1] != 'Project_ID'):
		vprint("Wrong fields in header line. Expecting SampleName,Project_ID: {},{} found".format(header_array[0], header_array[1]))
		return 0

	return 1

def get_header():
	if data[0] != None and len(header) >= 3:
		return data[0] + "\n" + ', '.join(header) + "\n"
	else:
		print(data[0])
		eprint("Header should be stored in [data] and [header]")
		exit(1)

opt_parser = argparse.ArgumentParser(description='Split a SampleSheet in smaller chunks')

opt_parser.add_argument('-i', '--input-file',
                        help='SampleSheet in CSV format')

opt_parser.add_argument('-o', '--output-prefix',
                        help='Basename for the resulting samplesheets',
                        default='Chunk_')

opt_parser.add_argument('-s', '--size',
						type=int,
						help="Number of samples per chunk",
						default=50)
 
opt_parser.add_argument('-v', '--verbose',
                        help='Increase output verbosity',
                        action='store_true')


opt = opt_parser.parse_args()


data = []
header = []
if __name__ == '__main__':

	samples = []

	if opt.input_file == None:
		eprint("Please, specify input file with -i FILE")
		exit()




	with open(opt.input_file, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')

		data = next(reader)
		header = next(reader)
		
		if not check_header(data, header):
			eprint("Invalid header found.")
			exit(2)
		
		for row in reader:
			samples.append(row)
		vprint("{} samples found".format(len(samples)))

		file_num = 0
		for start in range(0, len(samples), opt.size):
			file_num += 1
			out_file = open("{}{}.csv".format(opt.output_prefix, file_num), "w") 
			out_file.write(get_header())
			vprint('Printing chunk #{}'.format(file_num))
			for i in range(start, start + opt.size):
				if i >= len(samples):
					break
				out_file.write(','.join(samples[i]) + "\n")
