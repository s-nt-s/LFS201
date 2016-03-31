# -*- coding: utf-8 -*-

import os.path
import glob
import re
import bs4
import unicodedata

cp=re.compile(".*?LFS201_(\d+)\..*$")
pr=re.compile("(.*)¿(.*?)-(.*)")
ck=re.compile("(Haga|Haz) click (en|sobre) (el|los|en)", re.UNICODE|re.MULTILINE|re.DOTALL)
fg=re.compile(".*?(Figura|Figure)\s+\d+\.\d+(:|.)", re.UNICODE|re.MULTILINE|re.DOTALL)
lab=re.compile(".*\s+para\s+descargar\s+el\s+Laboratorio\s+(\d+\.\d+).*", re.UNICODE|re.MULTILINE|re.DOTALL)
sp=re.compile("\s+", re.UNICODE)
url=re.compile("(.*)(http://\S+)(.*)", re.UNICODE|re.MULTILINE|re.DOTALL)

hts=sorted(glob.glob('html/clean/*.html'))

caB=0
n=0
f=0

tpt="out/LFS201.htm"
oht="out/LFS201.html"
html4="out/LFS201_4.html"

def escribir(html,out):
	tags_tab="html|head|ul|ol|div|fieldset|body|html|table|tbody|thead"
	tags_ln=tags_tab+"|meta|link|title|p|li|h1|legend|div|tr"
	bks1=re.compile("(<("+tags_ln+")[^>]*>)")
	bks2=re.compile("(</("+tags_ln+")>)")
	bks3=re.compile("(<(meta|link) [^>]+/>)")
	begin_tag=re.compile("^<("+tags_tab+")[^>]*>$")
	end_tag=re.compile("^</("+tags_tab+")>$")

	html=bks1.sub("\n\\1",html)
	html=bks2.sub("\\1\n",html)
	html=bks3.sub("\\1\n",html)
	lineas=html.split("\n")

	with open(out, "wb") as file:
		tab=""
		for l in lineas:
			cl=sp.sub("",l).strip()
			if len(cl)==0:
				continue
			m1=end_tag.match(l)
			if m1:
				tab=tab[:-2]
			file.write((tab+l+"\n").encode('utf8'))
			m2=begin_tag.match(l)
			if m2 and not m1 and not l.endswith("/>"):
				tab=tab+"  "

def get_soup(html):
	html = open(html,"r+")
	soup = bs4.BeautifulSoup(html,'html.parser')#"lxml")
	html.close()
	return soup

def find_text(soup,r):
	rt=[]
	ps=soup.findAll('p')
	for p in ps:
		if r.match(p.get_text()):
			rt.append(p)
	return rt

def set_anchor(i,ca):
	a=soup.new_tag("a", **{"href": "#"+i.attrs['id'], "title":u"Cápitulo "+str(ca)})
	if i.name=="fieldset":
		i=i.legend
	a.string=i.string
	i.string=""
	i.append(a)

soup = get_soup(tpt)
soup.body.clear()
div=soup.new_tag("div", **{"class":"content"})
soup.body.append(div)

fldB=None
divCp=None

for ht in hts:
	soup2 = get_soup(ht)
	t=soup2.title
	b=soup2.body

	if "_popup" in ht:
		n=3
	else:
		ca=int(cp.sub("\\1",ht))
		if ca>caB:
			n=1
			f=1
			caB=ca
		else:
			n=2
			f=f+1

	if n==1:
		h=b.p.extract()#.strong
		h.attrs.clear()
		h.name="h1"
		h.string=sp.sub(" ",h.get_text()).strip('.')[9:].strip()
		h.attrs['id']="c"+str(ca)
		set_anchor(h,ca)
		divCp=soup.new_tag("div", **{"id":"cp"+str(ca)})
		soup.body.div.append(divCp)
		divCp.append(h)
		n=2

	fld = soup.new_tag("fieldset")
	fld.attrs['class']="n"+str(n)
	t.name="legend"
	fld.append(t)
	b.name="div"
	fld.attrs['id']="c"+str(ca)+"f"+str(f)
	fld.append(b)

	ps=fld.div.select(" > *")
	if len(ps)>0 and ps[0].name=="p" and ps[0].get_text().strip(':').lower() == fld.legend.get_text().lower():
		ps[0].extract()

	if n==3:
		cs=[]
		if fg.match(fld.legend.string):
			cs=find_text(fldB,fg)
		else:
			cs=find_text(fldB,ck)
		if len(cs)>0:
			c=cs[0]
			c.replace_with(fld)
		else:
			fldB.append(fld)
	else:
		set_anchor(fld,ca)
		divCp.append(fld)
		fldB=fld

flds=soup.findAll("fieldset", attrs={'class': re.compile(r".*\bn3\b.*")})
for fld in flds:
	if len(fld.parent.select(" > *"))==1:
		fld.parent.replace_with(fld.div)

