Aunque gran parte del contenido del curso `LFS201` es texto que se podria consultar 
perfectamente offline al menos para repasar conceptos,
la plataforma del curso esta pensada integramente para que se use solo desde internet.

Este proyecto sirve para automatizar parte de la extración del texto del curso
y su conversión a un html limpio y más manejab:le

1. `chrome/*`: Extensión para `chrome/chromium` que descarga el contenido renderizado según navegas por el curso
2. `run.sh`: script que realiza las siguiente acciones:
	1. Mueve los `html` al directorio de trabajo
	2. Limpia los `html` simplificando su formato con `clean.py`
	3. `join.py` une todos los html en out/LFS201.html indexado con cabeceras

De ahí creamos con `pandoc` un markdown o un epub según lo que queramos
