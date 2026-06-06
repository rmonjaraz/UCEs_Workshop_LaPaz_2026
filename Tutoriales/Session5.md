# Extracción y Búsqueda de UCEs
A este punto en le flujo de trabajo vamos a retomar directamente los programas de [Phyluce](https://phyluce.readthedocs.io/en/latest/index.html) pronunciado según el sitio como (phy-**loo**-chee). `Phyluce` es un compendio de muchos programas en lines de comandos que permiten realizar una innumerable cantidad de procesos, es bastante popular y es el programa preferido para el trabajo con UCEs, La documentación de `phyluce` es bastante extensa y sencilla de entender, contiene varios tutoriales y el [tutorial de filogenomica](https://phyluce.readthedocs.io/en/latest/tutorials/tutorial-1.html) es muy bueno para repasar lo aprendido en este tutorial y para indagar mas a fondo si así lo desean.

`Phyluce` fue escrito por Faircloth en 2016 y permite entre otros:
- Ensamblaje
- Determinar que contigs representan UCEs (extracción)
- Filtrado de UCEs potencialmente paralogos
- Generar matrices de datos
- Alinear secuencias
- Manipular alineamientos
- Convertir entre formatos de archivos
- Etc.

Para La extracción de UCEs utilizaremos 4 programas dentro de la colección de `phyluce`. La forma en que estos funcionan es que necesitamos 1) Encontrar los UCEs dentro del mar de contigs (ensambles) que obtuvimos en los pasos anteriores, hay que recordar que la secuenciación no es perfecta y se pueden secuenciar fragmentos adicionales a los seleccionados durante la preparación de bibliotecas genómicas. Esta búsqueda ocurre mediante el mapeo de nuestras sondas contra los contigs. 2) Una vez que encontramos que contigs corresponden a UCEs, necesitamos hacer un mapa por muestra de los UCEs asociados a estas, para esto `phyluce` crea un mapa en forma de base de datos, donde indica que contigs y en que posiciónes están los UCEs de cada muestra. 3) por últimó procedemos a extraer las secuencias en formato fasta, este será nuestro archivo final donde tendremos todas las secuencias asociadas de UCEs asociadas a esa muestra.

