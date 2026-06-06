# Introducción a linea de comandos
## Summary and Setup
Existen dos formas en que podemos interactuar con las computadores y su sistema operativo: la linea de comandos o Command Line Interface (CLI) y la interfaz grafica o graphic User Interface (GUI).

La mas común y a la cual la mayoría de la gente esta habituada es GUI, la cual esta disponible en Mac y Windows y en algunas distribuciones de Linux como Ubuntu, esta forma es mas intuitiva de usar ya que contiene multiples imagenes y puedes interactuar visualmente con representaciones gráficas de archivos, folders y aplicaciones. La línea de comando o CLI por su parte también llamado “shell” interactúa con la computadora a través de instrucciones escritas.

Ventajas del uso de CLI:

Muchas paqueterías bioinformáticas carecen de GUI, la linea de comandos permite automatizar tareas repetitivas, ademas permite ejecutar tareas que requiere de poder de computo y simplificar procesos. En pocas palabra te permite trabajar de forma mas eficiente y replicar el trabajo múltiples veces. Se pueden repetir parámetros cambiando variables de forma automática y de esta forma hacer pruebas y ensayos de forma rápida y eficiente. El uso de super computadores o computadores remotos, necesarios para analizar datos genómicos requieren en la mayoría de los casos comunicación a través de la linea de comandos.

