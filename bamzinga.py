#!/usr/bin/env python
#Gets read counts from an alignment bam file, by gene or by isoform.
#use the flags G or I for gene or isoform quantification
#Usage: python bamzinga.py [gff file] [sorted bam file] [outputfile] [G/I]

from sys import argv
from collections import OrderedDict
import pysam

def read_gtf_ensembl(infile):
	"""Gets the gff file (as seen in the ensemble references)
	and organize it in an ordered
	dictionary as [gene]=[chromossome, (start position,stop position)]
	Retrives the same dictionary"""
	fil=open(infile)
	dic=OrderedDict()
	for i in fil:
		d=i.split('\t')
		s=d[8].split('"')
		if d[2]==("exon"):
			if s[1] in dic:
				dic[s[1]].append(d[3]+","+d[4])#append the start and stop position
			else:
				dic[s[1]]=[d[0],d[3]+","+d[4]]#append the chromossome name, star and stop positions
	fil.close()
	return dic

def read_gtf_merge(infile):
	"""Read the merged.gtf file and organize a dictionary by
	dictionary as [gene]=[chromossome, (start position,stop position)]
	Retrives the same dictionary"""
	fil=open(infile)
	dic=OrderedDict()
	for i in fil:
		d=i.split('\t')
		s=d[8].split('"')
		if d[2]==("exon"):
			if s[1] in dic:
				dic[s[9]].append(d[3]+","+d[4])#append the start and stop position
			else:
				dic[s[9]]=[d[0],d[3]+","+d[4]]#append the chromossome name, star and stop positions
	fil.close()
	print(dic)
	return dic

def read_bam(dic,infile):
	"""reads the bam file and retrives the counts of the genes.
	Uses the ordered dictionary from read_gff and retrive the names of
	the reads of each gene, in other words, the reads mapping in the exons.
	This take into acount reads that are in more than one exon, and count it as only one.
	Finally retrives a dictionary with gene and number of reads"""
	dic_cont={}
	bamfile = pysam.AlignmentFile(infile, 'rb')#read bam
	for key, value in dic.items():
		a=1
		list_reads_temp=set()
		while(a<len(value)):
			f=value[a].split(",")
			itere = bamfile.fetch(value[0], int(f[0]), int(f[1]))#recives the chromossome and start and stop positions
			for x in itere:
				temp=str(x)#transforms the object from pysam into a string, to be possible retrive only the read name.
				list_reads_temp.add(temp.split("\t")[0])#adds the read name to a set
			a+=1
		dic_cont[key]=len(list_reads_temp)#add the gene and counts to the dictionary
	bamfile.close()
	return dic_cont

def counts_write(dic, outfile):
	"""Write the dictionary
	from read_bam  to a file"""
	out=open(outfile, "w")
	for key, value in dic.items():
		out.write(key+"\t"+str(value)+"\n")
	out.close()
	

if argv[4]=="G":
	counts_write(read_bam(read_gtf_ensembl(argv[1]),argv[2]),argv[3])
elif argv[4]=="I":
	counts_write(read_bam(read_gtf_merge(argv[1]),argv[2]),argv[3])
else:
	print ("Not a valid option. please run again with one of the options:\n"
	       "G - for gene quantification based on a reference genome gtf file\n"
		   "I - for isoform quantification using a merged gtf file, after cuffmerge step")
