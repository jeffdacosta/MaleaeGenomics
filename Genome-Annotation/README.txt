This directory describes steps used for genome annotations using MAKER v2.31.8. The same evidence files were used for all species, and examples are given from the Malus ioensis annotation. The procedure was guided by the MAKER Tutorial for GMOD Online Training and Campbell et al. Genome Annotation and Curation Using MAKER and MAKER-P.

1) Collect transcript and protein evidence for MAKER.

  -transcript evidence (file: unigene5_Malus_transcripts.fasta)
    -Malus domestica fruits (n=80,941); https://www.rosaceae.org/species/malus/malus_x_domestica/CU_RNA_seq_genes
    -Malus domestica unigene5 (n=25,525); https://www.rosaceae.org/species/malus/malus_spp/unigene_v5
    -Pyrus communis unigene5 (n=259); https://www.rosaceae.org/node/336109/
    -Prunus persica unigene5 (n=10,934); https://www.rosaceae.org/species/prunus/prunus_spp/unigene_v5
    -Fragaria vesca unigene5 (n=6,226); https://www.rosaceae.org/node/312468/
    -Rosa spp. unigene5 (n=1,215); https://www.rosaceae.org/species/rosa/rosa_spp/unigene_v5
    -Rubus spp. unigene5 (n=359); https://www.rosaceae.org/node/336091/
    
  -protein evidence (file: TAIR_BUSCO_ROSIDS_prot.fasta)
    -UniProt-SwissProt reviewed proteins for "rosids" (n=10,540); http://www.uniprot.org
    -Arabidopsis thaliana TAIR10 build (n=35,386); https://www.arabidopsis.org/download/
    -BUSCO plant sequences (n=956); http://busco.ezlab.org
    
2) Run MAKER (run1) with repeat masking to create imperfect gene models using transcript (est2genome=1) and protein (protein2genome=1) data.
  -control file: maker_opts1.ctl
  -shell file: maker1.sh
  
3) Check that MAKER finished completely.
  a-get the number of contigs in your genome that are long enough for MAKER (min_contig in opts file)
  b-check if the number of contigs with "FINISHED" in the master_datastore_index.log is equal to 3a
    grep -c "FINISHED" filename
  c-if yes then proceed to step 4
  d-if no then first increase the number for the "tries" parameter in the opts file and then re-run MAKER (run1) and it will attempt to annotate the remaining contigs. 

4) Create initial SNAP model from results of MAKER run1.
  -merge gff3 files
    gff3_merge -d Mioensis_run1_master_datastore_index.log
  -convert best models to zff format, create hmm file. x paramater was tweaked to obtain ~2000-2500 genes.
    maker2zff -c 0 -e 0 -o 0 -x 0.1 Mioensis_run1.all.gff
    fathom -categorize 1000 genome.ann genome.dna
    fathom -export 1000 -plus uni.ann uni.dna
    forge export.ann export.dna
    hmm-assembler.pl Mioensis . > ../Mioensis_run1.snap.hmm

5) Run MAKER (run2) with initial SNAP hmm file (snaphmm=Mioensis_run1.snap.hmm). Turn off the options to generate models from EST (est2genome=0) and protein (protein2genome=0) data. Provide gff file (maker_gff=Mioensis_run1.all.gff), turn off repeat masking (rm_pass=1), and use previous mapping results (altest_pass=1 and protein_pass=1) to reduce run time.
  -control file: maker_opts2.ctl
  -shell file: maker2.sh  

6) Check if run2 finished completely (see step 3 above). Create improved SNAP model from results of MAKER run2.
  -merge gff3 files
    gff3_merge -d Mioensis_run2_master_datastore_index.log
  -convert best models to zff format, create hmm file. x paramater was tweaked to obtain ~2000-2500 genes.
    maker2zff -c 0 -e 0 -o 0 -x 0.05 Mioensis_run2.all.gff
    fathom -categorize 1000 genome.ann genome.dna
    fathom -export 1000 -plus uni.ann uni.dna
    forge export.ann export.dna
    hmm-assembler.pl Mioensis . > ../Mioensis_run2.snap.hmm    

7) Run MAKER (run3) with improved SNAP hmm file (snaphmm=Mioensis_run2.snap.hmm) for further refinement. Turn off the options to generate models from EST (est2genome=0) and protein (protein2genome=0) data. Provide gff file (maker_gff=Mioensis_run2.all.gff), turn off repeat masking (rm_pass=1), and use previous mapping results (altest_pass=1 and protein_pass=1) to reduce run time.
  -control file: maker_opts3.ctl
  -shell file: maker3.sh  

8) Check if run3 finished completely (see step 3 above). Create refined SNAP model from results of MAKER run3.
  -merge gff3 files
    gff3_merge -d Mioensis_run3_master_datastore_index.log
  -convert best models to zff format, create hmm file. x paramater was tweaked to obtain ~2000-2500 genes.
    maker2zff -c 0 -e 0 -o 0 -x 0.05 Mioensis_run2.all.gff
    fathom -categorize 1000 genome.ann genome.dna
    fathom -export 1000 -plus uni.ann uni.dna
    forge export.ann export.dna
    hmm-assembler.pl Mioensis . > ../Mioensis_run3.snap.hmm    

9) Create AUGUSTUS gene model files using the online training service: 
  -provide name for your species in AUGUSTUS (species name field)
  -upload export.dna (created in step 7) as the genome file 
  -upload export.aa (created in step 7) as the protein file
  -submit with email contact, download results when ready
  -transfer (XXX) files to the proper AUGUSTUS directory on your server

