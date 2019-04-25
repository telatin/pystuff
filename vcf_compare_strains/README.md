# Compare multiple VCFs

This script is made to compare VCFs produced by SNIPPY (one VCF per sample), where one is a "reference" strain and all the others are derived from it.

The goal is to identify mutations in derived strains not present in the reference strain.

```
usage: vcf_compare_strains.py [-h] -r REF [--minqual MINQUAL]
                              [--mincov MINCOV] [--maxcov MAXCOV] [-v]
                              vcffiles [vcffiles ...]

```

This script is under development and the output is currently for debug purposes only:
 
| SNP              | Samples  | Reference     | Other samples                       | 
|------------------|---|-----|------------------------| 
| =U00096:3645:G   | 2 | [A] | sample1[A]             | 
| =U00096:71170:T  | 3 | [C] | sample1[C] sample2[C]  | 
| =U00096:81044:C  | 3 | [T] | sample1[T] sample2[T]  | 
| =U00096:81102:G  | 3 | [A] | sample1[A] sample2[A]  | 
| =U00096:85203:C  | 3 | [T] | sample1[T] sample2[T]  | 
| =U00096:154182:C | 3 | [T] | sample1[T] sample2[T]  | 
| =U00096:156068:A | 3 | [G] | sample1[G] sample2[G]  | 
| =U00096:223560:T | 3 | [A] | sample1[A] sample2[A]  | 
| =U00096:246985:C | 3 | [T] | sample1[T] sample2[T]  | 
| =U00096:284535:T | 3 | [G] | sample1[G] sample2[G]  | 
| =U00096:292019:C | 3 | [T] | sample1[T] sample2[T]  | 
| =U00096:309381:C | 3 | [T] | sample1[T] sample2[T]  | 
| =U00096:309985:T | 3 | [A] | sample1[A] sample2[A]  | 
| =U00096:366551:G | 1 | [T] |                        | 
| =U00096:366677:G | 1 | [A] |                        | 
| *U00096:367510:C | 1 | [?] | sample1[T]             | 
| =U00096:402007:C | 3 | [T] | sample1[T] sample2[T]  | 
| =U00096:410666:C | 2 | [T] | sample2[T]             | 

 SNPs marked as "=" are found both in the _reference_ strain and in the _derived_ strains.
 
 SNPs marked as "\*" are different in the _derived_ strain, if compared with the _reference strains_
