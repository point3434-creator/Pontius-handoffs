# Native source admission requires D:, outside the D:\a reparse workspace.
$v2Root = 'D:\pv3'
$v2Temp = 'D:\ptv3'
$v2Origin = 'C:\Users\point\.codex\worktrees\fa55\Pontius'
& $env:PONTIUS_GIT -c core.autocrlf=false clone --shared --no-checkout $v2Origin $v2Root
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $env:PONTIUS_GIT -C $v2Root -c core.autocrlf=false checkout --detach df6c896e8511e22281110aa7890cc36383dcd47a
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
New-Item -ItemType Directory -ErrorAction Stop $v2Temp | Out-Null
$env:TEMP = $v2Temp
$env:TMP = $v2Temp
$env:PYTHONPATH = Join-Path $v2Root 'src'
Set-Location -LiteralPath $v2Root
& 'C:/Users/point/AppData/Roaming/uv/python/cpython-3.11.15-windows-x86_64-none/python.exe' -B -P tests\test_v0a_evaluation_v2.py
exit $LASTEXITCODE
