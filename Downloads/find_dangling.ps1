$ErrorActionPreference = 'Stop'

$f2 = Get-Content 'c:\Users\User\Downloads\CIRCUITFILE.MD' -Raw
$lines2 = Get-Content 'c:\Users\User\Downloads\CIRCUITFILE.MD'

# Get all defined node names
$pat = '(?m)^\s*([a-z_][a-z_0-9]*)\s*\['
$definedNodes = [regex]::Matches($f2, $pat) | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique

# Find all wire references: -> nodename. or <- nodename. 
$wirePat = '(?:->|<-)\s+([a-z_][a-z_0-9]*)\s*[\.\[]'
$wireRefs = [regex]::Matches($f2, $wirePat) | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique

# Also find references in signal comments: SIGNAL: ... nodename.out
$sigPat = '\b([a-z_][a-z_0-9]*)\.(?:out|out0|out1|out2|q|q_bar|ctrl|ctrl0|ctrl1|ctrl2|in|in0|in1|in2|in3|d|clk|enable|preset|reset|s)\b'
$sigRefs = [regex]::Matches($f2, $sigPat) | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique

$allRefs = ($wireRefs + $sigRefs) | Sort-Object -Unique

# Dangling = referenced but not defined
$dangling = $allRefs | Where-Object { $definedNodes -notcontains $_ }

Write-Output "=== DANGLING WIRES IN CIRCUITFILE.MD ==="
Write-Output "Defined nodes: $($definedNodes.Count)"
Write-Output "Referenced nodes: $($allRefs.Count)"
Write-Output "Dangling (referenced but not defined): $($dangling.Count)"
Write-Output ""

if ($dangling.Count -gt 0) {
    # For each dangling node, find which lines reference it
    foreach ($d in $dangling) {
        Write-Output "--- Dangling: $d ---"
        $matchLines = @()
        for ($i = 0; $i -lt $lines2.Count; $i++) {
            if ($lines2[$i] -match "\b$([regex]::Escape($d))\.(?:out|out0|out1|out2|q|q_bar|ctrl|ctrl0|ctrl1|ctrl2|in|in0|in1|in2|in3|d|clk|enable|preset|reset|s)\b") {
                $matchLines += ($i + 1)
            }
        }
        if ($matchLines.Count -gt 0) {
            Write-Output "  Referenced on lines: $($matchLines -join ', ')"
            # Show first 3 references
            $shown = 0
            foreach ($ml in $matchLines) {
                if ($shown -ge 3) { break }
                $lineContent = $lines2[$ml - 1]
                if ($lineContent.Length -gt 200) {
                    $lineContent = $lineContent.Substring(0, 200) + "..."
                }
                Write-Output "  Line ${ml}: $lineContent"
                $shown++
            }
        }
        Write-Output ""
    }
}
