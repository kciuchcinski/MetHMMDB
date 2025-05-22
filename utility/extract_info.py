import json
import pandas as pd
import re
from collections import defaultdict
from glob import glob

# Replace as needed
hmm_path = "DATA/HMMS"
metadata_file = "DATA/methmm_metadata_v1.0.json"

# Function to split metal types and strip whitespace
def split_metal_types(metal_str):
    if pd.isna(metal_str):
        return []
    # Split by comma and strip spaces
    metals = [m.strip() for m in metal_str.split(',')]
    return metals

metal_name_map = {
    'Ag': 'Silver',
    'As': 'Arsenic',
    'Cd': 'Cadmium',
    'Co': 'Cobalt',
    'Cr': 'Chromium',
    'Cu': 'Copper',
    'Fe': 'Iron',
    'Hg': 'Mercury',
    'Mg': 'Magnesium',
    'Mn': 'Manganese',
    'Mo': 'Molybdenum',
    'Ni': 'Nickel',
    'Te': 'Tellurium',
    'Zn': 'Zinc',
    'Pb': 'Lead',
    'Non-specific': 'Non-specific'
}


# Get hmm_len and no_seq from hmm files
hmm_len_d = {}
hmm_seq_no_d = {}

for hmm_file in glob(f"{hmm_path}/*.hmm"):
    #Get model name
    model_id = hmm_file.split("/")[-1].split(".")[0]

    with open(hmm_file, 'r') as f:
        lines = f.readlines()
    # HMM length is in the 3rd line, no. seqs is in 11th
    model_len = lines[2].split(" ")[-1].strip()
    model_seq_no = lines[10].split(" ")[-1].strip()

    hmm_len_d[model_id] = model_len
    hmm_seq_no_d[model_id] = model_seq_no

# Load existing metadata JSON file
with open(metadata_file, 'r') as f:
    metadata = json.load(f)

# Convert metadata list to DataFrame for merging
metadata_df = pd.DataFrame(metadata)
metadata_df.rename(columns={'hmm_name': 'model'}, inplace=True)

metadata_df['length'] = metadata_df['model'].map(hmm_len_d)
metadata_df['no_sequences'] = metadata_df['model'].map(hmm_seq_no_d)

# Extract unique metal types for filtering
all_metals = []
for metal in metadata_df['metal']:
    all_metals.extend(split_metal_types(metal))
unique_metals = sorted(list(set(all_metals)))

# Extract unique resistance types for filtering
unique_resistance_types = metadata_df['resistance_type'].unique().tolist()

# Create a dictionary to group related models
# Pattern: base_name_number (e.g., As_lyase_1, As_lyase_2)
model_groups = defaultdict(list)
pattern = re.compile(r'(.+)_(\d+)$')

for model in metadata_df['model']:
    match = pattern.match(model)
    if match:
        base_name = match.group(1)
        model_groups[base_name].append(model)

# Build final data list
final_data = []
for _, row in metadata_df.iterrows():
    # Find related models
    related_models = []
    match = pattern.match(row['model'])
    if match:
        base_name = match.group(1)
        related_models = [m for m in model_groups[base_name] if m != row['model']]

    # Split metal types
    metals = split_metal_types(row['metal'])
    
    # Map metal abbreviations to full names
    metals_full = [metal_name_map.get(m, m) for m in metals]

    model_entry = {
        'id': row['model'],
        'metal_type': metals_full,
        'resistance_type': row['resistance_type'],
        'length': int(row['length']) if not pd.isna(row['length']) else None,
        'sequences_count': int(row['no_sequences']) if not pd.isna(row['no_sequences']) else None,
        'related_models': related_models,
        'rep_sequence': row['rep_sequence'],
        'best_foldseek_hit': row['best_foldseek_hit'],
        'foldseek_hit_evalue': row['foldseek_hit_evalue'],
        'hmm_file': f"hmms/{row['model']}.hmm",
        'alignment_file': f"alignments/{row['model']}.sto",
        'sequence_file': f"sequences/{row['model']}.fasta"
    }
    final_data.append(model_entry)

# Create the final JSON structure
output_data = {
    'models': final_data,
    'metadata': {
        'total_models': len(final_data),
        'metal_types': [metal_name_map.get(m, m) for m in unique_metals],
        'resistance_types': unique_resistance_types
    }
}

# Save to JSON file
with open('browse_models_data.json', 'w') as f:
    json.dump(output_data, f, indent=2)

print(f"Successfully created browse_models_data.json with {len(final_data)} models")
print(f"Found {len(model_groups)} groups of related models")
