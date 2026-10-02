from __future__ import annotations

from pathlib import Path


OUT_DIR = Path("analysis_results")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_MD = OUT_DIR / "external_anchor_closure.md"


def build_report() -> str:
    # External-known anchors only.
    alpha = 7.2973525643e-3
    g_f = 1.1663787e-5
    proton_mass_mev = 938.27208816
    u_quark_mev = 2.16
    d_quark_mev = 4.67
    dark_energy_fraction_nasa = 0.683
    dark_energy_fraction_planck = 0.6847

    # Local residual we are trying to explain; kept here only for comparison.
    residual_gap = 0.01973885682129521

    # Existing edge-stack BW_BW base from current code.
    bw_bw_base = 0.043209876543209874

    # External-derived primitives.
    bm_sm_raw = 8.0 * alpha * g_f
    valence_quark_mass = (2.0 * u_quark_mev) + d_quark_mev
    qcd_binding_fraction = 1.0 - (valence_quark_mass / proton_mass_mev)

    # Candidate projections using only known external numbers.
    bw_bw_dark_nasa = bw_bw_base * dark_energy_fraction_nasa
    bw_bw_dark_planck = bw_bw_base * dark_energy_fraction_planck
    bw_bw_dark_charge_nasa = bw_bw_base * dark_energy_fraction_nasa * (2.0 / 3.0)
    bw_bw_dark_charge_planck = bw_bw_base * dark_energy_fraction_planck * (2.0 / 3.0)
    bw_bw_dark_charge_qcd_nasa = bw_bw_dark_charge_nasa * qcd_binding_fraction
    bw_bw_dark_charge_qcd_planck = bw_bw_dark_charge_planck * qcd_binding_fraction

    lines = []
    lines.append("# External Anchor Closure")
    lines.append("")
    lines.append("## External Inputs")
    lines.append("")
    lines.append(f"- `alpha = {alpha:.13f}`")
    lines.append(f"- `G_F = {g_f:.13e}`")
    lines.append(f"- `m_p = {proton_mass_mev:.8f} MeV`")
    lines.append(f"- `m_u = {u_quark_mev:.2f} MeV`")
    lines.append(f"- `m_d = {d_quark_mev:.2f} MeV`")
    lines.append(f"- `Omega_Lambda (NASA) = {dark_energy_fraction_nasa:.4f}`")
    lines.append(f"- `Omega_Lambda (Planck-style) = {dark_energy_fraction_planck:.4f}`")
    lines.append("")
    lines.append("## Derived From External Physics")
    lines.append("")
    lines.append(f"- `BM_SM_raw = 8 * alpha * G_F = {bm_sm_raw:.17f}`")
    lines.append(f"- `valence_quark_mass(uud) = {valence_quark_mass:.2f} MeV`")
    lines.append(f"- `QCD_binding_fraction = {qcd_binding_fraction:.15f}`")
    lines.append("")
    lines.append("## BW_BW Projection Candidates")
    lines.append("")
    lines.append(f"- `BW_BW_base = {bw_bw_base:.17f}`")
    lines.append(f"- `BW_BW * Omega_Lambda(NASA) = {bw_bw_dark_nasa:.17f}`")
    lines.append(f"- `BW_BW * Omega_Lambda(Planck-style) = {bw_bw_dark_planck:.17f}`")
    lines.append(f"- `BW_BW * Omega_Lambda(NASA) * 2/3 = {bw_bw_dark_charge_nasa:.17f}`")
    lines.append(f"- `BW_BW * Omega_Lambda(Planck-style) * 2/3 = {bw_bw_dark_charge_planck:.17f}`")
    lines.append(f"- `BW_BW * Omega_Lambda(NASA) * 2/3 * QCD = {bw_bw_dark_charge_qcd_nasa:.17f}`")
    lines.append(f"- `BW_BW * Omega_Lambda(Planck-style) * 2/3 * QCD = {bw_bw_dark_charge_qcd_planck:.17f}`")
    lines.append("")
    lines.append("## Comparison To Current Residual")
    lines.append("")
    lines.append(f"- `residual_gap = {residual_gap:.17f}`")
    lines.append(f"- `residual - BM_SM_raw = {residual_gap - bm_sm_raw:.17f}`")
    lines.append(f"- `residual - BW_BW*Omega_Lambda(NASA) = {residual_gap - bw_bw_dark_nasa:.17f}`")
    lines.append(f"- `residual - BW_BW*Omega_Lambda(Planck-style) = {residual_gap - bw_bw_dark_planck:.17f}`")
    lines.append(f"- `residual - BW_BW*Omega_Lambda(NASA)*2/3 = {residual_gap - bw_bw_dark_charge_nasa:.17f}`")
    lines.append(f"- `residual - BW_BW*Omega_Lambda(Planck-style)*2/3 = {residual_gap - bw_bw_dark_charge_planck:.17f}`")
    lines.append(f"- `residual - BW_BW*Omega_Lambda(NASA)*2/3*QCD = {residual_gap - bw_bw_dark_charge_qcd_nasa:.17f}`")
    lines.append(f"- `residual - BW_BW*Omega_Lambda(Planck-style)*2/3*QCD = {residual_gap - bw_bw_dark_charge_qcd_planck:.17f}`")
    lines.append("")
    lines.append("## Verdict")
    lines.append("")
    lines.append("- `BM_SM_raw` by itself is far too small.")
    lines.append("- `BW_BW * Omega_Lambda` alone overshoots the residual scale.")
    lines.append("- `BW_BW * Omega_Lambda * 2/3` is the closest external-only candidate in the current search.")
    lines.append("- Adding `QCD_binding_fraction` after that pushes it away again.")
    lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    OUT_MD.write_text(build_report(), encoding="utf-8")
    print(str(OUT_MD))
