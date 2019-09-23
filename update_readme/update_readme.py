#!/usr/bin/env python3
import os
from pathlib import Path
import pprint
import sys
# A script to produce ../README.md
# uses a template in the script directory: TEMPLATE.md
# parses all directory in ../ and:
#    ignores directory if .ignore_readme found
#    looks for title and first paragraph of README.md

ignore_file = '.ignore_readme'
template    = 'TEMPLATE.md'


def eprint(*args, **kwargs):
	"""print to STDERR"""
	print(*args, file=sys.stderr, **kwargs)


def get_abstract(filename):
    with open(filename, 'r') as content_file:
        this_readme = content_file.read()
        answer = '#'
        whitelines = 0
        link = " [more...]({})".format(filename)
        try:
            for line in this_readme.splitlines():
                answer = answer + line + '\n'
                if len(line)==0:
                    whitelines += 1
                if whitelines > 1:
                    return answer + link + '\n'
        except Exception as e:
            eprint("Readme not found for {}".format(filename))
            return ''



path = os.path.dirname(os.path.realpath(__file__))
parent = path + '/../'
output_file = open(parent + '/README.md', 'w')

# Check for template
if not Path(path + '/' + template).exists():
    eprint("Unable to locate template file: {}/{}".format(path, template))
    exit(1)
else:
    with open(path + '/' + template, 'r') as content_file:
        template = content_file.read()

new_readme = template

print('Script dir: {}'.format(path))
files = os.listdir(parent)

# Foreach file in parent [= .. (git repository root) ]
for file in files:
    # if it's a directory and not hidden
    if os.path.isdir(file) and not file[0]=='.':
        # and it has not a .ignore_readme file
        readme = file + '/README.md'
        if not Path(file + '/' + ignore_file).exists() and Path(readme).exists():
            print('Processing: '+ file)
            new_readme += get_abstract(readme)

eprint(new_readme)
output_file.write(new_readme)
# walk = os.walk(path + '/../')
#
# for dir in walk:
#     print('---')
#     pprint.pprint(dir)
