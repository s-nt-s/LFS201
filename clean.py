import os.path
import zipfile
import bs4
import tempfile
import os
import glob
import re
import nltk
import string


tag_concat=['u','ul','ol','i','em','b','strong']
hr=re.compile(".*ObjLayerActionGoToNewWindow.*?'(.*?)'.*")
sp=re.compile("\s+", re.UNICODE)

printable = set(string.printable)

htmls=sorted(glob.glob('html/clean/*.html'))

def sclean(txt):
	txt=filter(lambda x: x in printable, txt)
	txt=sp.sub("",txt)
	txt=txt.replace("&nbsp;", "").strip()
	return txt

def vacio(soup,nodos, jump=False):
	r=[]
	tags=soup.find_all(nodos)
	for t in tags:
		if jump or (len(t.contents)==0 or len(t.select(" > *"))==0):
			txt=sclean(t.get_text())
			if len(txt)==0:
				r.append(t)
	return r

def nclean(ls):
	txt=""
	if ls:
		for n in ls:
			if isinstance(n, bs4.NavigableString) or isinstance(n, unicode):
				txt=txt+n
			else:
				txt=txt+n.get_text()
	txt=sclean(txt)
	return txt

for f in htmls:
	html = open(f,"r+")
	soup = bs4.BeautifulSoup(html)
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
		elif "rgb(0, 150, 200)" in s.attrs['style'] and s.parent.name!="a" and len(s.select(" > *"))==1 and s.select(" > *")[0].name!="a":
			s.attrs['class']="enlace"
		elif "rgb(0, 0, 255)" in s.attrs['style']:
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

	brs=soup.select("br")
	for b in brs:
		if len(nclean(b.next_sibling))==0 or len(nclean(b.previous_sibling))==0:
			b.extract()

	tags=vacio(soup, ['strong', 'em' , 'i', 'b', 'span', 'u'])
	for t in tags:
		t.unwrap()
	tags=vacio(soup, ['p', 'div', 'ul', 'li', 'ol'])
	for t in tags:
		t.extract()
	tags=vacio(soup, ['table'], True)
	for t in tags:
		t.extract()

	lis=soup.findAll("li")
	for li in lis:
		n=li.select(" > *")
		if len(n)==1 and n[0].name=="p":
			n[0].unwrap()

	for a in soup.select("a"):
		if "ObjLayerActionGoToNewWindow" in a.attrs['href']:
			a.attrs['href']=hr.sub("\\1",a.attrs['href'])

	for n in soup.html:
		if isinstance(n, bs4.Comment) or isinstance(n, bs4.NavigableString):
			n.extract()

	for lb in soup.findAll("label"):
		n=lb.select(" > *")
		if len(n)==1 and n[0].name=="p":
			lb.replaceWithChildren()

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

	h = str(soup)
	for t in tag_concat:
		r=re.compile("</"+t+">(\s*)<"+t+">", re.IGNORECASE|re.MULTILINE|re.DOTALL|re.UNICODE)
		h=r.sub("\\1",h)

	with open(f, "wb") as file:
		file.write(h)
