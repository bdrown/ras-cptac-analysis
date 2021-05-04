# Top-down Analysis of RAS Proteoforms in CPTAC Tumor Samples

The following analysis supports an effort to identify proteoforms of RAS 
GTPases to better understand colon cancer progression. Tumor tissue sections
from CPTAC-2 were obtained, KRAS was immunoprecipitated, and proteoforms were
identified by top-down LC-MS/MS. The same tumor samples were separately
analyzed by whole exom sequencing and RNA-seq. These sequencing data were
deposited on the GDC Data Portal (dbGaP Study Accession
[phs000892.v6.p1](https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs000892.v6.p1))

## Sample Info

Information about the Case IDs of samples and their associations to files can
be found in the `manifests` directory. `manifests/matches-case-list.tsv` lists
all of the sample Case IDs included in this study.

## Fetching data

Access to aligned sequence reads is controlled and requires approval by dbGaP.
Either edit `config.mk` to point to your GDC token or rename it
`gdc-user-token.txt`.

Download the [GDC Data Transfer Tool](https://gdc.cancer.gov/access-data/gdc-data-transfer-tool)
and set the variable in `config.mk` to match its path.

Run Make to fetch all of the data from GDC.
```
make download
```