10) Run MAKER (run4) with refined SNAP hmm file (snaphmm=Mioensis_run3.snap.hmm) and AUGUSTUS files (augustus_species=Malus_ioensis). Turn off the options to generate models from EST (est2genome=0) and protein (protein2genome=0) data. Provide gff file (maker_gff=Mioensis_run3.all.gff), turn off repeat masking (rm_pass=1), and use previous mapping results (altest_pass=1 and protein_pass=1) to reduce run time. Use keep_preds=1 to keep unsupported annotations generated by SNAP and AUGUSTUS.
  -control file: maker_opts4.ctl
  -shell file: maker4.sh

11) Check if run4 finished completely (see step 3 above). Merge gff3 and fasta files from run4. These represent the MAKER max build (sensu Campbell et al.) with all annotations (i.e., those with support from from EST/protein evidence and strict ab initio).
  -create complete gff3 file and a separate max file with lines containing annotation information
    gff3_merge -d Mioensis_run4_master_datastore_index.log
    awk '/\tmaker\t/' Mioensis_run4.all.gff > Mioensis.max.gff
  -create protein and transcript fasta files
    fasta_merge -d Mioensis_run4_master_datastore_index.log
    cp Mioensis_run4.all.maker.proteins.fasta Mioensis.max.proteins.fasta
    cp Mioensis_run4.all.maker.transcripts.fasta Mioensis.max.transcripts.fasta

12) Assign short names to each annotation in max build.
  -generate id mapping file
    maker_map_ids --prefix MAIO_ --justify 5 Mioensis.max.gff > Mioensis.max.map
  -use id mapping file to change names in gff3 and fasta files
    map_gff_ids Mioensis.max.map Mioensis.max.gff
    map_fasta_ids Mioensis.max.map Mioensis.max.proteins.fasta
    map_fasta_ids Mioensis.max.map Mioensis.max.transcripts.fasta

13) Assign putative gene functions to annotations in max build.
  -obtain fasta file of all reviewed proteins in UniProt-SwissProt database (http://www.uniprot.org)
  -create blast database for uniprot_sprot fasta file
    makeblastdb -in uniprot_sprot.fasta -input_type fasta -dbtype prot
  -blast max build annotations to uniprot_sprot database
    blastp -db uniprot_sprot.fasta -query Mioensis.max.proteins.fasta -out Mioensis.max.proteins.blastp -evalue 0.000001 -outfmt 6 -num_alignments 1 -seg yes -soft_masking true -lcase_masking -max_hsps_per_subject 1
  -add protein homology data to max build gff and fasta files
    maker_functional_gff uniprot_sprot.fasta Mioensis.max.proteins.blastp Mioensis.max.gff > Mioensis.max.func.gff    
    maker_functional_fasta uniprot_sprot.fasta Mioensis.max.proteins.blastp Mioensis.max.proteins.fasta > Mioensis.max.proteins.func.fasta
    maker_functional_fasta uniprot_sprot.fasta Mioensis.max.proteins.blastp Mioensis.max.transcripts.fasta > Mioensis.max.transcripts.func.fasta

14) Remove text wrapping from fasta files with fastx-toolkit to make compatible with downstream filtering.
  -remove wrapping
    fasta_format -i Mioensis.max.proteins.func.fasta -o Mioensis.max.proteins.func.fasta1
    fasta_format -i Mioensis.max.transcripts.func.fasta -o Mioensis.max.transcripts.func.fasta1
  -convert back to original name
    mv Mioensis.max.proteins.func.fasta1 Mioensis.max.proteins.func.fasta
    mv Mioensis.max.transcripts.func.fasta1 Mioensis.max.transcripts.func.fasta
    
15) Assign Pfam domains to annotations in max build.
  -run InterProScan to search for Pfam domains
    interproscan.sh -appl PfamA -iprlookup -goterms -f tsv -i Mioensis.max.proteins.func.fasta
  -add Pfam domain info to max build gff file
    ipr_update_gff Mioensis.max.func.gff Mioensis.max.proteins.func.fasta.tsv > Mioensis.max.func.ipr.gff
  
16) Characterize annotations in max build into different categories of support:
  -default build (sensu Campbell et al.): AED<1 (annotations supported by transcript and/or protein evidence)
  -standard build (sensu Campbell et al.): AED<1 and Pfam domain
  -standard-us build: AED<1, Pfam domain OR blast hit to UniProt-SwissProt
  -max build: all annotations
  -script filter_gff.py (might not be universal!) will detect annotations for default, standard, and standard-us builds. It will generate a list file with annotation names of each build and a reduced gff file.
    python3 filter_gff.py Mioensis.max.func.ipr.gff default Mioensis.default.func.ipr.gff
    python3 filter_gff.py Mioensis.max.func.ipr.gff standard Mioensis.standard.func.ipr.gff
    python3 filter_gff.py Mioensis.max.func.ipr.gff standard-us Mioensis.standard-us.func.ipr.gff
  -script maker_extract_fasta.py (might not be universal!) will extract protein/transcripts for each build.
    python3 maker_extract_fasta.py Mioensis.max.proteins.func.fasta default_parent.list Mioensis.default.proteins.func.fasta
    python3 maker_extract_fasta.py Mioensis.max.transcripts.func.fasta default_parent.list Mioensis.default.transcripts.func.fasta
    python3 maker_extract_fasta.py Mioensis.max.proteins.func.fasta standard_parent.list Mioensis.standard.proteins.func.fasta
    python3 maker_extract_fasta.py Mioensis.max.transcripts.func.fasta standard_parent.list Mioensis.standard.transcripts.func.fasta
    python3 maker_extract_fasta.py Mioensis.max.proteins.func.fasta standard-us_parent.list Mioensis.standard-us.proteins.func.fasta
    python3 maker_extract_fasta.py Mioensis.max.transcripts.func.fasta standard-us_parent.list Mioensis.standard-us.transcripts.func.fasta
