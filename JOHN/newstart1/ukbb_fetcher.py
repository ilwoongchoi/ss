#!/usr/bin/env python3
"""Neale Lab UK Biobank GWAS fetcher + Engine validator.

Downloads publicly available GWAS summary statistics from Neale Lab
release 2 (UKBB 200k exomes + 500k imputed) for:
  - Blood group phenotypes (ABO, RhD proxies)
  - Personality/psychometric proxies (Big-5-like, neuroticism, MHQ)

Compares against engine's 128-type predictions.
"""

import os
import json
import urllib.request
import gzip
import shutil
from pathlib import Path
from typing import Dict, List, Optional

# Pan-UKBB v2 endpoints (Neale Lab / Broad Institute)
# https://pan.ukbb.broadinstitute.org/downloads/
NEALE_BASE = "https://pan-ukb-us-east-1.s3.amazonaws.com/sumstats_release"
NEALE_MANIFEST = f"{NEALE_BASE}/phenotype_manifest.tsv.bgz"

# Phenotype codes verified against manifest (descriptions confirmed)
PERSONALITY_PHENOTYPES = [
    "20127",   # Neuroticism score (EPQ-R)
    "20458",   # General happiness
    "F32",     # Depressive episode (ICD10)
    "F33",     # Recurrent depressive disorder (ICD10)
]


