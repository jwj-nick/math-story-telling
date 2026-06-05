# run_execute_batch.ps1 — EXECUTE 병렬 배치 (메인세션 권한=API).
# 여러 unit 영상 디렉토리를 finish_video.py 로 N편 동시 실행. 연속 처리, 끝까지 무인.
# 자식 python 은 User-scope 환경변수(ELEVENLABS_API_KEY/GEMINI_API_KEY)를 자동 상속.
#
# 사용:
#   powershell -NoProfile -File 70_tools\run_execute_batch.ps1 -Dirs "dir1","dir2",... [-Parallel 2]
param(
  [Parameter(Mandatory=$true)][string]$Manifest,
  [int]$Parallel = 2
)
$ErrorActionPreference = "Continue"
$tool = "C:\Kids\math-story-telling\70_tools\finish_video.py"
$env:PYTHONIOENCODING = "utf-8"
# 매니페스트 = 한 줄당 unit 영상 dir (절대/상대 경로). 빈 줄·# 주석 무시.
$Dirs = Get-Content $Manifest | ForEach-Object { $_.Trim() } | Where-Object { $_ -and -not $_.StartsWith('#') }
$queue = [System.Collections.Generic.Queue[string]]::new()
$Dirs | ForEach-Object { $queue.Enqueue($_) }
$running = @()
$results = @()
Write-Output ("== batch 시작: {0}편, 동시 {1} ==" -f $Dirs.Count, $Parallel)
while ($queue.Count -gt 0 -or $running.Count -gt 0) {
  while ($running.Count -lt $Parallel -and $queue.Count -gt 0) {
    $d = $queue.Dequeue()
    $log = Join-Path $d "_exec.log"; $err = Join-Path $d "_exec.err"
    $p = Start-Process python -ArgumentList @($tool, $d) -PassThru -NoNewWindow `
         -RedirectStandardOutput $log -RedirectStandardError $err
    $running += [pscustomobject]@{ P = $p; D = $d }
    Write-Output ("  START {0} (pid {1})" -f $d, $p.Id)
  }
  Start-Sleep -Seconds 8
  $done = @($running | Where-Object { $_.P.HasExited })
  foreach ($x in $done) {
    $fin = Test-Path (Join-Path $x.D "8-final.mp4")
    $stat = if ($fin) { "OK" } else { "FAIL(final missing, rc=$($x.P.ExitCode))" }
    Write-Output ("  DONE  {0}  {1}" -f $x.D, $stat)
    $results += [pscustomobject]@{ Dir = $x.D; Status = $stat }
  }
  $running = @($running | Where-Object { -not $_.P.HasExited })
}
Write-Output "== batch 완료 =="
$results | ForEach-Object { Write-Output ("{0}  {1}" -f $_.Status, $_.Dir) }
