'use strict';
const modules = [
['L1','Listas','Productos disponibles y retirados','Escanea productos, consulta su cantidad y precio y conserva el historial de los que retiras.',[['clave','Clave para retirar','P1']],[['escanear','Escanear producto'],['retirar','Retirar por clave']]],
['L2','Listas','Pares e impares','Genera números aleatorios y descubre cómo se separan en dos listas según su paridad.',[['cantidad','Cantidad de números','20']],[['generar','Generar y separar']]],
['L3','Listas','Aprobados y reprobados','Registra alumnos con calificaciones de 0 a 10. Desde 7 se aprueba; debajo de 7 se reprueba.',[['nombre','Nombre del alumno',''],['nota','Calificación','8.5']],[['agregar','Agregar y clasificar']]],
['L4','Listas','Eliminar y ordenar productos','Organiza tu compra por nombre, elimina por clave y consulta el costo total.',[['clave','Clave única',''],['nombre','Nombre del producto',''],['precio','Precio ($)','']],[['agregar','Agregar producto'],['eliminar','Eliminar por clave']]],
['L5','Listas','Palabras por letra','Una lista para cada inicial. Las nuevas letras crean sus propios grupos automáticamente.',[['palabra','Palabra','']],[['agregar','Agregar palabra']]],
['P1','Pilas','Invertir palabra','Una pila guarda los caracteres y los devuelve en orden inverso. Prueba con UTM.',[['texto','Palabra','UTM']],[['invertir','Invertir palabra']]],
['P2','Pilas','Palíndromo','Comprueba si una palabra, frase o número se lee igual hacia adelante y hacia atrás.',[['texto','Palabra, frase o número','Anita lava la tina']],[['comprobar','Comprobar']]],
['P3','Pilas','Suma de números grandes','Suma enteros no negativos dígito a dígito mediante pilas. Sin límite fijo de dígitos.',[['a','Primer número','999999999999999999999'],['b','Segundo número','1']],[['sumar','Sumar números']]],
['P4','Pilas','Reemplazar valor','Sustituye cada aparición del valor viejo sin cambiar el orden de los demás elementos.',[['valores','Valores separados por comas','1,2,3,2'],['viejo','Valor viejo','2'],['nuevo','Valor nuevo','9']],[['reemplazar','Reemplazar']]],
['C1','Colas','Ventanilla de banco','El primero en llegar es el primero en ser atendido. Consulta turnos y tiempos de espera.',[['nombre','Nombre del cliente',''],['movimiento','Movimiento',['Pago de servicio','Depósito','Retiro','Compra de tiempo-aire','Consulta de saldo']],['capacidad','Capacidad (con cola vacía)','5']],[['agregar','Agregar a la cola'],['atender','Atender en ventanilla'],['configurar','Configurar capacidad']]],
['C2','Colas','Juego de pintar coches','Pinta el primer coche con el color solicitado. Llegan cada 20 segundos; la velocidad aumenta cada tres aciertos. Pierdes al acumular cinco.',[],[['iniciar','Iniciar partida'],['pintar','Rojo'],['pintar','Azul'],['pintar','Verde'],['pintar','Amarillo'],['pintar','Naranja']]],
['C3','Colas','Estacionamiento de autos','Una cola circular doblemente ligada sin cupo fijo. Sale el primero que entró; tarifa de $2.00 por segundo completo.',[['placas','Placas del auto',''],['propietario','Nombre del propietario','']],[['entrar','Entrada de auto'],['salir','Salida de auto']]]
];
const $ = id => document.getElementById(id);
const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const money = n => new Intl.NumberFormat('es-MX',{style:'currency',currency:'MXN'}).format(n);
const date = s => new Date(s).toLocaleString('es-MX');
const colors = {Rojo:'#d55a50',Azul:'#508bc2',Verde:'#4b9b72',Amarillo:'#e9c85d',Naranja:'#df8f49'};
let selected = modules[0], state, busy = false;
const empty = (text='Aquí aparecerán tus resultados al realizar una operación.') => `<div class="empty"><span>↗</span>${escape(text)}</div>`;
function table(rows, columns){
 if(!rows?.length) return empty('La lista está vacía.');
 return `<div class="table-wrap"><table><thead><tr>${columns.map(c=>`<th>${escape(c[1])}</th>`).join('')}</tr></thead><tbody>${rows.map(row=>`<tr>${columns.map(c=>`<td>${escape(c[2]?c[2](row[c[0]]):row[c[0]])}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
}
const title = text => `<h4>${escape(text)}</h4>`;
const chips = list => list.length ? `<div class="chips">${list.map(x=>`<span class="chip">${escape(x)}</span>`).join('')}</div>` : empty('Sin elementos.');
const metrics = entries => `<div class="metrics">${entries.map(([n,label])=>`<div class="metric"><strong>${escape(n)}</strong><span>${escape(label)}</span></div>`).join('')}</div>`;
const productCols = [['clave','Clave'],['nombre','Producto'],['cantidad','Cantidad'],['precio','Precio',money]];
function render(){
 if(!state) return;
 const d = state[selected[0].toLowerCase()];
 if(!d){$('output').innerHTML=empty();return;}
 let html='';
 switch(selected[0]){
 case 'L1': html=metrics([[d.disponibles.length,'DISPONIBLES'],[d.retirados.length,'RETIRADOS']])+title('Productos disponibles')+table(d.disponibles,productCols)+title('Historial de retirados')+table(d.retirados,productCols);break;
 case 'L2': html=title('Lista original')+chips(d.original)+title('Números pares')+chips(d.pares)+title('Números impares')+chips(d.impares);break;
 case 'L3': {const cols=[['nombre','Alumno'],['calificacion','Calificación']];html=title('Aprobados · calificación ≥ 7')+table(d.aprobados,cols)+title('Reprobados · calificación < 7')+table(d.reprobados,cols);break;}
 case 'L4':html=metrics([[money(d.total),'TOTAL DE COMPRA']])+table(d.productos,productCols);break;
 case 'L5':html=title('Lista original')+chips(d.original)+Object.entries(d.grupos).map(([k,v])=>title(`Inicial ${k}`)+chips(v)).join('');break;
 case 'P1':case 'P2':case 'P3':html=`<div class="answer">${escape(d.resultado)}</div>`;break;
 case 'P4':html=metrics([[d.cambios,'REEMPLAZOS']])+title('Cima → base de la pila')+chips(d.pila);break;
 case 'C1':html=metrics([[d.frente,'FRENTE'],[d.final,'FINAL'],[`${d.clientes.length}/${d.capacidad}`,'EN LA COLA']])+table(d.clientes,[['turno','Turno'],['nombre','Cliente'],['movimiento','Movimiento'],['llegada','Llegada',date]])+(d.atencion?`<p class="receipt">Último atendido: ${escape(d.atencion.cliente.nombre)}<br>Tiempo de espera: ${d.atencion.segundos} segundos.</p>`:'');break;
 case 'C2':html=metrics([[d.pintados,'COCHES PINTADOS'],[`${d.coches.length}/5`,'EN LA COLA'],[`${d.segundos} s`,'TIEMPO TOTAL'],[`${d.intervalo} s`,'ENTRE LLEGADAS'],[`${d.record} / ${d.tiempoRecord} s`,'RÉCORD / TIEMPO']])+`<p class="queue-note">${d.activo?'Pinta el coche de la izquierda.':'Inicia una partida para jugar.'}</p><div class="cars">${d.coches.map((c,i)=>`<div class="car"><svg viewBox="0 0 150 90" role="img" aria-label="Coche ${c.numero}"><path d="M12 44h20l17-24h49l19 24h19v28H12z" fill="#83978e"/><path d="M54 26h38l13 18H42z" fill="#d9e9e9"/><circle cx="40" cy="72" r="13" fill="#243b35"/><circle cx="112" cy="72" r="13" fill="#243b35"/><circle cx="40" cy="72" r="6" fill="#f4f5f0"/><circle cx="112" cy="72" r="6" fill="#f4f5f0"/></svg><div class="color-label"><span class="color-dot" data-color="${escape(c.color)}"></span>${escape(c.color)}</div>${i===0?'↑ Primero en la cola':`Coche #${c.numero}`}</div>`).join('')}</div>`;break;
 case 'C3':html=metrics([[d.autos.length,'AUTOS ESTACIONADOS']])+table(d.autos,[['placas','Placas'],['propietario','Propietario'],['entrada','Entrada',date]])+(d.recibo?title('Recibo de salida')+`<div class="receipt">Placas: ${escape(d.recibo.auto.placas)} · Propietario: ${escape(d.recibo.auto.propietario)}<br>Entrada: ${escape(date(d.recibo.auto.entrada))}<br>Salida: ${escape(date(d.recibo.salida))}<br>Tiempo: ${d.recibo.segundos} segundos<br><strong>Total: ${escape(money(d.recibo.costo))}</strong></div>`:'');break;
 }
 $('output').innerHTML=html;
 document.querySelectorAll('[data-color]').forEach(el=>{el.style.backgroundColor=colors[el.dataset.color]||'#ccc';});
}
function choose(m){
 selected=m;
 document.querySelectorAll('nav button').forEach(b=>{const active=b.dataset.id===m[0];b.classList.toggle('active',active);b.setAttribute('aria-current',active?'page':'false');});
 $('category').textContent=`${{Listas:'01',Pilas:'02',Colas:'03'}[m[1]]} / ${m[1].toUpperCase()}`;
 $('number').textContent=`EJERCICIO ${m[0]}`;$('title').textContent=m[2];$('description').textContent=m[3];
 $('fields').innerHTML=m[4].map(([name,label,value])=>`<div class="field"><label for="${name}">${escape(label)}</label>${Array.isArray(value)?`<select id="${name}" name="${name}">${value.map(v=>`<option>${escape(v)}</option>`).join('')}</select>`:`<input id="${name}" name="${name}" maxlength="20000" autocomplete="off" value="${escape(value)}">`}</div>`).join('');
 $('actions').innerHTML=m[5].map(([action,label],i)=>`<button type="button" data-action="${action}" class="${i?'secondary':''}">${escape(label)}</button>`).join('');
 $('actions').querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>act(b.dataset.action,b.textContent)));
 $('status').className='';$('status').textContent='Listo para comenzar.';render();
}
async function act(action,label){
 if(busy)return; busy=true;const modulo=selected[0];
 const values=Object.fromEntries(new FormData($('form')));if(modulo==='C2'&&action==='pintar')values.color=label;
 document.querySelectorAll('#actions button,nav button').forEach(b=>b.disabled=true);
 try{
  const response=await fetch('/api/accion',{method:'POST',headers:{'Content-Type':'application/json','X-Practica':'1'},body:JSON.stringify({modulo,accion:action,valores:values})});
  const data=await response.json();if(!response.ok)throw Error(data.error||'No se pudo realizar la operación.');
  state=data.estado;$('status').className='';$('status').textContent=data.mensaje;render();
 }catch(e){$('status').className='error';$('status').textContent=e.message;}
 finally{busy=false;document.querySelectorAll('#actions button,nav button').forEach(b=>b.disabled=false);}
}
async function refresh(){
 if(busy)return;
 try{const response=await fetch('/api/estado');if(!response.ok)throw Error('No se pudo conectar con el servidor.');state=await response.json();render();}
 catch(e){$('status').className='error';$('status').textContent='No se pudo conectar con el servidor. Verifica que siga ejecutándose.';}
}
let category='';
for(const m of modules){if(m[1]!==category){category=m[1];const h=document.createElement('div');h.className='group-title';h.textContent=category.toUpperCase();$('menu').append(h);}const b=document.createElement('button');b.type='button';b.dataset.id=m[0];b.textContent=`${m[0].slice(1)}. ${m[2]}`;b.addEventListener('click',()=>choose(m));$('menu').append(b);}
$('form').addEventListener('submit',e=>{e.preventDefault();act(selected[5][0][0],selected[5][0][1]);});
choose(selected);refresh();setInterval(()=>{if(selected[0]==='C2')refresh();},1000);
