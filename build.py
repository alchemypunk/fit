#!/usr/bin/env python3
"""从 index.html + data.js 生成 plan-full.html（长文版）和 晨练推拉腿计划.html（内联版，用于 claude 链接）。
改完 index.html 或 data.js 后运行：python3 build.py"""
import re,pathlib
root=pathlib.Path(__file__).parent
idx=(root/'index.html').read_text(encoding='utf-8')
data=(root/'data.js').read_text(encoding='utf-8')
style=re.search(r'<style>.*?</style>',idx,re.S).group(0)
doc=re.search(r'<main class="doc hidden" id="docView">(.*?)</main>',idx,re.S).group(1)

long_css="""<style>
body{display:block;overflow:auto;height:auto}
.wrap{max-width:860px;margin:0 auto;padding-inline:18px;padding-block:24px 64px}
.wrap h1{font-size:1.8rem;font-weight:900}
.lead{color:var(--muted)}
.dayhead{margin-top:2.6rem;padding-top:1rem;border-top:3px solid var(--fg);scroll-margin-top:12px}
.dayhead h2{font-size:1.4rem;font-weight:800;margin:0}
.dayhead .sub{color:var(--muted);font-size:.9rem}
.blockhead{font-family:var(--font-num);font-size:.72rem;letter-spacing:.14em;color:var(--accent);text-transform:uppercase;margin:1.6rem 0 .2rem}
.ex{display:grid;grid-template-columns:200px 1fr;gap:16px;border:1px solid var(--line);background:var(--surface);border-radius:10px;padding:14px;margin-top:12px}
.ex .fig{background:var(--figbg);border-radius:8px;padding:10px;min-width:0}
.ex .fig svg{width:100%;height:auto;display:block;margin-top:8px}
.ex .fig figcaption,.ex .fig .pcap{font-size:.72rem;color:var(--muted);text-align:center;padding-top:4px}
.ex .info{padding:0;min-width:0}
.ex .info h2{font-size:1.05rem}
@media (max-width:560px){.ex{grid-template-columns:1fr}.ex .fig{max-width:260px;margin:0 auto}}
.doc{padding:0;overflow:visible}
.flowtbl{border-collapse:collapse;width:100%;font-size:.9rem;margin-top:.8rem}
.flowtbl th,.flowtbl td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
.flowtbl th{font-size:.74rem;color:var(--muted);font-weight:500}
.toc{display:flex;flex-wrap:wrap;gap:8px;margin-top:1rem}
.toc a{border:1px solid var(--line);border-radius:999px;padding:4px 12px;font-size:.85rem;text-decoration:none;color:var(--fg);background:var(--surface)}
.sheet tr.row{cursor:default}
</style>"""

plan_full=f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>晨练推拉腿计划 · 长文版</title>
{style}
{long_css}
</head>
<body>
<div class="wrap">
  <div style="font-family:var(--font-num);font-size:.72rem;letter-spacing:.14em;color:var(--accent);text-transform:uppercase">Morning · Push / Pull / Glutes+Legs · 60 min</div>
  <h1>晨练推拉腿计划 · 长文版</h1>
  <p class="lead">和手机卡片版（<a href="index.html">index.html</a>）是同一份数据，这里把总表和所有动作顺序列出来，适合在电脑上通读。</p>
  <div class="toc"><a href="#sheet-sec">训练总表</a><a href="#doc">说明</a><a href="#day-common">固定部分</a><a href="#day-push">推日</a><a href="#day-pull">拉日</a><a href="#day-legs">臀腿日</a><a href="#day-upper">上肢混合（5 天版）</a></div>
  <div class="dayhead" id="sheet-sec"><h2>训练总表</h2><div class="sub">与表格一一对应。前四个阶段每天都做，后三个按训练日轮换。</div></div>
  <div class="tbl"><table class="sheet" id="sheet"></table></div>
  <div class="doc dayhead" id="doc">{doc}</div>
  <div id="days"></div>
