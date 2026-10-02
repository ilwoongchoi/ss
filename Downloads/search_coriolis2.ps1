$results = Get-ChildItem 'd:\Users\user\Documents\newstart' -Recurse -Include *.py,*.md,*.txt | Select-String -Pattern 'coriolis|lunar.*torque|torque.*lunar|tidal.*torque|torque.*tidal|hemisphere.*rotation|rotation.*hemisphere|north.*south.*flip|south.*north.*flip|pole.*flip|magnetic.*flip|day.*night.*rotation|coriolis.*force|cyclone|chiral.*rotation' | Select-Object -First 80
foreach ($r in $results) {
    Write-Output ($r.Path + ":" + $r.LineNumber + ": " + $r.Line.Trim())
}
