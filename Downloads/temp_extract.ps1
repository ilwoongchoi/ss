$lines = Get-Content 'c:\Users\User\Downloads\all_128_full_dump.csv'
foreach ($line in $lines) {
    if ($line.StartsWith('ESFJ_M_B,') -or $line.StartsWith('ENFP_F_O,')) {
        $sub = $line.Substring(0, [Math]::Min(250, $line.Length))
        Write-Output $sub
        Write-Output "---"
    }
}