</div>
<script src="data.js"></script>
<script>
(function(){{
  var P=window.PLAN,EX=P.EX,out='',EQ={{'双杆':'双杠','划船':'划船机'}};
  var h='<thead><tr><th>设备</th><th>动作</th><th>时间</th><th>组数</th><th>次数</th><th>要领</th><th>备注</th></tr></thead><tbody>',cur='';
  P.ROWS.forEach(function(r){{if(r.stage!==cur){{cur=r.stage;h+='<tr class="grp"><td colspan="7">'+cur+'</td></tr>';}}
    h+='<tr class="row"><td>'+r.equip+'</td><td>'+r.name+'</td><td>'+r.time+'</td><td>'+r.sets+'</td><td>'+r.reps+'</td><td>'+r.cue+'</td><td>'+r.note+'</td></tr>';}});
  document.getElementById('sheet').innerHTML=h+'</tbody>';
  function card(st,n){{
    var e=EX[st.id],more=(e.more||[]).slice(),cue=st.cue;if(!cue&&more.length)cue=more.shift();
    var ph=e.p?'<div class="photos"><img src="img/'+e.p+'-0.jpg" alt="起始" loading="lazy"><img src="img/'+e.p+'-1.jpg" alt="结束" loading="lazy"></div><div class="pcap">照片：起始 → 结束'+(e.pn?' · '+e.pn:'')+'</div>':'';
    return '<article class="ex"><div class="fig">'+ph+P.fig(P.FIGS[e.f])+'</div><div class="info"><h2>'+n+'. '+st.name+(st.equip?' <span class="small">· '+(EQ[st.equip]||st.equip)+'</span>':'')+'</h2>'+(st.rx?'<div class="rx">'+st.rx+'</div>':'')+
      (st.only?'<div class="only">'+P.ONLY_LABEL[st.only]+'</div>':'')+(cue?'<p class="cue"><b>要领</b>'+cue+'</p>':'')+
      (more.length?'<ul>'+more.map(function(c){{return '<li>'+c+'</li>';}}).join('')+'</ul>':'')+
      ((e.d||e.u)?('<div class="opts">'+(e.d?'<div class="down"><b>退阶</b>'+e.d+'</div>':'')+(e.u?'<div class="up"><b>邪修</b>'+e.u+'</div>':'')+'</div>'):'')+'</div></article>';
  }}
  function section(steps){{var cur='',n=0,o='';steps.forEach(function(st){{if(st.id.charAt(0)==='_')return;if(st.blk!==cur){{cur=st.blk;o+='<div class="blockhead">'+cur+'</div>';}}o+=card(st,++n);}});return o;}}
  out+='<div class="dayhead" id="day-common"><h2>固定部分（每天都做）</h2><div class="sub">热身 → 胯 → 肩 → 核心 →（当天的力量）→ 收尾。收尾不在表格里，按之前的约定保留。</div></div>'+section(P.buildCommon());
  ['push','pull','legs','upper'].forEach(function(k){{
    var s=P.S[k];
    out+='<div class="dayhead" id="day-'+k+'"><h2>'+s.name+'</h2><div class="sub">'+s.sub+' · 预计 '+s.total+'</div></div>';
    out+='<table class="flowtbl"><tr><th>阶段</th><th>内容</th><th>时间</th></tr>'+s.flow.map(function(f){{return '<tr><td>'+f[0]+'</td><td>'+f[1]+'</td><td>'+f[2]+'</td></tr>';}}).join('')+'</table><p class="small">'+s.late+'</p>';
    out+=section(P.buildSteps(k));
  }});
  document.getElementById('days').innerHTML=out;
}})();
</script>
</body>
</html>
"""
(root/'plan-full.html').write_text(plan_full,encoding='utf-8')

# 内联版（claude 链接用）：去掉外层骨架，把 data.js 内联
title=re.search(r'<title>.*?</title>',idx).group(0)
body=re.search(r'<body>(.*)</body>',idx,re.S).group(1)
body=body.replace('<script src="data.js"></script>','<script>\n'+data+'\n</script>')
(root/'晨练推拉腿计划.html').write_text(title+'\n'+style+'\n'+body,encoding='utf-8')
print('built plan-full.html and 晨练推拉腿计划.html')
