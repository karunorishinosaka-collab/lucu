// 使い方：window.__IDS='id1,id2' を入れてから実行。くわしい情報を window.__X（JSON文字列）に入れる
(async()=>{const out=[];for(const id of (window.__IDS||'').split(',').filter(Boolean)){
const h=await (await fetch('/items/'+id)).text();const d=new DOMParser().parseFromString(h,'text/html');
const n=(d.querySelector('meta[property="og:title"]')?.content||'').replace(/ \| アジアン雑貨ルチュ.*$/,'').trim();
const p=(d.querySelector('.p-item-price')?.textContent||'').trim().replace(/[^\d,]/g,'');
const desc=(d.querySelector('.p-item-summary')?.textContent||'').trim();
const ph=[...new Set([...d.querySelectorAll('.p-item-view-thumbnail-pic img')].map(im=>(im.getAttribute('src')||'').match(/([0-9a-f]{32}\.(?:jpg|jpeg|png|gif|webp))/i)?.[1]).filter(Boolean))];
const s=d.querySelector('select');let v=[];if(s&&!/^\d+$/.test((s.options[0]||{}).textContent?.trim()||'')){v=[...s.options].map(o=>o.textContent.trim().replace(/[\s　]+/g,' '))}
out.push({id,n,p,off:'',d:desc,ph,v});}
window.__X=JSON.stringify(out);window.__XP='done';})();'started'
