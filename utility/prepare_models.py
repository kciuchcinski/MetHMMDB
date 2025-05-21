import os
import json

hmms_dir = "HMMS"

metal_map = {
    "Ag": "Silver",
    "As": "Arsenic",
    "Cd": "Cadmium",
    "Co": "Cobalt",
    "Cr": "Chromium",
    "Cu": "Copper",
    "Fe": "Iron",
    "Hg": "Mercury",
    "Mn": "Manganese",
    "Ni": "Nickel",
    "Pb": "Lead",
    "Sb": "Antimony",
    "Se": "Selenium",
    "Te": "Tellurium",
    "Zn": "Zinc"
}

models = []
for fname in os.listdir(hmms_dir):
    if fname.endswith('.hmm'):
        base = fname[:-4]  # Remove '.hmm'
        parts = base.split('_')
        if len(parts) >= 3:
            metal = parts[0]
            mechanism = parts[1]
            gene_id = parts[2]
            model_id = base
            description = f"Profile HMM for {metal} {mechanism} gene {gene_id}."
            models.append({
                "id": model_id,
                "metal": metal,
                "mechanism": mechanism,
                "gene_id": gene_id,
                "description": description
            })

with open("models.json", "w") as f:
    json.dump(models, f, indent=2)
