[CmdletBinding()]
param(
    [string]$EnvFile = $env:INFERADAR_ENV_FILE,
    [string]$Since = $env:INFERADAR_SUMMARY_SINCE,
    [string]$Only,
    [ValidateRange(0, 1000)]
    [int]$Limit = 0,
    [switch]$SkipPush,
    [switch]$SkipPull
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if ([string]::IsNullOrWhiteSpace($EnvFile)) {
    $EnvFile = Join-Path $env:LOCALAPPDATA "InfeRadar\inferadar.env"
}

$LogDir = Join-Path $env:LOCALAPPDATA "InfeRadar\logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$script:LogFile = Join-Path $LogDir ("stage2-{0}.log" -f (Get-Date -Format "yyyy-MM-dd"))

function Write-Log {
    param([Parameter(Mandatory)][string]$Message)
    $line = "[{0}] {1}" -f (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"), $Message
    Write-Host $line
    Add-Content -LiteralPath $script:LogFile -Value $line -Encoding UTF8
}

function Import-EnvFile {
    param([Parameter(Mandatory)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Environment file not found: $Path"
    }
    foreach ($rawLine in Get-Content -LiteralPath $Path) {
        $line = $rawLine.Trim()
        if (-not $line -or $line.StartsWith("#")) {
            continue
        }
        $parts = $line -split "=", 2
        if ($parts.Count -ne 2 -or $parts[0] -notmatch "^[A-Za-z_][A-Za-z0-9_]*$") {
            throw "Invalid environment line (expected NAME=value): $rawLine"
        }
        $name = $parts[0]
        $value = $parts[1]
        if (
            $value.Length -ge 2 -and
            (($value.StartsWith('"') -and $value.EndsWith('"')) -or
             ($value.StartsWith("'") -and $value.EndsWith("'")))
        ) {
            $value = $value.Substring(1, $value.Length - 2)
        }
        [Environment]::SetEnvironmentVariable($name, $value, "Process")
    }
}

function Invoke-Logged {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [Parameter(Mandatory)][string[]]$Arguments
    )
    # Windows PowerShell wraps native stderr lines as ErrorRecord objects. Keep
    # them as ordinary logged output; the native exit code is authoritative.
    $previousPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        $output = @(& $FilePath @Arguments 2>&1)
        $code = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $previousPreference
    }
    foreach ($item in $output) {
        Write-Log ($item.ToString())
    }
    return [pscustomobject]@{
        Code = $code
        Output = $output
    }
}

function Test-GatewayTcp {
    param([Parameter(Mandatory)][uri]$Uri)
    $port = if ($Uri.IsDefaultPort) {
        if ($Uri.Scheme -eq "https") { 443 } else { 80 }
    } else {
        $Uri.Port
    }
    $client = [System.Net.Sockets.TcpClient]::new()
    try {
        $connect = $client.ConnectAsync($Uri.DnsSafeHost, $port)
        if (-not $connect.Wait(5000) -or -not $client.Connected) {
            return $false
        }
        return $true
    } catch {
        return $false
    } finally {
        $client.Dispose()
    }
}

function Invoke-Stage2 {
    Set-Location $RepoDir
    Write-Log "Markdown stage start (repo: $RepoDir)"

    if (Test-Path -LiteralPath $EnvFile -PathType Leaf) {
        Import-EnvFile -Path $EnvFile
        Write-Log "Loaded private environment configuration."
    }
    $effectiveSince = $Since
    if ([string]::IsNullOrWhiteSpace($effectiveSince)) {
        $effectiveSince = $env:INFERADAR_SUMMARY_SINCE
    }

    foreach ($required in @(
        "INFERADAR_LLM_BASE_URL",
        "INFERADAR_LLM_API_KEY",
        "INFERADAR_LLM_MODEL"
    )) {
        if ([string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable($required, "Process"))) {
            Write-Log "ERROR: required setting $required is not configured."
            return 10
        }
    }

    $python = $env:PYTHON
    if ([string]::IsNullOrWhiteSpace($python)) {
        $python = Join-Path $RepoDir ".venv\Scripts\python.exe"
    }
    if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
        Write-Log "ERROR: Python environment not found: $python"
        return 11
    }

    $env:GIT_AUTHOR_NAME = "inferadar-bot"
    $env:GIT_AUTHOR_EMAIL = "inferadar-bot@users.noreply.github.com"
    $env:GIT_COMMITTER_NAME = "inferadar-bot"
    $env:GIT_COMMITTER_EMAIL = "inferadar-bot@users.noreply.github.com"

    if (-not $SkipPull) {
        Write-Log "Syncing main before summary generation."
        $pull = Invoke-Logged -FilePath "git" -Arguments @(
            "pull", "--rebase", "--autostash", "origin", "main"
        )
        if ($pull.Code -ne 0) {
            Write-Log "ERROR: git pull failed."
            return 12
        }
    }

    $gatewayUri = [uri]$env:INFERADAR_LLM_BASE_URL
    if (-not (Test-GatewayTcp -Uri $gatewayUri)) {
        Write-Log "Gateway is unreachable; leaving backlog untouched for the next scheduled retry."
        return 20
    }

    $summaryArgs = @(
        "-m", "inferadar.summarize",
        "--changelogs-dir", "changelogs",
        "--window", "all"
    )
    if (-not [string]::IsNullOrWhiteSpace($effectiveSince)) {
        $summaryArgs += @("--since", $effectiveSince)
    }
    if (-not [string]::IsNullOrWhiteSpace($Only)) {
        $summaryArgs += @("--only", $Only)
    }
    if ($Limit -gt 0) {
        $summaryArgs += @("--limit", $Limit.ToString())
    }

    Write-Log "Generating all missing or stale summaries in the eligible backlog."
    $summary = Invoke-Logged -FilePath $python -Arguments $summaryArgs
    $summaryCode = $summary.Code

    $status = Invoke-Logged -FilePath "git" -Arguments @(
        "status", "--porcelain", "--", ":(glob)changelogs/**/*.md"
    )
    if ($status.Code -ne 0) {
        Write-Log "ERROR: could not inspect generated Markdown."
        return 13
    }

    if (@($status.Output).Count -eq 0) {
        Write-Log "No Markdown changes to commit."
        return $summaryCode
    }

    $add = Invoke-Logged -FilePath "git" -Arguments @(
        "add", "--", ":(glob)changelogs/**/*.md"
    )
    if ($add.Code -ne 0) {
        Write-Log "ERROR: staging Markdown failed."
        return 14
    }
    $commit = Invoke-Logged -FilePath "git" -Arguments @(
        "commit", "-m", "Add changelog summaries"
    )
    if ($commit.Code -ne 0) {
        Write-Log "ERROR: committing Markdown failed."
        return 15
    }

    $skipPushRequested = $SkipPush -or $env:INFERADAR_SKIP_PUSH -eq "1"
    if ($skipPushRequested) {
        Write-Log "Push skipped by request; generated commit remains local."
        return $summaryCode
    }

    foreach ($attempt in 1..3) {
        $push = Invoke-Logged -FilePath "git" -Arguments @(
            "push", "origin", "HEAD:main"
        )
        if ($push.Code -eq 0) {
            Write-Log "Markdown commit pushed."
            return $summaryCode
        }
        Write-Log "Push attempt $attempt failed; rebasing before retry."
        $rebase = Invoke-Logged -FilePath "git" -Arguments @(
            "pull", "--rebase", "--autostash", "origin", "main"
        )
        if ($rebase.Code -ne 0) {
            Write-Log "ERROR: rebase after rejected push failed."
            return 16
        }
        Start-Sleep -Seconds (3 * $attempt)
    }

    Write-Log "ERROR: push failed after three attempts."
    return 17
}

$mutex = [System.Threading.Mutex]::new($false, "Local\InfeRadarStage2")
$acquired = $false
$exitCode = 1
try {
    try {
        $acquired = $mutex.WaitOne(0)
    } catch [System.Threading.AbandonedMutexException] {
        $acquired = $true
    }
    if (-not $acquired) {
        Write-Log "Another Stage-2 run is already active; exiting without overlap."
        $exitCode = 0
    } else {
        $exitCode = Invoke-Stage2
    }
} catch {
    Write-Log "ERROR: $($_.Exception.Message)"
    $exitCode = 1
} finally {
    if ($acquired) {
        $mutex.ReleaseMutex()
    }
    $mutex.Dispose()
}

Write-Log "Markdown stage finished with exit code $exitCode."
exit $exitCode