Este tutorial esta basado y modificado del tutorial de [Data Carpentry](https://datacarpentry.github.io/shell-genomics/)

## Terminal o Shell
La terminal es un programa que representa una interfaz de linea de comandos que te permite escribir instrucciones especificas a realizar por la computadora. Para accesar la linea de comandos o terminal en Mac podemos encontrarla en `Aplicaciones > Utilidades > Terminal.app`. En windows la forma mas fácil es a través de la barra de busqueda y buscar por `Windows Terminal` sin embargo para este curso, en sistemas operativos windows utilizaremos una distribución virtual de Linux llamada Windows Subsystem for Linux, dirígete a las [instrucciones de instalación](https://github.com/rmonjaraz/UCEs_Workshop_LaPaz_2026/blob/main/Tutoriales/Instalacion.md) para ver como activarla e instalarla en tu computadora.

## Navegación
La parte de nuestra computadora que organiza archivos y datos se denomina “sistema de archivos” y requerimos familiarizarnos con este para poder realizar diversas tareas. La primer parte para familiarizarse con la linea de comandos es el símbolo de dólar `$` este indica el comienzo del “prompt” o el inicio de las instrucciones, si ves este símbolo en comandos en general indican que ahi comienza el comando o instrucción y no debe ser incluido como parte del comando.

Existen muchas ayudas y “acordeones” que te pueden ayudar a simplificar y recordar los comandos, [aquí](https://drive.google.com/file/d/1RZjywLNAT1QfmpamwBJxMP00RQiWFqUi/view?usp=drive_link) se encuentra una bastante básica.

Después de localizar y abrir la terminal, empezemos con averiguar nuestra ubicación en el sistema de archivos, a esta dirección también se le conoce como PATH:
```bash
pwd
```
`/Users/Roderick`

Ahora vamos a averiguar como esta organizado nuestro sistema de archivos y los archivos disponibles en nuestra actual dirección utilizando `ls` que es abreviación de “list":
```bash
ls
```

`Applications	Movies
Desktop		Google Drive	Music	Documents		Library	
Downloads	Pictures	Public
`

`ls` imprime los nombres de los archivos y folders en la dirección actual en orden alfabético y organizado en columnas.

Ahora con la finalidad de poder estandarizar el trabajo procederemos a trabajar en nuestra carpeta de `Data` descarga [esta carpeta](https://drive.google.com/drive/folders/1KxKB5jOsHOl4zak6WhVBaljc5kiJzTFy?usp=drive_link) y pégala en tu folder de “Home” o directorio de inicio, utilizaremos esta carpeta durante todo el curso.

El comando para cambiar de folder o dirección es `cd` que es abreviación de “change directory”, seguido de la dirección o nombre del folder al que queremos movernos.

```bash
cd Data/ 
```
Luego:
```bash
cd SRA/ 
```
Ahora vamos a ver los contenidos:
```bash
ls 
```
`ls` tiene bastantes opciones para listar archivos con información adicional por ejemplo usando la opción **-F** podemos determinar si tenemos folders `/`, programas `*` or archivos sin ningún carácter especial.
```bash
ls -F
```
`biosample_SRA.txt		Examples_FASTQs			Indexing_Info.xlsx		raw_SRA_fastqs
clean_SRA_fastq			illumiprocessor_clean_fastqs	list_of_samples.txt		SraRunInfo.xlsx
clean-reads-phyluce		illumiprocessor.conf		prefetchSRA`

`ls` tiene muchas opciones, en linea de comandos la opción `man` abreviación de “manual” es una forma de ver todas las opciones y sus funciones, es en pocas palabras el manual de cada programa, principalmente para todos los programas de `bash`.
```bash
man ls
```
Puedes usar el mouse o las flechas para explorar el contenido, para salir presiona <kbd>q</kbd>

Prueba algunas otras opciones del comando `ls` e intenta determinar que significan. Por ejemplo:
```bash
ls -l
```

Naveguemos al folder `Examples_FASTQs`
```bash
cd Examples_FASTQs/
ls
```
***¿Que observas? ¿Que tipo de archivos son?***

## Atajos
Hay algunas formas de agilizar la escritura y movimiento del cursor en la terminal, regresemos al directorio base o Home Directory.
```bash
cd 
```

Ahora naveguemos de regreso a la ultima carpeta utilizando:
```bash
cd ../
```
*Mas sobre esto comando adelante.*

Utilizaremos un atajo para completar nombres de archivos y folders usando <kbd>Tab</kbd> esto nos permite completar texto para evitar escribir nombres de archivos muy largos, si tienes nombres parecidos el atajo necesita que proveas de los caracteres únicos a cada folder o archivo. Naveguemos a `raw_SRA_fastqs`, para evitar escribir todo el nombre usaremos el atajo

```bash
cd raw<tab>
```
Regresemos un folder atrás y hagamos otra prueba.
```bash
cd ../
```
Ahora naveguemos a `illumiprocessor_clean_fastqs`
```bash
cd illum<tab>
```
¿Qué ocurrió aquí? ¿Porque fallo? Provee de un nombre único y procede.

<kbd>Tab</kbd> también puede ayudar a completar nombres de programas si sabemos parte de ellos, por ejemplo, si tenemos instalado phyluce, podemos listar todos los programas de phyluce. Primero activemos el ambiente:
```bash
conda activate phyluce1.7
```
Recuerda cambiarlo por el nombre de tu ambiente, si no lo recuerdas siempre puedes usar el comando `conda env list` para ver que ambientes tienes.

Para ver la lista de programas disponibles en phyluce usando <kbd>Tab</kbd>

```bash
phyl<tab>
```

## Navegación compleja
Ahora vamos a intentar movernos a diferentes folders e intentar entrar y salir de estos utilizando la linea de comandos, así como listar el contenido de otros folders en los que no nos encontramos actualmente. A este punto aprendimos como encontrar nuestra ubicación utilizando `pwd` y cambiar de directorio usando `cd` y finalmente ver los contenidos usan `ls` ahora aprenderemos como combinar estos para navegar el sistema.

Para navegar directamente a un folder dentro de otro folder podemos listar la dirección completa de ese archivo si la conocemos por ejemplo:
```bash
cd clean-reads-phyluce/gallus_gallus/split-adapter-quality-trimmed
```

`cd` solo funciona para moverse en folders, si intentamos navegar a un archivo obtendremos un error por ejemplo intenta lo siguiente:
```bash
cd gallus_gallus-READ1.fastq.gz
```

Existen dos tipos de folders “especíales” `.` and `..`; `.` se refiere al actual folder donde te encuentras, y `..` se refiere al folder un nivel por arriba de donde estas. Si combinamos ambos `..` con `cd` podemos cambiar a diferentes folders.
```bash
$ cd ..
```
¿Que tal este?
```bash
$ cd ../../
```
Utiliza `pwd` para explicar que paso en este ultimo caso.

### Archivos Escondidos
*Reto: encuentra el Archivo escondido en la carpeta `clean-reads-phyluce`*

Para esto explora las opciones de `ls` utilizando `man`, ¿Que opción nos permite revelar archivos ocultos?

Ayuda: archivos ocultos comienzan con `.`, por ejemplo el clásico archivo creado por Mac .DS_Store, los folders igual comienzan de esta forma y se puede navegar y accesar a ellos.

*¿En donde se encuentra el archivo oculto y cual es su nombre?*

### Rutas absolutas y relativas (Path)
Las rutas absolutas y relativas sirven para poder localizar y proveer de la ruta indicada de algún archivo o folder, cuando utilizamos `pwd` normalmente obtenemos la ruta absoluta al directorio en el que nos encontramos. Al comando `cd` se le puede asignar un argumento (el nombre de un archivo o folder) `cd [ARGUMENTO]` por ejemplo `cd SRA` esta indicación es una ruta relativa al folder en el que nos encontramos, si ese folder se encuentra en algún otro lugar el sistema va a ser imposible de localizarlo y obtendremos un error. Cuando utilizamos `cd` sin argumentos el comportamiento por default es movernos al “Home Directory” o directorio de inicio.

En el folder que te encuentras actualmente escribe `pwd` ¿Qué observas? Esta se trata de la ruta absoluta y normalmente incluye tu directorio de inicio, mas cualquier otro folder en el que te encuentres.

Ahora escribe `cd` seguido de `pwd` ¿Que cambio?

Podemos usar estas rutas absolutas para listar `ls` contenidos de otros folders

```bash
ls /Users/Roderick/Data/SRA/clean-reads-phyluce/alligator_mississippiensis/split-adapter-quality-trimmed
```
`NOTA: Asegurate de cambiar en este comando la ruta absoluta dependiendo tu sistema, utiliza pwd para encontrarla`

También podemos movernos `cd` usando la ruta absoluta, como ya lo hicimos anteriormente.
```bash
cd /Users/Roderick/Data/SRA/clean-reads-phyluce/alligator_mississippiensis/split-adapter-quality-trimmed
```
`NOTA: En alguna ocasiones es importante proveer a los programas con las rutas absolutas, en particular si estamos trabajando con archivos en diferentes folders.`

Reto: Con base en el diagrama mostrado abajo, si escribimos `pwd` para ubicarnos en el sistema y obtenemos `/Users/thing`, ¿cual sera el resultado si escribimos ls ../backup?
<img src="https://github.com/rmonjaraz/UCEs_Workshop_LaPaz_2026/blob/main/Figuras/navegacion.svg" width="10%">

### Atajos de Navegación
El directorio de raiz es el folder mas alto en el sistema, normalmente aqui se almacenan archivos y folders importantes para el funcionamiento correcto de tu computadora, por lo cual se aconseja no trabajar directamente aquí nunca si no al contrario, crear directorios por debajo de esta categoría lo cual garantizara que no modifiquemos nada crucial en nuestra computadora. Cuando buscamos nuestra ubicación con `pwd` siempre observamos el archivo de raíz (root) y nuestro directorio de inicio (home) en mi caso es `/Users/Roderick` `Users` es mi directorio raíz y `Roderick` es mi directorio de inicio, aqui usualmente se instalan programas como conda o mesquite. Instalar cosas o modificar archivos en “root” normalmente require de permisos especiales.

Para aquellos usando **WSL** las cosas son un poco diferentes dado que esto es una maquina virtual, su aparente directorio de inicio (home) se encuentra dentro de Linux > Ubunto > home > tu_nombre_de_usuario

Si quieres acceder a archivos en tu computadora, fuera de Ubuntu, necesitas ubicar la instalación de Ubuntu en tu sistema, por default esta seria la ruta:

```bash
cd /mnt/c/Users/<TuWindowsUsername>
```

De aquí puede utilizar `cd` y `ls` para navegar en tu computadora.

El caracter de tilde `~` es un atajo a nuestro directorio de inicio (home) en este caso navegar a este símbolo me llevara siempre al home:
```bash
cd ~
```
`/Users/Roderick`

```bash
ls ~
```
Mostrara todos los folders en mi home directory.

`TIP: Para los usuarios de Mac, puedes mostrar la ruta absoluta en tu Finder para simplificar tu navegación, si no esta activa abre el Finder y ve a View > Show path Bar. También puedes seleccionar desde aquí el folder en que deseas utilizar y arrastrarlo a la terminal, la ruta absoluta se copiara automáticamente.`
`Para usuarios de Windows pueden checar como hacer algo similar en este` [video](https://www.youtube.com/watch?v=-UzTkSvKoy0)

### A recordar

- Los caracteres /, ~, y .. son importante atajos para navegar.
- Archivos ocultos empiezan con `.` y se pueden listar usando `ls -a`
- Rutas relativas muestran contenidos a partir de nuestra actual ubicación en el sistema, mientras que rutas ansolutas muestran la ubicación de un archivo desde la raiz o directorio de raiz.

## Trabajando con Archivos
Una vez que aprendemos a navegar por el sistema de archivos, lo siguiente es aprender unos pasos básicos para trabajar con archivos de forma mas eficiente. Lo primero va a ser crear directorios o folders, para esto existe un programa llamado `mkdir` o abreviación en ingles de “make directory”, podemos usar rutas absolutas o relativas para esta tarea. Vamos a crear un nuevo folder llamado `Nuevo_Folder`.

*TIP: Cuando trabajamos en linea de comandos es preferible nunca usar caracteres especiales o espacios, estos tienen significados específicos en código que es preferible evitar, en la mediad de lo posible en nombres sustituye espacios por renglones bajos `_`*

### Crear Directorios
Creemos nuestro nuevo folder, primero navega a la ruta donde lo quieres crear usando `cd` y crea ahi tu directorio:
```bash
mkdir Nuevo_Folder
```
Checa que fue exitoso el comando
```bash
ls
```
### Copiar
A continuación vamos a usar este mismo folder para aprender como copiar archivos y folders, utilizaremos el comando `cp`, recuerda que puedes usar `man` para aprender mas sobre los detalles de este programa. Si intentamos copiar nuestro folder sin usar ningún argumento adicional (i.e. opciónes adicionales del programa) obtendremos un error, esto se debe a que para poder copiar un folder tenemos que hacer de forma “recursiva” esto es copiar todos los documentos y folderes contenidos en esa ruta. Para ello tenemos que incluir el argumento `-r`
```bash
cp -r Nuevo_Folder/ Nuevo_Folder_copia
```
Si trabajamos solo con archivos no se requieren los argumentos adicionales.

`NOTA: Estos argumentos adicionales son también denominados “flags” y son bastante utilizados en programas python que veremos mas adelante.`

### Mover y renombrar
Ahora vamos a renombrar nuestro folder, este comando en bash puede ser un poco confuso ya que para hacerlo necesitamos usar el programa `mv` que es abreviación de “move”. Este comando igual sirve para poder archivos y carpetas de un lugar a otro. Funciona dando el archivo a mover (y su ubicación), seguido de a donde lo quieres mover. `mv [ORIGEN] [DESTINO]`. La lógica es que técnicamente le estas dando la indicación a el sistema de mover ese archivo a ese mismo lugar utilizando un nombre diferente, es decir una ruta absoluta diferente (dado el nombre diferente), cuando simplemente lo movemos a otro lugar estamos cambiando de igual forma la ruta absoluta pero sin cambiar el nombre solo quizás el folder.

Ejemplo: Para mover un archivo ubicado en `/Users/Jose/Mi_Folder/Archivo1.txt` al folder `/Users/Jose/Mi_Otro_Folder/` hacemos esto:
```bash
mv /Users/Jose/Mi_Folder/Archivo1.txt /Users/Jose/Mi_Otro_Folder/Archivo1.txt
```
Aquí lo que cambio fue `Mi_Folder` por `Mi_Otro_Folder` en la ruta absoluta del archivo. Para renombrar seria el siguiente comando usando el mis ejemplo anterior:
```bash
mv /Users/Jose/Mi_Folder/Archivo1.txt /Users/Jose/Mi_Folder/Archivo_renombrado.txt
```
Aqui les estamos diciendo a `mv` que ese archivo que se encuentra exactamente en esa ruta necesita ser movido con un nuevo nombre. Procedamos a renombrar el folder que acabamos de copiar en el paso anterior:
```bash
mv Nuevo_Folder_copia/ Nuevo_Folder_renombrado
```
### Eliminar
Para poder eliminar archivos o folders es la misma lógica que usamos con `cp` necesitamos hacerlo de forma recursiva con folders utilizando el programa `rm`.
```bash
rm -r Nuevo_Folder_renombrado
```
### wildcards
Los wildcards son por su traducción “comodines” que nos ayudan a encontrar zonas en común o ignorar regiones de los nombres de archivos y se denotan con el símbolo de asterisco `*`. Para explorar su uso vamos a dirigirnos a nuestro folder de `Data`, una ves ahi vamos a listar usando `ls` solo los archivos que tienen la extensión `.txt` ya que solo estamos interesados en ver ese tipo de archivos, usando un wildcard funcionaria de esta forma:
```bash
ls *.txt
```
Ahora intenta listar todos los archivos y folders que contengan la palabra `phyluce` ya sea al inicio, en medio o al final, como lo harías?
```bash
ls *phyluce*
```

*TIP: atajos del teclado:*
<kbd>Ctrl</kbd>+<kbd>C</kbd> Cancela el actual comando y devuelve una prompt limpia.
<kbd>Ctrl</kbd>+<kbd>R</kbd> Realiza una búsqueda retrospectiva de tu historial de comandos, baste util para repetir comandos anteriores sin escribirlos de nuevo.
<kbd>Ctrl</kbd>+<kbd>L</kbd> Para limpiar tu pantalla y regresar a una prompt limpia.

Pruébalos en tu terminal.

### Contenido de archivos
Ahora vamos a explorar el contenido de archivos utilizando tres programas diferentes `cat`, `head` y `tail`. Para entender su uso vamos a navegar al folder `Examples_FASTQs` ya sabes como hacerlo. Una ves ahi:
```bash
cat Sample1-READ1.fastq.gz
```
Este archivo es muy largo y el resultado no va a ser nada agradable a la vista, ya que este comando imprime a la pantalla los contenidos de todo el archivo, si estas trabajando con archivos grandes este comando no es aconsejable, para eso podemos usar `head` para ver solo el comienzo del archivo y `tail` para ver el final.
```bash
head Sample1-READ1.fastq.gz
```
Para ver el final:
```bash
tail Sample1-READ1.fastq.gz
```
Ahora podemos usar una argumento o flag para modificar el comportamiento de `head` y `tail` utilizando `-n` podemos agregar el número de lineas a imprimir, por ejemplo imprimamos las primeras 10 lineas:
```bash
head -n 10 Sample1-READ1.fastq.gz
```

Finalmente, `cat` también puede ser utilizado para combinar o concatenar los contenidos de dos o mas archivos. Primero vamos a explorar los contenidos de los archivos `file1.txt` y `file2.txt` usando `cat`. 
```bash
cat file1.txt
```
Ahora vamos a concatenar los contenidos de ambos archivos utilizando `cat` necesitamos proveer de dos o mar archivos y proporcionar al nombre del archivo que queremos crear `cat [ARCHIVO 1] [ARCHIVO 2] > [RESULTADO]`, de lo contrario el resultado sera solo mostrado en la terminal, hagamos primero este ultimo ejemplo:
```bash
cat file1.txt file2.txt
```
Para poder crear un archivo necesitamos utilizar de otro símbolo especial `>` este sirve para redirigir los resultado de un comando hacia otro enmarcado este caso para imprimir los contenidos en un nuevo archivo:
```bash
cat file1.txt file2.txt > concatenado.txt
```
Checa si tu archivo fue creado usando `ls` y ahora examina el contenido con `cat`

### Contenido de archivos
Permisos son importantes para poder ejecutar scripts o para poder evitar modificaciones indeseadas, por ejemplo borrar archivos de forma innecesaria, una buena medida de seguridad es cambiar permisos de to “RAW DATA” para evitar que usuarios (o tu mismo) hagan cambios por accdiente.
```bash
cd SRA/Examples_FASTQs/
ls -l
```
`-rw-r--r--@ 1 rmonjarazruedas  RESEARCH\Domain Users      10 May 29 18:39 file1.txt`
`-rw-r--r--@ 1 rmonjarazruedas  RESEARCH\Domain Users      11 May 29 18:35 file2.txt`
`-rwx------  1 rmonjarazruedas  RESEARCH\Domain Users  809565 Sep  6  2022 Sample1-READ1.fastq`
`-rwx------  1 rmonjarazruedas  RESEARCH\Domain Users  904299 Sep  6  2022 Sample1-READ2.fastq`

<img src="https://github.com/rmonjaraz/UCEs_Workshop_LaPaz_2026/blob/main/Figuras/rwx_figure.svg" width="10%">

Vamos a cambiar los permisos de `file1.txt` para solo leer `-r` y evitar así cambios por error, usaremos el programa `chmod` que es abreviación de “Change Mode” en ingles.
```bash
chmod -w file1.txt
ls -l
```
`-r--r--r--@ 1 rmonjarazruedas  RESEARCH\Domain Users      10 May 29 18:39 file1.txt`
`-rw-r--r--@ 1 rmonjarazruedas  RESEARCH\Domain Users      11 May 29 18:35 file2.txt`
`-rwx------  1 rmonjarazruedas  RESEARCH\Domain Users  809565 Sep  6  2022 Sample1-READ1.fastq`
`-rwx------  1 rmonjarazruedas  RESEARCH\Domain Users  904299 Sep  6  2022 Sample1-READ2.fastq`

## Bucles (For Loops) (super breve)
Un for loop (o bucle for) es una estructura que permite ejecutar un bloque de código repetidamente. Se utiliza para iterar sobre una lista de elementos (como nombres de archivos, palabras, o rangos de números) y realizar una acción específica para cada uno de ellos.

```bash
for variable in elemento1 elemento2 elemento3
do
    # Comandos a ejecutar
done
```
Ejemplo:
```bash
for dia in lunes martes miercoles
do
    echo "Hoy es $dia"
done
```
Con números:
```bash
for i in {1..5}
do
    echo "Número $i"
done
```
Finalmente interar sobre todos los archivos o folders en nuestro directorio, utilizando un wildcard:
```bash
for archivo in *.txt
do
    echo "Procesando el archivo: $archivo"
    # Aquí podrías agregar comandos para modificar el archivo
done
```
Esto es bastante util y común de ver en bioinformática y código en general, los detalles de como funcionan no nos alcanza el tiempo para verlos pero los muestro como forma de entender parte del código que utilizaremos el resto del curso.

## Python Argumentos o Flags
Cuando utilizamos programas como los de Bash o Python observamos que existe cierta sintaxis que es común en ambos programas, por ejemplo cuando usamos `ls` podemos agregar argumentos adicionales como `ls -a` esta `-a` es lo que se conoce como argumento y en ingles también se refieren a estas como “flags”, lo que hacen es modificar el comportamiento u opciones por default del programa. Por ejemplo durante el tutorial en phyluce es muy común observar esto:
```python
illumiprocessor \
    --input raw-fastq/ \
    --output clean-fastq/ \
    --config illumiprocessor.conf \
    --cores 4
```
Este comando esta utilizando el programa `Illumiprocessor` y los argumentos empezando con `—` reflejan opciones del programa, si utilizamos `-h` o `—help` podemos obtener una explicación de que efectos u opciones representan esas “flags”. El símbolo `\` representa un breack y le dice al programa que considere esto como una linea continua, se utiliza principalmente para cuestiones de facilitar la lectura.
```python
illumiprocessor --help
```
Así podemos ver que `—input` es el folder con nuestros datos de input para Illumiprocessor, o que `—cores` representa cuantos núcleos de la computadora queremos utilizar para realizar esta tarea, etc.
