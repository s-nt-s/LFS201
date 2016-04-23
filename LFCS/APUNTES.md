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

### Evaluate and compare the basic file system features and options

*no tengo claro a que se refiere*

### Compare, create and edit text files

* Crear fichero vacio: `touch fichero.txt`
* Editar fichero: `nano fichero.txt`
* Comparar ficheros: `diff fichero1.txt fichero2.txt`

### Compare binary files

`cmp` o `diff`

### Use input-output redirection (e.g. >, >>, |, 2>)

* Entraada estanadar = tipo 0
* Salida estanadar = tipo 1
* Error estandar = tipo 2


* `comando 2>&1`  redirigir errores a salida estandar
* `wc < archivo.txt` alimenta la entrada estandar de `wc` con `archivo.txt`
* `comando 2> /dev/null` desecha la salida de errores
* `ps -a | sort` redireciona la salida de `ps` a la entrada de `sort`

Más: [hipertextual.com](http://hipertextual.com/archivo/2014/07/redirecciones-y-tuberias-bash/)

### Analyze text using basic regular expressions

* `grep -e`
* `awk`
* `sed`

### Archive, backup, compress, unpack, and uncompress files

* `tar cvf file.tar *` comprimir
* `tar xvf file.tar` descomprimir
* `tar xpvf file.tar` descomprimir presrvando permisos
* `tar tf file.tar` listar contenido
* Para comprimir a la vez que se empaqueta añadir la opción:
  * `z` para comprimir con `gzip`
  * `j` para comprimir con `bz2`
  * `J` para comprimir con `xz`

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

### Read, and use system documentation

* `man comando`
* `comando --help`

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
9. Reiniciamos

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
6. `sudo chroot /mnt` cambiamos el directorio /
7. `sudo apt-get --reinstall install grub-common grub2-common grub-pc` reinstalamos los paquetes grub
8. `grub-install /dev/sda && grub-install --recheck /dev/sda && update-grub` instalamos grub
9. Desmontamos todo:
	* `exit`
	* `sudo umount /mnt/sys`
	* `sudo umount /mnt/proc`
	* `sudo umount /mnt/dev/pts`
	* `sudo umount /mnt/dev`
	* `sudo umount /mnt`
10. Reiniciamos

Más: [howtoubuntu.org](http://howtoubuntu.org/how-to-repair-restore-reinstall-grub-2-with-a-ubuntu-live-cd)
[lukeplant.me.uk](http://lukeplant.me.uk/blog/posts/sharing-internet-connection-to-chroot/)
[ubuntuforums.org](http://ubuntuforums.org/showthread.php?t=1467147)
[debian-handbook.info](https://debian-handbook.info/browse/es-ES/stable/sect.apt-get.html)

### Change the priority of a process
### Identify resource utilization by process
### Locate and analyze system log files
### Schedule tasks to run at a set date and time
### Verify completion of scheduled jobs
### Update software to provide required functionality and security
### Verify the integrity and availability of resources
### Verify the integrity and availability of key processes
### Change kernel runtime parameters, persistent and non-persistent
### Use scripting to automate system maintenance tasks
### Manage the startup process and services
### List and identify SELinux/AppArmor file and process contexts
### Configure and modify SELinux/AppArmor policies
### Install software from source

## User and Group Management - 15%

### Create, delete, and modify local user accounts
### Create, delete, and modify local groups and group memberships
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
### Create, modify and delete Logical Volumes
### Extend existing Logical Volumes and filesystems
### Create and configure encrypted partitions
### Configure systems to mount file systems at or during boot
### Configure and manage swap space
### Add new partitions, and logical volumes
### Assemble partitions as RAID devices
### Configure systems to mount standard, encrypted, and network file systems on demand
### Create and manage filesystem Access Control Lists (ACLs)
### Diagnose and correct file permission problems
### Setup user and group disk quotas for filesystems
