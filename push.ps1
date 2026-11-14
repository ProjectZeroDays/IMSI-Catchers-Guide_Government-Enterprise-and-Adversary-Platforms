<#
  push.ps1 - v3. Commit and push the working tree to GitHub.
  Run from the repository root. Safe to re-run.
#>
[CmdletBinding()]
param(
    [string] $Branch  = "Your-Momma-Beeotch",
    [string] $Remote  = "origin",
    [string] $Url     = "https://github.com/ProjectZeroDays/IMSI-Catchers-Guide_Government-Enterprise-and-Adversary-Platforms.git",
    [Alias('m')] [string[]] $Message = @(),
    [int]    $MinReadmeBytes = 200000,
    [switch] $Recover,
    [switch] $Force,
    [switch] $DryRun
)

$ErrorActionPreference = "Stop"

function Step($t) { Write-Host "`n== $t" -ForegroundColor Cyan }
function Ok($t)   { Write-Host "   $t" -ForegroundColor DarkGray }
function Warn($t) { Write-Host "   $t" -ForegroundColor Yellow }
function Bad($t)  { Write-Host "   $t" -ForegroundColor Red }

# NOTE: must not be named "Git" - that shadows git.exe and recurses.
function Invoke-Git {
    param([Parameter(ValueFromRemainingArguments = $true)] [string[]] $GitArgs)
    $shown = "git " + ($GitArgs -join " ")
    if ($DryRun) { Ok "(dry) $shown"; return }
    & git.exe @GitArgs
    if ($LASTEXITCODE -ne 0) { throw "failed: $shown" }
}

function Test-Git {
    param([Parameter(ValueFromRemainingArguments = $true)] [string[]] $GitArgs)
    & git.exe @GitArgs 2>&1 | Out-Null
    return ($LASTEXITCODE -eq 0)
}

function Write-NoBom([string] $Path, [string] $Text) {
    [IO.File]::WriteAllText($Path, $Text, (New-Object Text.UTF8Encoding $false))
}

# ---------------------------------------------------------------- preflight
Step "Preflight"

if (-not (Get-Command git.exe -ErrorAction SilentlyContinue)) {
    Bad "git.exe is not on PATH. Install Git for Windows first."; exit 1
}
Ok ((git.exe --version) -join "")

if (-not (Test-Path "README.md")) { Bad "README.md not found - run from the repo root."; exit 1 }

# ---- recovery path -------------------------------------------------------
$rawBase = ($Url -replace '\.git$', '') -replace '^https://github\.com/', 'https://raw.githubusercontent.com/'
$rawUrl  = "$rawBase/$Branch/README.md"

$readme = (Get-Item "README.md").Length
if ($readme -lt $MinReadmeBytes) {
    if ($Recover) {
        Warn "README.md is $readme bytes - fetching authoritative copy"
        Ok  $rawUrl
        try {
            Invoke-WebRequest -Uri $rawUrl -OutFile "README.md" -UseBasicParsing -ErrorAction Stop
        } catch {
            Bad "download failed: $($_.Exception.Message)"; exit 1
        }
        $readme = (Get-Item "README.md").Length
        if ($readme -lt $MinReadmeBytes) {
            Bad "recovered file is still only $readme bytes - check the branch name"; exit 1
        }
        Ok "recovered $readme bytes"
        $head = (Get-Content "README.md" -TotalCount 1)
        if ($head -notmatch '^(!\[|#)') { Warn "first line looks unusual: $head" }
    }
    else {
        Bad "README.md is only $readme bytes (expected >= $MinReadmeBytes)."
        Bad "A short README means the patcher truncated it."
        Bad "Re-run with -Recover to pull the authoritative copy from $Branch."
        if (-not $Force) { exit 1 }
        Warn "continuing because -Force was passed"
    }
}
else { Ok "README.md $readme bytes" }

if (-not (Test-Path "tools/patch_readme.py")) { Warn "tools/patch_readme.py missing - nothing to commit but the doc" }
if (-not (Test-Path "assets")) { Warn "assets/ missing - image links will stay hotlinked" }

# ---------------------------------------------------------------- repo init
Step "Repository"

if (Test-Git rev-parse --git-dir) {
    Ok "already a repository"
} else {
    Warn "not a repository - initialising"
    Invoke-Git init
    Invoke-Git branch -M $Branch
}

