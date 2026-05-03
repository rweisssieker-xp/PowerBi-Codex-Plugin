param(
    [Parameter(Mandatory = $true)]
    [string]$PbipPath,

    [string]$PowerBIDesktopExe,

    [int]$WaitSeconds = 25,

    [string]$OutJson
)

$ErrorActionPreference = "Stop"

function Get-FrownSnapshots {
    $storePath = Join-Path $env:USERPROFILE "Microsoft\Power BI Desktop Store App"
    $classicPath = Join-Path $env:LOCALAPPDATA "Microsoft\Power BI Desktop"
    @($storePath, $classicPath) |
        Where-Object { Test-Path $_ } |
        ForEach-Object { Get-ChildItem -Path $_ -Filter "FrownSnapShot*.zip" -File -ErrorAction SilentlyContinue } |
        Sort-Object LastWriteTimeUtc -Descending
}

if (-not (Test-Path -LiteralPath $PbipPath)) {
    throw "PBIP path does not exist: $PbipPath"
}

if (-not $PowerBIDesktopExe) {
    $candidates = @(
        "$env:LOCALAPPDATA\Microsoft\WindowsApps\PBIDesktopStore.exe",
        "$env:ProgramFiles\Microsoft Power BI Desktop\bin\PBIDesktop.exe",
        "${env:ProgramFiles(x86)}\Microsoft Power BI Desktop\bin\PBIDesktop.exe"
    )
    $PowerBIDesktopExe = $candidates | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1
}

if (-not $PowerBIDesktopExe) {
    throw "Power BI Desktop executable was not found. Pass -PowerBIDesktopExe."
}

$before = @(Get-FrownSnapshots)
$beforeLatest = if ($before.Count -gt 0) { $before[0].FullName } else { $null }
$startedAt = (Get-Date).ToUniversalTime().ToString("o")
$process = Start-Process -FilePath $PowerBIDesktopExe -ArgumentList "`"$PbipPath`"" -PassThru -WindowStyle Hidden
Start-Sleep -Seconds $WaitSeconds
$process.Refresh()
$after = @(Get-FrownSnapshots)
$afterLatest = if ($after.Count -gt 0) { $after[0].FullName } else { $null }
$newFrown = $false
if ($afterLatest -and ($afterLatest -ne $beforeLatest)) {
    $afterInfo = Get-Item -LiteralPath $afterLatest
    $newFrown = $afterInfo.LastWriteTimeUtc -gt ([datetime]::Parse($startedAt).AddSeconds(-5))
}

$result = [ordered]@{
    status = if ($newFrown) { "fail" } elseif ($process.HasExited) { "warning" } else { "pass" }
    pbipPath = (Resolve-Path -LiteralPath $PbipPath).Path
    executable = $PowerBIDesktopExe
    processId = $process.Id
    hasExited = $process.HasExited
    responding = if ($process.HasExited) { $false } else { $process.Responding }
    startedAtUtc = $startedAt
    waitSeconds = $WaitSeconds
    frownBefore = $beforeLatest
    frownAfter = $afterLatest
    newFrownDetected = $newFrown
}

$json = $result | ConvertTo-Json -Depth 5
if ($OutJson) {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $OutJson) | Out-Null
    $json | Set-Content -LiteralPath $OutJson -Encoding UTF8
}
$json
