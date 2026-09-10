param([string]$Label='r001')
$ErrorActionPreference='Stop'
$work='D:/Pontius-worktrees/codex-eval-panel-completion'
$stage='D:/Pontius/tmp/eval-completion'
$parent='beb84be566aa28029284bd35c526d33cd27af369'
$git='C:/Program Files/Git/cmd/git.exe'
$ref='refs/heads/review/v0a-eval-panel-completion/'+$Label
$savedIndex=$env:GIT_INDEX_FILE
$index=Join-Path $env:TEMP ('eval-completion-'+[guid]::NewGuid().ToString('N')+'.idx')
try {
    $env:GIT_INDEX_FILE=$index
    & $git -C $work read-tree $parent
    if ($LASTEXITCODE) { throw 'read-tree failed' }
    & $git -C $work add -- src/pontius/eval_bridge.py src/pontius/eval_agreement.py `
        tools/v0a_eval_panel.py tools/v0a_eval_panel_completion.py tests/cases.json `
        tests/test_eval_export.py tests/test_eval_agreement.py tests/test_eval_completion_tool.py
    if ($LASTEXITCODE) { throw 'add failed' }
    & $git -C $work diff --cached --check
    if ($LASTEXITCODE) { throw 'diff check failed' }
    $tree=& $git -C $work write-tree
    if ($LASTEXITCODE) { throw 'write-tree failed' }
    $candidate=& $git -C $work commit-tree $tree -p $parent `
        -m ('Freeze eval panel bridge completion '+$Label)
    if ($LASTEXITCODE) { throw 'commit-tree failed' }
} finally {
    if ($null -eq $savedIndex) { Remove-Item Env:GIT_INDEX_FILE -ErrorAction SilentlyContinue }
    else { $env:GIT_INDEX_FILE=$savedIndex }
    Remove-Item -LiteralPath $index -ErrorAction SilentlyContinue
}
& $git -C $work update-ref $ref $candidate ('0'*40)
if ($LASTEXITCODE) { throw 'Create-only ref failed' }
[IO.File]::WriteAllText((Join-Path $stage ($Label+'-commit.txt')),$candidate+"`n",
                       [Text.UTF8Encoding]::new($false))
Write-Output ($Label+' '+$candidate)
