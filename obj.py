import bs4
import re
import util
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

out="out/Objetivos.html"

soup=util.get_soup("out/LFS201.html")
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
