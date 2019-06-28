#!/usr/bin/env python3

# ALPHA RELEASE

import argparse
import json
import os
import pprint
from html import escape
import re 

month_names = {
  '01' : 'January',
  '02' : 'February',
  '03' : 'March',
  '04' : 'April',
  '05' : 'May',
  '06' : 'June',
  '07' : 'July',
  '08' : 'August',    
  '09' : 'September',
  '10' : 'October',    
  '11' : 'November',
  '12' : 'December',    
}

def thumbnail_filename(path):
    '''Return the name of the thubmnail given the path to the original image'''
    directory = os.path.dirname(path)
    filename  = os.path.basename(path)
    return directory + '/small_' + filename;

def caption_html(string):
    '''Clean the caption string (removing wide chars)'''
    re.sub(r"(?<!\\)\\n|\n", "<br>", string)
    string  = ''.join(c for c in string if ord(c) <= 1000)
    return escape(string)
    

def get_html_header(title = 'Picture Gallery'):
    '''This is a temporary function returning the header of each HTML page. TODO: Better templating '''
    template =  '''<!DOCTYPE html>
    <html>
<head>
<style>
    * {font-family: Helvetica; }
    h1,h2,h3 { text-align: center; }
    h2 {margin-top: 18px; }
    h3, h4 {margin-bottom: 0px; margin-top: 0px; }

    img.center {
    display: block;
    margin-left: auto;
    margin-right: auto;
    }

    div.gallery {
      margin: 5px;
      border: 1px solid #ccc;
      float: left;
      width: 300px;
      height: 390px;
    }

    div.gallery:hover {
      border: 1px solid #777;
    }

    div.gallery img {
      width: 100%;
      height: auto;
    }

    div.desc {
      font-size: 0.9em;
      padding: 15px;
      text-align: center;
    }
    a:link,a:visited {
        color: black;
        text-decoration: none;
    }
    a:hover {
        color: red;
    }
    .button {
      background-color: #F0E088; /* Green */
      border: none;
      color: white;
      padding: 20px;
      text-align: center;
      text-decoration: none;
      display: inline-block;
      font-size: 16px;
      margin: 4px 2px;
      cursor: pointer;
      border-radius: 8px;
    }
    .single { 
      border: 8px solid black;
      padding: 15px;
    }
</style>'''
    template += '<title>{}</title>\n</head>\n'.format(title)
    return template    

# Get command line arguments
opt_parser = argparse.ArgumentParser(description='Instagram dump to HTML')

opt_parser.add_argument('-d', '--dir',
                        help='Path to the dump directory (that should contain media.json)',
                        required=True)

opt_parser.add_argument('-t', '--title',
                        help='Main gallery title',
                        default='My Instagram Memories')

opt = opt_parser.parse_args()

# Check input
if not os.path.isdir(opt.dir):
    print("Please, specify the directory created unzipping the dump archive as input with -d DIRNAME")
    print("('{}' is not a valid directory)".format(opt.dir))
    exit(1)

# Check directory structure
if not os.path.isdir(opt.dir + '/photos'):
    print("ERROR:");
    print("Please, specify the directory created unzipping the dump archive as input with -d DIRNAME")
    print("The specified directory ({}) does not contain the requested subdirectory 'photos'.".format(opt.dir))
    exit(1)    

# Create output directory
outdir = opt.dir +'/html';
if not os.path.isdir(outdir):
    try:
        os.mkdir( outdir )
    except OSError as exc:
        raise

# Read JSON media in ''descriptions''
try:
    with open(opt.dir + '/media.json', encoding='utf-8') as json_file:  
        descriptions = json.load(json_file)
except Exception as e:
    print("FATAL ERRO: Unable to locate {}/media.json".format(opt.dir))
    exit(1)

# Initialize structure
files = {}
htmls = {}
index = get_html_header(opt.title);
index += '<h1>{}</h1>\n<ul>'.format(opt.title)


# Loop through descriptions
for insta_picture in descriptions['photos']:
    date = insta_picture['path'].split('/')
    if len(insta_picture['caption']) < 1:
        insta_picture['caption'] = 'A picture...'
    #year = date[1][0:4]
    #month = date[1][4:6]
    if not date[1] in files:
        files[date[1]] = []
        htmls[date[1]] = ''
    # files[022019] = array of pairs ( [path, desc], [path, desc] ....)

    if os.path.isfile(insta_picture['path']):
       files[date[1]].append([ insta_picture['path'], caption_html(insta_picture['caption']) ])

h2 = {}
counter = 0
for date in reversed(sorted(files)):
    year = date[0:4]
    month = month_names[date[4:6]]
    if year in h2:
        h2[year] += 1
    else:
        h2[year] = 1
        index += '<div style="clear: both;">&nbsp;<h2>{}</h2></div>\n'.format(year)

    monthly_gallery_html = get_html_header('{} {} - {}'.format(month_names[date[4:6]], year, opt.title)) ;
    monthly_gallery_html = monthly_gallery_html + '<button class="button"><a href="instagram.html">back</a></button><h1>{} {}</h1>'.format(month_names[date[4:6]], year)
    pprint.pprint(files[date])

    photo_counter = 0
    first_pic = ''
    for array in files[date]:
        counter += 1
        [filepath, description] = array
        single_page_filename = "{}/{}.html".format(outdir, counter)
        photo_counter += 1

        if photo_counter == 1:
            first_pic = filepath
        
        monthly_gallery_html = monthly_gallery_html + '''
        <div class="gallery">
              <a href="{}.html">
                <img src="../{}" alt="{}" width="800" height="800">
              </a>
         <div class="desc">{}</div>
        </div>\n'''.format(counter,thumbnail_filename(filepath), description, description)

        with open( single_page_filename, "w") as single_page:
            print('{}<body><button class="button"><a href="{}.html">back</a></button><br><h1>{}</h1><h2>{} {}</h2><br><img class="center single" src="../{}"><br><p class="center">&copy; <a href="https://www.telatin.com/">AT</a> 2019</p>'.format(
                get_html_header(description), 
                date, 
                description, 
                month_names[date[4:6]], 
                year, 
                filepath), file=single_page)

    plural = ''
    if photo_counter > 1:
        plural = 's'


    index += '''
        <div class="gallery">
              <a href="{}.html">
                <img src="../{}" alt="{}" width="800" height="800">
              </a>
         <div class="desc"><h3>{} {}</h3><br>{} photo{}</div>
        </div>\n'''.format(date, thumbnail_filename(first_pic), date, month_names[date[4:6]], year, photo_counter, plural)


    
    monthly_gallery_html = monthly_gallery_html + '\n</ul>\n';    
    
    with open(outdir + '/' + date + '.html', "w") as text_file:
        print(monthly_gallery_html, file=text_file)

index += '\n</ul></body></html>'
with open(outdir + '/instagram.html', "w") as text_file:
        print(index, file=text_file)


