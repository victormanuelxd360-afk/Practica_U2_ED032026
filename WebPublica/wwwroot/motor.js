'use strict';
window.practicaMotorReady = (async () => {
    await Blazor.start();
    try {
        const record = JSON.parse(localStorage.getItem('practica-u2-record') || 'null');
        if (record && Number.isSafeInteger(record.coches) && Number.isSafeInteger(record.segundos)) {
            await DotNet.invokeMethodAsync('PracticaPublica', 'RestaurarRecord', Math.max(0, record.coches), Math.max(0, record.segundos));
        }
    } catch { /* El navegador puede deshabilitar el almacenamiento local. */ }
    function recordar(estado) {
        try { localStorage.setItem('practica-u2-record', JSON.stringify({coches: estado.c2.record, segundos: estado.c2.tiempoRecord})); } catch { }
        return estado;
    }
    return {
        async read() { return recordar(JSON.parse(await DotNet.invokeMethodAsync('PracticaPublica', 'Consultar'))); },
        async action(solicitud) {
            const r = JSON.parse(await DotNet.invokeMethodAsync('PracticaPublica', 'Ejecutar', JSON.stringify(solicitud)));
            if (r.error) throw Error(r.error);
            recordar(r.estado);
            return r;
        }
    };
})();
