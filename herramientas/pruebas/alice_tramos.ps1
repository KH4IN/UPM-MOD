param([string]$Esc = 'upm97.bin', [string]$Marca = 'bookmark_aaaaaaaagkoiacdj-2000-1-1.bin', [string]$Anos = '2100,2110,2115,2120,2130,2150,2200,2250', [string]$Exe = 'AliceT.exe', [int]$Max = 150, [string]$Prefijo = 'tramo', [switch]$Stats, [int]$Guerras = 0)
# Juega por tramos sin ventana, a baja prioridad, y guarda cada tramo para poder volver cerca de un cierre.
$s = $PSScriptRoot
$A = "$env:USERPROFILE\Desktop\Victoria II + Alice dev"
$sv = "$env:USERPROFILE\Documents\Project Alice\saved games"
Remove-Item -LiteralPath "$A\crash_stack.txt" -ErrorAction SilentlyContinue
$carga = $Marca
foreach ($y in ($Anos -split ',')) {
  $t = Get-Date
  # Sin -Marca, el primer tramo empieza en la fecha inicial del escenario.
  $arg = @($Esc, '-headless', '-speed', '6')
  if ($carga) { $arg += @('-load', $carga) }
  $arg += @('-until', $y)
  if ($Stats) { $arg += '-stats' }
  # -wars N: cada 1 de enero, N paises de la IA en paz atacan a un vecino (necesita el Alice con esa opcion).
  if ($Guerras -gt 0) { $arg += @('-wars', "$Guerras") }
  $p = Start-Process -FilePath "$A\$Exe" -WorkingDirectory $A -ArgumentList $arg -PassThru
  $null = $p.Handle
  Start-Sleep 3; try { $p.PriorityClass = 'BelowNormal' } catch {}
  $pico = 0
  while (-not $p.HasExited -and ((Get-Date) - $t).TotalMinutes -lt $Max) {
    Start-Sleep 5; $p.Refresh()
    if (-not $p.HasExited) { $m = [int]($p.PrivateMemorySize64 / 1MB); if ($m -gt $pico) { $pico = $m } }
  }
  if (-not $p.HasExited) { "NO TERMINA hasta $y tras $Max min"; $p.Kill(); break }
  $min = [math]::Round(((Get-Date) - $t).TotalMinutes, 1)
  "hasta ${y}: salida $($p.ExitCode), $min min, pico $pico MB"
  if ($p.ExitCode -ne 0) { 'CIERRE'; if (Test-Path -LiteralPath "$A\crash_stack.txt") { Get-Content -LiteralPath "$A\crash_stack.txt" }; break }
  $f = Get-ChildItem -LiteralPath $sv -Filter 'autosave_*.bin' | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  $carga = "${Prefijo}_$y.bin"
  Copy-Item -LiteralPath $f.FullName "$sv\$carga" -Force
  python -I "$s\savedate.py" $sv '1492-1-1' ([int64]0) 1
}
