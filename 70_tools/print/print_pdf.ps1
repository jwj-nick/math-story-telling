# print_pdf.ps1 -- print-ready HTML to PDF via headless Chrome. No external deps.
#
# ASCII-ONLY BY DESIGN: Windows PowerShell 5.1 reads .ps1 as ANSI (cp949) unless the file
# has a UTF-8 BOM, so any Hangul literal here corrupts the parser. Korean file names are
# computed by build_sheet.py and passed in via <setid>_pdfplan.json.
#
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File print_pdf.ps1 -Plan <setid_pdfplan.json>

param(
  [Parameter(Mandatory = $true)][string]$Plan
)

$chromeCandidates = @(
  "C:\Program Files\Google\Chrome\Application\chrome.exe",
  "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
  "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe",
  "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
)
$chrome = $null
foreach ($c in $chromeCandidates) { if (Test-Path $c) { $chrome = $c; break } }
if (-not $chrome) { Write-Error "Chrome/Edge not found."; exit 1 }

$items = Get-Content $Plan -Raw -Encoding UTF8 | ConvertFrom-Json
$profileDir = Join-Path $env:TEMP ("chrome-print-" + [System.Guid]::NewGuid().ToString("N").Substring(0, 8))
$made = 0

foreach ($it in $items) {
  if (-not (Test-Path $it.html)) { Write-Warning ("missing html: " + $it.html); continue }
  $dir = Split-Path $it.pdf -Parent
  if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force $dir | Out-Null }
  $uri = ([System.Uri](Resolve-Path $it.html).Path).AbsoluteUri

  # A fresh profile makes Chrome try to phone home (GCM/sync/component update) and it can
  # hang forever after the PDF is already written. Disable all of it, and hard-kill on timeout.
  $chromeArgs = @(
    "--headless", "--disable-gpu", "--no-sandbox", "--no-first-run", "--no-default-browser-check",
    "--disable-extensions", "--disable-background-networking", "--disable-sync",
    "--disable-component-update", "--disable-default-apps", "--disable-domain-reliability",
    "--disable-client-side-phishing-detection", "--safebrowsing-disable-auto-update",
    "--metrics-recording-only", "--mute-audio", "--no-service-autorun",
    "--disable-features=Translate,OptimizationHints,MediaRouter,DialMediaRouteProvider,CalculateNativeWinOcclusion",
    "--user-data-dir=$profileDir", "--virtual-time-budget=4000",
    "--no-pdf-header-footer", "--print-to-pdf-no-header",
    "--print-to-pdf=$($it.pdf)", $uri
  )
  $p = Start-Process -FilePath $chrome -ArgumentList $chromeArgs -PassThru -WindowStyle Hidden
  if (-not $p.WaitForExit(90000)) {
    Write-Warning ("timeout, killing chrome for: " + (Split-Path $it.pdf -Leaf))
    try { $p.Kill() } catch {}
    Start-Sleep -Milliseconds 300
  }

  if (Test-Path $it.pdf) {
    $kb = [math]::Round((Get-Item $it.pdf).Length / 1KB, 1)
    Write-Output ("  OK  {0}  ({1} KB)" -f (Split-Path $it.pdf -Leaf), $kb)
    $made++
  }
  else {
    Write-Warning ("failed: " + (Split-Path $it.pdf -Leaf))
  }
}

if (Test-Path $profileDir) { Remove-Item -Recurse -Force $profileDir -ErrorAction SilentlyContinue }
Write-Output ("  -> {0} / {1} PDF" -f $made, $items.Count)
