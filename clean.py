import os.path
import zipfile
import bs4
import tempfile
import os
import glob
import re
import nltk
import string

uni_remove=('Mn', 'Me','Z', 'C')

tag_concat=['u','ul','ol','i','em','b','strong']
tag_round=['u','i','em','b','span','strong', 'a']
tag_trim=['li', 'th', 'td', 'div']
tag_right=['p']
hr=re.compile(".*ObjLayerActionGoTo.*?'(.*?)'.*")
sp=re.compile("\s+", re.UNICODE)

printable = set(string.printable)

def sclean(txt):
	txt=filter(lambda x: x in printable, txt)
	txt=sp.sub("",txt).strip()
	return txt

def vacio(soup,nodos):
	r=[]
	tags=soup.find_all(nodos)
	for t in tags:
		txt=sclean(t.get_text())
		if len(txt)==0:
			r.append(t)
	return r

def eqtxt(a,b):
	sa=sclean(a.get_text())
	sb=sclean(b.get_text())
	return sa==sb

def tail(n):
	txt=""
	s=n
	while s.next_sibling and len(txt)==0:
		s=s.next_sibling
		if isinstance(s, bs4.NavigableString) or isinstance(s, unicode):
			txt=txt+sclean(s)
		else:
			txt=txt+sclean(s.get_text())
	if len(txt)==0:
		return True
	txt=""
	s=n
	while s.previous_sibling and len(txt)==0:
		s=s.previous_sibling
		if isinstance(s, bs4.NavigableString) or isinstance(s, unicode):
			txt=txt+sclean(s)
		else:
			txt=txt+sclean(s.get_text())
	txt=sclean(txt)
	if len(txt)==0:
		return True
	return False



def parrafos(soup):
	prfs= soup.find_all(['li','table'])
	ps = soup.find_all('p')
	for p in ps:
		flag=False
		for c in p.contents:
			#(isinstance(c, bs4.Tag) and c.name=="a") or
			if ((isinstance(c, bs4.NavigableString) or isinstance(c, unicode)) and len(sclean(c))>0):
				flag=True
				break
		if flag:
			prfs.append(p)
	return prfs

def eqparents(n,tag=None):
	r=[]
	txt=sclean(n.get_text())
	if not tag:
		tag=n.name
	n=n.parent
	while n.parent:
		n=n.parent
		if txt!=sclean(n.get_text()):
			break
		if n.name==tag:
			r.append(n)
	return r

def eqsibling(n):
	r=[]
	tag=n.name
	s=n
	while s.next_sibling:
		s=s.next_sibling
		if isinstance(s, bs4.NavigableString) or isinstance(s, unicode):
			break
		if s.name!=tag:
			break
		if tag!="span" or n.attrs['class']==s.attrs['class']:
			r.append(s)
	return r


htmls=sorted(glob.glob('html/clean/*.html'))

for f in htmls:
	html = open(f,"r+")
	soup = bs4.BeautifulSoup(html,"lxml")
	html.close()
	head=soup.head.select("meta")
	head.append(soup.head.title)
	soup.head.clear()
	for h in head:
		soup.head.append(h)

#	imgs=[a.attrs['src'] for a in soup.select("img") if "_small_" in a.attrs['src']]
#	print str(imgs)

	ttxt=soup.select("div.ttxt")
	if len(ttxt)>0:
		if len(ttxt)>1:
			del ttxt[-1]
		soup.body.clear()
		for t in ttxt:
			soup.body.append(t)
	elif len(sclean(soup.body.get_text()))==0:
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

	spans=soup.select("span")
	for s in spans:
		if 'style' not in s.attrs:
			s.unwrap()
		elif "rgb(0, 150, 200)" in s.attrs['style'] and s.parent.name!="a" and not(len(s.select(" > *"))==1 and s.select(" > *")[0].name=="a"):
			s.attrs['class']="enlace"
		elif "rgb(0, 0, 255)" in s.attrs['style'] or "rgb(0, 0, 205)" in s.attrs['style'] or "color:#0000CD;" in s.attrs['style'] or "rgb(41, 1, 208)" in s.attrs['style']:
			s.attrs['class']="comando"
		elif "rgb(0, 200, 0)" in s.attrs['style']:
			s.attrs['class']="stout"
		elif "rgb(125, 110, 70)" in s.attrs['style']:
			s.attrs['class']="archivo"
		else:
			s.unwrap()
	us=soup.select("u")
	for u in us:
		if u.parent.name=="a":
			u.unwrap()
	strongs=soup.select("strong")
	for s in strongs:
		ps=eqparents(s)
		for p in ps:
			p.unwrap()
	spans=soup.select("span")
	for s in spans:
		ps=eqparents(s)
		for p in ps:
			p.unwrap()

	brs=soup.select("br")
	for b in brs:
		if tail(b):
			b.extract()

	tags=vacio(soup, ['table', 'p', 'div', 'ul', 'ol', 'li'])
	for t in tags:
		t.extract()
	tags=vacio(soup, ['strong', 'em' , 'i', 'b', 'span', 'u'])
	for t in tags:
		t.unwrap()

	for lb in soup.findAll("label"):
		n=lb.select(" > *")
		if len(n)==1 and n[0].name=="p":
			lb.replaceWithChildren()

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

	prfs=parrafos(soup)
	for p in prfs:
		texts=p.find_all(text=True)
		for t in texts:
			b=sp.sub(" ",t.string)
			t.replace_with(b)

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
	for t in soup.select("table"):
		t.attrs.clear()

	spans=soup.select("span")
	for s in spans:
		sb=eqsibling(s)
		if len(sb)>0:
			sblng=soup.new_tag("sblng")
			s.append(sblng)
			for b in sb:
				s.sblng.append(b)
				s.sblng.span.unwrap()
			s.sblng.unwrap()

	enlaces=soup.findAll("span", attrs={'class': "enlace"})
	for e in enlaces:
		us=e.findAll('u')
		for u in us:
			u.unwrap()
		txt=sp.sub(" ",e.get_text()).strip()
		if txt.startswith("http") and " " not in txt:
			e.name="a"
			e.attrs['href']=txt
			del e.attrs['class']

	h = unicode(soup)

	for t in tag_concat:
		r=re.compile("</"+t+">(\s*)<"+t+">", re.MULTILINE|re.DOTALL|re.UNICODE)
		h=r.sub("\\1",h)
	for t in tag_round:
		r=re.compile("(<"+t+"[^>]*>)(\s+)", re.MULTILINE|re.DOTALL|re.UNICODE)
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

	with open(f, "wb") as file:
		file.write(h.encode('utf8'))
