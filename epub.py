import bs4
import re
import os
from subprocess import call

html="out/LFS201.html"
out="out/epub.html"

def get_soup(html):
	html = open(html,"r+")
	soup = bs4.BeautifulSoup(html,'html.parser')#"lxml")
	html.close()
	return soup

soup=get_soup(html)

for h in soup.findAll(["h1","legend"]):
	if h.a:
		h.a.unwrap()

for l in soup.findAll("legend",text=re.compile("\s*(\d+\.\d+\. Laboratorios|Objetivos de aprendizaje \(revisi.n\))\s*")):
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
soup.head.link.attrs['href']="epub.css"

h=unicode(soup)
with open(out, "wb") as file:
	file.write(h.encode('utf8'))

os.chdir("out")
call(["miebup", "epub.html", "LFS201.epub"])
