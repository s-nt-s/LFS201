import bs4
import re

html="out/LFS201.html"
out="out/Objetivos.html"

def get_soup(html):
	html = open(html,"r+")
	soup = bs4.BeautifulSoup(html,'html.parser')#"lxml")
	html.close()
	return soup

soup=get_soup(html)
soup.title.string=soup.title.string+": Objetivos"

flds=soup.findAll("fieldset", attrs={'class': re.compile(r".*\bn2\b.*")})
for f in flds:
	if f.legend.get_text().strip().lower()=="objetivos de aprendizaje":
		f.legend.string=f.parent.h1.a.string
		f.div.p.extract()
	else:
		f.extract()

for h in soup.findAll("h1"):
	h.extract()

for div in soup.body.div.select(" > div"):
	div.unwrap()

h=unicode(soup)
with open(out, "wb") as file:
	file.write(h.encode('utf8'))