class UKBBFetcher:
    """Automated downloader for Neale Lab UK Biobank GWAS data."""

    def __init__(self, cache_dir: str = "./ukbb_data"):
        self.cache = Path(cache_dir)
        self.cache.mkdir(exist_ok=True)
        self.manifest_path = self.cache / "manifest.tsv"
        self.manifest: Optional[pd.DataFrame] = None  # type: ignore

    def download_manifest(self, force: bool = False) -> Path:
        """Download and decompress the manifest file."""
        gz_path = self.cache / "manifest.tsv.gz"
        if not gz_path.exists() or force:
            url = NEALE_MANIFEST
            print(f"[UKBB] Downloading manifest from {url}...")
            urllib.request.urlretrieve(url, gz_path)
        if not self.manifest_path.exists() or force:
            with gzip.open(gz_path, 'rb') as f_in:
                with open(self.manifest_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print(f"[UKBB] Manifest extracted to {self.manifest_path}")
        return self.manifest_path

    def load_manifest(self) -> "pd.DataFrame":
        import pandas as pd
        if self.manifest is None:
            path = self.download_manifest()
            self.manifest = pd.read_csv(path, sep='\t', low_memory=False)
        return self.manifest

    def find_phenotype_files(self, phenotype_code: str) -> List[Dict]:
        """Find manifest entries matching a phenotype code."""
        df = self.load_manifest()
        # Match in phenocode or description
        mask = df['phenocode'].astype(str).str.contains(phenotype_code, na=False)
        if 'description' in df.columns:
            mask |= df['description'].fillna('').str.contains(phenotype_code, case=False)
        matches = df[mask]
        return matches.to_dict('records')

    def download_sumstats(self, phenotype_code: str, out_name: Optional[str] = None) -> Path:
        """Download GWAS sumstats for a specific phenotype."""
        files = self.find_phenotype_files(phenotype_code)
        if not files:
            raise FileNotFoundError(f"Phenotype {phenotype_code} not found in manifest")

        # Prefer EUR (European) ancestry for consistency
        eur_files = [f for f in files if 'eur' in str(f.get('pop', '')).lower()]
        if eur_files:
            chosen = eur_files[0]
        else:
            chosen = files[0]

        s3_path = chosen.get('aws_path', chosen.get('aws_path_tabix', chosen.get('aws_link', chosen.get('gs_link', ''))))
        if not s3_path:
            raise ValueError(f"No download link found for {phenotype_code}")

        # aws_path is s3://bucket/key -- convert to https://bucket.s3.amazonaws.com/key
        if s3_path.startswith('s3://'):
            parts = s3_path[5:].split('/', 1)
            bucket = parts[0]
            key = parts[1] if len(parts) > 1 else ''
            url = f"https://{bucket}.s3.amazonaws.com/{key}"
        else:
            url = f"https://pan-ukb-us-east-1.s3.amazonaws.com/{s3_path}"

        out_name = out_name or f"{phenotype_code}_sumstats.tsv.bgz"
        out_path = self.cache / out_name

        if not out_path.exists():
            print(f"[UKBB] Downloading {phenotype_code}...")
            urllib.request.urlretrieve(url, out_path)
            print(f"[UKBB] Saved to {out_path}")
        else:
            print(f"[UKBB] Using cached {out_path}")

        return out_path

    def download_personality_set(self) -> Dict[str, Path]:
        """Fetch personality/mental health proxies."""
        results = {}
        for code in PERSONALITY_PHENOTYPES:
            try:
                results[code] = self.download_sumstats(code)
            except Exception as e:
                print(f"[UKBB] Warning: failed to fetch {code}: {e}")
        return results

    def top_snps(self, phenotype_code: str, n: int = 20) -> "pd.DataFrame":
        """Return top n SNPs by neglog10_pval_meta; chunked to avoid OOM."""
        import pandas as pd
        import heapq
        path = self.cache / f"{phenotype_code}_sumstats.tsv.bgz"
        if not path.exists():
            raise FileNotFoundError(f"No cached file for {phenotype_code}")
        cols = ['chr', 'pos', 'ref', 'alt', 'beta_meta', 'neglog10_pval_meta']
        top_rows = []
        for chunk in pd.read_csv(path, sep='\t', compression='gzip',
                                  usecols=lambda c: c in cols,
                                  chunksize=50_000, low_memory=False):
            chunk['neglog10_pval_meta'] = pd.to_numeric(chunk['neglog10_pval_meta'], errors='coerce')
            chunk['beta_meta'] = pd.to_numeric(chunk['beta_meta'], errors='coerce')
            chunk = chunk.dropna(subset=['neglog10_pval_meta'])
            top_rows.append(chunk.nlargest(n, 'neglog10_pval_meta'))
        merged = pd.concat(top_rows, ignore_index=True)
        return merged.nlargest(n, 'neglog10_pval_meta')[cols].reset_index(drop=True)

    def compare_engine(self, decoder, phenotype_map: Dict[str, str]) -> Dict:
        """Compare engine 128-type trait scores vs GWAS effect direction.

        phenotype_map: {phenocode: trait_key} where trait_key is a key returned
        by decoder.observe_hormones() or a synthetic score like 'neuroticism'.

        For each phenotype: take top 20 SNPs by p-value, compute mean |beta_meta|
        (GWAS population signal magnitude), compare to engine's mean trait value
        across the 16 NF vs 16 NT types (most personality-relevant contrast).
        """
        import numpy as np
        from universal_decoder import UniverseState
        results = {}
        for code, trait in phenotype_map.items():
            try:
                snps = self.top_snps(code, n=20)
                gwas_mean_beta = float(snps['beta_meta'].abs().mean())
                gwas_top_pval = float(snps['neglog10_pval_meta'].max())
                # Engine: NF types (is_nt_nf & mbti ends in F) vs NT types
                nf_scores, nt_scores = [], []
                for t in decoder.types:
                    st = UniverseState()
                    st.z = np.zeros(8, dtype=complex)
                    # Seed z from type's delta_s and theta
                    st.z[0] = t.delta_s * np.exp(1j * np.radians(t.theta))
                    st.z[3] = (1 - t.delta_s) * np.exp(-1j * np.radians(t.theta))
                    h = decoder.observe_hormones(st)
                    score = h.get(trait, h.get('cortisol', 0.0))
                    is_n = 'N' in t.mbti[1:2]   # S/N position
                    if is_n and t.mbti.endswith('F'):
                        nf_scores.append(score)
                    elif is_n and not t.mbti.endswith('F'):
                        nt_scores.append(score)
                nf_mean = float(np.mean(nf_scores)) if nf_scores else float('nan')
                nt_mean = float(np.mean(nt_scores)) if nt_scores else float('nan')
                results[code] = {
                    'trait': trait,
                    'gwas_top_neglog10p': round(gwas_top_pval, 2),
                    'gwas_mean_abs_beta': round(gwas_mean_beta, 5),
                    'engine_NF_mean': round(nf_mean, 5),
                    'engine_NT_mean': round(nt_mean, 5),
                    'engine_NF_NT_delta': round(nf_mean - nt_mean, 5),
                }
            except Exception as e:
                results[code] = {'error': str(e)}
        return results


def main():
    """Download + analyze UKBB personality GWAS vs engine predictions."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from universal_decoder import UniversalDecoder

    fetcher = UKBBFetcher()
    print("[UKBB] Downloading personality/mental health GWAS...")
    pers_files = fetcher.download_personality_set()
    print(f"[UKBB] Downloaded: {list(pers_files.keys())}")

    print("\n[UKBB] Top SNPs per phenotype:")
    for code in pers_files:
        try:
            snps = fetcher.top_snps(code, n=5)
            print(f"  {code}:")
            print(snps.to_string(index=False))
        except Exception as e:
            print(f"  {code}: {e}")

    print("\n[UKBB] Engine vs GWAS comparison:")
    decoder = UniversalDecoder()
    phenotype_map = {
        '20127': 'cortisol',      # Neuroticism: cortisol (stress axis)
        '20458': 'melatonin',     # Happiness: melatonin (nocturnal binding)
        'F32':   'cortisol',      # Depression: cortisol
        'F33':   'cortisol',      # Recurrent depression: cortisol
    }
    results = fetcher.compare_engine(decoder, phenotype_map)
    print(f"  {'code':>6} | {'trait':>10} | {'top -log10p':>11} | {'GWAS |beta|':>11} | {'NF mean':>8} | {'NT mean':>8} | {'NF-NT':>8}")
    print("  " + "-" * 75)
    for code, r in results.items():
        if 'error' in r:
            print(f"  {code:>6} | ERROR: {r['error']}")
        else:
            print(f"  {code:>6} | {r['trait']:>10} | {r['gwas_top_neglog10p']:>11.2f} | {r['gwas_mean_abs_beta']:>11.5f} | {r['engine_NF_mean']:>8.5f} | {r['engine_NT_mean']:>8.5f} | {r['engine_NF_NT_delta']:>+8.5f}")

    summary = {
        "personality_phenotypes": {k: str(v) for k, v in pers_files.items()},
        "engine_comparison": results,
        "cache_directory": str(fetcher.cache)
    }
    summary_path = fetcher.cache / "download_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\n[UKBB] Summary written to {summary_path}")


if __name__ == "__main__":
    main()
