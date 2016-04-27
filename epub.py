import bs4
import re
import os
from subprocess import call
import util

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

out="out/epub.html"

soup=util.get_soup("out/LFS201.html")
soup.head.link.attrs['href']="rec/epub.css"

for h in soup.findAll(["h1","legend"]):
	if h.a:
		h.a.unwrap()

for l in soup.findAll("legend",text=re.compile("\s*(\d+\.\d+\. Laboratorios|Objetivos de aprendizaje \(revisi.n\)|Comprobaci.n de Conocimientos [\d\.]+)\s*")):
	l.find_parent("fieldset").extract()

intros=re.compile("^c(\d\d+|[2-9])f1$")
for f in soup.findAll("fieldset", attrs={'class': re.compile(r".*\bn2\b.*")}):
	if intros.match(f.attrs['id']):
		f.legend.extract()
	else:
		f.legend.name="h2"
	f.div.unwrap()
	f.unwrap()

soup.body.div.unwrap()

code=unicode(soup)
with open(out, "wb") as file:
	file.write(code.encode('utf8'))

os.chdir("out")
call(["miebup", "epub.html", "LFS201.epub"])
