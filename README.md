# MetHMMDB
Source files and databases created during MetHMMDB creation

---
# Usage
The database was designed to be used with HMMER suite tools like `hmmscan` and `hmmsearch` (http://hmmer.org/).

Before starting, download the data and ensure you have HMMER installed:
```
# Clone the repository
git clone https://github.com/Haelmorn/MetHMMDB
cd MetHMMDB

# Ensure HMMER suite is installed on your system
# For Ubuntu/Debian:
sudo apt-get install hmmer

# For macOS:
brew install hmmer
```

Basic usage:
```
# Using hmmscan to search sequences against MetHMMDB
hmmscan --domtblout output.tbl path/to/MetHMMDB/MetHMMDb.hmm query_sequences.fasta

# Using hmmsearch to search MetHMMDB profiles against a sequence database
hmmsearch --domtblout output.tbl path/to/MetHMMDB/MetHMMDb.hmm sequence_database.fasta
```

Additionally, since reading the output files can be tricky, the HmmPy (https://github.com/EnzoAndree/HmmPy) package can be used to turn the `--domtblout` file into a nice `.tsv` that's easy to parse by your favourite tool.

For more detailed usage, including output options, we recommend reading the HMMER suite documentation and User's guide (available at http://hmmer.org/documentation.html)


---
# Citation
The paper is currently under review. In the meantime, you can find it on bioRxiv: 10.1101/2024.12.26.629440v2

If you use MetHMMDB in your research, please cite our work (citation details to be added upon publication).
