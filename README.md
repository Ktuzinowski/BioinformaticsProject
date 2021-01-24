BENCHMARK STUDY
===============

G3PO (Gene and Protein Prediction PrOgrams) Benchmark was designed to represent many of the typical challenges faced by current genome annotation projects. The benchmark is based on a carefully validated and curated set of real eukaryotic genes from 147 phylogenetically disperse organisms (from human to protists). 



# Project

Download the gitlab project [here](http://git.lbgi.fr/scalzitti/Benchmark_study) or:

```bash
git clone http://git.lbgi.fr/scalzitti/Benchmark_study.git
```

The new created directory called */Benchmark_study* is your root directory WORKPATH.
To run the scripts in /src please use __python 3.6__ or more.

```bash
cd src
python script_name.py
```
A description of the benchmark database is provided in __G3PO.csv__

The directory *WORKPATH/Sequences_types* contains specific species list files.


# Data

#### Reference Data
For convenience, you will find all the reference data of the benchmark study in a compressed file in this repository named __References.tar.gz__
Download and extract the file __References.tar.gz__ in the root directory */Benchmark_study*.  

#### Output Predictions
You will find the output predictions of each predictor in this repository as well in a compressed file named __Predictions.tar.gz__
Download and extract the file __Predictions.tar.gz__ in the root directory */Benchmark_study*



# Step 1 - Predictions using the "program_name" to be tested

* First, download and install gene predictors (Augustus, Genscan, GeneID, GlimmerHMM or Snap). 
    <ol>
    	<li>[Augustus](http://augustus.gobics.de/binaries/)</li>
    	<li>[Genscan](http://hollywood.mit.edu/license.html)</li>
    	<li>[GeneID](https://genome.crg.cat/software/geneid/index.html#code)</li>
    	<li>[GlimmerHMM](https://ccb.jhu.edu/software/glimmerhmm/)</li>
    	<li>[Snap](https://github.com/KorfLab/SNAP)</li>
    </ol>

 
The files models.csv (in *WORKPATH/Models/* directory) contain the codename of the species and the codename of the models for the programs used in the study. The files were generated using the taxonomic proximity of each species to the models proposed by the different programs. 

* To launch the prediction use the script *launch_prediction.py* 

Command lines:
```bash
	Augustus --species=Specie --softmasking=1 --gff3=off File_in.fasta > augustus_File_out.fasta
	Genscan Specie File_in.fasta > genscan_File_out.fasta
	Geneid -A -P param/new_param/Specie File_in.fasta > geneid_File_out.fasta
	Glimmerhmm_linux_x86_64 File_in.fasta -d trained_dir/Specie -g > glimmer_File_out.fasta
	Snap -gff -quiet -lcmask HMM/Specie File_in.fasta --a protein_dir/File_in.fasta > snap_File_out.fasta
```

`For SNAP, protein sequences are generated at this step and stored in : /Predictions/Proteines/snap/{add_nuc}Kb/`
`For Geneid, Copy and paste the new_param/ directory in the directory "param" in Geneid directory   `

`new_param contain 66 new models for the predictor Geneid version 1.4`


# Step 2 - Protein extraction

Run the *extract_protein_sequence.py* script   

Protein sequences are stored in *WORKPATH/Predictions/Proteins/PROGRAM_NAME/{X}Kb/*


# Step 3 - Conversion of the predictions in .gar format

Run the script *convert2gar.py* to convert the specific prediction format of each predictors to the .gar format.

The gar file is a specific format using for this study and look like as ZFF (korf et al., 2004). gar = Gene ARchitecture

### Example of .gar file :

---
\# Transcript X; ID_transcript_Ensembl; ID_Uniprot  
\> X exons  

|N° Exon | Start | Stop | len_Exon | Strand (1 or -1) |
|---------------|-------|------|-----------------|------------------|
|Exon_1|1|103|103|1|
|Exon_2|236|435|200|1|
|Exon_3|607|632|26|1|



# Step 4 - Comparison at nucleotide level
* Calculate the sensitivity, specificity and F1 score for the predictions. Run the *compar_lvl_nuc.py* script.

 The results of this step are 2 files :
- with all the values of metrics 
- the average  of metrics 


# Step 5 - Comparison at exon level

* Calculate the sensitivity, specificity, missingExon, wrongExon, % of correct donor and acceptor sites. Use the *compar_lvl_exon.py* script.

Two directory are created:
- Calculs (With the values)
- Details (With the details)

The file *results.csv* contain the mean of all results (not specifically for the 889 confirmed sequences)


# Step 6 - Comparison at protein level
To launch the protein comparison Run the compar_lvl_prot.py script

To compare predicted and reference protein sequences, first create a Fasta format file containing the two sequences. Stored in *WORKPATH/Predictions/Proteines/Joined/*
Next we aligned the predicted and reference protein sequences with Mafft version 7.307 :

```bash
	mafft --auto --clustalout --reorder file > output
```

After alignment, we calculate the % identity between the reference protein sequence and a predicted protein sequence. All results are stored in the file WORKPATH/Resultats/Proteins/{X}Kb/PROGRAM_NAME\_%similarity.csv and ./Results/Proteins/XXKb/\(soft\)\_\_best_%similarity.csv. The last file contains the resultats with the best prediction
	
