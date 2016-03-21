#!/bin/bash
if [ "$1" == "-r" ]; then
	rm ~/Descargas/LFS201*.html 2> /dev/null
else
	echo -n "Copiando html ... "
	mv ~/Descargas/LFS201*.html html/ori 2> /dev/null
	rm html/clean/* 2> /dev/null
	rm md/* 2> /dev/null
	cp html/ori/* html/clean/
	rename 's/_popup.html$/_popup (0).html/' html/clean/*.html
	echo "ok"
fi
echo -n "Limpiando html ... "
python clean.py
echo "ok"

echo -n "Creando salida ... "
python join.py
echo "ok"

echo -n "Creando listado de objetivos... "
python obj.py
echo "ok"
