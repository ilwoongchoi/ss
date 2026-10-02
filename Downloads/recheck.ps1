$ErrorActionPreference = 'Stop'

$lines = Get-Content 'c:\Users\User\Downloads\CIRCUITFILE.MD'
$content = $lines -join "`n"

# 1. Extract all defined node names
$nodePat = '(?m)^\s*([a-z_][a-z_0-9]*)\s*\['
$definedNodes = [regex]::Matches($content, $nodePat) | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
$definedSet = [System.Collections.Generic.HashSet[string]]::new()
foreach ($n in $definedNodes) { [void]$definedSet.Add($n) }

Write-Output "Defined nodes: $($definedNodes.Count)"
Write-Output ""

# 2. Check ALL wire references (-> and <-) for undefined nodes
$falsePositives = @('element','element2','particle','color','group','role','vector','personality','archetype','field','physics','geology','biochemistry','science','isomorphism','receptor','location','note','reverse','forward','signal','wire','bio','geo','phys','www','http','https','Horsehead_Nebula','Vega')

$wireIssues = @()
$allRefs = @()

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    
    # -> target.port
    $outMatches = [regex]::Matches($line, '->\s+([a-z_][a-z_0-9]*)\.([a-z_0-9]+)')
    foreach ($m in $outMatches) {
        $target = $m.Groups[1].Value
        $port = $m.Groups[2].Value
        $allRefs += [PSCustomObject]@{Node=$target; Port=$port; Line=$i+1; Dir='->'}
        if (-not $definedSet.Contains($target) -and $falsePositives -notcontains $target) {
            $wireIssues += [PSCustomObject]@{Type='OUTPUT_TO_UNDEFINED'; Node=$target; Port=$port; Line=$i+1; Dir='->'; Content=$line}
        }
    }
    
    # <- source.port
    $inMatches = [regex]::Matches($line, '<-\s+([a-z_][a-z_0-9]*)\.([a-z_0-9]+)')
    foreach ($m in $inMatches) {
        $source = $m.Groups[1].Value
        $port = $m.Groups[2].Value
        $allRefs += [PSCustomObject]@{Node=$source; Port=$port; Line=$i+1; Dir='<-'}
        if (-not $definedSet.Contains($source) -and $falsePositives -notcontains $source) {
            $wireIssues += [PSCustomObject]@{Type='INPUT_FROM_UNDEFINED'; Node=$source; Port=$port; Line=$i+1; Dir='<-'; Content=$line}
        }
    }
}

Write-Output "=== DANGLING WIRES (referenced node not defined) ==="
Write-Output "Total: $($wireIssues.Count)"
Write-Output ""
if ($wireIssues.Count -gt 0) {
    $wireIssues | Sort-Object Line | ForEach-Object {
        $lc = $_.Content
        if ($lc.Length -gt 300) { $lc = $lc.Substring(0,300) + "..." }
        Write-Output "Line $($_.Line) [$($_.Dir) $($_.Node).$($_.Port)] $($_.Type)"
        Write-Output "  $lc"
        Write-Output ""
    }
}

# 3. Orphan nodes (defined but never referenced)
$referencedNodes = $allRefs | Where-Object { $falsePositives -notcontains $_.Node } | ForEach-Object { $_.Node } | Sort-Object -Unique
$orphanNodes = $definedNodes | Where-Object { $referencedNodes -notcontains $_ }
Write-Output ""
Write-Output "=== ORPHAN NODES (defined but never referenced by any wire) ==="
Write-Output "Total: $($orphanNodes.Count)"
$orphanNodes | ForEach-Object { Write-Output "  $_" }

# 4. Invalid port references - check gate types
$nodeDefs = [regex]::Matches($content, $nodePat) | ForEach-Object {
    $gt = $_.Groups[2].Value
    # Get the full line for gate type
    $lineNum = ($_.Index -split "`n").Count
    [PSCustomObject]@{Name=$_.Groups[1].Value; GateType=$gt}
}

# Also check for alias nodes
$aliasPat = '(?m)^\s*([a-z_][a-z_0-9]*)\s*\[alias:'
$aliasMatches = [regex]::Matches($content, $aliasPat)
foreach ($m in $aliasMatches) {
    Write-Output "ALIAS NODE: $($m.Groups[1].Value)"
}

Write-Output ""
Write-Output "=== NODE GATE TYPES ==="
$gateTypes = $nodeDefs | Group-Object { $_.GateType.Substring(0, [Math]::Min(40, $_.GateType.Length)) } | Sort-Object Count -Descending
$gateTypes | ForEach-Object { Write-Output "  ($($_.Count)) $($_.Name)" }
