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

* Entraada estanadar = tipo 0
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
* Para que `cron` genere logs no debe estar activada la opción `-L 0` en `/etc/default/cron`
* Si no sabemos en que log escribe lo podemos buscar con `sudo grep -icr CRON /var/log/* | grep -v :0`
* En `ubuntu` probablemente nos interese `/var/log/syslog`

Más: [bencane.com](http://bencane.com/2011/11/02/did-my-cronjob-run/)
[help.ubuntu.com](https://help.ubuntu.com/community/CronHowto#Troubleshooting_and_Common_Problems)

### Update software to provide required functionality and security

`sudo apt-get update` +:

* `sudo apt-get upgrade` actualiza todo lo que se pueda actualizar sin tener que resolver conflictos (nunca eliminara paquetes)
* `sudo apt-get dist-upgrade` actualiza intentando resolver conflictos si los hubiera (puede que elimine paquete)

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

Más: [www.tecmint.com](http://www.tecmint.com/monitor-linux-processes-and-set-process-limits-per-user/)

### Change kernel runtime parameters, persistent and non-persistent

http://www.tecmint.com/change-modify-linux-kernel-runtime-parameters/

### Use scripting to automate system maintenance tasks

http://www.tecmint.com/linux-basic-shell-scripting-and-linux-filesystem-troubleshooting/

### Manage the startup process and services

http://www.tecmint.com/linux-boot-process-and-manage-services/

### List and identify SELinux/AppArmor file and process contexts
### Configure and modify SELinux/AppArmor policies
### Install software from source

## User and Group Management - 15%

### Create, delete, and modify local user accounts
### Create, delete, and modify local groups and group memberships

http://www.tecmint.com/manage-users-and-groups-in-linux/

### Manage system-wide environment profiles
### Manage template user environment
### Configure user resource limits
### Manage user processes
### Configure PAM

## Networking - 15%

### Configure networking and hostname resolution statically or dynamically
### Configure network services to start automatically at boot
### Implement packet filtering
### Configure firewall settings
### Start, stop, and check the status of network services
### Statically route IP traffic
### Dynamically route IP traffic
### Synchronize time using other network peers

## Service Configuration - 10%

### Configure a basic DNS server
### Maintain a DNS zone
### Configure an FTP server
### Configure anonymous-only download on FTP servers
### Provide/configure network shares via NFS

```console
sudo apt-get install nfs-common nfs-kernel-server
sudo systemctl start nfs-kernel-server
```

http://www.tecmint.com/mount-filesystem-in-linux/
https://help.ubuntu.com/community/SettingUpNFSHowTo

### Provide/configure network shares via CIFS
### Configure email aliases
### Configure SSH servers and clients
### Configure SSH-based remote access using public/private key pairs
### Restrict access to the HTTP proxy server
### Configure an IMAP and IMAPS service
### Query and modify the behavior of system services at various run levels
### Configure an HTTP server
### Configure HTTP server log files
### Restrict access to a web page
### Diagnose routine SELinux/AppArmor policy violations
### Configure database server

## Virtualization - 5%

### Configure a hypervisor to host virtual guests
### Access a VM console
### Configure systems to launch virtual machines at boot
### Evaluate memory usage of virtual machines
### Resize RAM or storage of VMs

## Storage Management - 10%

### List, create, delete, and modify storage partitions

http://www.tecmint.com/create-partitions-and-filesystems-in-linux/

### Create, modify and delete Logical Volumes

http://www.tecmint.com/manage-and-create-lvm-parition-using-vgcreate-lvcreate-and-lvextend/

### Extend existing Logical Volumes and filesystems
### Create and configure encrypted partitions
### Configure systems to mount file systems at or during boot
### Configure and manage swap space
### Add new partitions, and logical volumes
### Assemble partitions as RAID devices

http://www.tecmint.com/creating-and-managing-raid-backups-in-linux/

### Configure systems to mount standard, encrypted, and network file systems on demand
### Create and manage filesystem Access Control Lists (ACLs)

http://www.tecmint.com/set-access-control-lists-acls-and-disk-quotas-for-users-groups/

### Diagnose and correct file permission problems
### Setup user and group disk quotas for filesystems
