// ルチュのウェブショップ（https://ajianlucu.thebase.in/ のタブ）で実行。売っている商品のID一覧を window.__L に入れる
(async()=>{const live=[],sold=[],seen=new Set();
for(let p=1;p<=80;p++){const t=await (await fetch('/load_items/'+p)).text();const d=new DOMParser().parseFromString(t,'text/html');
const as=[...d.querySelectorAll('a[href*="/items/"]')];if(!as.length)break;let add=0;
for(const a of as){const id=a.href.match(/items\/(\d+)/)?.[1];if(!id||seen.has(id))continue;seen.add(id);add++;
const c=a.closest('li,div.c-card,article')||a;(/SOLD OUT/.test(c.textContent)?sold:live).push(id);}
if(!add)break;}
window.__L=live.join(',');window.__LS=sold.length;window.__LP='done';})();'started'
