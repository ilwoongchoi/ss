$files = Get-ChildItem 'd:\Users\user\Documents\newstart' -Recurse -Include *.py,*.md,*.txt | Where-Object { $_.LastWriteTime -gt (Get-Date).AddMonths(-6) }
$results = $files | Select-String -Pattern '1/28|1\.28|0\.0357|coriolis' | Select-Object -First 50
foreach ($r in $results) {
    Write-Output ($r.Path + ":" + $r.LineNumber + ": " + $r.Line.Trim())
}
