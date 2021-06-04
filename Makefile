include config.mk

.PHONY : all download renamed analyze

all : download analyze rename

download : maf/downloaded bam/downloaded fpkm/downloaded

maf/downloaded : manifests/gdc_manifest.maf.txt
	mkdir -p maf
	${GDC_CLIENT} download -m $< -d maf -t ${GDC_TOKEN}
	cd maf && find . -mindepth 2 -type f -print -exec mv {} . \;
	cd maf && rm -R -- */
	cd maf && gunzip *.gz
	touch maf/downloaded
	
bam/downloaded : manifests/gdc_manifest.bam.txt
	mkdir -p bam
	${GDC_CLIENT} download -m $< -d bam -t ${GDC_TOKEN}
	cd bam && find . -mindepth 2 -type f -print -exec mv {} . \;
	cd bam && rm -R -- */
	touch bam/downloaded
	
fpkm/downloaded : manifests/gdc_manifest.fpkm.txt
	mkdir -p fpkm
	${GDC_CLIENT} download -m $< -d fpkm -t ${GDC_TOKEN}
	cd fpkm && find . -mindepth 2 -type f -print -exec mv {} . \;
	cd fpkm && rm -R -- */
	cd fpkm && gunzip *.gz
	touch fpkm/downloaded

rename : maf/renamed bam/renamed fpkm/renamed

maf/renamed : manifests/gdc_sample_sheet.maf.tsv maf/downloaded
	python scripts/rename-files.py $< maf
	touch maf/renamed

bam/renamed : manifests/gdc_sample_sheet.bam.tsv bam/downloaded
	python scripts/rename-files.py $< bam
	touch bam/renamed

fpkm/renamed : manifests/gdc_sample_sheet.fpkm.tsv fpkm/downloaded
	python scripts/rename-files.py $< fpkm
	touch fpkm/renamed

analyze : maf/merged.csv convert-fastq run-salmon

maf/merged.csv : scripts/get-snp.py maf/downloaded maf/renamed
	python $< maf KRAS NRAS HRAS

# Need to convert BAM files to fastq in order to run Salmon
BAMS=$(wildcard bam/*.bam)
FASTQS=$(patsubst bam/%.gdc_realn.bam, fastq/%.fastq, $(BAMS))
convert-fastq : $(FASTQS) bam/renamed

fastq/%.fastq : bam/%.gdc_realn.bam
	samtools bam2fq $< > $@

# Run Salmon
SALMON_OUTPUT=$(patsubst bam/%.rna_seq.genomic.gdc_realn.bam, salmon/%/quant.sf, $(BAMS))
run-salmon : $(SALMON_OUTPUT)
salmon/%/quant.sf : fastq/%.rna_seq.genomic.fastq
	mkdir -p salmon
	salmon quant -i refs/GRCh38_index -l A -r $< --validateMappings -o salmon/$* --threads 10

clean :
	rm maf/merged.csv
	rm -Rf salmon

clean-deep :
	rm -Rf maf
	rm -Rf bam
	rm -Rf fpkm