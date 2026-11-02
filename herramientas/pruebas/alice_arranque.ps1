param([int]$Veces = 10, [string]$Exe = 'AliceT.exe', [string]$Esc = 'upm97.bin', [string]$Carga = 'tramo_2120.bin', [int]$Until = 2125, [int]$Seg = 15)
# Arranca muchas veces, captura stderr y cuenta los cierres al cargar.
$s = $PSScriptRoot
$A = "$env:USERPROFILE\Desktop\Victoria II + Alice dev"
$buenos = 0; $malos = 0
foreach ($i in 1..$Veces) {
  $e = "$env:TEMP\arranque_err_$i.txt"; $o = "$env:TEMP\arranque_out_$i.txt"
  $t = Get-Date
  $p = Start-Process -FilePath "$A\$Exe" -WorkingDirectory $A -ArgumentList $Esc, '-headless', '-speed', '6', '-load', $Carga, '-until', $Until, '-nosave' -PassThru -RedirectStandardError $e -RedirectStandardOutput $o
  $h = $p.Handle
  while (-not $p.HasExited -and ((Get-Date) - $t).TotalSeconds -lt $Seg) { Start-Sleep -Milliseconds 300 }
  if (-not $p.HasExited) { $buenos++; $p.Kill(); $p.WaitForExit(); Start-Sleep -Milliseconds 500; Remove-Item $e, $o -ErrorAction SilentlyContinue; continue }
  $p.WaitForExit()
  $c = $p.ExitCode; $seg = [int]((Get-Date) - $t).TotalSeconds
  if ($c -eq 0) { $buenos++; Remove-Item $e, $o -ErrorAction SilentlyContinue } else {
    $malos++
    "intento ${i}: salida $('0x{0:X8}' -f [int]$c) a los $seg s; stderr $((Get-Item $e).Length) bytes, stdout $((Get-Item $o).Length) bytes"
    Get-Content $e -TotalCount 12
  }
}
"buenos $buenos, malos $malos"
