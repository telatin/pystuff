#!/usr/bin/env python3
import urllib.request, json 
import pprint
import sys
import re

query = 'uminoc'

def data_from_remote_json(url):
    try:
        with urllib.request.urlopen(url) as url:
            json_str = url.read().decode()
            #eprint('[FETCH]\tReceived JSON: {}'.format(len(json_str)))
            return json.loads(json_str)
    except Exception as e:
        eprint('[FETCH] Error {}'.format(url))
        return {}

def get_analyses(study_id):
    url = "https://www.ebi.ac.uk/metagenomics/api/v1/studies/{}/analyses".format(study_id)
    data = data_from_remote_json(url)
    return data['data']

def print_taxonomy(url, query, char=''):
    data = data_from_remote_json(url)
    lines = ''
    for taxon in data['data']:
        if re.search(query, taxon['id']):
            lines += ' {}- {}\n'.format(char, taxon['id']) 
    return lines

def print_analyses(study_id):
    data = get_analyses(study_id)
    for exp in data:
        taxurl = exp['relationships']['taxonomy-ssu']['links']['related'];
        #taxurl = 'https://www.ebi.ac.uk/metagenomics/api/v1/analyses/{}/taxonomy'.format(exp['attributes']['accession'])
        if exp['attributes']['experiment-type'] == 'metagenomic':
            lines   = print_taxonomy(exp['relationships']['taxonomy']['links']['related'], query)
            sulines = print_taxonomy(taxurl, query, '-')
            if len(lines) > 0 or len(sulines) > 0:
                print('## {}\t{}\t{}\t{}'.format(exp['attributes']['accession'],exp['attributes']['experiment-type'],exp['attributes']['instrument-platform'], taxurl))
                print(lines)
                print(sulines)
            
            

def get_biomes(study_id):
    biomes = {}
    biome_string = ''
    url = "https://www.ebi.ac.uk/metagenomics/api/v1/studies/{}/biomes".format(study_id)
    data = data_from_remote_json(url)
    if 'data' in data:
        for attr in data['data']:
            biome = attr['attributes']['biome-name']
            biome_string += '{};'.format(attr['attributes']['biome-name'])
            if biome in biomes:
                biomes[biome] += 1
            else:
                biomes[biome] = 1
        return biome_string
    else:
        eprint('Unexpected data: get_biome({}) failed'.format(study_id))
        return {}

def eprint(*args, **kwargs):
    """print to STDERR"""
    print(*args, file=sys.stderr, **kwargs)    



#print_analyses('MGYS00001868');
#exit();

# DOWNLOADED 3000 human records:

#curl -X GET "https://www.ebi.ac.uk/metagenomics/api/v1/studies" -H "accept: application/json"
 
url = "https://www.ebi.ac.uk/metagenomics/api/v1/studies?page_size=3000&biome_name=Human"

data = {}
try:
    # LOAD FROM FILE
    with open('human.json', encoding='utf-8') as json_file:  
        data = json.load(json_file)
except Exception as e:
    # LOAD FROM URL + SAVE TO FILE
    eprint('Getting data from APIs: human.json not found')
    with urllib.request.urlopen(url) as url:
        json_str = url.read().decode()
        eprint('Received JSON: {}'.format(len(json_str)))
        data = json.loads(json_str)
        try:
            eprint('saving to file')
            with open('human.json', "w") as json_file:
                print(json_str, file=json_file)
        except Exception as write_e:
            eprint("Unable to write to JSON file")


         
for datum in data['data']:
    accession  = datum['attributes']['accession']
    bioproject = datum['attributes']['bioproject']
    samples    = datum['attributes']['samples-count']
    biomes     = get_biomes(accession)

    if re.search('(Fecal|Digestive|Intestine)', biomes):
        eprint('-- skipping {}: biome is {}'.format(accession, biomes))
    else:
        eprint('OK getting {}: biome is {}'.format(accession, biomes))
        header = '# {} ({}, {} samples)\nBiomes: {}'.format(accession, bioproject, samples, biomes )
        print(header)
        
        print_analyses(accession)
       
        print('')

