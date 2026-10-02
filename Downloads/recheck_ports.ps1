$ErrorActionPreference = 'Stop'

$lines = Get-Content 'c:\Users\User\Downloads\CIRCUITFILE.MD'
$content = $lines -join "`n"

# Extract all defined node names and their gate type lines
$nodePat = '(?m)^\s*([a-z_][a-z_0-9]*)\s*\[([^\]]+)\]'
$nodePorts = @{}

$nodeDefs = [regex]::Matches($content, $nodePat)
foreach ($nd in $nodeDefs) {
    $name = $nd.Groups[1].Value
    $gt = $nd.Groups[2].Value.ToLower()
    $ports = @()
    
    if ($gt -match 'd flip.?flop|d.?ff') {
        $ports = @('d','clk','enable','preset','reset','q','q_bar','s','r','set')
    } elseif ($gt -match 'sr.?latch') {
        $ports = @('s','r','q','q_bar','set','reset')
    } elseif ($gt -match 'tristate|tri-state|2 tristate|3 tristate|1 tristate') {
        $ports = @('in0','in1','in2','in3','ctrl0','ctrl1','ctrl2','out0','out1','out2','out')
    } elseif ($gt -match 'mux|multiplexer') {
        $ports = @('in0','in1','in2','in3','ctrl0','ctrl1','ctrl2','out0','out1','out')
    } elseif ($gt -match 'buffer') {
        $ports = @('in0','in1','out0','out1','out')
    } elseif ($gt -match 'alias') {
        $ports = @('in0','out','out0')
    } elseif ($gt -match '\band\b') {
        $ports = @('in0','in1','in2','in3','in4','out','out0')
    } elseif ($gt -match '\bor\b') {
        $ports = @('in0','in1','in2','in3','in4','out','out0')
    } elseif ($gt -match '\bxor\b') {
        $ports = @('in0','in1','in2','out','out0')
    } elseif ($gt -match '\bxnor\b') {
        $ports = @('in0','in1','in2','out','out0')
    } elseif ($gt -match '\bnor\b') {
        $ports = @('in0','in1','in2','out','out0')
    } elseif ($gt -match '\bnand\b') {
        $ports = @('in0','in1','in2','out','out0')
    } else {
        $ports = @('in0','in1','in2','in3','in4','ctrl0','ctrl1','ctrl2','ctrl3','out','out0','out1','out2','q','q_bar','d','clk','enable','preset','reset','s','r','set')
    }
    
    if ($nodePorts.ContainsKey($name)) {
        $nodePorts[$name] = ($nodePorts[$name] + $ports) | Sort-Object -Unique
    } else {
        $nodePorts[$name] = $ports | Sort-Object -Unique
    }
}

# Check all wire references for invalid ports
$falsePositives = @('element','element2','particle','color','group','role','vector','personality','archetype','field','physics','geology','biochemistry','science','isomorphism','receptor','location','note','reverse','forward','signal','wire','bio','geo','phys','www','http','https','Horsehead_Nebula','Vega')

$invalidPortRefs = @()
$validPortPattern = '^(out|out0|out1|out2|out3|out_1|out_2|q|q_bar|ctrl|ctrl0|ctrl1|ctrl2|ctrl3|in|in0|in1|in2|in3|in4|in_sub|d|clk|enable|preset|reset|s|r|set)$'

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    $matches = [regex]::Matches($line, '(?:(?:->|<-)\s+)?([a-z_][a-z_0-9]*)\.([a-z_0-9]+)')
    foreach ($m in $matches) {
        $nodeName = $m.Groups[1].Value
        $port = $m.Groups[2].Value
        if ($falsePositives -contains $nodeName) { continue }
        if (-not $nodePorts.ContainsKey($nodeName)) { continue }
        
        $validPorts = $nodePorts[$nodeName]
        if ($validPorts -notcontains $port -and $port -match $validPortPattern) {
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

Write-Output "=== INVALID PORT REFERENCES ==="
Write-Output "Total: $($invalidPortRefs.Count)"
Write-Output ""

if ($invalidPortRefs.Count -gt 0) {
    $invalidPortRefs | Sort-Object Node, Line | ForEach-Object {
        $lc = $_.Content
        if ($lc.Length -gt 200) { $lc = $lc.Substring(0, 200) + "..." }
        Write-Output "Line $($_.Line): $($_.Node).$($_.Port) -- valid: $($_.ValidPorts)"
        Write-Output "  $lc"
        Write-Output ""
    }
} else {
    Write-Output "NONE"
}
