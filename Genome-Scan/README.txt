This directory contains Python (version 3) scripts that were used for genome scans comparing diploid and tetraploid samples of Malus ioensis. Genome scans were completed on the "general" and "serial-requeue" partitions of the Harvard Odyssey computer cluster.

The Python scripts collect input files and create SLURM files to send jobs to the Odyssey cluster. Althought the syntax of the SLURM files may be specific to this cluster, these files contain command lines that can be modified for other systems.

Collectively, these scripts form a pipeline that starts with raw fastq files for each sample and ends with allele frequency tables for each cohort (diploids vs tetraploids). Several filtering steps are included, which can be modified for the specific needs of the project. Each script will print help directions with the -h arguement (e.g., python3 batch_cutadapt1.8_PE.py -h). The pipeline steps are as follows:

1) Trim adapter sequences from paired-end reads with cutadapt program.
  -script: batch_cutadapt1.8_PE.py

2) Map trimmed paired-end reads to a reference genome with the programs BWA and stampy.
  -script: BWA-STAMPY_PE_mapping.py
  
3) Remove duplicate reads with the program picard tools.
  -script: PicardTools_RemoveDuplicates.py

4) Fix syntax of names with the program picard tools.
  -script: PicardTools_NameFix.py

5) Realign regions around probable indels with the program GATK.
  -script: GATK_IndelRealigner.py

6) Discover and genome variants (SNPs) with GATK. NOTE: if cohorts have different ploidy then they should be genotyped separately.
  -script: GATK_UnifiedGenotyper_AllScaffolds.py

7) IF NEEDED: Merge vcf files from different genotyping runs with GATK.
  -no script, see CombineVariants command
  -https://www.broadinstitute.org/gatk/gatkdocs/org_broadinstitute_gatk_tools_walkers_variantutils_CombineVariants.php

8) Filter for variants that are biallelic and genotyped in XX chromosomes in GATK. For example, if you have 5 tetraploid samples (cohort1) and 10 diploid samples (cohort2) and you want variants with no missing genotypes then you want to filter for those genotyped in 40 chromosomes (5*4)+(10*2).
  -script: GATK_SelectVariants_biallelic_nChr.py

9) Mask low quality variants using the "best practices" filter expression in GATK. Note that masked variants remain in the vcf file, but with a flag in the FILTER column.
  -script: GATK_VariantFiltration_BestPracticesMask.py

10a) Identify variants that fail a specified coverage filter with GATK. The two filtering parameters used in this script are -minCov and -percent. For example, if you want to further filter for variants with at least 4 reads in all samples in the above scenario then you would use -minCov 4 and -percent 0.99.
  -script: GATK_CoveredByNSamplesSites_minCov_FAIL.py

10b) Mask variants that fail step 10a with GATK.
  -script: GATK_VariantFiltration_MaskVCF.py

11) IF NEEDED: gather the number of categories in the FILTERED column and count variants in each category.
  -script: VCF_filter_count.py

12) Remove all masked (filtered) variants from the vcf file with GATK.
  -script: GATK_SelectVariants_excludeFiltered.py

13) Split vcf file by cohort with GATK (run separately for each cohort).
  -script: GATK_SelectVariants_sf.py

14) Generate allele frequency tables for each cohort with GATK.
  -script: GATK_VariantsToTable.py

15) Paste together allele frequency tables with the function "paste" in linix/unix.
