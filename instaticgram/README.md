# Instatigram

![Alpha release](https://img.shields.io/badge/Release-ALPHA-red.svg)

A script to convert the _Instagram_ backup (a set of photos and JSON files) into a static website (see [my example gallery](https://telatin.com/pics/instagram)).

This is currently a working *prototype*.

```
usage: instaticgram.pl -d BACKUP_DIR [ -t "gallery title" ]

```

## How to use the script

1. Get your Instagram backup from your settings/privacy page (see [instructions](https://smartphones.gadgethacks.com/how-to/instagram-101-download-backup-your-account-save-photos-comments-more-0184403/) if needed)
1. Create a directory (we'll refere to that as `$BACKUP_DIR` and expand your downloaded backup (it comes as a ZIP file).
1. At the moment it's necessary to manually generate the thumbnails. I used ImageMagik (see below), in any case the goal is to produce for each _filename.jpg_ a thumbnail called _small\_filename.jpg_, in the same directory. 
1. Run the script

### Example
```
cd $BACKUP_DIR
for i in $(find -name "*.jpg");
  do convert -resize 300x300 "$i" "$(dirname $i)/small_$(basename $i)"
done

python instaticgram.py -d ./ -t "My memories from Instagram"

```

## Output

The script will create an `./html` directory within `$BACKUP_DIR`, with:
1. An *index.html* file, with a thumbnail for each month
1. A *{YEAR}{MONTH}.html* page for each month, with the full gallery of that month (same template as *index.html*)
1. A page for each photo (in full size)

