$ErrorActionPreference = 'Stop'

$f1 = Get-Content 'c:\Users\User\Downloads\circuitfile1.md' -Raw
$f2 = Get-Content 'c:\Users\User\Downloads\CIRCUITFILE.MD' -Raw

$pat = '(?m)^\s*([a-z_][a-z_0-9]*)\s*\['

$n1 = [regex]::Matches($f1, $pat) | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
$n2 = [regex]::Matches($f2, $pat) | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique

Write-Output "circuitfile1 nodes: $($n1.Count)"
Write-Output "CIRCUITFILE nodes: $($n2.Count)"

$missing = $n1 | Where-Object { $n2 -notcontains $_ }
Write-Output "Still missing: $($missing.Count)"
if ($missing.Count -gt 0) {
    $missing | ForEach-Object { Write-Output "  $_" }
}

# Check what non-node content exists in circuitfile1.md that's NOT in CIRCUITFILE.MD
# Count lines that are NOT node definitions (headers, comments, blank lines, etc.)
$nodeLines1 = 0
$nonNodeLines1 = 0
foreach ($line in (Get-Content 'c:\Users\User\Downloads\circuitfile1.md')) {
    if ($line -match '^\s*[a-z_][a-z_0-9]*\s*\[') {
        $nodeLines1++
    } else {
        $nonNodeLines1++
    }
}

$nodeLines2 = 0
$nonNodeLines2 = 0
foreach ($line in (Get-Content 'c:\Users\User\Downloads\CIRCUITFILE.MD')) {
    if ($line -match '^\s*[a-z_][a-z_0-9]*\s*\[') {
        $nodeLines2++
    } else {
        $nonNodeLines2++
    }
}

Write-Output ""
Write-Output "circuitfile1.md: $nodeLines1 node-def lines, $nonNodeLines1 non-node lines"
Write-Output "CIRCUITFILE.MD: $nodeLines2 node-def lines, $nonNodeLines2 non-node lines"

# Check for section headers / comments in circuitfile1.md not in CIRCUITFILE.MD
$headers1 = [regex]::Matches($f1, '(?m)^#+\s.*$') | ForEach-Object { $_.Value.Trim() } | Sort-Object -Unique
$headers2 = [regex]::Matches($f2, '(?m)^#+\s.*$') | ForEach-Object { $_.Value.Trim() } | Sort-Object -Unique

$missingHeaders = $headers1 | Where-Object { $headers2 -notcontains $_ }
Write-Output ""
Write-Output "Missing headers/comments: $($missingHeaders.Count)"
$missingHeaders | Select-Object -First 30 | ForEach-Object { Write-Output "  $_" }
