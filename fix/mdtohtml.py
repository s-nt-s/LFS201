import os.path
import zipfile
import bs4
import tempfile
import os
import glob
import re
import nltk
import string
import unicodedata
from subprocess import call

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def get_soup(f):
	h = open(html,"r+")
	soup = bs4.BeautifulSoup(h,"lxml")
	h.close()
	return soup

for md in glob.glob('*.md'):
	html=md[:-2] + "html"
	call(["pandoc", "-o", html, md])
	soup=get_soup(html)

	for i in soup.findAll(["tr","th","td"]):
		i.attrs.clear()

	hj=soup.body.select(" > *")

	if len(hj)==2 and hj[0].name=="p" and hj[1].name=="table":
		c=hj[0]
		t=hj[1]
		t.insert(0,c)
		c.name="caption"

	h=unicode(soup)
	with open(html, "wb") as file:
		file.write(h.encode('utf8'))
