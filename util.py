import re
import unicodedata
import string
import bs4
import os

tag_concat=['u','ul','ol','i','em','strong']
tag_round=['u','i','em','span','strong', 'a']
tag_trim=['li', 'th', 'td', 'div','caption','h[1-6]']
tag_right=['p']
sp=re.compile("\s+", re.UNICODE)

def get_tpt(title,css):
	soup=bs4.BeautifulSoup('''
	<!DOCTYPE html>
	<html>
		<head>
			<title></title>
			<meta charset="utf-8"/>
			<link href="" rel="stylesheet" type="text/css"/>
		</head>
		<body>
			<div class="content">
			</div>
		</body>
	</html>
	''','lxml')
	soup.head.title.string=title
	soup.head.link.attrs["href"]=css
	return soup

def get_soup(html):
    if not os.path.isfile(html):
        return None
    html = open(html,"r+")
    soup = bs4.BeautifulSoup(html,'lxml')
    html.close()
    return soup

def ischar(ch):
    c=unicodedata.category(ch)
    return c[0] not in ('M','C') and c not in ('Zl', 'Zp')

def get_html(soup,multiline=False):
    if not multiline:
        for t in get_textos(soup):
            b=sp.sub(" ",t.string)
            t.replace_with(b)
    h=unicode(soup)
    if not multiline:
        h=filter(ischar , h)
    r=re.compile("(\s*\.\s*)</a>", re.MULTILINE|re.DOTALL|re.UNICODE)
    h=r.sub("</a>\\1",h)
    for t in tag_concat:
        r=re.compile("</"+t+">(\s*)<"+t+">", re.MULTILINE|re.DOTALL|re.UNICODE)
        h=r.sub("\\1",h)
    for t in tag_round:
        r=re.compile("(<"+t+">)(\s+)", re.MULTILINE|re.DOTALL|re.UNICODE)
        h=r.sub("\\2\\1",h)
        r=re.compile("(<"+t+" [^>]+>)(\s+)", re.MULTILINE|re.DOTALL|re.UNICODE)
        h=r.sub("\\2\\1",h)
        r=re.compile("(\s+)(</"+t+">)", re.MULTILINE|re.DOTALL|re.UNICODE)
        h=r.sub("\\2\\1",h)
    for t in tag_trim:
        r=re.compile("(<"+t+">)\s+", re.MULTILINE|re.DOTALL|re.UNICODE)
        h=r.sub("\\1",h)
        r=re.compile("\s+(</"+t+">)", re.MULTILINE|re.DOTALL|re.UNICODE)
        h=r.sub("\\1",h)
    for t in tag_right:
        r=re.compile("\s+(</"+t+">)", re.MULTILINE|re.DOTALL|re.UNICODE)
        h=r.sub("\\1",h)
        r=re.compile("(<"+t+">) +", re.MULTILINE|re.DOTALL|re.UNICODE)
        h=r.sub("\\1",h)
    r=re.compile("<br/>\s*<br/>", re.MULTILINE|re.DOTALL|re.UNICODE)
    h=r.sub("<br/>",h)
    r=re.compile("\s*<br/>", re.MULTILINE|re.DOTALL|re.UNICODE)
    h=r.sub("<br/>",h)
    h=h.replace("___ -","-")
    return h

def escribir(html,out):
    tags_tab="html|head|ul|ol|div|fieldset|body|html|table|tbody|thead"
    tags_ln="title|p|li|h[123456]|legend|tr|pre"

    r=re.compile("(<("+tags_tab+")[^>]*>)",re.UNICODE)
    html=r.sub("\n\\1\n",html)
    r=re.compile("(</("+tags_tab+")>)",re.UNICODE)
    html=r.sub("\n\\1\n",html)
    r=re.compile("(<(meta|link) [^>]+/>)",re.UNICODE)
    html=r.sub("\n\\1\n",html)
    r=re.compile("(<("+tags_ln+")[^>]*>)",re.UNICODE)
    html=r.sub("\n\\1",html)
    r=re.compile("(</("+tags_ln+")>)",re.UNICODE)
    html=r.sub("\\1\n",html)
    html=html.replace("\r","")

    begin_tag=re.compile("^<("+tags_tab+")[^>]*>$",re.UNICODE)
    end_tag=re.compile("^</("+tags_tab+")>$",re.UNICODE)
    pre1=re.compile("^(<pre[^>]*>).*",re.UNICODE)
    pre2=re.compile(".*(</pre>)$",re.UNICODE)
    pre=0
    tab=""
    lineas=html.split("\n")
    with open(out, "wb") as file:
        for l in lineas:
            if pre!=2 and len(sp.sub("",l).strip())==0:
                continue
            if pre==1:
				pre=2
            elif pre1.match(l):
				pre=1
            if end_tag.match(l):
                tab=tab[:-2]
            if pre==2:
                file.write((l+"\n").encode('utf8'))
            else:
                file.write((tab+l+"\n").encode('utf8'))
            if begin_tag.match(l):
                tab=tab+"  "
            if pre2.match(l):
				pre=0

