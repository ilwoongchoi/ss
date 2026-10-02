$results = Get-ChildItem 'd:\Users\user\Documents\newstart\geometry_package' -Recurse -Include *.py,*.md,*.json | Select-String -Pattern 'coriolis|lunar.*torque|1/28|VERTICAL_MOBIUS|twist.*28|28.*twist|chiral.*torque|torque.*chiral' | Select-Object -First 50
foreach ($r in $results) {
    Write-Output ($r.Path + ":" + $r.LineNumber + ": " + $r.Line.Trim())
}
