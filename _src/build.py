# -*- coding: utf-8 -*-
import json, importlib, sys, io

BASE = "https://blog.apluslocksmith.bg/"
BIZ  = "https://apluslocksmith.bg#business"
STYLE = open('/home/claude/style_base.css', encoding='utf-8').read()
EXTRA = open('/home/claude/extra.css', encoding='utf-8').read()

BIZNODE = {
  "@type":"Locksmith","@id":BIZ,"name":"А+ Ключар",
  "image":BASE+"img/post01_3.jpg","telephone":"+359879993321",
  "email":"a.plus.locksmith.ltd@gmail.com","url":"https://apluslocksmith.bg","priceRange":"$$",
  "address":{"@type":"PostalAddress","streetAddress":"ж.к. Малинова долина, бл. 25",
             "addressLocality":"София","postalCode":"1797","addressCountry":"BG"},
  "areaServed":{"@type":"City","name":"София"},
  "sameAs":["https://blog.apluslocksmith.bg/"]
}

def build(mod):
    m = importlib.import_module(mod)
    url = BASE + m.slug
    graph = [
      BIZNODE,
      {"@type":"Organization","@id":"https://apluslocksmith.bg#org","name":"А ПЛЮС ЛОКСМИТ ООД",
       "alternateName":"А+ Ключар","url":"https://apluslocksmith.bg",
       "logo":BASE+"img/logo-white.png","telephone":"+359879993321",
       "sameAs":["https://blog.apluslocksmith.bg/"]},
      {"@type":"BlogPosting","@id":url+"#post","headline":m.title,"description":m.desc,
       "image":[BASE+"img/"+x for x in (m.img if isinstance(m.img,list) else [m.img])],"datePublished":m.date,"dateModified":getattr(m,"modified",m.date),
       "inLanguage":"bg-BG","url":url,
       "author":{"@id":BIZ},"publisher":{"@id":BIZ},
       "isPartOf":{"@id":BASE+"#blog"},
       "mainEntityOfPage":{"@type":"WebPage","@id":url},
       "articleSection":m.cat,"keywords":m.kw},
      {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Блог","item":BASE},
        {"@type":"ListItem","position":2,"name":m.cat,"item":BASE},
        {"@type":"ListItem","position":3,"name":m.title,"item":url}]},
    ]
    if m.faq:
        graph.append({"@type":"FAQPage","@id":url+"#faq","mainEntity":[
            {"@type":"Question","name":q,
             "acceptedAnswer":{"@type":"Answer","text":a}} for q,a in m.faq]})
    ld = json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False)
    json.loads(ld)  # validate

    faqhtml = "\n".join(
        '<div class="q"><h3>%s</h3><p>%s</p></div>' % (q, a) for q, a in m.faq)
    faqblock = ('<div class="faq wrap"><h2>Често задавани въпроси</h2>\n'+faqhtml+'\n</div>') if m.faq else ''
    relhtml = "".join(
        '<a href="%s"><div class="rc">%s</div><div class="rt">%s</div></a>' % r for r in m.related)

    imgs = m.img if isinstance(m.img, list) else [m.img]
    alts = m.imgalt if isinstance(m.imgalt, list) else [m.imgalt]
    cls = " two" if len(imgs)==2 else (" three" if len(imgs)==3 else "")
    figs = getattr(m,"figs_html",None) or '<div class="figs%s">%s</div>' % (cls, "".join(
        '<figure><img src="./img/%s" alt="%s" loading="%s"></figure>' % (i,a,"eager" if n==0 else "lazy")
        for n,(i,a) in enumerate(zip(imgs,alts))))
    return f"""<!DOCTYPE html>
<html lang="bg">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{m.title} | А+ Ключар</title>
<meta name="description" content="{m.desc}">
<meta name="keywords" content="{m.kw}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{m.ogtit}">
<meta property="og:description" content="{m.desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}img/{imgs[0]}">
<meta property="og:locale" content="bg_BG">
<meta property="og:site_name" content="А+ Ключар — Блог">
<meta property="article:published_time" content="{m.date}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{m.ogtit}">
<meta name="twitter:description" content="{m.desc}">
<meta name="twitter:image" content="{BASE}img/{imgs[0]}">
<meta name="author" content="А+ Ключар">
<meta name="geo.region" content="BG-23">
<meta name="geo.placename" content="София">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800;900&display=swap" rel="stylesheet">
<style>
{STYLE}
{EXTRA}
</style>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="./index.html"><img class="logo" src="./img/logo-white.png" alt="А+ Ключар — ключарски услуги в София"></a>
<nav>
<a class="hidem" href="./index.html">Блог</a>
<a class="hidem" href="https://apluslocksmith.bg">Официален сайт</a>
<a class="callbtn" href="tel:+359879993321">☎ 0879 99 33 21</a>
<button class="menubtn" aria-label="Меню" aria-expanded="false" aria-controls="mnav">☰</button>
</nav></div>
<div class="mnav" id="mnav">
<a href="./index.html">Всички случаи<span class="n">31</span></a>
<div class="sep">Категории</div>
<a href="./index.html#avto">Автоключарски услуги<span class="n">15</span></a>
<a href="./index.html#bravi">Битови брави<span class="n">9</span></a>
<a href="./index.html#garaji">Гаражи и бариери<span class="n">6</span></a>
<a href="./index.html#dostap">Контрол на достъп<span class="n">1</span></a>
<div class="sep">А+ Ключар</div>
<a href="https://apluslocksmith.bg">Официален сайт<span class="n">→</span></a>
<a href="tel:+359879993321">Обади се<span class="n">0879 99 33 21</span></a>
</div>
</header>
<article>
<div class="back wrap"><a href="./index.html">← Всички случаи</a></div>
<div class="arthead wrap">
<div class="artmeta"><span class="tag">{m.cat}</span>
<time datetime="{m.date}">{m.datebg}</time>
<span>· А+ Ключар</span></div>
<h1>{m.title}</h1>
<p class="lead">{m.lead}</p>
</div>
{figs}
<div class="content">{m.body}</div>
{faqblock}
<div class="cta">
<h3>Имате подобен случай?</h3>
<p>Обадете се за оглед или консултация — работим в София с посещение на адрес.</p>
<div class="row"><a class="call" href="tel:+359879993321">☎ 0879 99 33 21</a>
<a class="site" href="https://apluslocksmith.bg">Виж всички услуги →</a></div>
</div>
<div class="rel"><h3>Още от блога</h3><div class="rr">{relhtml}</div></div>
</article>
<footer><div class="wrap"><div class="cols">
<div>
<img class="flogo" src="./img/logo-white.png" alt="А+ Ключар">
<p style="margin-top:12px;max-width:320px">Професионални ключарски услуги в София — автоключове, брави, дистанционни за гаражи и бариери, системи за контрол на достъп. Посещение на адрес.</p>
</div>
<div><h4>Услуги</h4><a class="fl" href="./index.html">Автоключарски услуги</a><a class="fl" href="./index.html">Битови брави</a><a class="fl" href="./index.html">Гаражи и бариери</a><a class="fl" href="./index.html">Контрол на достъп</a></div>
<div><h4>Контакт</h4>
<a class="fl" href="tel:+359879993321">☎ 0879 99 33 21</a>
<a class="fl" href="mailto:a.plus.locksmith.ltd@gmail.com">a.plus.locksmith.ltd@gmail.com</a>
<span class="fl">ж.к. Малинова долина, бл. 25, София</span>
<a class="fl" href="https://apluslocksmith.bg">apluslocksmith.bg</a>
</div>
</div>
<div class="base">© 2026 А+ Ключар · А ПЛЮС ЛОКСМИТ ООД · Всички права запазени.</div>
</div></footer>
<script>
(function(){
 var b=document.querySelector('.menubtn'), m=document.getElementById('mnav');
 if(b&&m){b.addEventListener('click',function(){
   var o=m.classList.toggle('open'); b.setAttribute('aria-expanded',o?'true':'false');
   b.textContent=o?'\u2715':'\u2630';});}
 var f=document.getElementById('filters');
 if(f){
  var cards=[].slice.call(document.querySelectorAll('.grid > .card'));
  function apply(s){
   cards.forEach(function(c){c.style.display=(!s||c.dataset.cat===s)?'':'none';});
   [].forEach.call(f.children,function(x){x.classList.toggle('on',(x.dataset.cat||'')===(s||''));});
   history.replaceState(null,'',s?('#'+s):location.pathname);
  }
  f.addEventListener('click',function(e){
   var t=e.target.closest('button'); if(!t)return; apply(t.dataset.cat||'');});
  apply((location.hash||'').replace('#','')); 
 }
})();
</script>
</body>
</html>
"""

sys.path.insert(0, '/home/claude')
for mod in ("article12",):
    m = importlib.import_module(mod)
    html = build(mod)
    open('/home/claude/aplus-blog/'+m.slug,'w',encoding='utf-8').write(html)
    words = len(__import__('re').sub(r'<[^>]+>',' ', m.body + " ".join(q+a for q,a in m.faq)).split())
    print(m.slug, len(html), 'bytes,', words, 'думи')
