# eggNOG 7 Protein Annotation Pipeline

A lightweight Python pipeline that annotates protein sequences against the [eggNOG 7 database](https://eggnogdb.org/) without requiring eggnog-mapper. It takes a `.faa` FASTA file, runs DIAMOND blastp against the eggNOG 7 reference proteins, and produces a formatted `.xlsx` with GO terms, KEGG annotations, and protein family assignments.

---

## Repository Structure

```
eggNOG/
├── eggnog_pipeline.py        # Main annotation pipeline
├── decompress_databases.py   # Utility to decompress .gz database files
├── utility/
│   └── fasta.py              # Converts Proteomics_input.xlsx → .faa
├── input/
│   └── Proteomics_input.xlsx # Input Excel with Protein.IDs, Gene.names, Sequences
├── databases/                # NOT included — download separately (see below)
│   ├── e7.proteins.fa
│   ├── e7.og_info_kegg_go.tsv
│   └── e7.protein_families.tsv
└── results/                  # Created automatically on first run
    ├── e7_ref.dmnd
    ├── diamond_hits.tsv
    └── Proteins_Sequence_annotated.xlsx
```

---

## Database Files (Not Included)

The three eggNOG 7 database files are too large to include in this repository. Download them from the official eggNOG database:

**Download page:** http://eggnog6.embl.de/download/eggnog_6.0/

| File | Description | Size |
|------|-------------|------|
| `e7.proteins.fa.gz` | All protein sequences in eggNOG 7 — used by DIAMOND as the reference database | ~20 GB |
| `e7.og_info_kegg_go.tsv.gz` | OG info file — maps each OG to its member proteins, GO slim terms, and KEGG KO annotations | ~2 GB |
| `e7.protein_families.tsv.gz` | Protein family info — maps protein families to their member proteins and OG assignments | ~1 GB |

After downloading, place all three `.gz` files in the `databases/` folder. The pipeline handles decompression automatically (see Usage below).

---

## Requirements

### Option A: Windows (Anaconda Prompt)
```
conda create -n eggnog python=3.10
conda activate eggnog
conda install -c bioconda diamond
pip install pandas openpyxl
```

### Option B: WSL / Linux
```bash
conda create -n eggnog python=3.10
conda activate eggnog
conda install -c bioconda diamond
pip install pandas openpyxl
```

### Option C: Google Colab
```python
!pip install pandas openpyxl -q
!apt-get install -y diamond-aligner -q
```

---

## Usage

### Step 1 — Generate your .faa from Excel (if needed)

If your proteins are in an Excel file with columns `Protein.IDs`, `Gene.names`, `Sequences`:

```bash
python utility/fasta.py input/Proteomics_input.xlsx Protein.IDs Sequences Proteins_Sequence.faa
```

### Step 2 — Decompress the database files

Only needs to be done once. Run this before the pipeline on first use:

```bash
python decompress_databases.py
```

This will decompress all three `.gz` files in the `databases/` folder. It skips any files already decompressed. The `e7.proteins.fa` is very large so this step may take several minutes.

### Step 3 — Run the annotation pipeline

```bash
python eggnog_pipeline.py Proteins_Sequence.faa
```

Output will be written to `Proteins_Sequence_annotated.xlsx` in the same directory as the input `.faa`.

---

## Output

The annotated `.xlsx` contains two sheets:

### Annotations sheet

| Column | Description |
|--------|-------------|
| `Protein_ID` | Query protein ID from your `.faa` |
| `Best_Hit` | Best DIAMOND hit in eggNOG 7 (format: `taxid.proteinID`) |
| `OG_Name` | eggNOG Orthologous Group name |
| `Protein_Family` | Protein family name from `e7.protein_families.tsv` |
| `GO_Terms` | GO slim terms (semicolon-separated) |
| `KEGG_KO` | KEGG KO identifiers (semicolon-separated) |
| `KEGG_Symbols` | KEGG gene symbols (semicolon-separated) |

### Summary sheet

Provides a quick overview of annotation rates — total proteins, proteins with OG hits, GO terms, protein family, and KEGG annotations.

---

## How the Pipeline Works

1. **DIAMOND blastp** — Builds a searchable database from `e7.proteins.fa` (one-time) and searches each query protein against it. Returns the single best hit per query using an e-value threshold of 1e-5.

2. **OG lookup** — Each DIAMOND hit is in `taxid.proteinID` format (e.g. `1127695.HMPREF9163_00007`). The pipeline reads `e7.og_info_kegg_go.tsv` line by line and builds a direct `protein → GO/KEGG` dictionary using the member protein list in column 5.

3. **Family lookup** — Similarly reads `e7.protein_families.tsv` and builds a `protein → family name` dictionary from the member protein list in column 4.

4. **Excel output** — Merges all annotations per query protein and writes a formatted `.xlsx` with alternating row shading, frozen header, and auto-filter.

---

## Why Not eggnog-mapper?

eggnog-mapper requires a full local database setup and HMM infrastructure that can be difficult to configure across different environments. This pipeline replicates the core annotation logic by using DIAMOND for sequence homology search and direct lookups against the same eggNOG 7 flat files that eggnog-mapper uses internally, without requiring the mapper itself to be installed.

---

## Adapting the Pipeline for Other Inputs

The pipeline expects a standard `.faa` FASTA file. Any tool that produces a `.faa` can feed into it. To swap in a different input:

1. Produce a `.faa` file from your data (using `utility/fasta.py` or any other tool)
2. Run `python eggnog_pipeline.py your_file.faa`
3. The output `.xlsx` will be named `your_file_annotated.xlsx`

To change the database paths (e.g. if running on a different machine), edit the `BASE_DIR` variable at the top of both `eggnog_pipeline.py` and `decompress_databases.py`:

```python
# Windows
BASE_DIR = r"C:\Users\YourName\Downloads\eggNOG"

# WSL / Linux / Colab
BASE_DIR = "/path/to/eggNOG"
```

---

## Notes

- The DIAMOND database build (`e7_ref.dmnd`) only happens once and is reused on subsequent runs
- Both annotation TSVs are read line by line to avoid loading several GB into RAM at once
- If your `e7.og_info_kegg_go.tsv` is missing GO/KEGG columns (older download), those fields will be empty in the output but the pipeline will still run
