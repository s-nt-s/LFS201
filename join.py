# -*- coding: utf-8 -*-

import os.path
import glob
import re
import bs4
import unicodedata

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

cp=re.compile(".*?LFS201_(\d+)\..*$")
pr=re.compile("(.*)¿(.*?)-(.*)")
ck=re.compile("(Haga|Haz) click (en|sobre) (el|los|en)", re.UNICODE|re.MULTILINE|re.DOTALL)
fg=re.compile(".*?(Figura|Figure)\s+\d+\.\d+(:|.)", re.UNICODE|re.MULTILINE|re.DOTALL)
lab=re.compile(".*\s+para\s+descargar\s+el\s+Laboratorio\s+(\d+\.\d+).*", re.UNICODE|re.MULTILINE|re.DOTALL)
sp=re.compile("\s+", re.UNICODE)
url=re.compile("(.*)(http://\S+)(.*)", re.UNICODE|re.MULTILINE|re.DOTALL)

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
	if not os.path.isfile(html):
		return
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

def find_fld(soup,r,tipo=None,txt=None):
	rt=[]
	for l in soup.findAll('legend'):
		if r.match(l.get_text()):
			f=l.parent
			if tipo==None:
				rt.append(f)
			elif tipo==1 or tipo==4:
				if f.div.find("p",text="Verdadero") and f.div.find("p",text="Falso"):
					hjs=f.div.select(" > *")
					if tipo==4 or (len(hjs)>2 and hjs[1].get_text().strip()=="Verdadero"):
						rt.append(f)
			elif tipo==2:
				hjs=f.div.select(" > *")
				if len(hjs)>1 and hjs[0].name=="p":
					rt.append(f)
			elif tipo==3:
				if f.div.p and f.div.p.get_text().strip()==txt:
					rt.append(f)
			elif tipo==5:
				hjs=f.div.select(" > *")
				cg=0
				sg=0
				for h in hjs:
					if h.name!="p":
						break
					c=h.get_text().strip()
					if c.startswith("- "):
						cg=cg+1
					else:
						sg=sg+1
						if sg>1:
							break
				if cg>1 and sg==1:
					rt.append(f)
	return rt

def set_anchor(i,ca):
	a=soup.new_tag("a", **{"href": "#"+i.attrs['id'], "title":u"Cápitulo "+str(ca)})
	if i.name=="fieldset":
		i=i.legend
	a.string=i.string
	i.string=""
	i.append(a)

def get_lab(f,txt):
	a=soup.new_tag("a",  **{"href": "labs/"+f, "title":"Fichero original en: https://lms.360training.com/custom/12396/808239/"+f})
	a.string=txt
	return a

def ischar(ch):
	c=unicodedata.category(ch)
	return c[0] not in ('M','C') and c not in ('Zl', 'Zp')

soup = get_soup(tpt)

soup.body.clear()
div=soup.new_tag("div", **{"class":"content"})
soup.body.append(div)

fldB=None
divCp=None

hts=sorted(glob.glob('html/clean/*.html'))
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


ins=find_fld(soup.body.div, re.compile(u".*Instalación: qué usar para este curso.*", re.UNICODE|re.MULTILINE|re.DOTALL))
if len(ins)>0:
	i=ins[0]
	a=i.div.a
	a.attrs["href"]="labs/Preparing%20Your%20Computer%20for%20LFS101x.pdf"
	i.findAll("p")[-1].extract()
	c=a.parent.contents[-1]
	if isinstance(c, bs4.NavigableString) or isinstance(c, unicode):
		c.replace_with(c.string.replace(u" (si es que se ha registrado para el MOOC) o haciendo clic en el botón Documento a continuación",""))
	p=soup.new_tag("p")
	p.string=u"Otros recursos últiles: "
	i.div.append(p)
	p.append(get_lab("welcome.pdf","documento de bienvenida"))
	p.append(", ")
	a=soup.new_tag("a")
	a.string="Ready-For LF Course"
	a.attrs["href"]="https://training.linuxfoundation.org/cm/prep/?course=LFS201&dist=Default"
	p.append(a)
	p.append(" (")
	p.append(get_lab("ready-for.sh","ready-for.sh"))
	p.append(").")

