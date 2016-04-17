import os.path
import bs4
import glob
import re
import util

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

hr=re.compile(".*ObjLayerActionGoTo.*?'(.*?)'.*")
sp=re.compile("\s+", re.UNICODE)
punto=re.compile(u'\u2022\s*', re.UNICODE)
comandos=re.compile("^\s*(yum|zypper|apt-get|apt-cache|apt-file|dpkg)\s+.*", re.UNICODE)

htmls=sorted(glob.glob('html/clean/*.html'))

for f in htmls:
	soup = util.get_soup(f)
	head=soup.head.select("meta")
	head.append(soup.head.title)
	soup.head.clear()
	for h in head:
		soup.head.append(h)

	ttxt=soup.select("div.ttxt")
	if len(ttxt)>0:
		if len(ttxt)>1:
			del ttxt[-1]
		soup.body.clear()
		for t in ttxt:
			soup.body.append(t)
	elif util.is_vacio(soup.body):
		imgs=soup.select("img")
		soup.body.clear()
		for i in imgs:
			soup.body.append(i)

	ttxt=soup.select("div.ttxt")
	for t in ttxt:
		t.replaceWithChildren()

	comments = soup.findAll(text=lambda text:isinstance(text, bs4.Comment))
	for n in comments:
		n.extract()

	tags=util.vacio(soup, ['table', 'p', 'div', 'ul', 'ol', 'li'])
	for t in tags:
		t.extract()

	spans=soup.select("span")
	for s in spans:
		txt=util.sclean(s)
		if len(txt)==0 or txt==":":
			s.unwrap()
		elif 'style' not in s.attrs:
			s.unwrap()
		elif "rgb(0, 150, 200)" in s.attrs['style'] and s.parent.name!="a" and not(len(s.select(" > *"))==1 and s.select(" > *")[0].name=="a"):
			s.attrs['class']="enlace"
		elif util.has(s.attrs['style'],["rgb(0, 0, 255)","rgb(0, 0, 205)", "color:#0000CD", "rgb(41, 1, 208)", "color:#0000FF"]):
			s.attrs['class']="comando"
		elif util.has(s.attrs['style'],["rgb(0, 200, 0)", "color:#00FF00", "color:#00c800"]):
			s.attrs['class']="stdout"
		elif util.has(s.attrs['style'],["rgb(125, 110, 70)","color:#7D6E46"]):
			s.attrs['class']="archivo"
		else:
			s.unwrap()
	for u in soup.findAll("u"):
		u.unwrap()
	for s in soup.findAll("b"):
		s.name="strong"
	for s in soup.findAll("strong"):
		if util.is_vacio(s) or s.find_parent("strong") or s.find_parent("span") or s.find_parent("table"):
			s.unwrap()
	for s in soup.findAll("span"):
		s2=s.find_parent("span")
		if s2:
			if s2.attrs["class"]==s.attrs["class"]:
				s.unwrap()
			elif util.eqtxt(s,s2):
				s2.unwrap()

	for s in soup.findAll(["span","strong"], text=comandos):
		if len(s.select(" > *"))==0:
			s.name="span"
			s.attrs['class']="comando"

	tags=util.vacio(soup, ['strong', 'em' , 'i', 'span', 'u'])
	for t in tags:
		t.unwrap()

	for lb in soup.findAll("label"):
		lb.unwrap()

	lis=soup.findAll("li")
	for li in lis:
		n=li.select(" > *")
		if len(n)==1 and n[0].name=="p":
			n[0].unwrap()

	for a in soup.select("a"):
		if "ObjLayerActionGoTo" in a.attrs['href']:
			a.attrs['href']=hr.sub("\\1",a.attrs['href'])

	for n in soup.html:
		if isinstance(n, bs4.Comment) or isinstance(n, bs4.NavigableString):
			n.extract()

	for p in soup.select("*"):
		if 'style' in p.attrs:
			del p.attrs['style']
		if p.name!='span' and 'class' in p.attrs:
			del p.attrs['class']
		if 'name' in p.attrs:
			del p.attrs['name']
		if 'id' in p.attrs:
			del p.attrs['id']
		if 'align' in p.attrs and p.attrs['align']=="left":
			del p.attrs['align']
	for t in soup.findAll(['table','tr']):
		t.attrs.clear()

	for strong in soup.findAll("strong"):
		txt=""
		for c in strong.contents:
			if not isinstance(c, bs4.Tag) or c.name not in ["span", "strong"]:
				txt=util.sclean(c)
		if len(txt)<2:
			strong.unwrap()
		elif not strong.span:
			txt=util.sclean(strong)
			if txt.startswith("$"):
				if txt!="$6$":
					strong.name="span"
					strong.attrs["class"]="comando"
			elif txt.startswith("/"):
				strong.name="span"
				strong.attrs["class"]="archivo"

	spans=soup.select("span")
	for s in spans:
		if s.attrs["class"] !="archivo":
			archs=s.findAll("span", attrs={'class': "archivo"})
			if len(archs)>0:
				s.unwrap()
				continue
		sb=util.eqsibling(s)
		for b in sb:
			s.append(b)
			if isinstance(b, bs4.Tag):
				b.unwrap()
	for s in soup.select("strong"):
		sb=util.eqsibling(s)
		for b in sb:
			s.append(b)
			if isinstance(b, bs4.Tag):
				b.unwrap()

	for s in soup.findAll("span",attrs={'class': "comando"}):
		if len(s.contents)>0:
			ult=s.contents[-1]
			if (isinstance(ult, bs4.NavigableString) or isinstance(ult, unicode)) and util.sclean(ult)=="$":
				ult.extract()

	hjs=soup.body.select(" > *")
	if len(hjs)>1 and hjs[0].name=="p" and hjs[1].name=="p":
		p1=hjs[0]
		p2=hjs[1]
		sp1=p1.find("span", attrs={'class': "enlace"})
		sp2=p2.find("span", attrs={'class': "enlace"})
		if sp1 and sp2 and util.eqtxt(p1,sp1) and util.eqtxt(p2,sp2):
			sp1.append(sp2)
			sp2.unwrap()
			p2.extract()

	for table in soup.findAll("table"):
		if len(table.findAll("tr"))>1:
			thead=soup.new_tag("thead")
			thead.append(table.tbody.tr)
			table.insert(0,thead)
			necesita_p=False
			for tdh in table.findAll(["td","th"]):
				if tdh.parent.parent.name=="thead":
					tdh.name="th"
				else:
					tdh.name="td"
				ps=tdh.findAll("p")
				if len(ps)>1 or (len(ps)==1 and not util.eqtxt(tdh,ps[0])):
					necesita_p=True
			if not necesita_p:
				for p in table.findAll("p"):
					p.unwrap()

	for ul in soup.findAll("ul"):
		txt=util.sclean(ul)
		if txt[-1]==":":
			li=ul.select(" > li")[-1]
			sig=ul.next_sibling
			while sig and isinstance(sig, bs4.Tag) and sig.name=="p":
				p=sig
				sig=p.next_sibling
				txt=util.sclean(p)
				txt2=None
				if p.span:
					txt2=util.sclean(p)
				if txt in ("o","comoen") or (txt2 and txt.startswith(txt2)):
					br=soup.new_tag("br")
					li.append(br)
					li.append(p)
					p.unwrap()
				else:
					break

	for s in soup.findAll("strong"):
		if s.span:
			s.unwrap()

	for s in soup.findAll(["span","strong"]):
		hjs=reversed(s.contents)
		for c in hjs:
			if (isinstance(c, bs4.NavigableString) or isinstance(c, unicode)):
				if util.is_vacio(c):
					s.insert_after(c)
				else:
					if s.span:
						nt=soup.new_tag(s.name)
						if s.name=="span":
							nt.attrs["class"]=s.attrs["class"]
						nt.append(c)
						s.insert_after(nt)
					else:
						break
			elif c.name in ("span","br"):
				s.insert_after(c)
			else:
				break
		hjs=[c for c in s.contents]
		for c in hjs:
			if (isinstance(c, bs4.NavigableString) or isinstance(c, unicode)):
				if util.is_vacio(c):
					s.insert_before(c)
				else:
					break
			elif c.name in ("span","br"):
				s.insert_before(c)
			else:
				break

	for p in soup.findAll(["p","li"]):
		hjs=reversed(p.contents)
		for c in hjs:
			if (isinstance(c, bs4.NavigableString) or isinstance(c, unicode)):
				if util.is_vacio(c):
					c.extract()
				else:
					break
			elif c.name=="br" or util.is_vacio(c):
				c.extract()
			else:
				break
		bns=[]
		ibr=0
		for c in p.contents:
			if isinstance(c, bs4.NavigableString) or isinstance(c, unicode):
				if util.is_vacio(c):
					bns.append(c)
				else:
					break
			elif c.name=="br" or util.is_vacio(c):
				bns.append(c)
				if c.name=="br":
					ibr=len(bns)
			else:
				break
		for i in range(0,ibr):
			bns[i].extract()

	for b in soup.findAll("br"):
		if b.next_sibling and isinstance(b.next_sibling,bs4.Tag) and b.next_sibling.name=="br":
			b.extract()

	for p in soup.find_all("p"):
		if p.get_text().startswith(u'\u2022'):
			ul=soup.new_tag("ul")
			li=soup.new_tag("li")
			hjs=[c for c in p.contents]
			for h in hjs:
				if isinstance(h, bs4.NavigableString) or isinstance(h, unicode):
					h=punto.sub("",h)
					if len(h)>0:
						li.append(h)
				else:
					if h.name=="br":
						ul.append(li)
						li=soup.new_tag("li")
						continue
					else:
						li.append(h)
			ul.append(li)
			p.replace_with(ul)

	for s in soup.findAll("span"):
		cl=s.attrs["class"]
		if cl!="stdout":
			txt=util.sclean(s)
			c=txt[0]
			if c=="$":
				if not txt.startswith("$HOME") and cl!="comando":
					s.attrs["class"]="comando"
			elif c=="/":
				if cl!="archivo":
					s.attrs["class"]="archivo"
			elif ("root root" in s.get_text() or "/sbin/nologin" in s.get_text() or "Ethernet controller" in s.get_text()):
				s.attrs["class"]="stdout"

	for s in soup.findAll("span",text="#",attrs={'class': "comando"}):
		if s.next_sibling and isinstance(s.next_sibling, bs4.Tag) and s.next_sibling.name=="span":
			ss=s.next_sibling
			if ss.attrs["class"]=="stdout":
				ss.insert(0," ")
				ss.insert(0,s)
				s.unwrap()

	enlaces=soup.findAll("span", attrs={'class': "enlace"})
	for e in enlaces:
		txt=sp.sub(" ",e.get_text()).strip()
		if txt.startswith("html://www."):
			txt=txt.replace("html://www.","http://www.")
		if txt.startswith("http") and " " not in txt:
			e.name="a"
			e.attrs['href']=txt
			del e.attrs['class']

	pcmd=util.get_spbr(soup)
	while len(pcmd)>0:
		for p in pcmd:
			s=p.span
			p.br.extract()
			s.name="p"
			p.insert_before(s)
		pcmd=util.get_spbr(soup)

	for s in soup.findAll("span"):
		if s.parent.name=="p" and util.eqtxt(s,s.parent):
			s.parent.attrs["class"]=s.attrs["class"]
			s.unwrap()

	ps=reversed(soup.findAll("p"))
	for p in ps:
		if "class" in p.attrs and p.attrs["class"] in ("stdout","archivo","comando"):
			if p.previous_sibling and isinstance(p.previous_sibling, bs4.Tag) and p.previous_sibling.name=="p":
				pr=p.previous_sibling
				if "class" in pr.attrs:
					if pr.attrs["class"]==p.attrs["class"]:
						pr.append(soup.new_tag("br"))
						pr.append(p)
						p.unwrap()

	if len(soup.body.contents)==1:
		p=soup.body.contents[0]
		if len(p.contents)==1:
			c=p.contents[0]
			if isinstance(c, bs4.Tag):
				c.unwrap()

	for t in soup.findAll("table"):
		if t.previous_sibling and t.previous_sibling.name=="p":
			p=t.previous_sibling
			if p.get_text().strip().startswith("Tabla "):
				t.insert(0,p)
				p.name="caption"
				for s in p.findAll("strong"):
					s.unwrap();

	h = util.get_html(soup)
	with open(f, "wb") as file:
		file.write(h.encode('utf8'))
	#util.escribir(h,f)
