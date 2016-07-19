# Introdución

Estos apuntes seguiran el esquema de apartado **Overview of Domains and Competencies**
de [training.linuxfoundation.org/certification/lfcs](https://training.linuxfoundation.org/certification/lfcs#examDetails)
ya que el contenido del curso **LFS201** no esta siendo (en mi opinión) suficiente
para presentarse al examen **LFCS**

Gracias por adelantado a:

* [pablox.co](https://pablox.co/obteniendo-la-linux-foundation-certified-system-administrator-lfcs/)
* [leonelatencio.com](http://leonelatencio.com/notas-de-preparacion-para-el-examen-de-certificacion-de-linux-foundation/)
* [daemons.cf](http://daemons.cf/cgit/apuntes-LFS201)

## Instalación

Tengo registrado el examen para hacerlo sobre Ubuntu, por lo tanto usare
una maquina virtual de [Virtual Box](https://www.virtualbox.org/) con
[**Lubuntu 14.04.4**](http://cdimage.ubuntu.com/lubuntu/releases/14.04/release/),
en concreto la versión `32-bit PC (i386) desktop image`

Para agilizar el uso de este entorno realizare las siguientes configuraciones:

**1- Facilitar acceso por ssh**

Primero, instalo ssh en lubuntu con `sudo apt-get install openssh-server`.

Segundo, configuro Virtual Box para que redirija el puerto 2222 local al
puerto 22 de la máquina virtual

Propiedades máquina virtual -> Red -> Adaptador 1 -> Avanzadas ->
Reenvio de puertos -> Nombre: ssh, Protocolo: TCP, Puerto anfritión: 2222
Puerto invitado: 22

Tercero, creo una clave publica/privada para entrar directamente
(como es para esto me puedo permitir crearla sin contraseña)

```console
me@local ~ $ ssh-keygen -C vbox
Generating public/private rsa key pair.
Enter file in which to save the key (/home/me/.ssh/id_rsa): /home/me/.ssh/vbox
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/me/.ssh/vbox.
Your public key has been saved in /home/me/.ssh/vbox.pub.
...
me@local ~ $ ssh-copy-id -i /home/me/.ssh/vbox.pub -p 2222 me@localhost
```

Cuarto, configuro `~/.ssh/config` para que todo se más facil aún:

```
Host lubuntu
HostName 127.0.0.1
IdentityFile /home/me/.ssh/vbox
User me
Port 2222
```

**2- Arranque en modo consola por defecto**

`sudo nano /etc/default/grub` y cambio

```
GRUB_HIDDEN_TIMEOUT=0
GRUB_CMDLINE_LINUX_DEFAULT=”quiet splash”
GRUB_CMLDLINE_LINUX=""
#GRUB_TERMINAL=console
```

por

```
#GRUB_HIDDEN_TIMEOUT=0
#GRUB_CMDLINE_LINUX_DEFAULT=”quiet splash”
GRUB_CMLDLINE_LINUX="text"
GRUB_TERMINAL=console
```

\* De paso comento la linea de GRUB_HIDDEN_TIMEOUT para que aparezca
el menú de grub ya que lo necesitare para algunas pruebas

Guardo los cambios y actualizo con `sudo update-grub`

**3- Autologin**

`sudo nano /etc/init/tty1.conf` para añadir la linea:

```
exec /sbin/getty -8 38400 tty1 -a me
```

**4- Configuro sudo para que no pida contraseña**

Hago `sudo visudo` para añadir la linea:

```
me ALL = NOPASSWD : ALL
```

**5- Ejecuto  ready-for.sh**

```console
me@vbx:~$ cd /tmp
me@vbx:/tmp$ wget -q https://training.linuxfoundation.org/cm/prep/ready-for.sh
me@vbx:/tmp$ chmod +x ready-for.sh
me@vbx:/tmp$ ./ready-for.sh --install LFS201
Checking that this computer is suitable for LFS201: Essentials of System Administration
...
Is that okay? [y/N] y
...
```

**BONUS: Debian 8**

Adicionalmente, para algunos casos usare
[Debian 8.4.0](http://cdimage.debian.org/debian-cd/current-live/i386/iso-hybrid/debian-live-8.4.0-i386-lxde-desktop.iso)
en otra maquina virtual y con una configuración similar a la ya
detallada en los pasos anteriores

**BONUS: Red interna**

Para algunos ejercicios en los que quiero conectar varias maquinas
virtuales entre si hago esto: https://www.youtube.com/watch?v=lhOY-KilEeE
http://superuser.com/questions/119732/how-to-do-networking-between-virtual-machines-in-virtualbox
(*con debian 8 no funcionaba, he tenido que hacerlo entre un ubuntu y un lubuntu*)

# Temario

Fuente: [training.linuxfoundation.org/certification/lfcs](https://training.linuxfoundation.org/certification/lfcs#examDetails)

## Essential Commands - 25%

### Log into graphical and text mode consoles

Si estamos en modo texto y queremos ir a modo grafico tenemos dos opciones:

* `startx` (para esto en lubuntu antes necesitamos `sudo apt-get install lxde-common && echo "exec startlxde" > ~/.xinitrc`)
* `telinit 5` (en lubuntu no funciona pero en debian si)

Si se trata de que antes de que se ejecute el arranque por defecto en modo
grafico lo abortemos y entremos en mode texto tenemos que:

1. Posicionarnos en la opción de grub deseada
2. Pulsar `e` para que nos deje editarla
3. Buscar la linea donde se carga el kernel y escribir al final de todo `text`
(en otras distribuciones seria escribir `3`, es decir, el runlevel al que
queremos ir).

### Search for files

`find` con:

* `-name`
* `-iname`
* `-type`
* `-mtime`
* `-size`
* `-user`
* `-not` o `!`
* `-perm 755`

y para ejecutar algo sobre los resultados `-exec`. Ejemplos:

```
find / -name "test.txt" -exec chmmod 700 {} \;
```

Tambien podemos usar:

* `which` busca ejecutables en el PATH
* `locate` busca en base de datos del sistema de ficheros (que se puede actualizar con `sudo updatedb`)

Más: [www.tecmint.com](http://www.tecmint.com/compress-files-and-finding-files-in-linux/)

### Evaluate and compare the basic file system features and options

*no tengo claro a que se refiere*

### Compare, create and edit text files

* Crear fichero vacio: `touch fichero.txt`
* Editar fichero: `nano fichero.txt`
* Comparar ficheros: `diff fichero1.txt fichero2.txt`

Más: [www.tecmint.com - vi](http://www.tecmint.com/vi-editor-usage/)

### Compare binary files

`cmp` o `diff`

### Use input-output redirection (e.g. >, >>, |, 2>)

* Entrada estanadar = tipo 0
* Salida estanadar = tipo 1
* Error estandar = tipo 2

Ejemplos:

* `comando 2>&1` redirigir errores a salida estandar
* `wc < archivo.txt` alimenta la entrada estandar de `wc` con `archivo.txt`
* `comando 2> /dev/null` desecha la salida de errores
* `ps -a | sort` redireciona la salida de `ps` a la entrada de `sort`

Más: [hipertextual.com](http://hipertextual.com/archivo/2014/07/redirecciones-y-tuberias-bash/)

### Analyze text using basic regular expressions

* `grep -e`
* `awk`
* `sed`

Más: [www.tecmint.com - part 1](http://www.tecmint.com/sed-command-to-create-edit-and-manipulate-files-in-linux/)

### Archive, backup, compress, unpack, and uncompress files

* `tar cvf file.tar *` comprimir
* `tar xvf file.tar` descomprimir
* `tar xpvf file.tar` descomprimir presrvando permisos
* `tar tf file.tar` listar contenido
* Para comprimir a la vez que se empaqueta añadir la opción:
  * `z` para comprimir con `gzip`
  * `j` para comprimir con `bz2`
  * `J` para comprimir con `xz`

Más: [www.tecmint.com](http://www.tecmint.com/compress-files-and-finding-files-in-linux/)
https://www.youtube.com/watch?v=ZxVyhZEYEAU

### Create, delete, copy, and move files and directories

`touch`, `cp`, `mv`, `rm` ...

`dd if=input-file of=output-file options` crear `output-file` usando `input-file` según las opciones pasadas:

* `dd if=/dev/zero of=outfile bs=1M count=10` crea un archivo de 10 MB lleno con ceros
* `dd if=/dev/sda of=/dev/sdb` crea una copia de `/dev/sda` en `/dev/sdb` (datos en bruto)
* `dd if=/dev/sda of=sdadisk.img` crea una imagen del disco duro `/dev/sda`
* `dd if=/dev/sda1 of=partition1.img` respaldar una partición
* `dd if=ndata conv=swab count=1024 | uniq > ofile`

### Create hard and soft links

Enlaces simbolicos:

* Es parecido a un acceso directo de windows
* El enlace y el fichero original no comparten inodo
* Borrar el enlace no borra el fichero original
* Borrar el fichero original no borra el enlace, pero lo deja *roto*
* Se crean con `ln -s fichero_original enlace_simbolico`

Enlaces duros:

* El enlace y el fichero original comparten inodo
* No puede haber enlaces duros entre distintos sitemas de ficheros
* No se puede hacer enlaces duros a directorios
* Los cambios en un enlace duro (permisos, contenidos, etc) se propagan
al fichero original y los demás enlaces duros
* Si se borra el fichero original no se pierde la información porque
tambien la tiene el enlace duro
* Se crean con `ln fichero_original enlace_duro`

Se puede comprobar si dos ficeros tienen el mismo inodo o no con `ls -li` o `stat fichero`

Más: [rm-rf.es](http://rm-rf.es/diferencias-entre-soft-symbolic-y-hard-links/)

### List, set, and change standard file permissions

* `ls`, `ll` ... muestra los ficheros con sus permisos
* `chmod 755` pone los permisos a `-rwxr--r-x`
* `chmod u+rwx,g+wx,o-rx` da los permisos indicados y no modifica los no indicados
(es decir, el valor de lectura de grupo y el de escritura de otros se queda como estuvieran antes)
* `chmod a+rwx` da los permisos indicados a todo el mundo (`a` de `all`)

### Read, and use system documentation

* `man comando`
* `comando --help`
* `help comando`

http://www.tecmint.com/explore-linux-installed-help-documentation-and-tools/

### Manage access to the root account

* `sudo comando` ejecutar comando como root
* `sudo -u you comando` ejecuta el comando como el usuario you
* `su xxx` cambiar a usuario xxx (pide contraseña de xxx)
* `sudo su xxx` cambiar a usuario xxx (no pide contraseña)
* `sudo su -` cambiar a usuario root (el `-` simula que te logueas directamente, por ejemplo, en vez de dejarte en el directorio donde estas te llevara a la home de root)
* `visudo` edita `/etc/sudoers`
* `visudo -f /etc/sudoers.d/loqquesea` edita `/etc/sudoers.d/loqquesea`
(para que tenga efecto asegurarse de que la linea `includedir /etc/sudoers.d` de `/etc/sudoers` este descomentada)

En `/etc/sudoers` la cadena `ALL=(ALL:ALL) ALL` significa:

* `ALL=` En todos los host por si ponemos este mismo fichero en varias máquinas.
* `(ALL:ALL)` Puede escalar privilegios a cualquier usuario (primer ALL) y cualquier grupo (segundo ALL).
* `ALL` Puede ejecutar cualquier comando.

otros ejemplos:

* `ALL = NOPASSWD: ALL` no pide autenticarse al usar `sudo`
* `ALL = /bin/ls` solo puede usar `sudo` con `ls`

Más: [www.linuxtotal.com.mx](http://www.linuxtotal.com.mx/?cont=info_admon_014)
y [www.formandome.es](http://www.formandome.es/linux/configuracion-fichero-sudoers-en-ubuntu/)
http://www.tecmint.com/su-vs-sudo-and-how-to-configure-sudo-in-linux/

## Operation of Running Systems - 20%

### Boot, reboot, and shut down a system safely

* `sudo shutdown -h +1 "Power Failure imminent"` apagar en un minúto y avisar a los usarios con el mensaje "Power Failure imminent"
* `sudo shutdown -h now` = `halt` apaga ahora mismo
* `sudo shutdown -p now` = `poweroff` apaga ahora mismo
* `sudo shutdown -r now` = `reboot` reinicia ahora mismo

La diferencia entre `poweroff` y `halt` es que `halt` detiene el sistema
y `poweroff` detiene el sistema y lo apaga.

### Boot systems into different runlevels manually

Editamos la entrada de grub y en la linea de carga del kernel ponemos el número del runlevel en el que queremos iniciar

### Install, configure and troubleshoot the bootloader

`sudo grub-install /dev/sda` instala grub 2 en `/dev/sda`.
La configuración se hace modificando los ficheros de `/etc/grub.d` y
`/etc/default/grub`, ejecutando tras esto `update-grub` para que se
actualice el fichero `/boot/grub/grub.cfg` que no debemos tocar a mano.

Ejemplo 1 de reparación:

1. `sudo dd if=/dev/zero of=/dev/sda bs=446 count=1` eliminamos el MBR
2. Reinicamos y peta
3. Reinicamos con un live cd
4. `sudo mount /dev/sda1 /mnt` montamos el disco duro
5. Asociamos los directorios que grub necesita:
	* `sudo mount --bind /dev /mnt/dev`
	* `sudo mount --bind /dev/pts /mnt/dev/pts`
	* `sudo mount --bind /proc /mnt/proc`
	* `sudo mount --bind /sys /mnt/sys`
6. `sudo chroot /mnt` cambiamos el directorio /
7. `grub-install /dev/sda && grub-install --recheck /dev/sda && update-grub` instalamos grub
8. Desmontamos todo:
	* `exit`
	* `sudo umount /mnt/sys`
	* `sudo umount /mnt/proc`
	* `sudo umount /mnt/dev/pts`
	* `sudo umount /mnt/dev`
	* `sudo umount /mnt`
9. Reiniciamos y funciona

Ejemplo 2 de reparación:

1. `sudo rm /boot/grub/grub.cfg /etc/default/grub /etc/grub.d/*` eliminamos los ficheros de configuración
2. Reinicamos y peta
3. Reinicamos con un live cd
4. `sudo mount /dev/sda1 /mnt` montamos el disco duro
5. Asocciamos los directorios que necesitamos para tener internet:
	* `sudo mount --bind /dev /mnt/dev`
	* `sudo mount --bind /tmp /mnt/tmp`
	* `sudo mount --bind /proc /mnt/proc`
	* `sudo mount --bind /etc/resolv.conf /mnt/etc/resolv.conf`
6. Asociamos los directorios que grub necesita:
	* `sudo mount --bind /dev/pts /mnt/dev/pts`
	* `sudo mount --bind /sys /mnt/sys`
7. Recuperamos los archivos perdidos:
	* `sudo cp /etc/grub.d/* /mnt/etc/grub.d/`
	* `sudo cp /boot/grub/grub.cfg /mnt/boot/grub`
8. `sudo chroot /mnt` cambiamos el directorio /
9. `dpkg --get-selections | grep "grub"` consultamos que paquetes de grub estan instalados
10. `dpkg -V grub-common` comprobamos paquete a paquete cual es el que esta mal
11. `apt --reinstall install grub-common` reinstalamos el paquete roto
12. `update-grub` reconfiguramos grub
13. Desmontamos todo:
	* `exit`
	* `sudo umount /mnt/sys`
	* `sudo umount /mnt/proc`
	* `sudo umount /mnt/dev/pts`
	* `sudo umount /mnt/dev`
	* `sudo umount /mnt/tmp`
	* `sudo umount /mnt/etc/resolv.conf`
	* `sudo umount /mnt`
14. Reiniciamos y funciona

Más: [howtoubuntu.org](http://howtoubuntu.org/how-to-repair-restore-reinstall-grub-2-with-a-ubuntu-live-cd)
[lukeplant.me.uk](http://lukeplant.me.uk/blog/posts/sharing-internet-connection-to-chroot/)
[ubuntuforums.org](http://ubuntuforums.org/showthread.php?t=1467147)
[debian-handbook.info](https://debian-handbook.info/browse/es-ES/stable/sect.apt-get.html)
http://www.tecmint.com/configure-and-troubleshoot-grub-boot-loader-linux/

### Change the priority of a process

`nice` es lo opuesto a la prioridad: un proceso con `nice` -20 tienen
la máxima prioridad, y otro con `nice` 19 tienen la mínima prioridad.

* `nice -n 5 cat` o `nice -5 cat` ejecuta cat con un valor `nice` incrementado en 5 unidades.
* `nice cat` usa el valor 10 por defecto, por lo tanto es igual a `nice -n 10 cat` o `nice -10 cat`
* `nice` nos da el valor `nice` actual

```console
me@lub ~ $ nice
0
me@lub ~ $ nice bash
me@lub ~ $ nice
10
me@lub ~ $ nice -20 bash
me@lub ~ $ nice
19
me@lub ~ $ exit
exit
me@lub ~ $ nice
10
me@lub ~ $ exit
exit
me@lub ~ $ nice
0
me@lub ~ $ nice -3 cat &
[1] 1797
me@lub ~ $ ps -l
F S   UID   PID  PPID  C PRI  NI ADDR SZ WCHAN  TTY          TIME CMD
0 S  1000  1740  1739  0  80   0 -  2110 wait   pts/1    00:00:00 bash
0 T  1000  1797  1740  1  83   3 -  1369 signal pts/1    00:00:00 cat
0 R  1000  1798  1740  0  80   0 -  1569 -      pts/1    00:00:00 ps
```

`renice` cambia el valor nice de un proceso en ejecución.
Por defecto solo root puede disminuirlo, sin embargo editando
`/etc/security/limits.conf` se puede determinar por usuario unos limites
en los que dicho usuario si puede variar el valor `nice` de sus procesos.

```console
e@lub ~ $ cat &
[1] 1813
me@lub ~ $ renice -n 1 1813
1813 (ID de proceso) prioridad antigua 0, prioridad nueva 1
me@lub ~ $ renice -n 0 1813
renice: fallo al establecer la prioridad para 1813 (ID de proceso): Permiso denegado
me@lub ~ $ sudo renice -n 0 1813
1813 (ID de proceso) prioridad antigua 1, prioridad nueva 0
```

Añado la línea `me - nice -20` en `/etc/security/limits.conf`, salgo y
vuelvo a entrar con el usuario me

```console
me@lub ~ $ cat &
[1] 1872
me@lub ~ $ renice -n 1 1872
1872 (ID de proceso) prioridad antigua 0, prioridad nueva 1
me@lub ~ $ renice -n 0 1872
1872 (ID de proceso) prioridad antigua 1, prioridad nueva 0
```

http://www.tecmint.com/monitor-linux-processes-and-set-process-limits-per-user/

### Identify resource utilization by process

* `top` muestra la actividad de los procesos
* `ps` da información detallada de cada proceso
* `pstree` muestra un arbol de procesos y sus conexiones
* `strace` da información de las llamadas a sistema de un proceos

En `/proc` hay un directorio por cada proceso ( el cual se llama como
el PID de su proceso) donde aparece información sobre él.

```console
me@lub ~ $ cat &
[1] 2205
me@lub ~ $ cat /proc/2205/cmdline
cat
me@lub ~ $ cat /proc/2205/status
Name:	cat
State:	T (stopped)
Tgid:	2205
Ngid:	0
Pid:	2205
...
me@lub ~ $ realpath /proc/2205/cwd/
/home/me
```

En `/proc/PID/fd/1` se puede ver la salida estanadar de haberla.

http://www.tecmint.com/monitor-linux-processes-and-set-process-limits-per-user/

### Locate and analyze system log files

* `/var/log/` contine los logs
* `head` muestra el principio de un fichero
* `tail` muestra el final de un fichero (con la opción `-f` actualiza la salida según se incrementa el fichero)
* `dmesg` lista el buffer de mensajes del núcleo ( = `/var/log/dmesg`)
* `zcat`, `zgrep`, etc sirve para usarse con ficheros `.gz` como si fuera de texto plano
* `/var/log/cron` (`grep -i cron /var/log/syslog` si esta desactivad) para ver la actividad del `cron`
* `/var/log/boot.log` mensajes de arranque del sistema
* `last` da los accesos de cada usuario, `lastlog` da el último acceso de cada usuario y `lastb` los accesos fallidos
* `/var/log/messages` mensajes principales del sistema
* `/var/log/auth.log` información sobre el sistema de autorización de usuarios y permisos


Más: [www.securityartwork.es](http://www.securityartwork.es/2012/05/30/analisis-forense-en-sistemas-linux-obteniendo-informacion-parte-2/)

### Schedule tasks to run at a set date and time

* `/etc/crontab` y `/etc/cron.d/*` son ficheros crontab "multiusuario" (en cada linea se dice con que usuario se ejecuta la tarea)
* `/etc/cron.hourly/` y similares son ficheros ejecutables que lanzara root en los periodos que indican el nombre de la carpeta
* `contab -e` edita el fichero contrab del usuario

Ejemplo

```
# Cada hora en horario laboral
0 7-20 * * 1,2,3,4  /bin/bash ~/.owa/owa.sh
0 7-18 * * 5  /bin/bash ~/.owa/owa.sh
# Cada 4 horas fuera de horario laboral y entre semana
0 23,3 * * 1,2,3,4  /bin/bash ~/.owa/owa.sh
# Cada 8 horas en fin de semana
0 */8 * 6,7 /bin/bash ~/.owa/owa.sh

# Notificacion cada 2 o 3 horas entre semana de 7 a 20
0 7,9,11,14,17,20 * * 1,2,3,4,5  /bin/bash ~/.owa/notif.sh
# Notificacion cada 12 horas en fin de semana
0 */12 * 6,7 /bin/bash ~/.owa/notif.sh

@hourly /bin/bash /home/pi/wks/segundamano/run.sh
@weekly /bin/bash ~/wks/emvs/mail.sh
```

Más: [www.alcancelibre.org](http://www.alcancelibre.org/staticpages/index.php/configuracion-uso-crond)

### Verify completion of scheduled jobs

* `cron` manda un email a la dirección del campo `MAILTO` o al usuario
que ejecuta el comando
* La linea `EXTRA_OPTS="-L 0"` en `/etc/default/cron` define el nivel de log: 
siendo 0 nada de log, 1 log normal y 2 log detallado
* Si no sabemos en que log escribe lo podemos buscar con `sudo grep -icr CRON /var/log/* | grep -v :0`
* En `ubuntu` probablemente nos interese `/var/log/syslog`

Más: [bencane.com](http://bencane.com/2011/11/02/did-my-cronjob-run/)
[help.ubuntu.com](https://help.ubuntu.com/community/CronHowto#Troubleshooting_and_Common_Problems)

### Update software to provide required functionality and security

`sudo apt-get update` +:

* `sudo apt-get upgrade` actualiza todo lo que se pueda actualizar sin tener que resolver conflictos (nunca eliminara paquetes)
* `sudo apt-get dist-upgrade` actualiza intentando resolver conflictos si los hubiera (puede que elimine algún paquete)

Más: http://www.tecmint.com/linux-package-management/
http://www.tecmint.com/useful-basic-commands-of-apt-get-and-apt-cache-for-package-management/
http://www.tecmint.com/dpkg-command-examples/

### Verify the integrity and availability of resources

`dpkg -V` comprueba la integridad de todos los paquetes (o de alguno en concreto si se pasa como parametro).
Solo ofrece salida cuando ha habido alguna información que mostrar.

Los caracteres mostrados significan:

* .: prueba pasada
* ?: la prueba no se ha podido realizar
* S: el tamaño de archivo difiere
* M: los permisos del archivo y/o tipo difieren
* 5: el checksum MD5 difiere
* D: discrepancia entre los números mayor/menor
* L: discrepancia de ruta de enlace simbólico
* U: el usuario propietario difiere
* G: el grupo propietario difiere
* T: el tiempo de modificación difiere
* P: las capacidades difieren
* c: se trata de un fichero de configuración que ha sido modificado de forma legitima

Un mensaje no siempre es un error (por ejemplo, un fichero de configuración modificado).

*no tengo claro a que más se refiere*

### Verify the integrity and availability of key processes

* `mpstat` muestra el uso de los procesadores. Ejemplo: `mpstat -P ALL -u 2 3`
* `ps` da información detallada de cada proceso. Elmplo `ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%cpu`
* `kill` y `pkill` para matar procesos
* `pgrep` para buscar procesos al estilo de `pkill` pero sin matarlos
* `sar` da estadisticas del sistema

Más: [www.tecmint.com](http://www.tecmint.com/monitor-linux-processes-and-set-process-limits-per-user/)

### Change kernel runtime parameters, persistent and non-persistent

`/proc/sys` y `sysctl` muestran y permiten editar opciones del sistema

* `sysctl dev.cdrom.autoclose` = `cat /proc/sys/dev/cdrom/autoclose`
* `echo 0 > /proc/sys/net/ipv4/ip_forward` = `sysctl -w net.ipv4.ip_forward=0`
* Para que el cambio sea persistente añadir la linea `net.ipv4.ip_forward=0` en `/etc/sysctl.conf`
(o usar ficheros .conf en `/etc/sysctl.d`)
* `sysctl -p` aplica los valores de `/etc/sysctl.conf`

`sudo modprobe -a ip_tables` carga iptables de manera no persistente.
Para hacerlo persistente añadir una linea que diga `ip_tables` en el
fichero `/etc/modules`

http://www.tecmint.com/change-modify-linux-kernel-runtime-parameters/

### Use scripting to automate system maintenance tasks

* `shebang` es la primera linea de un script, la cual empieza por `#!`, 
que indica el interprete con que ejecutar dicho script. Ejemplo: `#!/bin/bash`
* `chmod 755 myscript.sh` para que el script sea ejecutable
* `$?` da el código de salida del último comando ejecutado (0 = OK)

http://www.tecmint.com/linux-basic-shell-scripting-and-linux-filesystem-troubleshooting/

### Manage the startup process and services

MBR:

* Backup `dd if=/dev/sda of=mbr.bkp bs=512 count=1`
* Restaurar `dd if=mbr.bkp of=/dev/sda bs=512 count=1`

GRUB:

* Editar `/etc/default/grub`
* Actualizar `update-grub`

SysVinit:

* Runleves de 0 a 5
* Runlevel por defecto en `/etc/inittab`
* Scripts ejecutacos en cada runlevel `ls /etc/rc*.d` (`S` de start y `K` de kill)
* Configurar con `chkconfig` o `sysv-rc-conf`
* `service [servicio] start|stop|status` arranca, para y muestra estado de un servicio

systemd:

* `systemctl` sin parametros lista los servicios y cia. (unidades)
* `systemctl status [unit]` muestra el estado de una unidad
* `systemctl start [unit]` arranca una unidad
* `systemctl stop [unit]` para una unidad
* `systemctl restart [unit]` reinicia una unidad
* `systemctl enable [unit]` deshabilita una unidad (se arrancara al inicio de sistema)
* `systemctl disable [unit]` habilita una unidad (no se arrancara al inicio del sistema)
* `systemctl is-enabled [unit]` muestra si esta habilitado para arrancar al inicio del sistema

Upstart:

* Ficheros de configuración (.conf) en `/etc/init`
* `initctl reload-configuration` recarga la configuración
* `sudo start [servicio]`  arranca un servicio

http://www.tecmint.com/linux-boot-process-and-manage-services/

### List and identify SELinux/AppArmor file and process contexts<br/>Configure and modify SELinux/AppArmor policies

AppArmor y SELinux no pueden estar arrancados a la vez.

**SELinux**:

Instalar SELinux con `sudo apt-get install policycoreutils selinux-utils auditd` 
y para habilitarlo ejecutar `sudo selinux-activate`

SELinux tiene tres modos:

* Disabled: no hace nada
* `setenforce 1` Enforcing: Deniega el acceso si no se cumplen las reglas
* `setenforce 0` Permissive: No deniega el acceso si no se cumplen las reglas, simplemente genera un log

`setenforce` no es persistente, para que el cambio sea permanente hay
que editar `/etc/selinux/config` poniendo por ejemplo `SELINUX=enforcing`

Los logs se pueden leer con `grep AVC /var/log/audit/audit.log`

SELinux usa tres concetos fundamentales:

* Contextos: Son etiquetas a archivos, procesos y puertos. Ejemplos de contextos son usuarios de SELinux, rol y tipo.
* Reglas: Describe el control de acceso en términos de contextos, procesos, archivos, puertos, usuarios, etc.
* Políticas: Son un conjunto de reglas que describen las decisiones de control de acceso aplicables a todo el sistema, las que deberían ser aplicadas por SELinux.

El parametro `Z` en `ps axZ` y `ls -Z` muestra los contextos.

`sudo semanage boolean -l` muestra los booleanos de las políticas y 
`setsebool` cambia dichos booleanos, por defecto de manera no persistente
y con el parametro `-P` de manera persistente.

```console
me@deb ~ $ getsebool ssh_chroot_rw_homedirs
ssh_chroot_rw_homedirs --> off
me@deb ~ $ sudo setsebool ssh_chroot_rw_homedirs on
me@deb ~ $ getsebool ssh_chroot_rw_homedirs
ssh_chroot_rw_homedirs --> on
```

Habilitar el puerto 9999 para ssh:

```console
me@deb ~ $ sudo semanage port -l | grep ssh
ssh_port_t               tcp       22
me@deb ~ $ sudo semanage port -m -t ssh_port_t -p tcp 9999
jboss_management_port_t  tcp       4712, 4447, 7600, 9123, 9990, 9999, 18001
me@deb ~ $ sudo semanage port -lC
SELinux Prot Type         Proto    Port Number

ssh_port_t                tcp      9999
me@deb ~ $ sudo semanage port -l | grep ssh
ssh_port_t                tcp      9999, 22
```

Habilitar DocumentRoot fuera de `/var/www/html/`:

```console
me@deb ~ $ sudo semanage fcontext -a -t httpd_sys_content_t "/websrv/sites/gabriel/public_html(/.*)?"
me@deb ~ $ sudo restorecon -R -v /websrv/sites/gabriel/public_html
```

**AppArmor**:

Instalar AppArmor con `sudo apt-get install apparmor apparmor-utils`

AppArmor se basa en perfiles y cada uno de ellos puede estar en dos estados:

* Enforcing: Deniega el acceso si no se cumplen las reglas
* Complain: No deniega el acceso si no se cumplen las reglas, simplemente genera un log

Para trabajar con los perfiles tenemos:

* `sudo apparmor_status` muestra el estado de AppArmor
* Los perfiles se guardan en `/etc/apparmor.d`
* Los perfiles con un enlace blando en `/etc/apparmor.d/disabled` estan deshabilitados
* Se pueden conseguir más perfiles con `sudo apt-get install apparmor-profiles`
* `sudo aa-complain /path/to/file` pasa un perfil a complain mode
* `sudo aa-enforce /path/to/file` pasa un perfil a enforce mode

Para deshabilitar AppArmor:

* `sudo systemctl stop apparmor.service` o
* `sudo update-rc.d -f apparmor remove`

editar `/etc/default/grub` para poner `apparmor=0` en `GRUB_CMDLINE_LINUX` 
y ejecutar `sudo update-grub`

http://www.tecmint.com/mandatory-access-control-with-selinux-or-apparmor-linux/
https://wiki.debian.org/SELinux/Notes
https://wiki.archlinux.org/index.php/AppArmor

### Install software from source

Ejemplo con pidgin:

```console
me@lub /tmp $ sudo apt-get install build-essential
...
me@lub /tmp $ wget http://downloads.sourceforge.net/project/pidgin/Pidgin/2.11.0/pidgin-2.11.0.tar.bz2
...
me@lub /tmp $ tar -xjvf pidgin-2.11.0.tar.bz2
me@lub /tmp $ cd pidgin-2.11.0/
me@lub /tmp/pidgin-2.11.0 $ ./configure 
...
checking whether NLS is requested... yes
./configure: line 14338: intltool-update: command not found
checking for intltool-update... no
checking for intltool-merge... no
checking for intltool-extract... no
configure: error: The intltool scripts were not found. Please install intltool.
me@lub /tmp/pidgin-2.11.0 $ sudo apt-get install intltool
...
me@lub /tmp/pidgin-2.11.0 $ ./configure
...
configure: error: 

You must have GLib 2.16.0 or newer development headers installed to build.

If you have these installed already you may need to install pkg-config so
I can find them.
me@lub /tmp/pidgin-2.11.0 $ sudo apt-get install pkg-config libglib2.0-dev libgtk2.0-dev libgtkspell-dev libavahi-client-dev libavahi-glib-dev libdbus-glib-1-dev libgstreamer0.10-dev tk8.4-dev tcl8.4-dev libperl-dev network-manager-dev libmeanwhile-dev libidn11-dev libnss3-dev
...
me@lub /tmp/pidgin-2.11.0 $ ./configure --disable-screensaver --disable-vv
...
Pidgin will be installed in /usr/local/bin.
configure complete, now type 'make'

me@lub /tmp/pidgin-2.11.0 $ sudo make
...
me@lub /tmp/pidgin-2.11.0 $ sudo make install
...
me@lub /tmp/pidgin-2.11.0 $ pidgin --version
Pidgin 2.11.0 (libpurple 2.10.9)

```

http://www.howtogeek.com/105413/how-to-compile-and-install-from-source-on-ubuntu/

## User and Group Management - 15%

### Create, delete, and modify local user accounts<br/>Create, delete, and modify local groups and group memberships

* `userad` para añadir un usuario
* `usermod` modifica un usuario
* `userdel` borrar usuario
* `groupdel` borrar grupo
* `groupadd` para añadir un grupo
* `gropmod` modifica un grupo

Por cada usuario y grupo se crea una linea en `/etc/passwd` y ` /etc/group` respectivamente

Ejemplos:

* `useradd -s /bin/csh -m -k /etc/skel -c "Bullwinkle J Moose" bmoose`
* `usermod --expiredate 2014-10-30 tecmint`
* `usermod --append --groups root,users tecmint`
* `usermod --home /tmp tecmint`
* `usermod --shell /bin/sh tecmint`
* `usermod --lock tecmint`
* `usermod --unlock tecmint`
* `chage -E 2014-09-11 isabelle`
* `sudo passwd kevin`
* `chage -l me`
* `useradd -m -s /bin/bash miusuario`
* `usermod -Ga sudo miusuario`

Sustituir la contraseña por `!` en `/etc/shadow` bloquea el usuario, el cual
podemos editar usando `sudo vipw`

http://www.tecmint.com/manage-users-and-groups-in-linux/

### Manage system-wide environment profiles

En `/etc/environment` vienen definidas variables que afectan a todo el sistema, 
como por ejemplo PATH

Otras variables de entorno:

* HOME = home del usuario actual
* USER = nick del usuario actual
* SHELL = shell actual
* PS1 = Define como se ve el prompt de la shell actual
* EDITOR = editor de texto preferido
* LD_LIBRARY_PATH = Directorios donde se encuentran las librerias
* ? = código de salida del último comando ejecutado

Escribir en la shell algo como `VARIABLE=valor` no crea una varible de entorno
si no una variable shell ya que solo afectara a la shell actual.
Para que esta varaible shell se convierta en una variable de entorno es necesario
exportarla.
Podemos usar `echo` para ver el contenido de una variable.


```console
me@lub ~ $ EDITOR=nano
me@lub ~ $ export EDITOR
me@lub ~ $ echo $EDITOR
nano
```

* `printenv` muestra todas las variables de entorno y su contenido.
* `env VAR=xxx programa`o `LANGUAGE=he FOO=bar gedit` ejecuta un programa modificando las variables de entorno
que va a usar.
* `unset VAR` elimina una variable
* `export -n VAR` "desexporta" una variable, es decir, deja de ser variable de entorno pero sigue siendo variable shell

Al se arranca la shell bash de un usuario procesa:

* `/etc/profile` para leer los valores definidos para todos los usuarios
* Adicionalmente `/etc/profile.d/*.sh` seran ejecutados en cualquier login
* `~/.bash_profile`, ~/.bash_login` y `~/.profile`, para leer los valores definidos para ese usuario en concreto

Otros ficheros a tener en cuenta:

`/etc/bash.bashrc` valido para programas ejecutados desde la shell, pero puede 
no surtir efecto con programas ejecutados desde el entorno gráfico-

Los comando ejecutados con `sudo` tienen sus propias variables de entorno, indicadas
en `/etc/sudoers`. Si se quiere que no se sobreescriba o pierda alguna variable
hay que editar dicho fichero para añadir una linea de este tipo:

```
Defaults env_keep += "http_proxy SOMEOTHERVARIABLES ANOTHERVARIABLE ETC"
```

https://wiki.debian.org/EnvironmentVariables
https://help.ubuntu.com/community/EnvironmentVariables

### Manage template user environment

*no tengo claro a que se refiere*

### Configure user resource limits

Podemos definir los limites por usuario en `/etc/security/limits.conf`

http://www.tecmint.com/monitor-linux-processes-and-set-process-limits-per-user/ -> Setting Resource Limits on a Per-User Basis in Linux

### Manage user processes

*creo que se repite con otros apartados sobre `ps`, `kill`, `nice`, etc*

### Configure PAM

Los ficheros de configuración estan en `/etc/pam.d/`.

Cada línea de uno de estos ficheros tiene la estructura:

```
type control module-path module-arguments
```

donde, `type` especifica el grupo de gestión al que el módulo estará asociado:

* auth: Le indica a la aplicación que debe pedir la identificación del usuario (nombre de usuario, contraseña, etc). Puede configurar las credenciales y otorgar privilegios.
* account: Verifica aspectos de la cuenta del usuario, tales como envejecimiento de la contraseña, control de acceso, etc.
* password: Es responsable de actualizar el token de autenticación del usuario, generalmente una contraseña.
* session: Se usa para proveer funciones antes y después de que se establece la sesión (tales como la configuración del ambiente, inicio de sesión, etc).

` control` controla cómo el éxito o fracaso de un módulo afecta el proceso general de autenticación:

* required: Debe devolver éxito para que el servicio se otorgue. Si es parte de un conjunto, el resto de módulos serán ejecutados. No se le informa a la aplicación qué módulo o módulos fallaron.
* requisite: Igual a required, con la excepción de que una falla en cualquier módulo termina el stack (conjunto de módulos) y devuelve un estado, el cual se envía a la aplicación.
* optional: El módulo no es requerido. Si este es el único módulo, el estado que se envía a la aplicación puede causar una falla.
* sufficient: Si este módulo termina con éxito no hay módulos subsecuentes a ser ejecutados. Si este falla, no causa una falla general en el resto de módulos, a menos de que sea el único módulo del stack.
* include: significa que las lineas dadas por el type deben ser leidas de otro archivo
substack: similar a includes pero los fallos o exitos del fichero incluido no provocan la salida del modulo, solo del substack.

http://www.tecmint.com/manage-users-and-groups-in-linux/ -> PAM (Pluggable Authentication Modules)

## Networking - 15%

### Configure networking and hostname resolution statically or dynamically

* Resolución de nombres estaticamente: `/etc/hosts
* Resolución de nombres dinamicamente: DNS

http://www.tecmint.com/setup-recursive-caching-dns-server-and-configure-dns-zones/

### Configure network services to start automatically at boot

`sysv-rc-conf` o `update-rc.d servicio defaults` p `chkconfig --level runlevel servicio on`

http://www.tecmint.com/installing-network-services-and-configuring-services-at-system-boot/

### Implement packet filtering<br/>Configure firewall settings

`firewalld` o `iptables`, pero no se debe usar los dos a la vez.

**iptables**

* Tiene la configuración en `/etc/iptables/rules.v*`
* `iptables -L` lista todas las reglas habitlitadas
* Las cadenas son: INPUT, OUTPUT, FORWARD
* Las politicas son: ACCEPT, DROP, REJECT
* `iptables -P FORWARD DROP` define la politica DROP para la cadena FORWARD, es decir, los paquetes que no cumplan ninguna regla de FORWARD se les aplicara la politica DROP
* `iptables -F INPUT` elimina todas las reglas de INPUT
* Añadir regla: `iptables -A cadena criterio -j politica`:
  

Ejemplo 1: Permitir entrada y salida de trafico web

```console
me@ubu ~ $ sudo iptables -A INPUT -i enp0s3 -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
me@ubu ~ $ sudo iptables -A OUTPUT -o enp0s3 -p tcp --sport 80 -m state --state ESTABLISHED -j ACCEPT
me@ubu ~ $ sudo iptables -A INPUT -i enp0s3 -p tcp --dport 443 -m state --state NEW,ESTABLISHED -j ACCEPT
me@ubu ~ $ sudo iptables -A OUTPUT -o enp0s3 -p tcp --sport 443 -m state --state ESTABLISHED -j ACCEPT
```

Ejemplo 2: Bloquear trafico entrante desde una red espeficica

DROP todo el trafico que venga desde 192.168.1.0/24:

```console
me@ubu ~ $ sudo iptables -I INPUT -s 192.168.1.0/24 -j DROP
```

DROP solo el trafico que venga de 192.168.1.0/24 por el puerto 22:

```console
me@ubu ~ $ iptables -A INPUT -s 192.168.1.0/24 --dport 22 -j ACCEPT
```

Ejemplo 3: Redirigir trafico entrate a otro destino

1. Editamos `/etc/sysctl.conf` para poner `net.ipv4.ip_forward = 1`
2. Refrescamos la configuración con `sysctl -p /etc/sysctl.conf`
3. Redirigimos el trafico entrante por el purto 631 a 192.168.0.10:631

```console
me@ubu ~ $ sudo iptables -t nat -A PREROUTING -i enp0s3 -p tcp --dport 631 -j DNAT --to 192.168.0.10:631
```

Ejemplo 4: Bloquear ping entrante

```console
me@ubu ~ $ sudo iptables -A INPUT --protocol icmp --in-interface eth0 -j DROP
```

Ejemplo 5: Deshabilitar/rehabilitar ssh logins desde dev2 a dev1

```console
me@ubu ~ $ sudo iptables -A OUTPUT --protocol tcp --destination-port 22 --out-interface eth0 --jump REJECT
```

Ejemplo 6: Permitir/prohibir a clientes NFS (de 192.168.0.0/24) motar unidades NFS4 compartidas

```console
me@ubu ~ $ sudo iptables -A INPUT -i eth0 -s 0/0 -p tcp --dport 2049 -j REJECT
me@ubu ~ $ sudo iptables -A INPUT -i eth0 -s 0/0 -p tcp --dport 111 -j REJECT
```

Otros ejemplos:

* Insertar en la posición 2 de INPUT: `iptables -I INPUT 2 -p tcp --dport 80 -j ACCEPT`
* BORRAR la regla 1 de INPUT: `iptables -D INPUT 1`
* Mostrar las reglas con número de linea: `iptables -nL -v --line-number`
* Remplaza la regla 2 de INPUT: `iptables -R INPUT 2 -i eth0 -s 0/0 -p tcp --dport 2049 -j REJECT`
* `iptables-save > /etc/iptables/rules.v4` guardar las reglas para que se cargen al reiniciar (si iptables-persistent esta instalado)
* Cargar manualmente las reglas guardadas `iptables-restore < /etc/iptables/rules.v4`

**FirewallD**

Tiene la configuración en `/usr/lib/firewalld/` y `/etc/firewalld/`.

`firewall-cmd --get-active-zones` nos da las zonas activas, es decir, las zonas a las que se les ha asociado "algo"

```console
me@deb ~ $ sudo firewall-cmd --get-active-zones 
me@deb ~ $ sudo firewall-cmd --zone=internal --change-interface=eth0
success
me@deb ~ $ sudo firewall-cmd --zone=external --change-interface=eth1
success
me@deb ~ $ sudo firewall-cmd --get-active-zones 
internal
  interfaces: eth0
external
  interfaces: eth1
me@deb ~ $ sudo firewall-cmd --zone=internal --remove-interface=eth0
success
me@deb ~ $ sudo firewall-cmd --zone=external --remove-interface=eth1
success
me@deb ~ $ sudo firewall-cmd --get-active-zones
me@deb ~ $
```

Ejemplo 1: Permitir servicios a traves del firewall

```console
me@ubu ~ $ sudo firewall-cmd --get-services
...
me@ubu ~ $ sudo firewall-cmd --zone=MyZone --add-service=http
me@ubu ~ $ sudo firewall-cmd --zone=MyZone --permanent --add-service=http
me@ubu ~ $ sudo firewall-cmd --zone=MyZone --add-service=https
me@ubu ~ $ sudo firewall-cmd --zone=MyZone --permanent --add-service=https
me@ubu ~ $ sudo firewall-cmd --reload
```

Ejemplo 2: Redirigir IP/Puerto

```console
me@ubu ~ $ sudo firewall-cmd --zone=MyZone --query-masquerade
no
me@ubu ~ $ sudo firewall-cmd --zone=MyZone --add-masquerade
me@ubu ~ $ sudo firewall-cmd --zone=MyZone --add-forward-port=port=631:proto=tcp:toport=631:toaddr=192.168.0.10
me@ubu ~ $ sudo firewall-cmd --reload
```

http://www.tecmint.com/configure-iptables-firewall/
http://www.tecmint.com/firewalld-vs-iptables-and-control-network-traffic-in-firewall/

### Start, stop, and check the status of network services

* `sudo netstat -atup | grep LISTEN` ver network services arrancados
* `sudo service servicio (start | stop | status)`
* `sudo systemctl (start | stop | status) servicio`

### Statically route IP traffic

El comando básico es `ip objeto comando` donde el objeto puede ser:

* link: dispositivo network
* addr: dirección del dispositivo (IP o IPv6)
* route: entrada en la tabla de ruta
* rule: regla de la base de datos de politicas de rutas

y el comando es uno de los que podemos ver, por ejemplo, haciendo `ip link help`

Ejemplos:

```console
root@lub:~# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default 
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:06:7e:79 brd ff:ff:ff:ff:ff:ff
root@lub:~# ip link set eth0 down
root@lub:~# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default 
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc pfifo_fast state DOWN mode DEFAULT group default qlen 1000
    link/ether 08:00:27:06:7e:79 brd ff:ff:ff:ff:ff:ff
root@lub:~# ip link set eth0 up
root@lub:~# ip link show eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:06:7e:79 brd ff:ff:ff:ff:ff:ff

```

Ejemplo 1: Rutear paquetes de una red privada a otra

Cliente 1: CentOS 7 enp0s3: 192.168.0.17/24
Router: Debian Wheezy 7.7 eth0: 192.168.0.15/24, eth1: 10.0.0.15/24
Cliente 2: openSUSE 13.2 enp0s3: 10.0.0.18/24

```console
root@rtr:~# echo 1 > /proc/sys/net/ipv4/ip_forward
```

```console
root@cl1:~# ip route add 10.0.0.0/24 via 192.168.0.15 dev enp0s3
root@cl1:~# ping 10.0.0.18
```

```console
root@cl2:~# ip route add 192.168.0.0/24 via 10.0.0.15 dev enp0s3
root@cl2:~# ping 192.168.0.17
```

En openSUSE `/etc/sysconfig/network-scripts/ifcfg-enp0s3`:

```
BOOTPROTO=static
BROADCAST=10.0.0.255
IPADDR=10.0.0.18
NETMASK=255.255.255.0
GATEWAY=10.0.0.15
NAME=enp0s3
NETWORK=10.0.0.0
ONBOOT=yes
```

Ejemplo 1: Enrutar paquetes entre red interna e internet

Router: Debian Wheezy 7.7 eth0: Public IP, eth1: 10.0.0.15/24
Client: openSUSE 13.2 enp0s3: 10.0.0.18/24

```console
root@cl1:~# iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
root@cl1:~# iptables -A FORWARD -i eth0 -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT
root@cl1:~# iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
```

http://www.tecmint.com/setup-linux-as-router/

### Dynamically route IP traffic

`quagga` sirve para ruteo dinamico.

Router: Debian Wheezy 7.7 eth0: Public IP, router getaway 192.168.0.1, eth1: 10.0.0.15/24  
Client: openSUSE 13.2 enp0s3: 10.0.0.18/24

En `/etc/quagga/daemons`:

```
zebra=1
ripd=1
```

Crear ficheros de configuración

``console
root@rtr:~# touch /etc/quagga/zebra.conf
root@rtr:~# touch /etc/quagga/ripd.conf
root@rtr:~# chown quagga:quaggavty /etc/quagga/*.conf
root@rtr:~# chmod 640 /etc/quagga/*.conf 
```

Rellenarlos con:

``
service quagga restart
hostname    	usuario
password    	contraseña
```

Ejecutamos `service quagga restart`

Teniendo dos maquinas:  
dev2: 192.168.0.15, 10.0.0.15  
dev3: 192.168.1.1,  10.0.0.16  

En cada una de ellas:

Conectamos a zebra:

```console
root@dev2:~# telnet localhost 2601
...
DebianRouter> enable
DebianRouter# configure terminal
DebianRouter(config)# inter eth0
DebianRouter(config-if)# ip addr 192.168.0.15/24
DebianRouter(config-if)# inter eth1
DebianRouter(config-if)# ip addr 10.0.0.15/24
DebianRouter(config-if)# exit
DebianRouter(config)# exit
DebianRouter# write
Configuration saved to /etc/quagga/zebra.conf
```

Conectamos a RIP:

```console
root@dev2:~# telnet localhost 2602
...
DebianRouter> enable
DebianRouter# configure terminal
DebianRouter(config)# router rip
DebianRouter(config-router)# version 2
DebianRouter(config-router)# network 192.168.0.0/24
There is a same network configuration 192.168.0.0/24
DebianRouter(config-router)# network 10.0.0.0/24
DebianRouter(config-router)# exit
DebianRouter(config)# exit
DebianRouter# write
Configuration saved to /etc/quagga/rip.conf
```

Al volver a conectar a zebra veremos que los routers han aprendido la ruta de una a otro

```console
root@dev2:~# telnet localhost 2601
...
dev2> show ip route
Codes: K - kernel route, C - connected, S - static, R - RIP
       O - OSPF, I - IS-IS, B - BGP, A - Babel,
       > - selected route, * - FIB route

K>* 0.0.0.0/0 via 192.168.0.1, eth0
C>* 10.0.0.0/24 is directly connected, eth1
C>* 127.0.0.0/8 is directly connected, lo
C>* 192.168.0.0/24 is directly connected, eth0
R>* 192.168.1.10/24 [120/2] via 10.0.0.16, eth1, 00:00:20
```

```console
root@dev3:~# telnet localhost 2601
...
dev2> show ip route
Codes: K - kernel route, C - connected, S - static, R - RIP
       O - OSPF, I - IS-IS, B - BGP, A - Babel,
       > - selected route, * - FIB route

K>* 0.0.0.0/0 via 10.0.0.15, eth0
C>* 10.0.0.0/24 is directly connected, eth0
C>* 127.0.0.0/8 is directly connected, lo
K>* 169.254.0.0/16 is directly connected eth1
C>* 192.168.0.0/24 [120/2] via 10.0.0.15, eth0, 00:36:09
R>* 192.168.1.10/24 is directly connected eth1
```

http://www.tecmint.com/setup-linux-as-router/

### Synchronize time using other network peers

```console
me@deb ~ $ sudo apt-get install ntp ntpdate
...
me@deb ~ $ sudo service ntp status
● ntp.service - LSB: Start NTP daemon
   Loaded: loaded (/etc/init.d/ntp)
   Active: active (running) since dom 2016-07-17 13:48:50 CEST; 26s ago
   CGroup: /system.slice/ntp.service
           └─4357 /usr/sbin/ntpd -p /var/run/ntpd.pid -g -u 121:130
...
me@deb ~ $ sudo ntpq -p
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
+static-21.herco 158.227.98.15    2 u   21   64    1  181.480   66.936  42.859
*i2t15.i2t.ehu.e .GPS.            1 u   20   64    1  160.858   70.449  39.383
+ntp.redimadrid. 193.147.107.33   2 u   21   64    1  131.977   63.068  32.831
 masip.celingest .STEP.          16 u  726   64    0    0.000    0.000   0.000
```

* La configuración esta en `/etc/ntp.conf`
* Los logs se pueden ver con `grep ntp /var/log/syslog`
* Las opciones con las que se arranca el demonio `ntpd` estan en `/etc/default/ntp`

Sin necesidad de tener `ntpd` se puede actualizar la feca con `ntpdate pool.ntp.org` (añadir -u si se tiene isntalado `ntpd`)

http://www.tecmint.com/how-to-synchronize-time-with-ntp-server-in-ubuntu-linux-mint-xubuntu-debian/  
http://www.tecmint.com/install-and-configure-ntp-server-client-in-debian/
http://www.pool.ntp.org/es/use.html

## Service Configuration - 10%

### Configure a basic DNS server<br/>Maintain a DNS zone

```console
me@lub ~ $ sudo apt-get install bind9 bind9utils
...
me@lub ~ $ sudo cp /etc/bind/named.conf.options /etc/bind/named.conf.options.orig
me@lub ~ $ sudo cp /etc/bind/named.conf.local /etc/bind/named.conf.local.orig
```

Siendo 10.13.13.101 la ip en la red que comparte con otras máquinas, editamos `/etc/bind/named.conf.options`:

```
options {
..
  listen-on port 53 { 127.0.0.1; 10.13.13.101;};
  allow-query 	{ localhost; 10.13.13.0/24; };
  recursion yes;
  forwarders {
    8.8.8.8;
    8.8.4.4;
  };
...
}
```

Luego editamos `/etc/bind/named.conf.local`:

```
  zone "sales.me.com." IN {
    type master;
    file "/var/named/sales.me.com.zone";
  };
  zone "13.13.10.in-addr.arpa" IN {
    type master;
    file "/var/named/13.13.10.in-addr.arpa.zone";
  };
```

Chekeamos errores con `sudo named-checkconf /etc/bind/named.conf`

Siendo `/var/named/sales.me.com.zone`:

```
$TTL    604800
@       IN      SOA     sales.me.com. root.sales.me.com. (
2016051101 ; Serial
10800 ; Refresh
3600  ; Retry
604800 ; Expire
604800) ; Negative TTL
;
@       IN      NS      dns.sales.me.com.
dns     IN      A       10.13.13.101
web1    IN      A       10.13.13.104
www.web1        IN      CNAME   web1
```

y `/var/named/13.13.10.in-addr.arpa.zone`:

```
$TTL    604800
@       IN      SOA     sales.me.com. root.sales.me.com. (
2016051101 ; Serial
10800 ; Refresh
3600  ; Retry
604800 ; Expire
604800) ; Minimun TTL
;
@       IN      NS      dns.sales.me.com.
104     IN      PTR     web1.sales.me.com.
```

Chequeamos los ficheros

```
me@lub ~ $ sudo named-checkzone sales.me.com /var/named/sales.me.com.zone
zone sales.me.com/IN: loaded serial 2016051101
OK
me@lub ~ $ sudo named-checkzone 0.168.192.in-addr.arpa /var/named/13.13.10.in-addr.arpa.zone 
zone 0.168.192.in-addr.arpa/IN: loaded serial 2016051101
OK
```

Reiniciamos el servicio con `sudo service bind9 restart`

Editamos `/etc/network/interfaces` para añadir la linea `dns-nameservers 10.13.13.101`

```
auto eth1
iface eth1 inet dhcp
dns-nameservers 10.13.13.101
```

Reiniciamos la red con `sudo restart network-manager` (en realidad tuve que reiniciar), 
y comprobamos que funciona

```
me@lub ~ $ host web1.sales.me.com
web1.sales.me.com has address 10.13.13.104
me@lub ~ $ host 10.13.13.104
104.13.13.10.in-addr.arpa domain name pointer web1.sales.me.com.
me@lub ~ $ host www.web1.sales.me.com
www.web1.sales.me.com is an alias for web1.sales.me.com.
web1.sales.me.com has address 10.13.13.104
```

http://www.tecmint.com/setup-recursive-caching-dns-server-and-configure-dns-zones/ -> Installing and Configuring a DNS Server

### Configure an FTP server<br/>Configure anonymous-only download on FTP servers

Instalamos con `sudo apt-get install vsftpd ftp`.  
La configuración esta en `/etc/vsftpd.conf`, el cual editamos para habilitar
el acceso anonimo de solo lectura

```
anonymous_enable=YES
no_anon_password=YES
anon_root=/var/ftp/
write_enable=NO
anon_max_rate=10240
max_per_ip=5
```

```console
me@lub ~ $ sudo mkdir /var/ftp
me@lub ~ $ sudo chmod 555 /var/ftp
me@lub ~ $ man -t vsftpd.conf | sudo ps2pdf - /var/ftp/vstpd.conf.pdf
me@lub ~ $ sudo service vsftpd restart
vsftpd stop/waiting
vsftpd start/running, process 4188
me@lub ~ $ ftp localhost
Connected to localhost.
220 (vsFTPd 3.0.2)
Name (localhost:me): anonymous
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-rw-rw-    1 0        0           39599 Jul 17 20:35 vstpd.conf.pdf
226 Directory send OK.
ftp> get vstpd.conf.pdf
local: vstpd.conf.pdf remote: vstpd.conf.pdf
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for vstpd.conf.pdf (39599 bytes).
226 Transfer complete.
39599 bytes received in 0.01 secs (2598.2 kB/s)
ftp> exit
221 Goodbye.
me@lub ~ $ ls vstpd.conf.pdf 
vstpd.conf.pdf
```

Si en vez de eso queremos dar acceso a home a los usuarios del sistema haremos:

```
anonymous_enable=NO
local_enable=YES
chroot_local_user=YES
chroot_list_enable=YES
chroot_list_file=/etc/vsftpd.chroot_list
local_max_rate=20480
max_per_ip=5
```

Donde `/etc/vsftpd.chroot_list` es un fichero donde estan los nombres de los usuarios que queremos que si puedan salir de su home, por lo tanto en principio estará vacio.  
Y si se usa SELinux ejecutar `setsebool -P ftp_home_dir 1`

Podemos añadir la linea `allow_writeable_chroot=YES` a la configuración para que
no nos de problemas del tipo `500 OOPS: vsftpd: refusing to run with writable root inside chroot()`

```console
me@lub ~ $ sudo touch ../walterwhite/walterwhite.txt
me@lub ~ $ ftp localhost
Connected to localhost.
220 (vsFTPd 3.0.2)
Name (localhost:me): walterwhite
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0               0 Jul 17 21:02 walterwhite.txt
226 Directory send OK.
ftp> get walterwhite.txt
local: walterwhite.txt remote: walterwhite.txt
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for walterwhite.txt (0 bytes).
226 Transfer complete.
ftp> quit
221 Goodbye.
me@lub ~ $ ls walterwhite.txt 
walterwhite.txt
```

http://www.tecmint.com/setup-ftp-anonymous-logins-in-linux/
https://www.benscobie.com/fixing-500-oops-vsftpd-refusing-to-run-with-writable-root-inside-chroot/

### Provide/configure network shares via NFS

En el servidor:

```console
me@ubu ~ $ sudo apt-get install nfs-common nfs-kernel-server
me@ubu ~ $ mkdir nfsshare
me@ubu ~ $ sudo bash -c 'echo "/home/me/nfsshare 10.13.13.101(rw,sync,no_root_squash)" >> /etc/exports'
me@ubu ~ $ sudo service nfs-kernel-server start
```

En el cliente:

```console
me@lub ~ $ sudo apt-get install nfs-common
me@lub ~ $ showmount -e 10.13.13.102
Export list for 10.13.13.102:
/home/me/nfsshare 10.13.13.101
me@lub ~ $ sudo mkdir /mnt/nfsshare
me@lub ~ $ sudo mount -t nfs 10.13.13.102:/home/me/nfsshare /mnt/nfsshare
me@lub ~ $ sudo bash -c 'echo "10.13.13.102:/home/me/nfsshare /mnt/nfsshare  nfs defaults 0 0" >> /etc/fstab'
```


http://www.tecmint.com/mount-filesystem-in-linux/ -> Mounting a NFS share on Linux
https://help.ubuntu.com/community/SettingUpNFSHowTo

### Provide/configure network shares via CIFS

En el servidor:

```console
me@ubu ~ $ sudo apt-get install samba-client samba-common cifs-utils
me@ubu ~ $ sudo nano /etc/samba/smb.conf
[share]
    comment = Ubuntu File Server Share
    path = /home/me/smb    
    browsable = yes
    guest ok = yes
    read only = no
    create mask = 0755
me@ubu ~ $ mkdir smb
me@ubu ~ $ sudo chown nobody:nogroup smb
me@ubu ~ $ sudo service smbd restart
smbd stop/waiting
smbd start/running, process 4978
me@ubu ~ $ sudo service nmbd restart
nmbd stop/waiting
nmbd start/running, process 5015
```

En el cliente

```console
me@lub ~ $ sudo apt-get install samba-client samba-common cifs-utils
me@lub ~ $ smbclient -L 10.13.13.102
me@lub ~ $ smbclient -L 10.13.13.102
WARNING: The "syslog" option is deprecated
Enter me's password: 
Domain=[WORKGROUP] OS=[Windows 6.1] Server=[Samba 4.3.8-Ubuntu]

	Sharename       Type      Comment
	---------       ----      -------
	print$          Disk      Printer Drivers
	share           Disk      Ubuntu File Server Share
	IPC$            IPC       IPC Service (ubu server (Samba, Ubuntu))
Domain=[WORKGROUP] OS=[Windows 6.1] Server=[Samba 4.3.8-Ubuntu]

	Server               Comment
	---------            -------
	UBU                  ubu server (Samba, Ubuntu)

	Workgroup            Master
	---------            -------
	WORKGROUP            
me@lub ~ $ sudo mkdir /mnt/samba
me@lub ~ $ sudo chown me:me /mnt/samba
me@lub ~ $ echo "username=samba_username" > /mnt/samba/.smbcredentials
me@lub ~ $ echo "password=samba_password" >> /mnt/samba/.smbcredential
me@lub ~ $ chmod 600 /mnt/samba/.smbcredentials
me@lub ~ $ sudo bash -c 'echo "//10.13.13.102/share /mnt/samba cifs credentials=/mnt/samba/.smbcredentials,defaults 0 0" >> /etc/fstab'
me@lub ~ $ sudo mount //10.13.13.102/share
```

http://www.tecmint.com/mount-filesystem-in-linux/ -> Mounting a Samba share on Linux
https://help.ubuntu.com/12.04/serverguide/samba-fileserver.html

### Configure email aliases

* `/etc/aliases` + `newaliases`, o
* `/etc/postfix/aliases` + `postalias /etc/postfix/aliases`

La 1º opción si me funciono, la seguna no.

### Configure SSH servers and clients<br/>Configure SSH-based remote access using public/private key pairs

* `/etc/ssh/sshd_config` condigura sshd
* `/etc/default/ssh` permite añadir parametros para el arranque de sshd
* `ssh-keygen` genera una clave privada y pública para usar con ssh
* `~/.ssh/authorized_keys` tiene las claves publicas autorizadas
* `ssh-copy-id` manda una clave publica a la maquina a la que queremos conectar
* `~/.ssh/config` configura las conexiones ssh.

```console
me@lub ~ $ mkdir .ssh
me@lub ~ $ touch .ssh/config
me@lub ~ $ chmod 700 .ssh
me@lub ~ $ chmod 600 ~/.ssh/*
me@lub ~ $ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/me/.ssh/id_rsa): /home/me/.ssh/ubuntu
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/me/.ssh/ubuntu.
Your public key has been saved in /home/me/.ssh/ubuntu.pub.
The key fingerprint is:
1e:10:a5:fd:d4:e4:91:0e:63:49:7d:db:b0:bf:81:94 me@lub
The key's randomart image is:
+--[ RSA 2048]----+
|      .....oo.   |
|       +  =+o.o  |
|      o ...+o..= |
|       . o  .Eo .|
|        S . . .. |
|       . .   . ..|
|        .       o|
|               . |
|                 |
+-----------------+
me@lub ~ $ ssh-copy-id -i .ssh/ubuntu.pub me@10.13.13.102
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
me@10.13.13.102's password: 

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'me@10.13.13.102'"
and check to make sure that only the key(s) you wanted were added.

me@lub ~ $ nano .ssh/config
Host ubuntu
HostName 10.13.13.102
IdentityFile /home/me/.ssh/ubuntu
User me
Port 22
me@lub ~ $ ssh ubuntu
Enter passphrase for key '/home/me/.ssh/ubuntu': 
Welcome to Ubuntu 14.04.4 LTS (GNU/Linux 4.2.0-27-generic i686)
Last login: Mon Jul 18 20:49:36 2016 from 10.13.13.101
me@ubu ~ $ ls .ssh
authorized_keys
me@ubu ~ $ exit
me@lub ~ $ eval "$(ssh-agent -s)"
Agent pid 4986
me@lub ~ $ ssh-add ~/.ssh/ubuntu
me@lub ~ $ ssh-add ~/.ssh/ubuntu
Enter passphrase for /home/me/.ssh/ubuntu: 
Identity added: /home/me/.ssh/ubuntu (/home/me/.ssh/ubuntu)
me@lub ~ $ ssh ubuntu
Welcome to Ubuntu 14.04.4 LTS (GNU/Linux 4.2.0-27-generic i686)
Last login: Mon Jul 18 22:14:01 2016 from 10.13.13.101
me@ubu ~ $ exit

```

### Restrict access to the HTTP proxy server

`sudo apt-get install install squid3 squidguard`

http://www.tecmint.com/onfigure-squid-server-in-linux
http://www.tecmint.com/configure-squidguard-for-squid-proxy/

### Configure an IMAP and IMAPS service

http://www.tecmint.com/setting-up-email-services-smtp-and-restricting-access-to-smtp/

### Query and modify the behavior of system services at various run levels

*no tengo claro a que se refiere*

### Configure an HTTP server<br/>Configure HTTP server log files

http://www.tecmint.com/setup-apache-with-name-based-virtual-hosting-with-ssl-certificate/

### Restrict access to a web page

http://www.tecmint.com/apache-htaccess-tricks
https://www.cs.cmu.edu/~help/web_publishing/htaccess.html

### Diagnose routine SELinux/AppArmor policy violations



### Configure database server

* Instalamos con `sudo apt-get install mariadb-server`
* Nos conectamos con `mysql -u root -p`
* Securizamos con `mysql_secure_installation`
* Configuramos editando `/etc/mysql/my.cnf`, `/etc/my.cnf`, `~/.my.cnf`
* Reiniciamos con `sudo service mysql restart`

http://www.tecmint.com/install-mariadb-in-linux/
http://www.tecmint.com/install-secure-performance-tuning-mariadb-database-server/

## Virtualization - 5%

### Configure a hypervisor to host virtual guests

http://www.tecmint.com/install-and-configure-kvm-in-linux/
https://help.ubuntu.com/community/KVM/Installation

### Access a VM console
### Configure systems to launch virtual machines at boot
### Evaluate memory usage of virtual machines
### Resize RAM or storage of VMs

## Storage Management - 10%

### List, create, delete, and modify storage partitions

* `fdisk` crea, lista, borra y modifica particiones
* `mkfs` y derivados formatean particiones
* `mkswap` formatea particiones swap (se recomienda que sean del doble de la memoria ran si esta es menor de 2GB, e igual en caso contrario)
* ´/etc/fstab´ tiene la información necesaria para que estas particiones se carguen al reiniciar.

http://www.tecmint.com/create-partitions-and-filesystems-in-linux/

### Create, modify and delete Logical Volumes<br/>Extend existing Logical Volumes and filesystems<br/>Add new partitions, and logical volumes

Uno o más disco (`/dev/sdb`) o una o más particiones te tipo 8e (`/dev/sdb1`)
forman un volumen fisico, los cuales se agrupan en grupos de volumenes (`vg`), 
el cual se divide en uno o varios volumenes lógicos (`mylvm`)

```console
me@lub ~ $ sudo pvcreate /dev/sdb1
me@lub ~ $ sudo pvcreate /dev/sdc1
me@lub ~ $ sudo vgcreate -s 16M vg /dev/sdb1
me@lub ~ $ sudo vgextend vg /dev/sdc1
me@lub ~ $ sudo lvcreate -L 50G -n mylvm vg
me@lub ~ $ sudo mkfs -t ext4 /dev/vg/mylvm
me@lub ~ $ mkdir /mylvm
me@lub ~ $ sudo mount /dev/vg/mylvm /mylvm
```

Mostrar información:

* Volumnes fisicos: `pvs`, `pvsdisplay` o `pvsdisplay /dev/sdX`
* Grupos de volumenes: `vgs`, `vgdisplay` o `vgdisplay /dev/vg00`
* Volumnes lógicos: `lvs`, `lvdisplay` o `lvdisplay /dev/vg00/mylvm`

Crear movidas:

* Volumnes fisicos: `ppvcreate /dev/sdX`
* Grupos de volumenes: `vgcreate vg00 /dev/sdb /dev/sdc`
* Volumnes lógicos:
  * `lvcreate -n vol_projects -L 10G vg00`
  * `lvcreate -n vol_backups -l 100%FREE vg00`
  * `lvcreate -l 128 -s -n mysnap /dev/vg/mylvm`

Extender volumen lógico:

```console
me@lub ~ $ sudo lvextend -L +500M /dev/vg/mylvm
me@lub ~ $ sudo resize2fs /dev/vg/mylvm
```

Reducir un grupo de volumenes:

```console
me@lub ~ $ sudo pvdisplay 
  --- Physical volume ---
  PV Name               /dev/sdf
  VG Name               vg00
  PV Size               10,00 MiB / not usable 2,00 MiB
  Allocatable           yes (but full)
  PE Size               4,00 MiB
  Total PE              2
  Free PE               0
  Allocated PE          2
  PV UUID               aZnPnF-QFFg-M1Wb-wvLq-9Ku1-dWB3-2zY4c7
   
  --- Physical volume ---
  PV Name               /dev/sdh
  VG Name               vg00
  PV Size               10,00 MiB / not usable 2,00 MiB
  Allocatable           yes (but full)
  PE Size               4,00 MiB
  Total PE              2
  Free PE               0
  Allocated PE          2
  PV UUID               uWEcvk-n2DU-6Nbq-RfUy-4fe8-1Ofo-BeDUDu
   
  --- Physical volume ---
  PV Name               /dev/sdg
  VG Name               vg00
  PV Size               10,00 MiB / not usable 2,00 MiB
  Allocatable           yes 
  PE Size               4,00 MiB
  Total PE              2
  Free PE               1
  Allocated PE          1
  PV UUID               DdPUP0-nYAz-aKzz-vhpo-Rtt1-el3C-kz53AM
me@lub ~ $ sudo pvcreate /dev/sdk
  Physical volume "/dev/sdk" successfully created
me@lub ~ $ sudo vgextend vg00 /dev/sdk
  Volume group "vg00" successfully extended
me@lub ~ $ sudo pvmove /dev/sdg --alloc anywhere
  /dev/sdg: Moved: 100,0%
me@lub ~ $ sudo vgreduce vg00 /dev/sdg
  Removed "/dev/sdg" from volume group "vg00"
me@lub ~ $ sudo vgdisplay 
  --- Volume group ---
  VG Name               vg00
  System ID             
  Format                lvm2
  Metadata Areas        3
  Metadata Sequence No  29
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                2
  Open LV               2
  Max PV                0
  Cur PV                3
  Act PV                3
  VG Size               112,00 MiB
  PE Size               4,00 MiB
  Total PE              28
  Alloc PE / Size       5 / 20,00 MiB
  Free  PE / Size       23 / 92,00 MiB
  VG UUID               TndQtC-yVoV-ati9-Y76w-UApW-jGb5-o6vYJk
   
me@lub ~ $ sudo pvdisplay 
  --- Physical volume ---
  PV Name               /dev/sdf
  VG Name               vg00
  PV Size               10,00 MiB / not usable 2,00 MiB
  Allocatable           yes (but full)
  PE Size               4,00 MiB
  Total PE              2
  Free PE               0
  Allocated PE          2
  PV UUID               aZnPnF-QFFg-M1Wb-wvLq-9Ku1-dWB3-2zY4c7
   
  --- Physical volume ---
  PV Name               /dev/sdh
  VG Name               vg00
  PV Size               10,00 MiB / not usable 2,00 MiB
  Allocatable           yes (but full)
  PE Size               4,00 MiB
  Total PE              2
  Free PE               0
  Allocated PE          2
  PV UUID               uWEcvk-n2DU-6Nbq-RfUy-4fe8-1Ofo-BeDUDu
   
  --- Physical volume ---
  PV Name               /dev/sdk
  VG Name               vg00
  PV Size               100,00 MiB / not usable 4,00 MiB
  Allocatable           yes 
  PE Size               4,00 MiB
  Total PE              24
  Free PE               23
  Allocated PE          1
  PV UUID               wUahgs-13gr-gNhq-qVmG-lrJV-Yfsy-3PMwWG
   
  "/dev/sdg" is a new physical volume of "10,00 MiB"
  --- NEW Physical volume ---
  PV Name               /dev/sdg
  VG Name               
  PV Size               10,00 MiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               DdPUP0-nYAz-aKzz-vhpo-Rtt1-el3C-kz53AM
```

Extender volumen logico

```console
me@lub ~ $ sudo lvextend -r -L +50M /dev/vg00/vol_dos
  Rounding size to boundary between physical extents: 52,00 MiB
  Extending logical volume vol_dos to 68,00 MiB
  Logical volume vol_dos successfully resized
resize2fs 1.42.9 (4-Feb-2014)
Filesystem at /dev/mapper/vg00-vol_dos is mounted on /home/me/vol_dos; on-line resizing required
old_desc_blocks = 1, new_desc_blocks = 1
The filesystem on /dev/mapper/vg00-vol_dos is now 69632 blocks long.
me@lub ~ $ sudo lvdisplay 
  --- Logical volume ---
  LV Path                /dev/vg00/vol_uno
  LV Name                vol_uno
  VG Name                vg00
  LV UUID                kgAVDg-II7h-MoRM-394R-ZFox-ti7r-vhYCbb
  LV Write Access        read/write
  LV Creation host, time lub, 2016-05-22 20:51:21 +0200
  LV Status              available
  # open                 1
  LV Size                8,00 MiB
  Current LE             2
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           252:0
   
  --- Logical volume ---
  LV Path                /dev/vg00/vol_dos
  LV Name                vol_dos
  VG Name                vg00
  LV UUID                ltBKDO-11vk-2oNN-rj1w-0RNa-ptYo-pi6FUe
  LV Write Access        read/write
  LV Creation host, time lub, 2016-05-22 20:51:35 +0200
  LV Status              available
  # open                 1
  LV Size                68,00 MiB
  Current LE             17
  Segments               3
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           252:1
```

Reducir volumen logico

```console
me@lub ~ $ sudo lvreduce -r -L -50M /dev/vg00/vol_dos
  Rounding size to boundary between physical extents: 48,00 MiB
Do you want to unmount "/home/me/vol_dos"? [Y|n] y
fsck de util-linux 2.20.1
/dev/mapper/vg00-vol_dos: 11/9216 files (9.1% non-contiguous), 2294/69632 blocks
resize2fs 1.42.9 (4-Feb-2014)
Resizing the filesystem on /dev/mapper/vg00-vol_dos to 20480 (1k) blocks.
The filesystem on /dev/mapper/vg00-vol_dos is now 20480 blocks long.

  Reducing logical volume vol_dos to 20,00 MiB
  Logical volume vol_dos successfully resized
```

Crear una nueva partición:

```console
me@lub ~ $ sudo lvcreate -n vol_tres -L 10M vg00
  Rounding up size to full physical extent 12,00 MiB
  Logical volume "vol_tres" created
me@lub ~ $ sudo lvcreate -n vol_cuatro -l 100%FREE vg00
  Logical volume "vol_cuatro" created
me@lub ~ $ sudo mkfs.ext4 /dev/vg00/vol_tres
...
```

Montar:

```console
me@lub ~ $ mkdir vol_tres
me@lub ~ $ sudo blkid | grep vg00
/dev/mapper/vg00-vol_uno: UUID="ea692853-a0cc-49d1-904a-a72be6162312" TYPE="ext4" 
/dev/mapper/vg00-vol_dos: UUID="be2350c7-e4ed-45a0-8ebf-9aeb2f4eb774" TYPE="ext4" 
/dev/mapper/vg00-vol_tres: UUID="f026ffd3-0910-437e-aac5-fce9195ee60c" TYPE="ext4" 
/dev/mapper/vg00-vol_cuatro: UUID="cb76d1aa-5ea9-4130-b19c-bc375d90fa28" TYPE="ext4" 
me@lub ~ $ sudo bash -c "echo 'UUID=\"f026ffd3-0910-437e-aac5-fce9195ee60c\"  /home/me/vol_tres ext4 defaults 0 2' >> /etc/fstab"
me@lub ~ $ sudo mount /home/me/vol_tres
me@lub ~ $ ls vol_tres/
lost+found
```


http://www.tecmint.com/manage-and-create-lvm-parition-using-vgcreate-lvcreate-and-lvextend/
http://blog.timmattison.com/archives/2009/11/01/how-to-fix-lvm2s-no-extents-available-for-allocation-errors-when-using-pvmove/

### Create and configure encrypted partitions
### Configure systems to mount file systems at or during boot

`/etc/fstab`

### Configure and manage swap space
### Assemble partitions as RAID devices

Muy importante usar el tipo `fd` (ver abajo), sino el raid no se montara
al iniciar el equipo aunque este configurado `/etc/fstab`

```console
me@lub ~ $ sudo fdisk /dev/sdb
Orden (m para obtener ayuda): n
Tipo de partición:
   p primaria (0 primaria, 0 extendida, 4 libre)
   e extendido
Seleccione (predeterminado p): 
Uso predeterminado de la respuesta p
Número de partición (1-4, valor predeterminado 1): 
Se está utilizando el valor predeterminado 1
Primer sector (2048-20479, valor predeterminado 2048): 
Se está utilizando el valor predeterminado 2048
Último sector, +sectores o +tamaño{K,M,G} (2048-20479, valor predeterminado 20479): 
Se está utilizando el valor predeterminado 20479

Orden (m para obtener ayuda): t
Se ha seleccionado la partición 1
Código hexadecimal (escriba L para ver los códigos): fd
Se ha cambiado el tipo de sistema de la partición 1 por fd (Linux raid autodetect)

Orden (m para obtener ayuda): p

Disco /dev/sdd: 10 MB, 10485760 bytes
71 cabezas, 5 sectores/pista, 57 cilindros, 20480 sectores en total
Unidades = sectores de 1 * 512 = 512 bytes
Tamaño de sector (lógico / físico): 512 bytes / 512 bytes
Tamaño E/S (mínimo/óptimo): 512 bytes / 512 bytes
Identificador del disco: 0x391538bc

Dispositivo Inicio    Comienzo      Fin      Bloques  Id  Sistema
/dev/sdd1            2048       20479        9216   fd  Linux raid autodetect

Orden (m para obtener ayuda): w
¡Se ha modificado la tabla de particiones!

Llamando a ioctl() para volver a leer la tabla de particiones.
Se están sincronizando los discos.

me@lub ~ $ sudo fdisk /dev/sdc
...
me@lub ~ $ sudo mdadm --create /dev/md0 --level=1 --raid-disks=2 /dev/sdb1 /dev/sdc1
me@lub ~ $ sudo mkfs.ext4 /dev/md0
me@lub ~ $ sudo mdadm --detail --scan
ARRAY /dev/md0 metadata=1.2 name=lub:0 UUID=d57fb9f6:0eb21ac7:d23f8d55:f4e810e3
me@lub ~ $ sudo bash -c "mdadm --detail --scan >> /etc/mdadm/mdadm.conf"
me@lub ~ $ sudo mkdir /myraid
me@lub ~ $ sudo bash -c "echo '/dev/md0 /myraid ext4 defaults 0 2' >> /etc/fstab"
```

Si un disco tiene problemas (por ejemplo `sdc1`):

1. Añadimos un disco de reserva `sudo mdadm /dev/md0 --add /dev/sdd1`
2. Marcamos el disco defectuoso `sudo mdadm /dev/md0 --fail /dev/sdc1`
3. Eliminamos el disco defectuoso `sudo mdadm /dev/md0 --remove /dev/sdc1`

Esto hará que el disco de reserva (`sdd1`) pase a ocupar el puesto del defectuoso (`sdc1`).

http://www.tecmint.com/creating-and-managing-raid-backups-in-linux/

### Configure systems to mount standard, encrypted, and network file systems on demand
### Create and manage filesystem Access Control Lists (ACLs)

http://www.tecmint.com/set-access-control-lists-acls-and-disk-quotas-for-users-groups/

### Diagnose and correct file permission problems
### Setup user and group disk quotas for filesystems
