import csv


def main():
    categories = {
        "physics": [
            "tunneling", "diffraction", "interference", "entanglement", "decoherence",
            "phase_transition", "criticality", "symmetry_breaking", "chirality",
            "spin_orbit", "magnetism", "superconductivity", "superfluidity",
            "plasma_confinement", "radiation_transport", "shock_wave", "turbulence",
            "renormalization", "holography", "black_hole", "event_horizon",
            "gravitational_lensing", "cosmic_rays", "neutrino_oscillation",
            "nuclear_fusion", "nuclear_fission", "pair_production", "synchrotron",
            "bremsstrahlung", "photodissociation", "photoelectric_effect",
            "band_structure", "fermi_surface", "phonon", "polaron",
        ],
        "chemistry": [
            "redox", "acid_base", "hydrolysis", "polymerization", "isomerization",
            "catalysis", "chelation", "solvation", "precipitation",
            "adsorption", "desorption", "diffusion", "osmosis",
            "ligand_binding", "enzyme_kinetics", "free_energy",
            "reaction_coordinate", "transition_state",
        ],
        "biology": [
            "respiration", "photosynthesis", "glycolysis", "krebs_cycle",
            "fermentation", "electron_transport_chain", "membrane_potential",
            "ion_channel", "synaptic_transmission", "neurotransmitter_release",
            "hormone_binding", "signal_transduction", "gene_expression",
            "protein_folding", "chaperone", "autophagy", "apoptosis",
            "cell_cycle", "mitosis", "meiosis", "morphogenesis",
            "homeostasis", "inflammation", "oxidative_stress", "mitochondrial_fission",
        ],
        "neurochem": [
            "dopamine", "serotonin", "gaba", "glutamate", "acetylcholine",
            "noradrenaline", "adrenaline", "vasopressin", "oxytocin",
            "histamine", "melatonin", "cortisol", "endorphin",
        ],
        "systems": [
            "feedback_loop", "hysteresis", "limit_cycle", "attractor", "bifurcation",
            "stability", "resilience", "adaptation", "plasticity",
            "synchronization", "phase_lock", "oscillation", "entrainment",
        ],
    }

    # Expand to ~1000 items with templates
    templates = [
        "{base}_transport",
        "{base}_flux",
        "{base}_coupling",
        "{base}_gradient",
        "{base}_gate",
        "{base}_seam",
        "{base}_bridge",
        "{base}_band",
        "{base}_axis",
        "{base}_sink",
    ]

    concepts = []
    for cat, items in categories.items():
        for base in items:
            concepts.append((base, cat))
            for t in templates:
                concepts.append((t.format(base=base), cat))

    # Dedup
    seen = set()
    out = []
    for name, cat in concepts:
        if name in seen:
            continue
        seen.add(name)
        out.append((name, cat))

    with open("CONCEPTS_LIST.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["concept", "category"])
        for name, cat in out:
            w.writerow([name, cat])

    print(f"Wrote CONCEPTS_LIST.csv ({len(out)} concepts)")


if __name__ == "__main__":
    main()
