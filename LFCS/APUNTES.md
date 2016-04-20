# Introdución

Estos apuntes seguiran el esquema de apartado **Overview of Domains and Competencies**
de [training.linuxfoundation.org/certification/lfcs](https://training.linuxfoundation.org/certification/lfcs#examDetails)
ya que el contenido del curso **LFS201** no esta siendo (en mi opinión) suficiente
para presentarse al examen **LFCS**

Gracias por adelantado a:

* [pablox.co](https://pablox.co/obteniendo-la-linux-foundation-certified-system-administrator-lfcs/)
* [leonelatencio.com](http://leonelatencio.com/notas-de-preparacion-para-el-examen-de-certificacion-de-linux-foundation/)
* [daemons.cf](http://daemons.cf/cgit/apuntes-LFS201)

# Instalación

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

Cuarto, configuro `~/.ssh/config para` que todo se más facil aún:

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



# Essential Commands - 25%

## Log into graphical and text mode consoles

Para ir del modo texto al modo grafico hay varias opciones:

* `startx`
* `runlevel 5`

## Search for files
## Evaluate and compare the basic file system features and options
## Compare, create and edit text files
## Compare binary files
## Use input-output redirection (e.g. >, >>, |, 2>)
## Analyze text using basic regular expressions
## Archive, backup, compress, unpack, and uncompress files
## Create, delete, copy, and move files and directories
## Create hard and soft links
## List, set, and change standard file permissions
## Read, and use system documentation
## Manage access to the root account

# Operation of Running Systems - 20%

## Boot, reboot, and shut down a system safely
## Boot systems into different runlevels manually
## Install, configure and troubleshoot the bootloader
## Change the priority of a process
## Identify resource utilization by process
## Locate and analyze system log files
## Schedule tasks to run at a set date and time
## Verify completion of scheduled jobs
## Update software to provide required functionality and security
## Verify the integrity and availability of resources
## Verify the integrity and availability of key processes
## Change kernel runtime parameters, persistent and non-persistent
## Use scripting to automate system maintenance tasks
## Manage the startup process and services
## List and identify SELinux/AppArmor file and process contexts
## Configure and modify SELinux/AppArmor policies
## Install software from source

# User and Group Management - 15%

## Create, delete, and modify local user accounts
## Create, delete, and modify local groups and group memberships
## Manage system-wide environment profiles
## Manage template user environment
## Configure user resource limits
## Manage user processes
## Configure PAM

# Networking - 15%

## Configure networking and hostname resolution statically or dynamically
## Configure network services to start automatically at boot
## Implement packet filtering
## Configure firewall settings
## Start, stop, and check the status of network services
## Statically route IP traffic
## Dynamically route IP traffic
## Synchronize time using other network peers

# Service Configuration - 10%

## Configure a basic DNS server
## Maintain a DNS zone
## Configure an FTP server
## Configure anonymous-only download on FTP servers
## Provide/configure network shares via NFS
## Provide/configure network shares via CIFS
## Configure email aliases
## Configure SSH servers and clients
## Configure SSH-based remote access using public/private key pairs
## Restrict access to the HTTP proxy server
## Configure an IMAP and IMAPS service
## Query and modify the behavior of system services at various run levels
## Configure an HTTP server
## Configure HTTP server log files
## Restrict access to a web page
## Diagnose routine SELinux/AppArmor policy violations
## Configure database server

# Virtualization - 5%

## Configure a hypervisor to host virtual guests
## Access a VM console
## Configure systems to launch virtual machines at boot
## Evaluate memory usage of virtual machines
## Resize RAM or storage of VMs

# Storage Management - 10%

## List, create, delete, and modify storage partitions
## Create, modify and delete Logical Volumes
## Extend existing Logical Volumes and filesystems
## Create and configure encrypted partitions
## Configure systems to mount file systems at or during boot
## Configure and manage swap space
## Add new partitions, and logical volumes
## Assemble partitions as RAID devices
## Configure systems to mount standard, encrypted, and network file systems on demand
## Create and manage filesystem Access Control Lists (ACLs)
## Diagnose and correct file permission problems
## Setup user and group disk quotas for filesystems
