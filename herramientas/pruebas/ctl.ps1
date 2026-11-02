param(
  [string]$Shots,
  [string]$Click = '',      # "x,y;x,y" en coordenadas de la captura de ventana
  [string]$Keys = '',       # texto a teclear (SendKeys)
  [string]$Raw = '',        # teclas virtuales hex separadas por coma, p.ej. "DC" o "6B"
  [int]$Wait = 1,
  [string]$Shot = '',
  [string]$Hover = '',      # "x,y" mueve el raton sin pulsar
  [string]$Rueda = '',      # "x,y,n": n pasos de rueda hacia abajo, o hacia arriba si es negativo
  [string]$Proc = 'v2game'
)
# Control basico del juego en ventana: enfoca, hace clic, teclea y captura.
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
Add-Type @'
using System; using System.Runtime.InteropServices;
public class C {
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L,T,R,B; }
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint x, uint y, uint d, UIntPtr e);
  [DllImport("user32.dll")] public static extern void keybd_event(byte vk, byte sc, uint f, UIntPtr e);
  [DllImport("user32.dll")] public static extern uint MapVirtualKey(uint c, uint t);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
}
'@
$p = Get-Process $Proc -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $p) { 'juego no esta abierto'; exit 1 }
$h = $p.MainWindowHandle
if ($Proc -ne 'v2game') {
  # Windows solo cede el primer plano tras una pulsacion: ALT lo permite
  [C]::keybd_event(0x12, 0, 0, [UIntPtr]::Zero); [C]::keybd_event(0x12, 0, 2, [UIntPtr]::Zero)
} else { [C]::ShowWindow($h, 9) | Out-Null }
[C]::SetForegroundWindow($h) | Out-Null
Start-Sleep -Milliseconds 400
$r = New-Object C+RECT; [C]::GetWindowRect($h, [ref]$r) | Out-Null
# Nunca enviar raton ni teclado si la ventana del juego no esta delante
if (($Click -or $Raw -or $Keys -or $Hover -or $Rueda) -and [C]::GetForegroundWindow() -ne $h) { 'la ventana no esta delante: no envio nada'; exit 2 }
if ($Rueda) {
  $v = $Rueda -split ','
  [C]::SetCursorPos($r.L + [int]$v[0], $r.T + [int]$v[1]) | Out-Null
  Start-Sleep -Milliseconds 300
  $d = if ([int]$v[2] -gt 0) { [uint32]4294967176 } else { [uint32]120 }
  for ($i = 0; $i -lt [math]::Abs([int]$v[2]); $i++) { [C]::mouse_event(0x0800, 0, 0, $d, [UIntPtr]::Zero); Start-Sleep -Milliseconds 40 }
}
foreach ($c in ($Click -split ';' | Where-Object { $_ })) {
  $xy = $c -split ','
  [C]::SetCursorPos($r.L + [int]$xy[0], $r.T + [int]$xy[1]) | Out-Null
  Start-Sleep -Milliseconds 250
  [C]::mouse_event(2, 0, 0, 0, [UIntPtr]::Zero); Start-Sleep -Milliseconds 90; [C]::mouse_event(4, 0, 0, 0, [UIntPtr]::Zero)
  Start-Sleep -Milliseconds 500
}
if ($Hover) { $xy = $Hover -split ','; [C]::SetCursorPos($r.L + [int]$xy[0], $r.T + [int]$xy[1]) | Out-Null }
foreach ($k in ($Raw -split ',' | Where-Object { $_ })) {
  $vk = [Convert]::ToByte($k, 16); $sc = [byte][C]::MapVirtualKey($vk, 0)
  [C]::keybd_event($vk, $sc, 0, [UIntPtr]::Zero); Start-Sleep -Milliseconds 90; [C]::keybd_event($vk, $sc, 2, [UIntPtr]::Zero)
  Start-Sleep -Milliseconds 300
}
if ($Keys) { [Windows.Forms.SendKeys]::SendWait($Keys); Start-Sleep -Milliseconds 300 }
Start-Sleep -Seconds $Wait
if ($Shot) {
  [C]::GetWindowRect($h, [ref]$r) | Out-Null
  $bmp = New-Object Drawing.Bitmap ($r.R - $r.L), ($r.B - $r.T)
  $g = [Drawing.Graphics]::FromImage($bmp); $g.CopyFromScreen($r.L, $r.T, 0, 0, $bmp.Size)
  $bmp.Save((Join-Path $Shots $Shot), [Drawing.Imaging.ImageFormat]::Png); $g.Dispose(); $bmp.Dispose()
}
$p.Refresh()
"ok ram {0} MB virt {1} MB cpu {2}s resp {3}" -f [math]::Round($p.WorkingSet64 / 1MB), [math]::Round($p.VirtualMemorySize64 / 1MB), [math]::Round($p.TotalProcessorTime.TotalSeconds), $p.Responding
