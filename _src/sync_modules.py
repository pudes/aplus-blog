# -*- coding: utf-8 -*-
"""Пресъздава article*.py от КАЧЕНИЯ HTML, за да не връща генераторът стари версии."""
import re, io, os, json, sys

BLOG='/home/claude/aplus-blog/'

def grab(pat, s, flags=re.S, grp=1, req=True):
    m=re.search(pat, s, flags)
    if not m:
        if req: raise ValueError(pat[:60])
        return None
    return m.group(grp)

def py(v, indent=0):
    return json.dumps(v, ensure_ascii=False)

def build_module(slug, modname):
    s=io.open(BLOG+slug, encoding='utf-8').read()
    ld=json.loads(grab(r'<script type="application/ld\+json">(.*?)</script>', s))
    post=[n for n in ld["@graph"] if n["@type"]=="BlogPosting"][0]

    cat    = grab(r'<span class="tag">(.*?)</span>', s)
    date   = grab(r'<time datetime="(.*?)"', s)
    datebg = grab(r'<time datetime=".*?">(.*?)</time>', s)
    title  = grab(r'<h1>(.*?)</h1>', s)
    ogtit  = grab(r'<meta property="og:title" content="(.*?)">', s)
    desc   = grab(r'<meta name="description" content="(.*?)">', s)
    kw     = grab(r'<meta name="keywords" content="(.*?)">', s)
    lead   = grab(r'<p class="lead">(.*?)</p>', s)
    body   = grab(r'<div class="content">(.*?)</div>\s*(?:<div class="faq wrap">|<div class="cta">)', s)

    figs   = grab(r'</div>\s*(<div class="(?:figs|shots)[^"]*">.*?)\s*<div class="content">', s)
    imgs   = re.findall(r'<img src="\./img/([^"]+)" alt="([^"]*)"', figs)
    default = '<div class="figs%s">%s</div>' % (
        " two" if len(imgs)==2 else (" three" if len(imgs)==3 else ""),
        "".join('<figure><img src="./img/%s" alt="%s" loading="%s"></figure>'%(i,a,"eager" if n==0 else "lazy")
                for n,(i,a) in enumerate(imgs)))
    custom = None if figs.strip()==default else figs.strip()

    faq=[(q, re.sub(r'\s+',' ',a).strip())
         for q,a in re.findall(r'<div class="q"><h3>(.*?)</h3><p>(.*?)</p></div>', s, re.S)]
    rel=re.findall(r'<a href="(\./[^"]+)"><div class="rc">(.*?)</div><div class="rt">(.*?)</div></a>', s)

    L=[]
    L.append('# -*- coding: utf-8 -*-')
    L.append('# ГЕНЕРИРАН ОТ КАЧЕНИЯ HTML — източникът на истината е публикуваният файл.')
    L.append('slug   = %s' % py(slug))
    L.append('cat    = %s' % py(cat))
    L.append('date   = %s' % py(date))
    if post.get("dateModified") and post["dateModified"]!=date:
        L.append('modified = %s' % py(post["dateModified"]))
    L.append('datebg = %s' % py(datebg))
    L.append('title  = %s' % py(title))
    L.append('ogtit  = %s' % py(ogtit))
    L.append('desc   = %s' % py(desc))
    L.append('kw     = %s' % py(kw))
    L.append('img    = %s' % py([i for i,_ in imgs] if len(imgs)!=1 else imgs[0][0]))
    L.append('imgalt = %s' % py([a for _,a in imgs] if len(imgs)!=1 else imgs[0][1]))
    if custom:
        L.append("figs_html = r'''%s'''" % custom)
    L.append('lead   = %s' % py(lead))
    L.append('')
    L.append('faq = [')
    for q,a in faq: L.append(' (%s,\n  %s),' % (py(q), py(a)))
    L.append(']')
    L.append('')
    L.append('body = r"""%s"""' % body)
    L.append('')
    L.append('related = [')
    for h,c,t in rel: L.append(' (%s, %s, %s),' % (py(h), py(c), py(t)))
    L.append(']')
    io.open('/home/claude/%s.py'%modname,'w',encoding='utf-8').write("\n".join(L)+"\n")
    return len(faq), len(imgs)

if __name__=='__main__':
    pairs=json.loads(sys.argv[1])
    for mod,slug in pairs:
        n,i=build_module(slug,mod)
        print(f"{mod:<12} {slug:<52} faq={n} img={i}")
