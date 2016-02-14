#!/bin/bash
echo -n "Copiando html ... "
mv ~/Descargas/LFS201*.html html/ori 2> /dev/null
rm html/clean/* 2> /dev/null
rm md/* 2> /dev/null
cp html/ori/* html/clean/
echo "ok"
echo -n "Limpiando html ... "
python clean.py
echo "ok"
for f in html/clean/*.html; do
	MD=`basename "$f" | sed 's/html$/md/'`
	echo "Generando $MD"
	MD="md/$MD"
	pandoc --ascii -o "$MD" "$f"
	if [[ "$f" != *_popup*.html ]]; then
		tail -n +382 "$MD" | head -n -3 > aux
		mv aux "$MD"
	fi
	cat "$MD"| tr -dc '[[:print:]]áéíóúñäëïöüÁÉÍÓÚÑÄËÏÖÜ\n' | iconv --from-code=UTF-8 --to-code=UTF-8 -c | awk -f clean.awk > aux
	mv aux "$MD"
	sed '/\!\[\].images\/defaultProgBarH.gif/d' -i "$MD"

done
