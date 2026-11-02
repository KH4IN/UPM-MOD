param([string]$Esc = 'upm32.bin', [int]$Min = 40, [int]$Cada = 60, [string]$Inicio = '1492-1-1', [string]$Speed = '6', [string]$A = "$env:USERPROFILE\Desktop\Victoria II + Alice dev", [string]$Exe = 'Alice.exe', [string]$Load = '', [string]$Until = '')
# Partida sin ventana a baja prioridad: mide memoria y lee la fecha de los autoguardados.
$s = $PSScriptRoot
$sv = "$env:USERPROFILE\Documents\Project Alice\saved games"
$t0 = Get-Date
$ep = [int64](($t0.ToUniversalTime() - [datetime]'1970-01-01').TotalSeconds)
$arg = @($Esc, '-headless', '-speed', $Speed)
if ($Load) { $arg += @('-load', $Load) }
if ($Until) { $arg += @('-until', $Until) }
$p = Start-Process -FilePath "$A\$Exe" -WorkingDirectory $A -ArgumentList $arg -PassThru
Start-Sleep 3; try { $p.PriorityClass = 'BelowNormal' } catch {}
$pico = 0
while (-not $p.HasExited -and ((Get-Date) - $t0).TotalMinutes -lt $Min) {
  Start-Sleep -Seconds $Cada; $p.Refresh()
  if ($p.HasExited) { break }
  $m = [int]($p.PrivateMemorySize64 / 1MB); if ($m -gt $pico) { $pico = $m }
  $u = python -I "$s\savedate.py" $sv $Inicio $ep 1
  '{0,6:N1} min priv {1} MB cpu {2}s | {3}' -f ((Get-Date) - $t0).TotalMinutes, $m, [int]$p.TotalProcessorTime.TotalSeconds, $u
}
if ($p.HasExited) { "SALIO codigo $($p.ExitCode) a los $([int]((Get-Date) - $t0).TotalMinutes) min" } else { 'sigue vivo; lo cierro'; $p.Kill() }
"pico privado $pico MB"
python -I "$s\savedate.py" $sv $Inicio $ep 4