## Encontrar UCEs
En este paso necesitamos mapear nuestras sondas contra nuestros contigs, necesitamos utilizar nuestro archivo de sondas (probes) que es el mismo que utilizamos para hacer las bibliotecas genómicas, estos están disponibles como parte de los materiales suplementarios de los artículos donde fueron publicadas las sondas. Para este ejercicio utilizaremos los `Spider_Probes` creados por [Kulkarni, et al (2019)](https://drive.google.com/file/d/1Fn3Yvub5s93Y6Ze1nHuzfMKLcu1h-dTC/view?usp=sharing), el archivo esta cobrado como `Spider_Probes.fasta` y  pueden encontrarlo en: el folder compartido en la siguiente ruta: `/Data/Extraccion/Spider_Probes.fasta`

El programa que utilizaremos se llama `phyluce_assembly_match_contigs_to_probes` y requiere 4 argumentos principales, la ruta del folder con nuestros contigs, la ruta a nuestro archivo de sondas (probes) y valores para coverage e identidad - **Ver Presentación**.

Vamos a utilizar un par de “variables” para poder correr los comandos de forma mas fácil, así todos podemos modificar estas variables de a cuerdo a su computadora.

Crear variables:

```bash
AssembliesFolder="/Users/Roderick/Desktop/Hexurella_UCEs_Exercise/Extraccion/contigs_Hexurella"
ProbeFile="/Users/Roderick/Desktop/Hexurella_UCEs_Exercise/Extraccion/Spider_Probes.fasta"
```

Y ahora si corremos el programa usando valores de identidad y cobertura de 80 y 80

```bash
phyluce_assembly_match_contigs_to_probes \
--contigs $AssembliesFolder \
--probes $ProbeFile \
--output Hexurella_uce_search_results \
--min-coverage 80 \
--min-identity 80 \
--csv Hexurella_uce_search_stats.csv
```
Tomate tu tiempo y revisa el archivo `Hexurella_uce_search_stats.csv`

- ¿Qué observas aqui?
- ¿Cuantos UCEs tenemos por muestra?
- ¿Cuantos potenciales genes parálogos fueron removidos?
- Compara estos valores con los STATS de Ensamblaje y FASTq QC, ¿Qué observas?

## Extraer UCEs
Ahora que ya detectamos que UCEs pertenecen a que muestras y creamos nuestro mapa (almacenado en `Hexurella_uce_search_results/probe.matches.sqlite`) esta es una base de datos en formato `.sql` que contiene la muestra, el nombre del contig y el nombre del UCE al que corresponden. Ahora sigue extraer las secuencias.

*NOTA: `Phyluce` sugiere en este punto crear sets de datos con las muestras que quieres utilizar, yo aconsejo siempre extraer todos los UCEs de todas tus muestras y armar tus sets de datos mas tarde en el proceso, esto facilitara el manejo de muestras.*

Necesitamos crear un archivo de configuración diciendo a `phyluce` que muestras extraer, una vez mas, yo sugiero extraer todas tus muestras en este paso. Por consiguiente crearemos una lista de todas las muestras y la guardaremos en un archivo de texto con el nombre `taxon-set.conf` este archivo si lo abres se ve así:

```
[all]
Hexurella_apachea_SDSU_MY5064
Hexurella_encina_SDSU_MY5277
Hexurella_pinea_SDSU_MY5314
Hexurella_rupicola_SDSU_MY5317
Megahexura_fulva_SDSU_MY4841

```
La opción`[all]` Se utilizara mas adelante en el comando, puedes cambiarla a cualquier otra palabra, pero considerando que vamos a extraer todas las muestras, entonces mantengamos la palabra `all`.

Para mantener las cosas ordenadas vamos a crear primero un par de folders, nota el uso del argumento `-p` este sirve para crear un folder dentro de otro nuevo folder:

```bash
mkdir -p taxon-sets/all
```
Creemos unas variables mas, necesitamos la ruta a nuestra base de datos mapa de los UCEs por muestra `probe.matches.sqlite` y la ruta al archivo de texto que acabamos de crear `taxon-set.conf`.

```bash
db="/Users/Roderick/Desktop/Hexurella_UCEs_Exercise/Extraccion/Hexurella_uce_search_results/probe.matches.sqlite"
taxon="/Users/Roderick/Desktop/Hexurella_UCEs_Exercise/Extraccion/taxon-set.conf"
```
Corramos el programa, observamos el uso de `all` este debe coincidir con el nombre asignado en tu archivo de configuración:

```bash
phyluce_assembly_get_match_counts \
    --locus-db $db \
    --taxon-list-config $taxon \
    --taxon-group 'all' \
    --output taxon-sets/all/Hexurella_incomplete.conf \
    --incomplete-matrix
```
Este paso a creado otro mapa de la base de datos original que será utilizado en el ultimo paso para extraer las secuencias en formato fasta, observa el resultado de salida en la terminal ¿Qué observas respecto al numero total de UCEs en el data set?

Por ultimo vamos a crear un archivo fasta conteniendo todas nuestras secuencias y muestras, este es nombrado como el **Archivo fasta Monolítico**. Este archivo es bastante importante para pasos subsecuentes, así que mantengamos esto en mente.

Primero vamos a navegar a nuestro folder creado anteriormente:
```bash
cd taxon-sets/all
```

Recuerda esto es para organizar las cosas, pero no es obligatorio hacer estos pasos, pero siempre es mejor tener archivos organizados de la forma que tu prefieras.

Una vez mas creemos algunas variables, necesitamos de nuevo la ruta a nuestros contigs, la ruta a nuestra base de datos `sql` y la ruta a nuestro archivo mapa `incomplete.conf`
```bash
AssembliesFolder="/Users/Roderick/Desktop/Hexurella_UCEs_Exercise/Extraccion/contigs_Hexurella"
db="/Users/Roderick/Desktop/Hexurella_UCEs_Exercise/Extraccion/Hexurella_uce_search_results/probe.matches.sqlite"
incomplete_conf="/Users/Roderick/Desktop/Hexurella_UCEs_Exercise/Extraccion/taxon-sets/all/Hexurella_incomplete.conf"
```

Corremos el programa para extraer secuencias en formato fasta
```bash
phyluce_assembly_get_fastas_from_match_counts \
    --contigs $AssembliesFolder \
    --locus-db $db \
    --match-count-output $incomplete_conf \
    --output Hexurella-incomplete.fasta \
    --incomplete-matrix Hexurella-incomplete.incomplete
```
Ahora abres y examina el contenido de `Hexurella-incomplete.fasta`.

- Qué tipo de información hay almacenada aquí?
- ¿Qué mas notas respecto a este archivo?

En efecto este archivo contiene todas las secuencias de UCEs para todas las muestras es decir es un archivo global, lidiar con este archivo es un poco complejo para armar sets de datos, vamos a realizar un paso que nos separara esta información en partes, ya sea por genes o por muestras, a esto se le conoce como “Explode” el archivo Monolítico.

Vamos a separar nuestros datos por muestras, esta forma siempre es mas intuitiva para pasos futuros.

Asignemos a una variable la ruta a nuestro archivo fasta monolítico:
```bash
monolithic="/Users/Roderick/Desktop/Hexurella_UCEs_Exercise/Extraccion/taxon-sets/all/Hexurella-incomplete.fasta"
```

Ahora separemos nuestros datos por muestra, para esto utilizamos el argumento `-—by-taxon` si no especificamos este argumento, el programa por default va a separar los datos por gen.
```bash
phyluce_assembly_explode_get_fastas_file \
    --input $monolithic \
    --output exploded-fastas \
    --by-taxon
```

Examina los contenidos del folder `exploded-fastas` ¿Qué observas?

## Sets de Datos
A este punto, armar diferentes sets de datos se vuelve mas sencillo, ya tenemos nuestros archivos fasta con todos los UCEs que encontramos para esa muestra en un solo archivo. Si tuviéramos muestras de otros experimentos o quisiéramos remover algunas muestras, supongamos, porque son de otro analysis, imagína que secuenciaste toda una placa con muestras de tres proyectos distintos, aquí es el momento adecuado para organizarlas.

Antes de continuar te aconsejo guardar estos archivos fasta en un lugar seguro y dejarlos como tu back up, así evitaras tener que hacer todos los pasos anteriores cuando quieras usar diferentes muestras.

Nuestra forma de procesar datos en `phyluce` y posteriormente en `FUSe` es a travez del archivo monolítico. Entonces podemos crear este archivo una vez que decidamos que muestras incluir.

Supongamos que la muestra `Megahexura-fulva-SDSU-MY4841.unaligned.fasta` no va a formar parte del proyecto porque solo queremos muestras del grupo de interés “in-group” de *Hexurella*, entonces tenemos que excluirla del archivo monolítico. Aquí utilizaremos una serie de comandas que aprendimos anteriormente para facilitar esta tarea.

Si bien podrías abrir cada archivo de forma manual, copiar los contenidos y pegarlos en un nuevo archivo, y así uno de tras del otro, esto es muy tedioso con muchas muestras, utilizaremos el comando `cat` que si recuerdan de la sesión anterior sirve para concatenar contenidos. De igual forma utilizaremos una wildcard `*` para decirle al programa que solo combine archivos que contengan en el nombre la palabra `Hexurella`.

Navegamos al folder con los fastas
```bash
cd exploded-fastas
ls
```
Ahora concatenamos los archivos de interés y creamos un nuevo archivo monolítico denominado `Hexuralla_InGroup_monolithic.fasta`:
```bash
cat Hexurella*.fasta > Hexuralla_InGroup_monolithic.fasta
```

Así puedes utilizar diferentes combinatorias para poder crear tus archivos. Algo util que yo utilizo cuando tengo cientos de muestras es crear un archivo de texto con una lista de las muestras de interés, luego utilizo esa lista para copiar y pegar las muestras a otro folder y después concatenar todo. Puedes ser tan creativo como quieras.
