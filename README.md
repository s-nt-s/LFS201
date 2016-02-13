Aunque gran parte del contenido del curso `LFS201` es texto que se podria consultar 
perfectamente offline (desde un ebook, por ejemplo) al menos para repasar conceptos,
la plataforma del curso esta pensada integramente para que se use desde internet.

Este proyecto sirve para automatizar parte de la extración del texto del curso
y su conversión a un formato más manejable, de la siguiente manera:

1- `chrome/*`: Extensión para `chrome/chromium` que descarga el contenido renderizado según navegas por el curso
2. `run.sh`: script que realiza las siguiente acciones:
	a. Mueve los `html` al directorio de trabajo
	b. Limpia los `html` simplificando su formato con `clean.py`
	c. Crea ficheros `markdown` a partir de los ficheros `html` con `pandoc`
	d. Limpia los ficheros `markdown` eliminado cabeceras y demás contenido repetido con `clean.awk`

Finalmente estos ficheros `markdown` se revisan a mano y se genera un epub
para poder estudiar comodamente offline.