if (-not (Test-Git config user.email)) {
    $email = Read-Host "   git user.email"
    Invoke-Git config user.email $email
}
if (-not (Test-Git config user.name)) {
    $name = Read-Host "   git user.name"
    Invoke-Git config user.name $name
}
Ok "$(git.exe config user.name) <$(git.exe config user.email)>"

Invoke-Git config core.autocrlf false
Invoke-Git config core.safecrlf false

if (-not (Test-Git remote get-url $Remote)) {
    Warn "no '$Remote' remote - adding"
    Invoke-Git remote add $Remote $Url
}
Ok "remote $Remote -> $(git.exe remote get-url $Remote)"

# ---------------------------------------------------------------- ignore rules
Step "Ignore rules"

Write-NoBom ".gitignore" @'
# patcher artefacts
*.bak
*.tmp
.patch-*
# python
__pycache__/
*.py[cod]
.venv/
# os
Thumbs.db
desktop.ini
.DS_Store
# keep the doc, the tools and the assets
!assets/**
!tools/**
'@
Ok ".gitignore written"

Write-NoBom ".gitattributes" @'
* text=auto eol=lf
*.md text eol=lf
*.png binary
*.jpg binary
*.jpeg binary
*.webp binary
*.svg text eol=lf
'@
Ok ".gitattributes written"

# ---------------------------------------------------------------- reconcile
Step "Reconcile with remote"

Invoke-Git fetch $Remote --prune

$remoteTip = $null
if (Test-Git rev-parse --verify --quiet "refs/remotes/$Remote/$Branch") {
    $remoteTip = (git.exe rev-parse "refs/remotes/$Remote/$Branch").Trim()
    Ok "remote tip $($remoteTip.Substring(0,8))"
} else {
    Warn "remote branch '$Branch' does not exist yet - first push will create it"
}

$localTip = $null
if (Test-Git rev-parse --verify --quiet "HEAD") {
    $localTip = (git.exe rev-parse HEAD).Trim()
    Ok "local tip  $($localTip.Substring(0,8))"
}

if (-not $localTip -and $remoteTip) {
    Warn "no local commits - seating HEAD on $Remote/$Branch without touching files"
    Invoke-Git reset --mixed $remoteTip
}
elseif ($localTip -and $remoteTip -and $remoteTip -eq $localTip) {
    Ok "already level with remote"
}
elseif ($localTip -and $remoteTip -and -not (Test-Git merge-base --is-ancestor $remoteTip HEAD)) {
    Warn "histories diverge - rebasing local onto $Remote/$Branch, keeping local README"
    Invoke-Git rebase -X theirs "$Remote/$Branch"
}

if (Test-Git rev-parse --verify --quiet "refs/heads/$Branch") {
    Invoke-Git checkout $Branch
} else {
    Invoke-Git checkout -b $Branch
}

# ---------------------------------------------------------------- stage
Step "Stage"

Invoke-Git add -A

$staged = @(git.exe diff --cached --name-only)
if ($staged.Count -eq 0) { Ok "nothing to commit" }
else {
    Ok "$($staged.Count) path(s) staged"
    $staged | Select-Object -First 25 | ForEach-Object { Ok "  $_" }
    if ($staged.Count -gt 25) { Ok "  ... and $($staged.Count - 25) more" }

    $bak = @($staged | Where-Object { $_ -like "*.bak" })
    if ($bak.Count -gt 0) { Warn "staged .bak files: $($bak -join ', ')" }

    $big = @($staged | ForEach-Object {
        if (Test-Path $_ -PathType Leaf) {
            $s = (Get-Item $_).Length
            if ($s -gt 50MB) { "$_ ($([math]::Round($s/1MB,1)) MB)" }
        }
    })
    if ($big.Count -gt 0) { Warn "over 50 MB: $($big -join ', ') - consider git-lfs" }

    $msg = if ($Message.Count -gt 0) { $Message -join " " } else { "Update reference: assets, tooling and verified content" }
    Step "Commit"
    Invoke-Git commit -m $msg
}

# ---------------------------------------------------------------- push
Step "Push"

if ($DryRun) { Ok "(dry) git push -u $Remote $Branch"; exit 0 }

git.exe push -u $Remote $Branch
if ($LASTEXITCODE -ne 0) {
    Bad "push rejected. If the remote moved again:"
    Bad "  git fetch $Remote; git rebase -X theirs $Remote/$Branch; git push -u $Remote $Branch"
    exit 1
}

Step "Done"
Ok "https://github.com/ProjectZeroDays/IMSI-Catchers-Guide_Government-Enterprise-and-Adversary-Platforms/tree/$Branch"
git.exe log --oneline -3