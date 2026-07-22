[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$RepoPath,
    [string]$TaskName = "InfeRadar Markdown Summaries",
    [ValidateRange(5, 1440)]
    [int]$IntervalMinutes = 1440
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($RepoPath)) {
    $RepoPath = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}
$RepoPath = (Resolve-Path $RepoPath).Path
$RunnerPath = Join-Path $RepoPath "deploy\run-inferadar.ps1"
$TemplatePath = Join-Path $RepoPath "deploy\inferadar.windows.env.example"
$StateDir = Join-Path $env:LOCALAPPDATA "InfeRadar"
$EnvPath = Join-Path $StateDir "inferadar.env"
$VenvPath = Join-Path $RepoPath ".venv"
$VenvPython = Join-Path $VenvPath "Scripts\python.exe"
$CurrentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name

if (-not (Test-Path -LiteralPath $RunnerPath -PathType Leaf)) {
    throw "Windows runner not found: $RunnerPath"
}
if (-not (Test-Path -LiteralPath $TemplatePath -PathType Leaf)) {
    throw "Environment template not found: $TemplatePath"
}

if (-not (Test-Path -LiteralPath $VenvPython -PathType Leaf)) {
    if ($PSCmdlet.ShouldProcess($VenvPath, "Create Python virtual environment")) {
        $pythonCommand = Get-Command python.exe -ErrorAction Stop
        & $pythonCommand.Source -m venv $VenvPath
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create virtual environment."
        }
    }
}

if ($PSCmdlet.ShouldProcess($VenvPath, "Install InfeRadar with LLM and test dependencies")) {
    if (-not (Test-Path -LiteralPath $VenvPython -PathType Leaf)) {
        throw "Virtual-environment Python is unavailable: $VenvPython"
    }
    Push-Location $RepoPath
    try {
        & $VenvPython -m pip install -e ".[llm,test]"
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to install InfeRadar dependencies."
        }
    } finally {
        Pop-Location
    }
}

if ($PSCmdlet.ShouldProcess($StateDir, "Create private InfeRadar state directory")) {
    New-Item -ItemType Directory -Force -Path $StateDir | Out-Null
}
if (-not (Test-Path -LiteralPath $EnvPath -PathType Leaf)) {
    if ($PSCmdlet.ShouldProcess($EnvPath, "Create private environment configuration")) {
        Copy-Item -LiteralPath $TemplatePath -Destination $EnvPath
    }
}
if (Test-Path -LiteralPath $EnvPath -PathType Leaf) {
    if ($PSCmdlet.ShouldProcess($EnvPath, "Restrict ACL to $CurrentUser")) {
        & icacls.exe $EnvPath /inheritance:r /grant:r "${CurrentUser}:(F)" | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to restrict the private environment file ACL."
        }
    }
}

$PowerShellPath = (Get-Command powershell.exe -ErrorAction Stop).Source
$actionArguments = @(
    "-NoProfile",
    "-NonInteractive",
    "-ExecutionPolicy", "Bypass",
    "-File", "`"$RunnerPath`"",
    "-EnvFile", "`"$EnvPath`""
) -join " "

$action = New-ScheduledTaskAction `
    -Execute $PowerShellPath `
    -Argument $actionArguments `
    -WorkingDirectory $RepoPath
$logonTrigger = New-ScheduledTaskTrigger -AtLogOn -User $CurrentUser
$repeatTrigger = New-ScheduledTaskTrigger `
    -Once `
    -At (Get-Date).AddMinutes(2) `
    -RepetitionInterval (New-TimeSpan -Minutes $IntervalMinutes)
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Hours 3)
$principal = New-ScheduledTaskPrincipal `
    -UserId $CurrentUser `
    -LogonType Interactive `
    -RunLevel Limited

if ($PSCmdlet.ShouldProcess($TaskName, "Register per-user Scheduled Task")) {
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Description "Generate and push missing InfeRadar Markdown summaries when the laptop and VPN are available." `
        -Action $action `
        -Trigger @($logonTrigger, $repeatTrigger) `
        -Settings $settings `
        -Principal $principal `
        -Force | Out-Null
}

Write-Host ""
Write-Host "Windows automation setup complete."
Write-Host "Private config: $EnvPath"
Write-Host "Task:           $TaskName"
Write-Host "Logs:           $(Join-Path $StateDir 'logs')"
if (
    (Test-Path -LiteralPath $EnvPath -PathType Leaf) -and
    (Select-String -LiteralPath $EnvPath -SimpleMatch "replace-with-your-key" -Quiet)
) {
    Write-Warning "Edit the private config and replace the placeholder gateway values before starting the task."
}
Write-Host "Run on demand:  Start-ScheduledTask -TaskName `"$TaskName`""

