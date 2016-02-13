import os.path
import zipfile
import bs4
import tempfile
import os
import glob
import re
import nltk

i1=re.compile("</(i|em)>\s+<(i|em)>", re.IGNORECASE|re.MULTILINE|re.DOTALL)
b1=re.compile("</(b|strong)>\s+<(b|strong)>", re.IGNORECASE|re.MULTILINE|re.DOTALL)
i2=re.compile("</(i|em)><(i|em)>", re.IGNORECASE|re.MULTILINE|re.DOTALL)
b2=re.compile("</(b|strong)><(b|strong)>", re.IGNORECASE|re.MULTILINE|re.DOTALL)
sp=re.compile("\s+")

htmls=sorted(glob.glob('html/clean/*.html'))

for f in htmls:
	html = open(f,"r+")
	soup = bs4.BeautifulSoup(html)
	html.close()
	texts = soup.find_all(text=True)
	for t in texts:
	   t.replace_with(t.replace("&nbsp", " "))
	spans=soup.select("span")
	for s in spans:
		s.unwrap()

	for p in soup.select("*"):
		if 'style' in p.attrs:
			del p.attrs['style']
	h = str(soup)#soup.prettify("utf-8",formatter="minimal") #str(soup)
	h=i1.sub(" ",h)
	h=b1.sub(" ",h)
	h=i2.sub("",h)
	h=b2.sub("",h)
	h=sp.sub(" ",h)

	with open(f, "wb") as file:
		file.write(h)

