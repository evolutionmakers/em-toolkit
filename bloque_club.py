"""Mete el bloque del Club debajo del resultado de cada herramienta (modo socio, BZ-20261112-220607).
Uso: python3 bloque_club.py <url base del Club, sin barra final>
Idempotente: si el bloque ya está, lo sustituye."""
import re, sys, os
CLUB = sys.argv[1].rstrip('/')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SLUGS = ['cobro-y-pago', 'funciona-sin-ti', 'leyes-que-te-afectaran', 'margen-de-verdad',
         'plan-2027-en-un-folio', 'tareas-para-la-ia', 'test-de-resistencia']
CSS = ('<style id="club-css">.clb{margin-top:22px;padding:18px 20px;border:1px solid var(--line);border-left:4px solid var(--yellow);'
       'border-radius:16px;background:var(--white)}.clb h3{font:700 19px/1.3 var(--head);color:var(--ink);margin:0 0 6px}'
       '.clb p{margin:0 0 10px;font-size:16px}.clb ul{margin:0 0 10px;padding-left:20px;font-size:16px}.clb li{margin:2px 0}'
       '.clb .trow{margin-top:8px}.clb .nota{font-size:15px;color:var(--soft);margin:6px 0 0}</style>')
def bloque(slug):
    return f'''<!--club-ini--><div class="clb" id="club-bloque">
<h3>Esto se puede seguir mes a mes</h3>
<p>La hoja te sirve para hoy. En Evolution Club lo guardas, Evolution Analytics lo lee cada mes y te dice qué se mueve.</p>
<ul><li>Tus números, leídos cada mes: qué mejora, qué se tuerce y por qué.</li>
<li>Tu empresa al lado de las de tu sector, con cifras de verdad y no con impresiones.</li>
<li>Una vez al mes, salvo agosto, con empresarios como tú y los problemas encima de la mesa.</li></ul>
<p>Una foto está bien. Lo que te dice hacia dónde vas es la película.</p>
<div class="trow"><a class="pill" href="https://evolutionmakers.plus/solicitar-plaza">Solicitar plaza</a>
<button class="lnk" type="button" id="b-club">¿Ya eres socio? Entra y guárdalo</button></div>
<p class="nota">Estamos reuniendo a los treinta primeros y quedan plazas.</p>
<span class="ok" id="club-ok" role="status"></span></div>
<script>(function(){{const CLUB='{CLUB}',H='{slug}',b=document.getElementById('b-club'),o=document.getElementById('club-ok');
b.onclick=function(){{let r=null;try{{r=window.EMT&&EMT.resumen?EMT.resumen():null;}}catch(e){{r=null;}}
if(!r){{o.style.color='var(--red)';o.textContent='Primero saca tu resultado: el ejemplo no se guarda.';return;}}
o.textContent='';window.open(CLUB+'/toolkit/guardar#h='+H+'&d='+EMT.cod(r),'_blank','noopener');}};}})();</script><!--club-fin-->'''
for slug in SLUGS:
    f = slug + '.html'; s = open(f, encoding='utf-8').read()
    s = re.sub(r'<!--club-ini-->.*?<!--club-fin-->', '', s, flags=re.S)
    s = re.sub(r'<style id="club-css">.*?</style>', '', s, flags=re.S)
    m = re.search(r'<span class="ok" id="copy-ok"[^>]*></span>', s)
    assert m, f
    s = s[:m.end()] + bloque(slug) + s[m.end():]
    s = s.replace('</head>', CSS + '</head>', 1)
    open(f, 'w', encoding='utf-8').write(s); print('ok', f)