'''
labs=find_text(soup,lab)
for f in labs:
	l=lab.sub("\\1",f.get_text())
	n=f.select(" > *")[0]
	a=soup.new_tag("a", href="https://lms.360training.com/custom/12396/808239/LAB_"+l+".pdf")
	codigo=None
	if l == "4.1":
		codigo="https://lms.360training.com/custom/12396/808239/fake_service"
	elif l == "18.2":
		codigo="https://lms.360training.com/custom/12396/808239/writeit.c"
	elif l == "21.1":
		codigo="https://lms.360training.com/custom/12396/808239/signals.c"
	elif l == "25.1":
		codigo="https://lms.360training.com/custom/12396/808239/ioscript.sh"
	frase=n.get_text()
	if frase.endswith("."):
		frase=frase[:-1]
	n.string=""
	if codigo:
		y=frase.find(" y ")
		a.string=frase[:y].strip()
		c=soup.new_tag("a", href=codigo)
		c.string=frase[y+3:].strip()
		n.append(a)
		n.append(" y ")
		n.append(c)
		n.append(".")
	else:
		a.string=frase
		n.append(a)
		n.append(".")
'''
nxs=re.compile("^\s*(\d+\.\d+).*$", re.UNICODE|re.MULTILINE|re.DOTALL)
for d in soup.body.div.select(" > div"):
	a=d.h1.a
	a.attrs['title']=a.attrs['title']+" de "+str(ca)

	labos=find_text(d,lab)
	if len(labos)>0:
		ul=soup.new_tag("ul")
		primero=True
		for lb in labos:
			fld=lb.find_parent("fieldset")
			li=soup.new_tag("li")
			l=lab.sub("\\1",lb.get_text())
			a=soup.new_tag("a", href="https://lms.360training.com/custom/12396/808239/LAB_"+l+".pdf")
			a.string="Laboratorio "+l
			li.append(a)
			codigo=None
			if l == "4.1":
				codigo="https://lms.360training.com/custom/12396/808239/fake_service"
			elif l == "18.2":
				codigo="https://lms.360training.com/custom/12396/808239/writeit.c"
			elif l == "21.1":
				codigo="https://lms.360training.com/custom/12396/808239/signals.c"
			elif l == "25.1":
				codigo="https://lms.360training.com/custom/12396/808239/ioscript.sh"
			if codigo:
				c=soup.new_tag("a", href=codigo)
				c.string=codigo[codigo.rfind("/")+1:]
				li.append(u" (código fuente: ")
				li.append(c)
				li.append(")")
			ul.append(li)
			if primero:
				fld.legend.a.string=nxs.sub("\\1. Laboratorios",fld.legend.a.string)
				fld.div.clear()
				fld.div.append(ul)
				primero=False
			else:
				fld.extract()

	mrks=d.select(" > fieldset > legend > a")
	z=str(len(mrks))
	i=1
	for m in mrks:
		m.attrs['title']=m.attrs['title']+", ficha "+str(i)+" de "+z
		i=i+1

urls=soup.findAll(text=url)
for u in urls:
	if u.parent.name not in ["a","span"] and "class" not in u.parent.attrs:
		m=url.match(u)
		antes=m.group(1)
		link=m.group(2)
		despues=m.group(3)
		enlace=soup.new_tag("enlace")
		if len(antes)>0:
			enlace.append(antes)
		a=soup.new_tag("a",href=link)
		a.append(link)
		enlace.append(a)
		if len(despues)>0:
			enlace.append(despues)
		u.replace_with(enlace)
		enlace.unwrap()

ptabs=re.compile("(.*?)([^\.\?\s][^\.\?]+ 'tab' [^\.]+\.)(.*)", re.UNICODE|re.MULTILINE|re.DOTALL)
for p in soup.findAll(text=re.compile(" 'tab' ")):
	txt=ptabs.sub("\\1\\3",p).strip()
	padre=p.parent
	if len(txt)>0:
		if p.previous_sibling:
			txt=" "+txt
		if p.next_sibling:
			txt=txt+" "
		p.replace_with(txt)
	else:
		if p.parent.get_text().strip()==p.strip():
			p.parent.extract()
		else:
			p.extract()

for i in soup.findAll("img"):
	src=i.attrs['src']
	i.attrs['alt']="Imagen original en: "+src
	i.attrs['src']="imgs"+src[src.rfind("/"):]

def ischar(ch):
	c=unicodedata.category(ch)
	return c[0] not in ('M','C') and c not in ('Zl', 'Zp')

h=unicode(soup)
h=filter(ischar , h)

# Erratas
h=h.replace("Objectivos de aprendizaje","Objetivos de aprendizaje") #7 11
h=h.replace(">31</a></h1>",">31. zypper</a></h1>") #31
h=h.replace(" del sisco "," del disco ")
h=h.replace("___ -","-")
h=h.replace("miltihebra","multihebra")
h=h.replace("el ajusta de E/S","el ajuste de E/S")
h=h.replace(". Se este",". Si este")
h=h.replace(" tital "," total ")
h=h.replace(" para para "," para ")
h=h.replace("revision_umber","revision_number")
h=h.replace("cuentasde","cuentas de")
h=h.replace("/opt/dolphy_app /man","/opt/dolphy_app/man")
h=h.replace("archivosy propietarios","archivos y propietarios")
h=h.replace("$tar","$ tar")
h=h.replace("cpio -i somefile -I /dev/st0","cpio -i -I /dev/st0 somefile")

escribir(h,oht)

