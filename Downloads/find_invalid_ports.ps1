$ErrorActionPreference = 'Stop'

$lines = Get-Content 'c:\Users\User\Downloads\CIRCUITFILE.MD'
$content = $lines -join "`n"

# Extract all defined node names and their gate types
$nodePat = '(?m)^\s*([a-z_][a-z_0-9]*)\s*\[([^\]]+)\]'
$nodeDefs = [regex]::Matches($content, $nodePat) | ForEach-Object {
    [PSCustomObject]@{
        Name = $_.Groups[1].Value
        GateType = $_.Groups[2].Value
    }
}

# Build a map of node -> valid ports based on gate type
$nodePorts = @{}
foreach ($nd in $nodeDefs) {
    $gt = $nd.GateType.ToLower()
    $ports = @()
    
    if ($gt -match 'd flip-flop|d-ff|d_ff') {
        # D flip-flop: d, clk, enable, preset, reset, q, q_bar
        $ports = @('d','clk','enable','preset','reset','q','q_bar','s','r')
    } elseif ($gt -match 'sr.?latch|sr_latch') {
        $ports = @('s','r','q','q_bar','set','reset')
    } elseif ($gt -match 'tristate|tri-state|2 tristate|3 tristate') {
        $ports = @('in0','in1','in2','in3','ctrl0','ctrl1','ctrl2','out0','out1','out2')
    } elseif ($gt -match 'mux|multiplexer') {
        $ports = @('in0','in1','in2','in3','ctrl0','ctrl1','ctrl2','out0','out1')
    } elseif ($gt -match '\band\b') {
        $ports = @('in0','in1','in2','in3','in4','out','out0')
    } elseif ($gt -match '\bor\b') {
        $ports = @('in0','in1','in2','out','out0')
    } elseif ($gt -match '\bxor\b') {
        $ports = @('in0','in1','out','out0')
    } elseif ($gt -match '\bxnor\b') {
        $ports = @('in0','in1','out','out0')
    } elseif ($gt -match '\bnor\b') {
        $ports = @('in0','in1','in2','out','out0')
    } elseif ($gt -match '\bnand\b') {
        $ports = @('in0','in1','in2','out','out0')
    } else {
        # Default: assume standard ports
        $ports = @('in0','in1','in2','in3','ctrl0','ctrl1','out','out0','out1','q','q_bar','d','clk','enable','preset','reset','s','r','set')
    }
    
    if ($nodePorts.ContainsKey($nd.Name)) {
        # Merge ports
        $nodePorts[$nd.Name] = ($nodePorts[$nd.Name] + $ports) | Sort-Object -Unique
    } else {
        $nodePorts[$nd.Name] = $ports | Sort-Object -Unique
    }
}

# Now check all wire references for invalid ports
$refPat = '(?:(?:->|<-)\s+)?([a-z_][a-z_0-9]*)\.([a-z_0-9]+)'
$falsePositives = @('element','element2','particle','color','group','role','vector','personality','archetype','field','physics','geology','biochemistry','science','isomorphism','receptor','location','note','reverse','forward','signal','wire','bio','geo','phys','www','http','https')

$invalidPortRefs = @()

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    $matches = [regex]::Matches($line, $refPat)
    foreach ($m in $matches) {
        $nodeName = $m.Groups[1].Value
        $port = $m.Groups[2].Value
        if ($falsePositives -contains $nodeName) { continue }
        if (-not $nodePorts.ContainsKey($nodeName)) { continue } # undefined node, already checked
        
        $validPorts = $nodePorts[$nodeName]
        if ($validPorts -notcontains $port) {
            # Check if it's a known port pattern
            if ($port -match '^(out|out0|out1|out2|out3|q|q_bar|ctrl|ctrl0|ctrl1|ctrl2|ctrl3|in|in0|in1|in2|in3|in4|d|clk|enable|preset|reset|s|r|set)$') {
                $invalidPortRefs += [PSCustomObject]@{
                    Node = $nodeName
                    Port = $port
                    ValidPorts = $validPorts -join ','
                    Line = $i + 1
                    Content = $line
                }
            }
        }
    }
}

Write-Output "=== INVALID PORT REFERENCES ==="
Write-Output "Total: $($invalidPortRefs.Count)"
Write-Output ""

if ($invalidPortRefs.Count -gt 0) {
    $invalidPortRefs | Sort-Object Node, Line | ForEach-Object {
        $lc = $_.Content
        if ($lc.Length -gt 250) { $lc = $lc.Substring(0, 250) + "..." }
        Write-Output "Line $($_.Line): $($_.Node).$($_.Port) — valid ports: $($_.ValidPorts)"
        Write-Output "  $lc"
        Write-Output ""
    }
}
