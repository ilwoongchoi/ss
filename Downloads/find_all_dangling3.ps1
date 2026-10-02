$ErrorActionPreference = 'Stop'

$lines = Get-Content 'c:\Users\User\Downloads\CIRCUITFILE.MD'
$content = $lines -join "`n"

# Extract all defined node names
$nodePat = '(?m)^\s*([a-z_][a-z_0-9]*)\s*\['
$definedNodes = [regex]::Matches($content, $nodePat) | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
$definedSet = [System.Collections.Generic.HashSet[string]]::new()
foreach ($n in $definedNodes) { [void]$definedSet.Add($n) }

# Now check EVERY line for -> and <- patterns and extract target/source nodes
# -> nodename.port = this node outputs TO nodename
# <- nodename.port = this node inputs FROM nodename

$wireIssues = @()

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    
    # Find all -> target.port patterns (output wires)
    $outMatches = [regex]::Matches($line, '->\s+([a-z_][a-z_0-9]*)\.([a-z_0-9]+)')
    foreach ($m in $outMatches) {
        $target = $m.Groups[1].Value
        $port = $m.Groups[2].Value
        if (-not $definedSet.Contains($target)) {
            $wireIssues += [PSCustomObject]@{
                Type = 'OUTPUT_TO_UNDEFINED'
                Node = $target
                Port = $port
                Line = $i + 1
                Direction = '->'
                Content = $line
            }
        }
    }
    
    # Find all <- source.port patterns (input wires)
    $inMatches = [regex]::Matches($line, '<-\s+([a-z_][a-z_0-9]*)\.([a-z_0-9]+)')
    foreach ($m in $inMatches) {
        $source = $m.Groups[1].Value
        $port = $m.Groups[2].Value
        if (-not $definedSet.Contains($source)) {
            $wireIssues += [PSCustomObject]@{
                Type = 'INPUT_FROM_UNDEFINED'
                Node = $source
                Port = $port
                Line = $i + 1
                Direction = '<-'
                Content = $line
            }
        }
    }
}

Write-Output "=== WIRE REFERENCES TO UNDEFINED NODES ==="
Write-Output "Total issues: $($wireIssues.Count)"
Write-Output ""

if ($wireIssues.Count -gt 0) {
    $wireIssues | Sort-Object Line | ForEach-Object {
        $lc = $_.Content
        if ($lc.Length -gt 300) { $lc = $lc.Substring(0, 300) + "..." }
        Write-Output "Line $($_.Line) [$($_.Direction) $($_.Node).$($_.Port)] $($_.Type)"
        Write-Output "  $lc"
        Write-Output ""
    }
} else {
    Write-Output "NONE - all wire targets and sources are defined"
}

# Also check: nodes that have inputs referencing ports that don't exist on the source
# e.g., nodeA.out5 when nodeA only has out0, out1
Write-Output ""
Write-Output "=== CHECKING ORPHAN NODE INPUTS ==="
$orphanList = @(
    'actin_myosin_muscle','betti_11_residual','betti_7_residual','bile_salt_emulsifier',
    'blood_clot_fibrin','blue_tack_left_frontalis_inner_vertical_fall',
    'choline_glabella_midline_between_acetylcholine','cloudy_semen_buffer',
    'cochlea_hair_cell','cytochrome_c_oxidase_ctrl1_combined',
    'cytochrome_c_oxidase_retrograde_tg','ear_wax_sebum_filter',
    'fecal_brown_energy','fever_pyrogen_interleukin','glucagon_glucose_release',
    'grape_anti_peonidine','growth_hormone_igf1','hair_keratin_silk',
    'histosol_ctrl1_and','imagining_chopped_onion_night','insulin_glucose_storage',
    'interferon_antiviral','java_house_frozen_onion_cox','ketone_body_starvation',
    'kidney_glomerulus_filtration','lactate_hmp_shunt',
    'left_endorphin_electron_neutrino_rerouted','left_lumbar_hernia_point',
    'leptin_adiposity_signal','mast_cell_histamine',
    'melatonin_middle_lower_ridge_overlap','melatonin_upper_middle_third_overlap',
    'methionine_jesus_right_waist_forward_cross','microbiome_commensal',
    'mucus_protective_gel','myelin_sheath_nerve','nail_keratin_claw',
    'oxytocin_grit','podzol_complex_gate_after_podzol','retina_photoreceptor',
    'right_lip_orbicularis_oculi_endorphin','salivary_amylase_starch',
    'strawberry_buffer','substance_p','sweat_electrolyte',
    'synaptic_vesicle_release','t_ff_out','tears_lacrimal_salt',
    'testosterone_dht_receptor','thyroid_t3_t4','tooth_enamel_hydroxyapatite'
)

foreach ($orphan in $orphanList) {
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match "^\s*$([regex]::Escape($orphan))\s*\[") {
            $inputs = @()
            for ($j = $i + 1; $j -lt [Math]::Min($i + 50, $lines.Count); $j++) {
                if ($lines[$j] -match '^\s*[a-z_][a-z_0-9]*\s*\[') { break }
                $inMatches = [regex]::Matches($lines[$j], '<-\s+([a-z_][a-z_0-9]*)\.([a-z_0-9]+)')
                foreach ($m in $inMatches) {
                    $inputs += "$($m.Groups[1].Value).$($m.Groups[2].Value)"
                }
            }
            if ($inputs.Count -gt 0) {
                Write-Output "${orphan} (line $($i+1)): inputs <- $($inputs -join ', ')"
            } else {
                Write-Output "${orphan} (line $($i+1)): NO inputs (source-only node)"
            }
            break
        }
    }
}
