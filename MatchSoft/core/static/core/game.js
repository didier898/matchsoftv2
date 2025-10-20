(function(){
  function qs(sel){ return document.querySelector(sel); }
  function qsa(sel){ return Array.from(document.querySelectorAll(sel)); }
  function csrf(){ const el=document.querySelector('input[name=csrfmiddlewaretoken]'); return el? el.value: ''; }

  qsa('.ll').forEach(btn=>{
    btn.addEventListener('click',()=>{
      const kind=btn.getAttribute('data-ll');
      fetch(`/comodin/${kind}/`,{
        method:'POST',
        headers:{'X-CSRFToken':csrf()},
      }).then(r=>r.json()).then(data=>{
        if(!data.ok){qs('#ll-out').textContent=data.error||'Error';return;}
        if(data.type==='5050'){
          (data.disable||[]).forEach(lbl=>{
            const labelEl=qsa('label.opt').find(l=>l.textContent.trim().startsWith(lbl));
            if(labelEl){labelEl.classList.add('disabled');labelEl.style.filter='grayscale(100%)';}
          });
          qs('#ll-out').textContent='Se eliminaron dos opciones.';
        }
        if(data.type==='audiencia'){
          const poll=data.poll||{};
          const txt=['A','B','C','D'].map(k=>`${k}: ${poll[k]||0}%`).join('  ·  ');
          qs('#ll-out').textContent=`Audiencia opina → ${txt}`;
        }
        if(data.type==='amigo'){
          qs('#ll-out').textContent=data.hint||'Tu amigo no respondió';
        }
        if(data.type==='cambiar'){
          location.reload();
        }
        btn.classList.add('opacity-50');
        btn.style.pointerEvents='none';
      }).catch(()=>{qs('#ll-out').textContent='No se pudo usar el comodín.';});
    });
  });
})();
