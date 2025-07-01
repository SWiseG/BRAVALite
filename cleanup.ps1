# limpar_migracoes.ps1
$venvFolder = "brava_lite"

Write-Host "System Cleanup started"

Get-ChildItem -Recurse -Filter *.py | Where-Object {
    $_.FullName -like "*\migrations\*" -and
    $_.Name -ne "__init__.py" -and
    $_.FullName -notlike "*\$venvFolder\*"
} | ForEach-Object {
    Remove-Item $_.FullName -Force
}

Get-ChildItem -Recurse -Filter *.pyc | Where-Object {
    $_.FullName -like "*\migrations\*" -and
    $_.FullName -notlike "*\$venvFolder\*"
} | ForEach-Object {
    Remove-Item $_.FullName -Force
}

Get-ChildItem -Recurse -Directory -Filter migrations | Where-Object {
    $_.FullName -notlike "*\$venvFolder\*"
} | ForEach-Object {
    if (-Not (Get-ChildItem $_.FullName)) {
        Remove-Item $_.FullName -Force -Recurse
    }
}

Write-Host "System Cleanup started end"
