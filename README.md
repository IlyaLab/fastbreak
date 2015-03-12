# fastbreak
Automatically exported from code.google.com/p/fastbreak

Fastbreak is an rule based O(n) algorithm for detecting translocations and other genetic structural variants from aligned mate pair sequence data in SAM/BAM format. It is primarily of use as a coarse screen or prefilter for structural variation in studies where the amount of data prevents other methods from finishing in a reasonable amount of time. It is implemented here in python (2.5-2.7) but is simple enough to quickly port to other languages including distributed database query languages.

This project also includes scripts in python and R for data QA and downstream analysis of the detected structural variation, visualizations in javascript and a web application for presenting the results. It was developed in the Ilya lab at the Institute for Systems Biology as part of The Cancer Genome Atlas and has been published here.

To run an analysis you will need samtools, python 2.5-2.7 and a system that supports command line pipes ("|") (we have tested on linux and os x).

To run with default pramaters grab the fastbreak scripts and config and edit "ResultsRelativePath?" in the config to your desired output dir (additional paramaters can be found here)

Run pass 1 to parse and filter the bam to identify to "odd" reads:

samtools view -h XXX.sorted.bam | python findtrans.py sample-label myConfig.config
(This will produce filtered "oddreads.list" and "oddreads.bed", coverage "wig", .cov and disance (a list of all mate pair distance) files which can be used for making additional plots. The "bed" and "wig" files can be viewed in a genome browser like IGV.

To run pass 2 which applies rules to identify the likely SVs for each "oddreads.list" file in the results dir run:

python makeCalls.py sample-label.oddreads.list
Which will generate a "called" file of likely SVs and "distance" files which can be used to plot distributions of read pair distances.

The called file is a tsv of the form:

starChromsome   startPos        endChr  endPos  type    readCount       score
Start and end position will be rounded based on the bin size used. Type will be a field like 01 or 11 indicating the orientation of the two reads as in the orientation flags in bam files. Score is based on a probabilistic interpretation of the supporting read scores.

Further documentation including documentation of additional parameters is provided at the start of findtrans.py and in other scripts.

Developers interested in porting fastbreak or adapting it for use as part of their methods will find parsing and initial filtering logic (ie identifying reads that are oddly oriented or separated by more then 1000 base pairs) in findtrans.py and logic for identifying groups of odd reads that likely represent SVs in makeCall.py.

For more information, please contact codefor@systemsbiology.org.



The project described was supported by Award Number U24CA143835 from the National Cancer Institute. The content is solely the responsibility of the authors and does not necessarily represent the official views of the National Cancer Institute or the National Institutes of Health.