nxs=re.compile("^\s*(\d+\.\d+).*$", re.UNICODE|re.MULTILINE|re.DOTALL)
labfull=re.compile(u".*todos los ejercicios de laboratorio y soluciones.*", re.UNICODE|re.MULTILINE|re.DOTALL)
cono=re.compile(".*comprobaci.n de conocimiento*", re.UNICODE|re.MULTILINE|re.DOTALL|re.IGNORECASE)
preguntaVF=u"¿Cuáles de las siguientes afirmaciones son ciertas?"
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
			a=get_lab("LAB_"+l+".pdf","Laboratorio "+l)
			li.append(a)
			codigo=None
			if l == "4.1":
				codigo="fake_service"
			elif l == "18.2":
				codigo="writeit.c"
			elif l == "21.1":
				codigo="signals.c"
			elif l == "25.1":
				codigo="ioscript.sh"
			if codigo:
				c=get_lab(codigo,codigo)
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
	labs=find_text(d, labfull)
	if labs and len(labs)>0:
		p=labs[0]
		p.clear()
		p.append(u"Para mayor comodidad, también puede ")
		a=get_lab("LFS201-LABORATORIOS%20Y%20SOLUCIONES.pdf","descargar en un archivo todos los ejercicios de laboratorio y soluciones")
		p.append(a)
		p.append(".")

	pp=[]
	fs=find_fld(d, cono, 2)
	if len(fs)>1:
		for f in fs:
			txt=f.div.p.get_text().strip()
			if txt not in pp:
				pp.append(txt)
	if len(pp)>0:
		for p in pp:
			fs=find_fld(d, cono, 3,p)
			if len(fs)>1:
				f=fs[0]
				del fs[0]
				for n in fs:
					dv=n.div
					dv.p.extract()
					f.div.append(dv)
					dv.unwrap()
					n.extract()

	fs=find_fld(d, cono, 1)
	if len(fs)>1:
		v1=fs[0]
		del fs[0]
		for v in fs:
			dv=v.div
			v1.append(dv)
			dv.unwrap()
			v.extract()

	fs=find_fld(d, cono, 4)
	for v1 in fs:
		uls=[]
		ul=soup.new_tag("ul")
		for p in v1.findAll("p"):
			if p.next_sibling and p.next_sibling.name=="p" and p.next_sibling.get_text().strip()=="Verdadero":
				p.name="li"
				c=p.contents[0]
				if isinstance(c, bs4.NavigableString) or isinstance(c, unicode):
					cs=c.strip()
					if len(cs)>1 and cs[0].isdigit() and cs[1]==".":
						c.extract()
						ul.name="ol"
						if cs[0]=="1" and len(ul.contents)>0:
							uls.append(ul)
							ul=soup.new_tag("ul")
				ul.append(p)
			elif p.get_text().strip()=="Verdadero" or p.get_text().strip()=="Falso":
				p.extract()
		p=soup.new_tag("p")
		p.string=preguntaVF
		v1.div.append(p)
		if len(uls)>0:
			for u in uls:
				v1.div.append(u)
		v1.div.append(ul)

	fs=find_fld(d, cono, 5)
	for f in fs:
		ul=soup.new_tag("ul")
		for p in f.div.select(" > p"):
			c=p.get_text().strip()
			if c.startswith("- "):
				p.name="li"
				ul.append(p)
		f.div.append(ul)

	c=d.attrs["id"][2:]
	i=1
	fs=find_fld(d, cono)
	for f in fs:
		a=f.legend.a
		a.string=u"Comprobación de Conocimientos "+c
		if len(fs)>1:
			a.string=a.string+"."+str(i)
		i=i+1

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

