$ErrorActionPreference = 'Stop'
$raizPractica = Split-Path -Parent $PSScriptRoot
$puertoPractica = 5187
$basePractica = "http://127.0.0.1:$puertoPractica"
$resultadosPractica = [System.Collections.Generic.List[string]]::new()
$sesionPractica = [Microsoft.PowerShell.Commands.WebRequestSession]::new()
$encabezadosPractica = @{ 'X-Practica' = '1' }
function Confirmar-Practica($condicion, $nombre) {
    if (-not $condicion) { throw "Falló: $nombre" }
    $resultadosPractica.Add("OK | $nombre")
}
function Ejecutar-Practica($modulo, $accion, $valores = @{}) {
    $cuerpoPractica = @{ modulo = $modulo; accion = $accion; valores = $valores } | ConvertTo-Json -Depth 5
    Invoke-RestMethod "$basePractica/api/accion" -Method Post -WebSession $sesionPractica -Headers $encabezadosPractica -ContentType 'application/json; charset=utf-8' -Body ([System.Text.Encoding]::UTF8.GetBytes($cuerpoPractica))
}
function Rechazar-Practica($modulo, $accion, $valores, $nombre) {
    try { Ejecutar-Practica $modulo $accion $valores | Out-Null }
    catch {
        if ([int]$_.Exception.Response.StatusCode -eq 400) { Confirmar-Practica $true $nombre; return }
        throw
    }
    throw "Se esperaba un error 400: $nombre"
}
$servidorPractica = $null
try {
    dotnet build (Join-Path $raizPractica 'Web\PracticaWeb.csproj') -c Release --nologo
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo compilar la versión web.' }
    $dllPractica = Join-Path $raizPractica 'Web\bin\Release\net10.0\PracticaWeb.dll'
    $servidorPractica = Start-Process dotnet -ArgumentList "`"$dllPractica`" --urls $basePractica" -WorkingDirectory (Join-Path $raizPractica 'Web') -WindowStyle Hidden -PassThru
    $listoPractica = $false
    for ($i = 0; $i -lt 40; $i++) {
        try { $estadoPractica = Invoke-RestMethod "$basePractica/api/estado" -WebSession $sesionPractica; $listoPractica = $true; break } catch { Start-Sleep -Milliseconds 250 }
    }
    if (-not $listoPractica) { throw 'El servidor web no inició.' }
    Confirmar-Practica ((Invoke-WebRequest $basePractica -UseBasicParsing).StatusCode -eq 200) 'Página web disponible'
    Ejecutar-Practica L1 escanear | Out-Null
    $r = Ejecutar-Practica L1 retirar @{ clave = 'P1' }
    Confirmar-Practica ($r.estado.l1.retirados.Count -eq 1 -and $r.estado.l1.disponibles.Count -eq 0) 'L1: escanear y retirar'
    $r = Ejecutar-Practica L2 generar @{ cantidad = '50' }
    Confirmar-Practica ($r.estado.l2.original.Count -eq 50 -and ($r.estado.l2.pares.Count + $r.estado.l2.impares.Count) -eq 50) 'L2: clasificación completa'
    Ejecutar-Practica L3 agregar @{nombre='Ana';nota='7'} | Out-Null
    $r = Ejecutar-Practica L3 agregar @{nombre='Luis';nota='6.99'}
    Confirmar-Practica ($r.estado.l3.aprobados.Count -eq 1 -and $r.estado.l3.reprobados.Count -eq 1) 'L3: límite de aprobación'
    Ejecutar-Practica L4 agregar @{clave='P1';nombre='Zanahoria';precio='15,50'} | Out-Null
    $r = Ejecutar-Practica L4 agregar @{clave='P2';nombre='Arroz';precio='32.75'}
    Confirmar-Practica ($r.estado.l4.total -eq 48.25 -and $r.estado.l4.productos[0].nombre -eq 'Arroz') 'L4: orden y total decimal'
    $r = Ejecutar-Practica L4 eliminar @{clave='P2'}
    Confirmar-Practica ($r.estado.l4.total -eq 15.50) 'L4: eliminar por clave'
    Ejecutar-Practica L5 agregar @{palabra='Fresa'} | Out-Null
    $r = Ejecutar-Practica L5 agregar @{palabra='Fresca'}
    Confirmar-Practica ($r.estado.l5.grupos.F.Count -eq 2) 'L5: grupos por letra'
    $r = Ejecutar-Practica P1 invertir @{texto='UTM'}
    Confirmar-Practica ($r.estado.p1.resultado -eq 'MTU') 'P1: invertir palabra'
    $r = Ejecutar-Practica P2 comprobar @{texto='Anita lava la tina'}
    Confirmar-Practica ($r.estado.p2.resultado -eq 'Sí es palíndromo.') 'P2: palíndromo'
    $r = Ejecutar-Practica P3 sumar @{a=('9' * 1000);b='1'}
    Confirmar-Practica ($r.estado.p3.resultado -eq ('1' + ('0' * 1000))) 'P3: acarreo de mil dígitos'
    $r = Ejecutar-Practica P4 reemplazar @{valores='1,2,3,2';nuevo='9';viejo='2'}
    Confirmar-Practica (($r.estado.p4.pila -join ',') -eq '9,3,9,1' -and $r.estado.p4.cambios -eq 2) 'P4: reemplazar conservando el orden'
    Ejecutar-Practica C1 configurar @{capacidad='1'} | Out-Null
    Ejecutar-Practica C1 agregar @{nombre='Ana';movimiento='Depósito'} | Out-Null
    Rechazar-Practica C1 agregar @{nombre='Luis';movimiento='Retiro'} 'C1: rechazar sobreflujo'
    $r = Ejecutar-Practica C1 atender
    Confirmar-Practica ($r.estado.c1.frente -eq -1 -and $r.estado.c1.atencion.cliente.nombre -eq 'Ana') 'C1: atención FIFO y cola vacía'
    $r = Ejecutar-Practica C2 iniciar
    Confirmar-Practica ($r.estado.c2.coches.Count -eq 1 -and $r.estado.c2.activo) 'C2: partida y coche inicial'
    $r = Ejecutar-Practica C2 pintar @{color=$r.estado.c2.coches[0].color}
    Confirmar-Practica ($r.estado.c2.pintados -eq 1 -and $r.estado.c2.coches.Count -eq 0) 'C2: pintar el primer coche'
    Ejecutar-Practica C3 entrar @{placas='abc-123';propietario='Ana'} | Out-Null
    Ejecutar-Practica C3 entrar @{placas='xyz-987';propietario='Luis'} | Out-Null
    $r = Ejecutar-Practica C3 salir
    Confirmar-Practica ($r.estado.c3.recibo.auto.placas -eq 'ABC-123' -and $r.estado.c3.autos[0].placas -eq 'XYZ-987') 'C3: salida FIFO y recibo'
    Rechazar-Practica L3 agregar @{nombre='Error';nota='11'} 'Validación: nota fuera de rango'
    Rechazar-Practica P3 sumar @{a='-1';b='2'} 'Validación: suma inválida'
    Rechazar-Practica C3 entrar @{placas='XYZ-987';propietario='Otro'} 'Validación: placas repetidas'
    $sesionAislada = [Microsoft.PowerShell.Commands.WebRequestSession]::new()
    $aislado = Invoke-RestMethod "$basePractica/api/estado" -WebSession $sesionAislada
    Confirmar-Practica ($aislado.l1.retirados.Count -eq 0 -and $aislado.l3.aprobados.Count -eq 0) 'Sesiones: datos separados por navegador'
    try { Invoke-RestMethod "$basePractica/api/accion" -Method Post -ContentType 'application/json' -Body '{"modulo":"L1","accion":"escanear","valores":{}}' | Out-Null; throw 'Falta la protección de solicitudes.' }
    catch { if ([int]$_.Exception.Response.StatusCode -ne 400) { throw }; Confirmar-Practica $true 'Solicitudes: cabecera requerida' }
    $resultadosPractica.Add("TOTAL: $($resultadosPractica.Count) verificaciones web correctas. Sin fallos.")
    $resultadosPractica | Set-Content (Join-Path $raizPractica 'pruebas-web.txt') -Encoding utf8
    $resultadosPractica | ForEach-Object { Write-Host $_ }
} finally {
    if ($servidorPractica -and -not $servidorPractica.HasExited) { Stop-Process -Id $servidorPractica.Id }
}
