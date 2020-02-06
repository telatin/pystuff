# split_samplesheet

Split a SampleSheet (for IRIDA) into chuncks to simplify the upload process.

### Usage

```
usage: split_samplesheet.py [-h] [-i INPUT_FILE] [-o OUTPUT_PREFIX] [-s SIZE]
                            [-v]

Split a SampleSheet in smaller chunks

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        SampleSheet in CSV format
  -o OUTPUT_PREFIX, --output-prefix OUTPUT_PREFIX
                        Basename for the resulting samplesheets
  -s SIZE, --size SIZE  Number of samples per chunk
  -v, --verbose         Increase output verbosity

```
