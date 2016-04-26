# -*- coding: utf-8 -*-

import os.path
import glob
import re
import bs4
import util
import requests

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

urls=[
	"http://www.tecmint.com/sed-command-to-create-edit-and-manipulate-files-in-linux/",
	"http://www.tecmint.com/vi-editor-usage/",
	"http://www.tecmint.com/compress-files-and-finding-files-in-linux/",
	"http://www.tecmint.com/create-partitions-and-filesystems-in-linux/",
	"http://www.tecmint.com/mount-filesystem-in-linux/",
	"http://www.tecmint.com/creating-and-managing-raid-backups-in-linux/",
	"http://www.tecmint.com/linux-boot-process-and-manage-services/",
	"http://www.tecmint.com/manage-users-and-groups-in-linux/",
	"http://www.tecmint.com/linux-package-management/",
	"http://www.tecmint.com/linux-basic-shell-scripting-and-linux-filesystem-troubleshooting/",
	"http://www.tecmint.com/manage-and-create-lvm-parition-using-vgcreate-lvcreate-and-lvextend/",
	"http://www.tecmint.com/explore-linux-installed-help-documentation-and-tools/",
	"http://www.tecmint.com/configure-and-troubleshoot-grub-boot-loader-linux/",
	"http://www.tecmint.com/monitor-linux-processes-and-set-process-limits-per-user/",
	"http://www.tecmint.com/change-modify-linux-kernel-runtime-parameters/",
	"http://www.tecmint.com/set-access-control-lists-acls-and-disk-quotas-for-users-groups/",

	"http://www.tecmint.com/installing-network-services-and-configuring-services-at-system-boot/",
	"http://www.tecmint.com/configure-nfs-server/",
	"http://www.tecmint.com/disk-encryption-in-linux/",
	"http://www.tecmint.com/setup-apache-with-name-based-virtual-hosting-with-ssl-certificate/",
	"http://www.tecmint.com/configure-squid-server-in-linux/",
	"http://www.tecmint.com/configure-squidguard-for-squid-proxy/",
	"http://www.tecmint.com/setting-up-email-services-smtp-and-restricting-access-to-smtp/",
	"http://www.tecmint.com/configure-iptables-firewall/",
	"http://www.tecmint.com/linux-system-monitoring-troubleshooting-tools/",
	"http://www.tecmint.com/setup-linux-as-router/",
	"http://www.tecmint.com/setup-yum-repository-in-centos-7/",
	"http://www.tecmint.com/audit-network-performance-security-and-troubleshooting-in-linux/"
]

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

tpt="out/tecmint.htm"
oht="out/tecmint.html"
out = util.get_soup(tpt)
dv=out.new_tag("div")
out.append(dv)
h1=out.new_tag("h1")
h1.string="LFCS"
dv.append(h1)

flag=1
for u in urls:
	soup=get_url(u)
	tt=soup.head.title.get_text().strip()
	if tt.startswith("LFCE: "):
		h1=out.new_tag("h1")
		h1.string="LFCE"
		dv.append(h1)
		tt=tt[6:]
		flag=2
	elif tt.startswith("LFCS: "):
		tt=tt[6:]
	h2=out.new_tag("h2")
	h2.string=tt
	h2.attrs["id"]=u.split("/")[-2]
	div=soup.find("div", **{"class":"entry-inner"})

	if flag==4:
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
	if flag==2 and div.h3 and div.h3.previous_sibling:
		while div.h3.previous_sibling:
			div.h3.previous_sibling.extract()
		flag=4

	div.insert(0,h2)
	dv.append(div)

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
for a in out.findAll(**{"class":"adsbygoogle"}):
	a.parent.extract()
for a in out.findAll(text="Become a Linux Certified System Administrator"):
	a.find_parent("div").extract()
for a in out.findAll(text="Become a Linux Certified Engineer"):
	a.find_parent("div").extract()
for a in out.findAll("a"):
	if "href" in a.attrs and a.attrs["href"] in urls:
		a.attrs["href"]="#"+a.attrs["href"].split("/")[-2]

h=unicode(out)
util.escribir(h,oht)

