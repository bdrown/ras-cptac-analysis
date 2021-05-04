include config.mk

.PHONY : all download

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
	
clean :
	rm -Rf maf
	rm -Rf bam
	rm -Rf fpkm