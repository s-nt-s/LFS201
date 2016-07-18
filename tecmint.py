# -*- coding: utf-8 -*-

import os.path
import glob
import re
import bs4
import util
import requests
from html5print import HTMLBeautifier

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def get_url(url):
	try:
		headers = {
			'Accept-Encoding': None
		}
		response = requests.get(url, headers=headers)
		soup = bs4.BeautifulSoup(response.text,"lxml")
		return soup
	except Exception, e:
		print str(e)
		return None

urls=[]
oris=[
	"http://www.tecmint.com/sed-command-to-create-edit-and-manipulate-files-in-linux/",
	"http://www.tecmint.com/installing-network-services-and-configuring-services-at-system-boot/",
	"http://www.tecmint.com/install-and-configure-kvm-in-linux/"
]
extra=[
	"http://www.tecmint.com/how-to-synchronize-time-with-ntp-server-in-ubuntu-linux-mint-xubuntu-debian/",
	"http://www.tecmint.com/install-and-configure-ntp-server-client-in-debian/"
]

for ori in oris:
	if ori not in urls:
		urls.append(ori)
		soup=get_url(ori)
		cp=soup.findAll('div',**{"id":"exam_announcement"})
		for c in cp:
			if c.a and c.get_text().strip().startswith("Part "):
				url=c.a.attrs["href"]
				if url not in urls:
					urls.append(url)
for ext in extra:
	if ext not in urls:
		urls.append(ext)

ini1=[
	"This post is ",
	"This article is ",
	"This is the last ",
	"One of the most important ",
	"Once you get used to working ",
	"In this article we will introduce ",
	"Every Linux system administrator "
]
ini2=[
	"A Linux Foundation Certified Engineer​",
	"A LFCE (short for Linux Foundation Certified Engineer​)",
	"A LFCE (Linux Foundation Certified Engineer)​ is a "
]

def starts_in(t,ini):
	t=util.get_printable(t)
	for i in ini:
		if t.startswith(util.get_printable(i)):
			return True
	return False

def first_starts_in(div):
	if len(div.contents)==0:
		return False
	f=div.contents[0]
	txt=None
	if isinstance(f, bs4.Tag):
		if f.name=="h3":
			return False
		txt=f.get_text()
	else:
		txt=f.string
	return not starts_in(txt,ini1)

def get_h(txt,url):
	mrk=url.split("/")[-2]
	h=out.new_tag("h2")
	h.attrs["id"]=mrk
	h.append(out.new_tag("a"))
	h.a.string=txt
	h.a.attrs["href"]="#"+mrk
	h.append(" ")
	h.append(out.new_tag("span"))
	h.span.append("(")
	h.span.append(out.new_tag("a"))
	h.span.a.string="source"
	h.span.a.attrs["href"]=url
	h.span.append(")")
	return h

def fix_h(div):
	for i in range(6,3,-1):
		ha=div.findAll("h"+str(i))
		hb=div.findAll("h"+str(i-1))
		if len(ha)>0 and len(hb)==0:
			for h in ha:
				h.name="h"+str(i-1)
	flag=False
	ct=[]
	for h in div.findAll(["h2","h3","h4","h5","h6"]):
		c=int(h.name[1])
		aux=[x for x in ct if x<c]
		if len(aux)>0:
			a=aux[-1]+1
			if a<c:
				flag=True
				h.name="h"+str(a)
		ct.append(c)
	if flag:
		fix_h(div)

oht="out/tecmint.html"

out = util.get_tpt("LFCS and LFCE by tecmint.com","rec/tecmint.css")
h1=out.new_tag("h1")
h1.string="LFCS"
out.body.div.append(h1)

