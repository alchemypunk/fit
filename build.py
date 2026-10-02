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
.wrap{max-width:820px;margin:0 auto;padding-inline:18px;padding-block:24px 64px}
.wrap h1{font-size:1.8rem;font-weight:900}
.lead{color:var(--muted)}
.dayhead{margin-top:2.6rem;padding-top:1rem;border-top:3px solid var(--fg)}
.dayhead h2{font-size:1.4rem;font-weight:800;margin:0}
.dayhead .sub{color:var(--muted);font-size:.9rem}
.blockhead{font-family:var(--font-num);font-size:.72rem;letter-spacing:.14em;color:var(--accent);text-transform:uppercase;margin:1.6rem 0 .2rem}
.ex{display:grid;grid-template-columns:170px 1fr;gap:16px;border:1px solid var(--line);background:var(--surface);border-radius:10px;padding:14px;margin-top:12px}
.ex .fig{background:var(--figbg);border-radius:8px;padding:10px;min-width:0}
.ex .fig svg{width:100%;height:auto;display:block;margin-top:8px}
.ex .fig .pcap{font-size:.72rem;color:var(--muted);text-align:center;padding-top:4px}
.ex .fig figcaption{font-size:.72rem;color:var(--muted);text-align:center;padding-top:4px}
.ex .info{padding:0;min-width:0}
.ex .info h2{font-size:1.05rem}
.ex .info .blk{display:none}
@media (max-width:560px){.ex{grid-template-columns:1fr}.ex .fig{max-width:240px;margin:0 auto}}
.doc{padding:0;overflow:visible}
.toc{display:flex;flex-wrap:wrap;gap:8px;margin-top:1rem}
.toc a{border:1px solid var(--line);border-radius:999px;padding:4px 12px;font-size:.85rem;text-decoration:none;color:var(--fg);background:var(--surface)}
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
  <div class="eyebrow" style="font-family:var(--font-num);font-size:.72rem;letter-spacing:.14em;color:var(--accent);text-transform:uppercase">Morning · Push / Pull / Legs+Hip · 60 min</div>
  <h1>晨练推拉腿计划 · 长文版</h1>
  <p class="lead">和手机卡片版（<a href="index.html">index.html</a>）是同一份数据，这里按训练日把所有动作顺序列出来，适合在电脑上通读。</p>
  <div class="toc"><a href="#doc">说明</a><a href="#day-push">推日</a><a href="#day-pull">拉日</a><a href="#day-legs">腿胯日</a><a href="#day-upper">上肢混合（5 天版）</a></div>
  <div class="doc" id="doc">{doc}</div>
  <div id="days"></div>
</div>
<script src="data.js"></script>
<script>
(function(){{
  var P=window.PLAN,EX=P.EX,out='';
  ['push','pull','legs','upper'].forEach(function(k){{
    var s=P.S[k],steps=P.buildSteps(k),cur='';
    out+='<div class="dayhead" id="day-'+k+'"><h2>'+s.name+'</h2><div class="sub">'+s.sub+' · 共 '+steps.length+' 步，按区域顺序</div></div>';
    steps.forEach(function(st,i){{
      var e=EX[st.id],rx=st.rx||e.rx;
      if(st.blk!==cur){{cur=st.blk;out+='<div class="blockhead">'+cur+'</div>';}}
      var ph=e.p?'<div class="photos"><img src="img/'+e.p+'-0.jpg" alt="起始" loading="lazy"><img src="img/'+e.p+'-1.jpg" alt="结束" loading="lazy"></div><div class="pcap">照片：起始 → 结束'+(e.pn?' · '+e.pn:'')+'</div>':'';
      out+='<article class="ex"><div class="fig">'+ph+P.fig(P.FIGS[e.f])+'</div><div class="info"><h2>'+(i+1)+'. '+e.n+'</h2>'+(rx?'<div class="rx">'+rx+'</div>':'')+'<ul>'+e.c.map(function(c){{return '<li>'+c+'</li>';}}).join('')+'</ul>'+((e.d||e.u)?('<div class="opts">'+(e.d?'<div class="down"><b>退阶</b>'+e.d+'</div>':'')+(e.u?'<div class="up"><b>邪修</b>'+e.u+'</div>':'')+'</div>'):'')+'</div></article>';
    }});
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
