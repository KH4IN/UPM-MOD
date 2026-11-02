param([string]$Mask = 'Universal', [string]$Salida = 'upm.bin', [int]$Max = 1500, [string]$A = "$env:USERPROFILE\Desktop\Victoria II + Alice dev")
$a = $A
$t0 = Get-Date
$p = Start-Process -FilePath "$a\launch_alice.exe" -WorkingDirectory $a -ArgumentList '-modsMask', $Mask, '-outputScenario', $Salida, '-autoBuild' -PassThru
$pico = 0; $n = 0
while (-not $p.HasExited -and ((Get-Date) - $t0).TotalSeconds -lt $Max) {
  Start-Sleep -Seconds 2; $p.Refresh()
  if (-not $p.HasExited) {
    $m = [int]($p.PrivateMemorySize64 / 1MB); if ($m -gt $pico) { $pico = $m }
    if (($n++ % 15) -eq 0) { "{0,5}s priv {1} MB cpu {2}s" -f [int]((Get-Date) - $t0).TotalSeconds, $m, [int]$p.TotalProcessorTime.TotalSeconds }
  }
}
if (-not $p.HasExited) { "SIGUE tras $Max s; lo cierro"; $p.Kill() } else { "salio codigo $($p.ExitCode)" }
"tiempo $([int]((Get-Date) - $t0).TotalSeconds) s, pico privado $pico MB"
'--- archivos nuevos'
foreach ($r in "$env:LOCALAPPDATA\Project Alice", "$env:USERPROFILE\Documents\Project Alice", "$env:APPDATA\Project Alice") {
  if (Test-Path -LiteralPath $r) { Get-ChildItem -LiteralPath $r -Recurse -File | Where-Object { $_.LastWriteTime -gt $t0 } | ForEach-Object { "$($_.FullName) $($_.Length)" } }
}
