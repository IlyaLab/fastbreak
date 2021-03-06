#!/usr/bin/python
#
# 
#     Copyright (C) 2003-2010 Institute for Systems Biology
#                             Seattle, Washington, USA.
# 
#     This library is free software; you can redistribute it and/or
#     modify it under the terms of the GNU Lesser General Public
#     License as published by the Free Software Foundation; either
#     version 2.1 of the License, or (at your option) any later version.
# 
#     This library is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#     Lesser General Public License for more details.
# 
#     You should have received a copy of the GNU Lesser General Public
#     License along with this library; if not, write to the Free Software
#     Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA
# 

"""
"""

__author__ = "Ryan Bressler, Jake Lin"

def main():
	pf = open("patients.txt","r")
	
	
	bcbypatient ={}
	
	dataf = open("coverage.per.gene.per.sample.tsv","r")
	datalines=[]
	for line in dataf:
		line=line.split("\t")
		line.pop(1)
		line.pop(1)
		line.pop(1)
		line="\t".join(line)
		datalines.append(line)
	dataf.close()
	
	header=datalines[0]
	
	newheadermembers = []
	
	bcbypatient ={}
	for colhead in header.rstrip().split("\t"):
		if colhead.find("TCGA")!=-1:
			colhead = colhead.lstrip().lstrip("./").replace("-",".")
			colhead=colhead[0:15]
			bcbypatient[colhead]=colhead
		newheadermembers.append(colhead)
		
	datalines[0]="\t".join(newheadermembers)+"\n"
	dataf = open("formated.coverage.per.gene.per.sample.tsv","w")
	for line in datalines:
		dataf.write(line)
	dataf.close()
	
	patientStatus={}
	patientResistance = {}
	
	for scoreCutoff in [0]:#25,50,75,90,94,96,98,99]:
		for col in [4,5]:
			filename = "fastbreak.per.gene.score.minscore.%i.col.%i.matrix.tsv"%(scoreCutoff,col)
			dataf = open(filename,"r")
			datalines=[]
			for line in dataf:
				datalines.append(line)
			dataf.close()
			
			header=datalines[0]
			
			newheadermembers = []
			
			for colhead in header.rstrip().split("\t"):
				if colhead[0:4] == "TCGA":
					colhead=colhead[0:15].replace("-",".")
				newheadermembers.append(colhead)
				
			datalines[0]="\t".join(newheadermembers) +"\n"
			dataf = open("formated."+filename,"w")
			for line in datalines:
				if line.rstrip()!="":
					dataf.write(line)
			dataf.close()
	
	def loadClinicalDataf(hash,file,disease,headerhash):
		fin = open(file,"r")
		headers = []
		for header in fin.next().rstrip().split('\t'):
			header = header.split("}")
			if len(header)>1:
				header = header[1]
			else:
				header = header[0]
			headers.append(header)
			headerhash[header]=True
		for line in fin:
			line = line.rstrip().split('\t')
			patient = line[1].replace("-",".")
			hash[patient]={"CANCER_TYPE":disease}
			for i,val in enumerate(line):
				hash[patient][headers[i]]=val
	
	
	
	
	
	
	clinicaldata ={}
	headerhash={}
	loadClinicalDataf(clinicaldata,"gbm_clinical_data.tsv","GBM",headerhash)
	loadClinicalDataf(clinicaldata,"ov_clinical_data.tsv","OVARIAN",headerhash)
	
	
	headers = ["Name","TISSUE","CANCER_TYPE"]
	
	for header in headerhash.keys():
		if not header in ["file","patient","CANCER_TYPE"]:
			headers.append(header)
	dataf = open("sampleMetaData.txt","w")
	dataf.write("\t".join(headers)+"\n")
	
	
	for sample in sorted(newheadermembers[1:]):
		tissue = sample[13:15]
		oposite = sample[0:13]+sample[14:15]+sample[13:14]
		if oposite in bcbypatient:
			#decode the oposite tissue
			tissueopositesymbol = "ERROR"
			if tissue == "01":
				tissueopositesymbol ="BLOOD"	
			elif tissue =="10":
				tissueopositesymbol ="CANCER"
			patient = oposite[0:12]
			cancer_type="NA"
			if patient in clinicaldata:
				cancer_type=clinicaldata[patient]["CANCER_TYPE"]
			line = "\t".join([bcbypatient[oposite],tissueopositesymbol,cancer_type])
			for header in headers[3:]:
				line+="\t"
				if	patient in clinicaldata and header in clinicaldata[patient]:
					line+=clinicaldata[patient][header]
			line+="\n"
			dataf.write(line)
	
	
	
	
	
	dataf.close()
		
if __name__ == '__main__':
    main()