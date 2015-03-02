# BAMZINGA

Creates a file of read counts using a gff file from the genome and a BAM file of alignment.
This script was created due to the need of a counter different from bedtools or HTSeq counts. It takes into acount the need of count as one, the reads that map into different exons, of the same gene, at the same time.
The output of this script can be easly submited to different softwares to calculate differentially expressed genes.

##Usage:

In the command line:

<pre><code>python bamzinga.py [gff file] [sorted bam file] [outputfile]
</code></pre>

##Dependencies:
+ Python2
+ Bam file of the alignment, sorted (see [Samtools](http://www.htslib.org/) for that task);
+ gff of the genome used in the map step;
+ OrderedDict from [collections](https://docs.python.org/2/library/collections.html);


##License:

GPLv2


