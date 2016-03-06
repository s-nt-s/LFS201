# -*- coding: utf-8 -*-

import os.path
import glob
import re
import bs4

tt=re.compile(".*?LFS201_\d+.\d+_([^/]+?)(_popup \(\d+\))?.md$")
cp=re.compile(".*?LFS201_(\d+)\..*$")
pr=re.compile("(.*)¿(.*?)-(.*)")
bk=re.compile("<(fieldset|head|body|meta|link|script|p|ul|ol|li|div)>")
ck=re.compile("(Haga|Haz) click (en|sobre) (el|los|en)")
fg=re.compile(".*?(Figura|Figure)\s+\d+\.\d+(:|.)", re.UNICODE|re.MULTILINE|re.DOTALL)
ct=re.compile(".*? para ")
sp=re.compile("\s+", re.UNICODE)

hts=sorted(glob.glob('html/clean/*.html'))

caB=0
n=0
f=0

oht="out/LFS201.html"

def get_soup(html):
	html = open(html,"r+")
	soup = bs4.BeautifulSoup(html)
	html.close()
	return soup

def find_text(soup,r):
	rt=[]
	ps=soup.findAll('p')
	for p in ps:
		if r.match(p.get_text()):
			rt.append(p)
	return rt

soup = get_soup(oht)
soup.body.div.clear()

fldB=None

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
		h=b.p.extract().strong
		h.name="h1"
		h.string=sp.sub(" ",h.string).strip('.')[9:]
		h.attrs['id']="c"+str(ca)
		soup.body.div.append(h)
		n=2

	fld = soup.new_tag("fieldset")
	fld.attrs['class']="n"+str(n)
	t.name="legend"
	fld.append(t)
	b.name="div"
	fld.attrs['id']="c"+str(ca)+"f"+str(f)
	fld.append(b)

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
		soup.body.div.append(fld)
		fldB=fld

flds=soup.findAll("fieldset", attrs={'class': re.compile(r".*\bn3\b.*")})
for fld in flds:
	if len(fld.parent.select(" > *"))==1:
		fld.parent.replace_with(fld.div)

h = str(soup)
h=bk.sub("\\n<\\1>",h)
with open(oht, "wb") as file:
	file.write(h)