index=True
flag=0
part=re.compile(u"\s*[\-–—]\s*Part\s*\d+$", re.UNICODE | re.IGNORECASE)
for url in urls:
	if url in oris:
		index=True
		flag=flag+1
	else:
		index=False

	soup=get_url(url)
	tt=part.sub("",soup.head.title.get_text().strip())
	if tt.startswith("LFCE: "):
		h1=out.new_tag("h1")
		h1.string="LFCE"
		out.body.div.append(h1)
		tt=tt[6:]
	elif tt.startswith("LFCS: "):
		tt=tt[6:]

	div=soup.find("div", **{"class":"entry-inner"})
	mas=soup.find("a", **{"class":"nextpostslink"})
	while mas:
		soup2=get_url(mas.attrs["href"])
		mas=soup2.find("a", **{"class":"nextpostslink"})
		div2=soup2.find("div", **{"class":"entry-inner"})
		div.append(div2)
		div2.unwrap()

	if flag==2 and not index:
		i=div.find("p",text=re.compile("\s*Linux Foundation Certified Engineer . Part \d+\s*"))
		if not i:
			i=div.find("img",**{"src":re.compile(".*/lfce-?\d+\.(png|jpeg)$")})
		v=div.find("iframe",**{"src":"//www.youtube.com/embed/Y29qZ71Kicg"})
		if i and v:
			d1=i.find_parent("div")
			d2=v.find_parent("div",**{"class":"post-format"})
			if not d2:
				d2=v.find_parent("div",**{"class":"video-container"})
			if d1 and d2:
				while d1 and d1!=d2:
					aux=d1.next_sibling
					d1.extract()
					d1=aux
				d2.extract()
		if div.p and starts_in(div.p.get_text(),ini2):
			div.p.extract()

	if flag==1 and div.h3 and div.h3.previous_sibling:
		while first_starts_in(div):
			div.contents[0].extract()
	if flag==2 and index and div.h3 and div.h3.previous_sibling:
		while div.h3.previous_sibling:
			div.h3.previous_sibling.extract()
	if flag==3:
		div.img.find_parent("div").extract()
		if index:
			cp=soup.findAll('div',**{"id":"exam_announcement"})
			for c in cp:
				c.extract()

	div.attrs.clear()
	h2=get_h(tt,url)
	div.insert(0,h2)
	fix_h(div)
	out.body.div.append(div)

for n in out.findAll("noscript"):
	a=n.find_parent("a")
	if a:
		hj=a.select("> *")
		if len(hj)==2 and hj[0].name=="img" and hj[1].name=="noscript":
			a.replace_with(n)
			n.unwrap()

for i in out.findAll("img"):
	if "data-lazy-src" in i.attrs:
		i.attrs["src"]=i.attrs["data-lazy-src"]
		a=i.find_parent("a")
		if a and "href" in a.attrs and a.attrs["href"]==i.attrs["src"]:
			a.unwrap()
	d=i.find_parent("div")
	if d and "class" in d.attrs and "wp-caption" in d.attrs["class"]:
		d.name="figure"
		d.p.name="figcaption"
	src=i.attrs["src"]
	alt=i.attrs["alt"]
	i.attrs.clear()
	i.attrs["src"]=src
	i.attrs["alt"]=alt

for a in out.findAll(**{"class":"adsbygoogle"}):
	a.parent.extract()
for a in out.findAll(text="Become a Linux Certified System Administrator"):
	a.find_parent("div").extract()
for a in out.findAll(text="Become a Linux Certified Engineer"):
	a.find_parent("div").extract()
for a in out.findAll("a"):
	if a.find_parent("h2") or "href" not in a.attrs:
		continue
	if a.attrs["href"] in urls:
		a.attrs["href"]="#"+a.attrs["href"].split("/")[-2]
		if "target" in a.attrs:
			del a.attrs["target"]
	else:
		a.attrs["class"]="external"
		a.attrs["target"]="_blank"
for a in out.findAll(["figure","figcaption","td","th","table"]):
	if a.attrs:
		a.attrs.clear()
for a in out.findAll("colgroup"):
	a.extract()
for t in out.findAll("table"):
	for s in t.findAll(["span","b"]):
		s.unwrap()
	if not t.thead:
		t.insert(0,out.new_tag("thead"))
		t.thead.append(t.tr)
		for td in t.tr.findAll("th"):
			td.name="th"
for h in out.findAll("h1"):
	h.extract()
for h in out.findAll(["h3", "h4","h5"], text="Reference Links"):
	ol=h.find_next_sibling("ol")
	if ol:
		ol.extract()
		h.extract()
ct=1
for h in out.findAll(["h2", "h3", "h4","h5","h6"]):
	c=int(h.name[1])-1
	h.name="h"+str(c)
	if not h.a and c in (2,3,4):
		util.h_to_a(out,h,ct)
		ct=ct+1
for ol in out.findAll("ol"):
	if ol.parent and ol.parent.name=="ol":
		ol.unwrap()
for p in out.findAll("pre"):
	for s in p.findAll("strong"):
		if "style" in s.attrs and "class" not in s.attrs:
			del s.attrs["style"]
			s.attrs["class"]="resaltar"

html = util.get_html(out,True)
html=html.replace(u"–","-")
html=html.replace(u"—","-")
r=re.compile("([rwx])=2([210])")
html=r.sub("\\1=2<sup>\\2</sup>",html)
r=re.compile("</p>\s*<li>")
html=r.sub("</p><ul><li>",html)
r=re.compile("</li>\s*<p>")
html=r.sub("</li></ul><p>",html)
util.escribir(html,oht)

#out.prettify("utf-8",formatter="html")
#with open(oht, "wb") as file:
#	file.write(html)#.encode('utf8'))