for i in soup.findAll("img"):
	src=i.attrs['src']
	i.attrs['alt']="Imagen original en: "+src
	i.attrs['src']="imgs"+src[src.rfind("/"):]
	f=i.find_parent("fieldset")
	i.attrs['title']=f.legend.get_text().strip()
	f=i.find_parent("fieldset")
	f.div.unwrap()
	f.name="figure"
	f.legend.name="figcaption"
	del f.attrs['id']
	del f.attrs['class']

for t in soup.findAll("table"):
	if t.caption:
		f=t.find_parent("fieldset")
		if f.attrs["class"]=="n3":
			f.legend.extract()
			f.unwrap()
# Erratas

for t in soup.body.find_all(text=True):
	flag=False
	p=t.parent
	while p and not flag:
		if "class" in p.attrs:
			c=p.attrs["class"]
			if isinstance(c, basestring):
				if c in ("stdout","archivo"):
					flag=True
			else:
				for i in c:
					if i in ("stdout","archivo"):
						flag=True
		p=p.parent
	if not flag:
		b=sp.sub(" ",t.string)
		t.replace_with(b)

for s in soup.findAll(text=re.compile("^\s+Personalities\s+:\s+\[raid1\].*", re.MULTILINE|re.DOTALL|re.UNICODE)):
	for t in s.find_parent("p").find_all(text=True):
		b=sp.sub(" ",t.string)
		t.replace_with(b)

tb=soup.find(text=u"Haga click en el botón Información para ver algunos ejemplos acerca de cómo se utiliza systemctl")
if tb:
	p=tb.find_parent("p")
	rp=get_soup("fix/00-SysVinit-Systemd.html")
	if rp and rp.body:
		b=rp.body
		p.replace_with(b)
		b.unwrap()
	else:
		a=get_lab("Hoja de Apuntes de SysVinit a Systemd.pdf","Ejemplos acerca de cómo se utiliza systemctl")
		p.clear()
		p.append(a)

for f in soup.findAll(text=re.compile(u"(Estado de todos los servicios en el sistema|Archivos de configuración de upstart|Archivos y directorios en /etc)")):
	d=f.find_parent("fieldset").div
	texts=d.find_all(text=True)
	for t in texts:
		b=sp.sub(" ",t.string)
		t.replace_with(b)

e=soup.find("span", attrs={'class': "enlace"})
if e and e.parent.name=="li":
	e.parent.extract()

h=unicode(soup)

h=filter(ischar , h)

h=h.replace("Objectivos de aprendizaje","Objetivos de aprendizaje") #7 11
h=h.replace(">31</a></h1>",">31. zypper</a></h1>") #31
h=h.replace(" del sisco "," del disco ")
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
h=h.replace("html://","http://")
h=h.replace("<li>- ","<li>")
h=h.replace("mtu 1500 enp4s2","mtu 1500<br/>enp4s2")
h=h.replace("$getenforce","$ getenforce")
h=h.replace("$for machines in node1 node2 node3</p><p class=\"stdout\">","$ for machines in node1 node2 node3<br/>")
h=h.replace("(Zona desmilitarizada)</p><p>","(Zona desmilitarizada)<br/>")
h=h.replace("Se se produce","Si se produce")
h=h.replace("intentar de reparar","intentar reparar")
h=h.replace("n. El comando","n.</p><p>El comando")
h=h.replace("apt-ge</strong>t","apt-get</strong>")
h=h.replace("imgs/LVM_Components_large_Spanish%20(2).png","imgs/LVM_Components_large_Spanish.png")
h=h.replace("strong> or <strong","strong> o <strong")

r=re.compile("\s+(DUMP: )", re.MULTILINE|re.DOTALL|re.UNICODE)
h=h=r.sub("\\1",h)
r=re.compile(">\s\$ ", re.MULTILINE|re.DOTALL|re.UNICODE)
h=h=r.sub(">$ ",h)
r=re.compile("There are a variety of graphical desktop environments used in[^\.]+\.", re.MULTILINE|re.DOTALL|re.UNICODE)
h=r.sub("",h)

escribir(h,oht)

