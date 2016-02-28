# -*- coding: utf-8 -*-

import os.path
import glob
import re
import bs4

tt=re.compile(".*?LFS201_\d+.\d+_([^/]+?)(_popup \(\d+\))?.md$")
cp=re.compile(".*?LFS201_(\d+)\..*$")
pr=re.compile("(.*)¿(.*?)-(.*)")
bk=re.compile("<(fieldset|head|body|meta|link|script|p|ul|ol|li|div)>")
ck=re.compile("(Haga|Haz) click (en|sobre) (el|los)")
ct=re.compile(".*? para ")

hts=sorted(glob.glob('html/clean/*.html'))

p=1
t=""
c=0
n=0

oht="out/LFS201.html"

def get_soup(html):
	html = open(html,"r+")
	soup = bs4.BeautifulSoup(html)
	html.close()
	return soup

soup = get_soup(oht)
soup.body.clear()

fldB=None

for ht in hts:
	sp = get_soup(ht)
	t=sp.title
	b=sp.body

	if "_popup" in ht:
		n=3
		t.string="Popup "+str(p)
		p=p+1
	else:
		p=1
		ca=int(cp.sub("\\1",ht))
		if ca>c:
			n=1
			c=ca
		else:
			n=2

	if n==1:
		h=soup.new_tag("h1")
		h.string=u"Capítulo "+str(ca)+": "+t.get_text().strip()
		soup.body.append(h)

	fld = soup.new_tag("fieldset")
	t.name="legend"
	fld.append(t)
	b.name="div"
	fld.append(b)
	fld.div.replaceWithChildren()

	if n==3:
		cs=fldB.find_all('p',text=ck)
		if len(cs)>0:
			c=cs[0]
			fld.legend.append(": "+ct.sub("",c.string))
			c.replace_with(fld)
		else:
			fldB.append(fld)
	else:
		soup.body.append(fld)
		fldB=fld

h = str(soup)
h=bk.sub("\\n<\\1>",h)
with open(oht, "wb") as file:
	file.write(h)
