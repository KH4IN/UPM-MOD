param([string]$Esc = 'upm96.bin', [string]$Marca = 'bookmark_aaaaaaaagkohonok-2000-1-1.bin', [int]$Y1 = 2003, [int]$Y2 = 2005, [string]$Exe = 'AliceT.exe', [string]$Inicio = '1492-1-1', [int]$Max = 20)
# Carga, juega, guarda, vuelve a cargar lo guardado y sigue: todo sin ventana.
$s = $PSScriptRoot
$A = "$env:USERPROFILE\Desktop\Victoria II + Alice dev"
$sv = "$env:USERPROFILE\Documents\Project Alice\saved games"
function Tramo($carga, $hasta) {
  $t = Get-Date
  $p = Start-Process -FilePath "$A\$Exe" -WorkingDirectory $A -ArgumentList $Esc, '-headless', '-speed', '6', '-load', $carga, '-until', $hasta -PassThru
  $pico = 0
  while (-not $p.HasExited -and ((Get-Date) - $t).TotalMinutes -lt $Max) {
    Start-Sleep 2; $p.Refresh()
    if (-not $p.HasExited) { $m = [int]($p.PrivateMemorySize64 / 1MB); if ($m -gt $pico) { $pico = $m } }
  }
  if (-not $p.HasExited) { "NO TERMINA tras $Max min"; $p.Kill(); return $false }
  "tramo $carga hasta ${hasta}: salida $($p.ExitCode), $([int]((Get-Date) - $t).TotalSeconds) s, pico $pico MB"
  return $true
}
Tramo $Marca $Y1
$f = Get-ChildItem -LiteralPath $sv -Filter 'autosave_*.bin' | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Copy-Item -LiteralPath $f.FullName "$sv\prueba_ciclo.bin" -Force
python -I "$s\savedate.py" $sv $Inicio ([int64]0) 1
Tramo 'prueba_ciclo.bin' $Y2
python -I "$s\savedate.py" $sv $Inicio ([int64]0) 1
