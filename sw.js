/* DELTADIS-SW-1-0810 — deixa o app do motorista abrir sem internet.
   Com internet: sempre pega a versão nova do site e guarda uma cópia.
   Sem internet: abre a última cópia guardada. */
var CACHE='deltadis-app-v1';
self.addEventListener('install',function(e){ self.skipWaiting(); });
self.addEventListener('activate',function(e){
  e.waitUntil(caches.keys().then(function(ks){ return Promise.all(ks.filter(function(k){ return k!==CACHE; }).map(function(k){ return caches.delete(k); })); }).then(function(){ return self.clients.claim(); }));
});
self.addEventListener('fetch',function(e){
  var r=e.request;
  if(r.method!=='GET') return;
  var u=new URL(r.url);
  if(u.origin!==self.location.origin) return;           /* API e outros sites: não mexe */
  if(r.mode!=='navigate') return;                        /* só a página do app */
  e.respondWith(
    fetch(r).then(function(res){
      if(res&&res.ok){ var c=res.clone(); caches.open(CACHE).then(function(ch){ ch.put('/app-offline',c); }); }
      return res;
    }).catch(function(){
      return caches.open(CACHE).then(function(ch){ return ch.match('/app-offline'); }).then(function(m){
        return m||new Response('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><body style="font-family:sans-serif;padding:30px;text-align:center"><h3>Sem internet</h3><p>Abra o app uma vez com sinal para ele funcionar sem internet.</p></body>',{headers:{'Content-Type':'text/html; charset=utf-8'}});
      });
    })
  );
});
