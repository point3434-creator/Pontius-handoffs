# Native source admission requires D:, outside the D:\a reparse workspace.
$v2Root = 'D:\pv2'
$v2Temp = 'D:\ptv2'
& $env:PONTIUS_GIT -c core.autocrlf=false clone --shared --no-checkout C:\Users\point\.codex\worktrees\fa55\Pontius $v2Root
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $env:PONTIUS_GIT -C $v2Root -c core.autocrlf=false checkout --detach 2f8e540204dc41521d447a158f0da8c7983125f6
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
New-Item -ItemType Directory -ErrorAction Stop $v2Temp | Out-Null
$env:TEMP = $v2Temp
$env:TMP = $v2Temp
$env:PYTHONPATH = Join-Path $v2Root 'src'
Set-Location -LiteralPath $v2Root
& 'C:/Users/point/AppData/Roaming/uv/python/cpython-3.11.15-windows-x86_64-none/python.exe' -B -P tests\test_v0a_evaluation_v2.py
exit $LASTEXITCODE