printable = set(string.printable)

def get_printable(txt):
	txt=txt.strip()
	txt=filter(lambda x: x in printable, txt)
	return sp.sub(" ",txt).strip()

def sclean(txt):
    if isinstance(txt, bs4.Tag):
        txt=txt.get_text()
    txt=filter(lambda x: x in printable, txt)
    txt=sp.sub("",txt).strip()
    return txt

def is_vacio(txt):
    return len(sclean(txt))==0

def vacio(soup,nodos):
    r=[]
    tags=soup.find_all(nodos)
    for t in tags:
        if is_vacio(t):
            r.append(t)
    return r

def eqtxt(a,b):
    if not a or not b:
        return False
    sa=sclean(a)
    sb=sclean(b)
    return sa==sb

def tail(n):
    txt=""
    s=n
    while s.next_sibling and len(txt)==0:
        s=s.next_sibling
        txt=txt+sclean(s)
    if len(txt)==0:
        return True
    txt=""
    s=n
    while s.previous_sibling and len(txt)==0:
        s=s.previous_sibling
        txt=txt+sclean(s)
    if len(txt)==0:
        return True
    return False

def get_parrafos(soup):
    prfs= soup.find_all(['li','table'])
    ps = soup.find_all('p')
    for p in ps:
        if not p.span:
            prfs.append(p)
            continue
        flag=False
        for c in p.contents:
            if ((isinstance(c, bs4.NavigableString) or isinstance(c, unicode)) and not is_vacio(c)):
                flag=True
                break
        if flag:
            prfs.append(p)
    return prfs

def get_textos(soup):
    r=[]
    for t in soup.body.find_all(text=True):
        if t.find_parent("pre"):
            continue
        s=t.find_parent("span")
        p=t.find_parent("p")
        if not s:
            s=p
        if not s:
            r.append(t)
        else:
            if "class" not in s.attrs or (p and not p.br):
                r.append(t)
            else:
                c=s.attrs["class"]
                if not isinstance(c, basestring):
                    c=c[0]
                if c!="stdout" and c!="archivo":
                    r.append(t)
    return r

def eqsibling(n):
    r=[]
    tag=n.name
    s=n.next_sibling
    while s:
        if (isinstance(s, bs4.NavigableString) or isinstance(s, unicode)):
            if not is_vacio(s):
                break
        elif s.name!=tag or not eqclass(s,n):
            break
        r.append(s)
        s=s.next_sibling
    return r

def eqclass(n,s):
    if "class" not in n.attrs and "class" not in s.attrs:
        return True
    if "class" in n.attrs and "class" in s.attrs:
        c1=n.attrs["class"]
        c2=s.attrs["class"]
        if not isinstance(c1, basestring):
            c1=c1[0]
        if not isinstance(c2, basestring):
            c2=c2[0]
        if c1==c2:
            return True
    return False

def has(s,ar):
    s=s.lower()
    for a in ar:
        if a.lower() in s:
            return True
    return False

def get_spbr(soup):
    pcmd=[]
    for p in soup.findAll("p"):
        if len(p.contents)>2:
            c1=p.contents[0]
            c2=p.contents[1]
            c3=p.contents[2]
            if isinstance(c1, bs4.Tag) and isinstance(c2, bs4.Tag):
                if c1.name=="span" and c2.name=="br":
                    if not isinstance(c3, bs4.Tag) or c3.name!="span" or c1.attrs["class"]!=c3.attrs["class"]:
                        pcmd.append(p)
    return pcmd

def find_text(soup,r):
    rt=[]
    ps=soup.findAll('p')
    for p in ps:
        if r.match(p.get_text()):
            rt.append(p)
    return rt

def h_to_a(soup,h,ct):
	t=h.get_text().strip()
	i=sp.sub("-",t).lower()
	if ct:
		i=i+"-"+str(ct)
	a=soup.new_tag("a")
	a.string=t
	a.attrs["href"]="#"+i
	h.attrs["id"]=i
	h.clear()
	h.append(a)
