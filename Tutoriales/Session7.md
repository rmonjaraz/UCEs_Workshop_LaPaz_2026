# Filtrado por Secuencias
En la sesión anterior revisamos como filtrar alineamientos dependiendo su numero total de secuencias o longitudes máximas, esto quiere decir que dentro de cada alineamiento, las secuencias pueden aun tener longitudes variables o mostrar otra serie de eventos como duplicaciones, regiones poco alineadas, zonas muy divergentes o secuencias extremadamente cortas, el proceso de poda puede resolver algunas de estas cuestiones, pero en algunos casos vale la pena remover secuencias que pueden introducir ruido en los análisis.

Existe un sin fin de herramientas que lideran con este tipo de problemas, y de formas variables, este tema realmente es "un agujero sin fin” que puede llevar mucho tiempo y estudio el decidir que parámetros o programas usar. Entre los mas populares están [spruceup](https://github.com/marekborowiec/spruceup) el cual remueve principalmente secuencias “outliers”. [CIAlign](https://github.com/KatyBrown/CIAlign) Que es toda una colección de programas para limpiar, editar, visualizar y manipular alineamientos, usando ambos métodos por secuencia y pr alineamiento. [TAPER](https://github.com/chaoszhang/TAPER) que es similar a `spruceup` pero utilizando un enfoque diferente, pero que busca en general remover secuencias anómalas.

Finalmente [FUSe](https://github.com/rmonjaraz/FUSe), (Align, Trim and **F**ilter **U**CE **Se**quences and Alignments) que es principalmente un “wrapper” de multiples funciones que busca automatizar y simplificar muchos de estos pasos de filtrado por alineamiento y secuencias. `FUSe` no es un reemplazo de `spruceup` or `TAPER`, de hecho aconsejo utilizar esos métodos después de filtrar con `FUSe` pero en mi experiencia es mas util en casos específicos. 

Existen otros flujos de trabajo como el aconsejado por Wayne Maddison en Mesquite, que utiliza un método de poda y el uso de `spruceup` para refinar el filtrado por secuencia y que también es bastante efectivo y que veremos mas tarde.

`FUSe` es mucho mas similar a CIAlign en sus funciones, podría decirse que es una simplificación de CIALign que tiene un sin fin de funciones bastante utiles. `FUSe` permite flexibilidad para realizar Alineamientos, Poda, Filtrado y remover secuencias cortas y divergentes principalmente, es bastante eficaz para reducir los mismo parámetros a travez de multiples sets de datos, sin tener que escribir múltiples comandos repetidas veces.

## FUSe
Primero empecemos por explorar la eficiencia de `FUSe` vamos a repetir los pasos que realizamos en la sesión anterior, mas filtrado de secuencias cortas y secuencias divergentes. La version 2.0 de `FUSe` ahora tiene alineamiento con mafft que no depende de `phyluce`. Estas son las opciones en `FUSe`:

```
usage: FUSe [-h] [-i MONOLITHIC_FILE] -t TAXA [-I ALIGNMENTS_FOLDER]
            [-p PREFIX] [-o {fasta,nexus,phylip,clustal,emboss}] [-c CORES]
            [--align-m {localpair,globalpair,auto}] [--trimAL]
            [-a {automated1,gappyout,strict,strictplus,nogaps}] [--gblocks]
            [--b1 B1] [--b2 B2] [--b3 B3] [--b4 B4] [--remove-div]
            [-d DIVERGENT] [--remove-short] [-s SHORT_CUTOFF]
            [--filter-alignments] [-l MIN_LENGTH] [-m MIN_TAXA]
            [--get-completeness] [-e PERCENT] [--taxa-count] [-v]

Align, Trimm and Filter UCE Sequences and Alignments.

optional arguments:
  -h, --help            show this help message and exit
  -I ALIGNMENTS_FOLDER, --alignments ALIGNMENTS_FOLDER
                        Folder with alignments to process.
  -p PREFIX, --prefix PREFIX
                        The name to be used for all output folders (default:
                        OUTPUT).
  -o {fasta,nexus,phylip,clustal,emboss}, --out-format {fasta,nexus,phylip,clustal,emboss}
                        The ouput alignment format (default: fasta).
  -c CORES, --cores CORES
                        The number of PHYSICAL CPUs (default: 1).
  --align-m {localpair,globalpair,auto}
                        Mafft algorithm to use (default: auto).
  --trimAL              Wether to trim alignments using trimal.
  -a {automated1,gappyout,strict,strictplus,nogaps}, --t-method {automated1,gappyout,strict,strictplus,nogaps}
                        trimAl automated method to use (default: automated1).
  --gblocks             Wether to trim alignments using gblocks.
  --b1 B1               The GBLOCKS -b1 proportion (default: 0.5)
  --b2 B2               The GBLOCKS -b2 proportion (default: 0.70)
  --b3 B3               The GBLOCKS -b3 integer value (default: 10)
  --b4 B4               The GBLOCKS -b4 integer value (default: 4)
  --remove-div          Wether to remove divergent sequences from alignments.
  -d DIVERGENT, --divergent DIVERGENT
                        Percentage of pairwise identity in every sequence to
                        retain (default: 0.7).
  --remove-short        Wether to remove short sequences from alignments.
  -s SHORT_CUTOFF, --short-cutoff SHORT_CUTOFF
                        Percentage of "-" (gaps) in every sequece to retain
                        (default: 0.7).
  --filter-alignments   Wether to filter alignments by No. taxa and length in
                        bp.
  -l MIN_LENGTH, --min-length MIN_LENGTH
                        The minimum alignment lenght to retain alignment
                        (default: 50).
  -m MIN_TAXA, --min-taxa MIN_TAXA
                        The minimum number of taxa in alignments to retain
                        (default: 4).
  --get-completeness    Wether to filter alignments by completeness.
  -e PERCENT, --percent PERCENT
                        Completeness matrix percentage to output (default:
                        0.8).
  --taxa-count          Wether to print taxa count in alignments summary.
  -v, --version         show program's version number and exit

Required arguments:
  -i MONOLITHIC_FILE, --input MONOLITHIC_FILE
                        The input monolithic fasta file.
  -t TAXA, --taxa TAXA  The total number of taxa in all alignments.
```

Como pueden ver `FUSe`, permite realizar todos los pasos de `phyluce` mas otros adicionales. Alinearemos utilizando `mafft` usando el algoritmo `globalpair` después obtendremos una matriz al 80% de datos faltantes, removiendo alineamientos menores a 500bp y vamos a podar usando trimAL usando el método `gappyout`,después removeremos secuencias cortas que tengan un porcentaje de 80% de datos faltantes dentro del mismo alineamiento, es decir, solo un 20% de datos. Por último removeremos secuencias que tenga un porcentaje de 80% de divergencia, esto es secuencias que en una comparación pareada difieren en un 80% con el resto de las secuencias, esto puede ser el resultado de secuencias parálogas, mal alineadas o errores de secuenciación.

El archivo de entrada para `FUSe` es el Fasta Monolítico:

```bash
FUSe.py \
-i Hexurella-incomplete.fasta \
-t 5 \
-p Hexurella \
-c 12 \
--align-m globalpair \
--trimAL \
-a gappyout \
--remove-div \
-d 0.8 \
--remove-short \
-s 0.8 \
--filter-alignments \
-l 500 \
--get-completeness \
-e 0.8 \
--taxa-count
```
- ¿Qué pedemos observar del resultado?
- ¿Como se ve la estructura del directorio?
- ¿Porque no coincide el numero de alineamientos con los de la sesión anterior?
  - Removimos bastantes secuencias divergentes
- ¿Cómo utilizarias el archivo `summary-taxa.csv` para checar la calidad de tus muestras?
- ¿Qué observas en el texto impeso en la pantalla o en el archivo `FUSe.log`?
  - ¿A que se debe este fenómeno con Megahexura? ¿Cómo lo cambiarias?

Veamos como se ve una secuencia corta, busca y examina la siguiente muestra en el correspondiente alineamiento: `Hexurella_pinea_SDSU_MY5314 from uce-5839`

Ahora examinemos una secuencia divergente, busca la secuencia y alineamiento de la siguiente muestra: `Hexurella_encina_SDSU_MY5277 from uce-1779`

### Refinando los filtros
Cambiemos algunos parámetros para ver como se ve el resultado final, sobre todo queremos mantener nuestro grupo externo, entonces no queremos removerlo por accidente. Bajemos el porcentaje de divergencia a `0.65`. También cambia tu prefijo para que `FUSe` cree un molder diferente, esto te permite tener muchos sets de datos diferentes y comparar mas tarde.

```bash
FUSe.py \
-i Hexurella-incomplete.fasta \
-t 5 \
-p Hexurella2 \
-c 12 \
--align-m globalpair \
--trimAL \
-a gappyout \
--remove-div \
-d 0.65 \
--remove-short \
-s 0.8 \
--filter-alignments \
-l 500 \
--get-completeness \
-e 0.8 \
--taxa-count
```

- ¿Mejoro el filtrado en `Megahexura`? 
- ¿En cuantos alineamientos esta presente en esta ronda vs la anterior?
  *TIP: checa el el archivo `summary-taxa.csv`*

RESUMEN: Algunos de estos pasos reducen bastante el número de alineamientos a usar, son considerados conservadores, ya que prefieren reducir la cantidad de datos (número de alineamientos o loci) para maximizar la calidad de los datos al remover potenciales errores de secuenciación, genes parálogos o secuencias contaminadas. Existen muchas extrategias de filtrado adicionales a estas, inclusive el orden de los pasos en que estos filtros son aplicados resultan en diferentes sets de datos, es a discreción del usuario elegir la mejor estrategia.

## AMAS
[AMAS](https://github.com/marekborowiec/AMAS) (Alignment manipulation and summary statistics) es un programa escrito por Marek Borowiec (mismo author de `spruceup`) para manipular alineamientos, a pesar de que `phyluce` también provee de ciertos programas para convertir formatos (como vimos en la sesión anterior) o para concatenar, personalmente prefiero usar `AMAS` para convertir y sobre todo para obtener métricas de mis alineamientos.

Vamos a usar `AMAS` primero para crear una matriz concatenada y luego para extraer la proporción de sitios parsimoniosamente informativos por alineamiento.

Para algunos programas es importante obtener una matríz concatenada, esto es “pegar” uno después de otro todos nuestros alineamientos de cada loci. El requisito es que todos nuestros taxa deben de estar nombrados de la misma forma a través de todos los alineamientos, esto fue realizado durante el paso de Limpieza en la sesión anterior.

Usando `AMAS` procederemos a crear una matriz concatenada de nuestro folder de alineamientos filtrados al 80%, dentro de nuestro folder `Hexurella2-Alignments` corremos:

```bash
AMAS.py -h
```
```
usage: AMAS <command> [<args>]

The AMAS commands are:
  concat      Concatenate input alignments
  convert     Convert to other file format
  replicate   Create replicate data sets for phylogenetic jackknife
  split       Split alignment according to a partitions file
  summary     Write alignment summary
  remove      Remove taxa from alignment
  translate   Translate DNA alignment into protein alignment
  trim        Remove columns from alignment

Use AMAS <command> -h for help with arguments of the command of interest

positional arguments:
  command     Subcommand to run

optional arguments:
  -h, --help  show this help message and exit
```
Aquí vemos que para concatenar necesitamos usar el comando concat.

```bash
AMAS.py concat -h
```
```
usage: AMAS.py [-h] [-p CONCAT_PART] [-t CONCAT_OUT]
               [-u {fasta,phylip,nexus,phylip-int,nexus-int}]
               [-y {nexus,raxml,unspecified}] [-e] [-c CORES] -i IN_FILES
               [IN_FILES ...] -f {fasta,phylip,nexus,phylip-int,nexus-int} -d
               {aa,dna}

Concatenate input alignments

optional arguments:
  -h, --help            show this help message and exit
  -p CONCAT_PART, --concat-part CONCAT_PART
                        File name for the concatenated alignment partitions.
                        Default: 'partitions.txt'
  -t CONCAT_OUT, --concat-out CONCAT_OUT
                        File name for the concatenated alignment. Default:
                        'concatenated.out'
  -u {fasta,phylip,nexus,phylip-int,nexus-int}, --out-format {fasta,phylip,nexus,phylip-int,nexus-int}
                        File format for the output alignment. Default: fasta
  -y {nexus,raxml,unspecified}, --part-format {nexus,raxml,unspecified}
                        Format of the partitions file. Default: 'unspecified'
  -e, --check-align     Check if input sequences are aligned. Default: no
                        check
  -c CORES, --cores CORES
                        Number of cores used. Default: 1

required arguments:
  -i IN_FILES [IN_FILES ...], --in-files IN_FILES [IN_FILES ...]
                        Alignment files to be taken as input. You can specify
                        multiple files using wildcards (e.g. --in-files
                        *fasta)
  -f {fasta,phylip,nexus,phylip-int,nexus-int}, --in-format {fasta,phylip,nexus,phylip-int,nexus-int}
                        The format of input alignment
  -d {aa,dna}, --data-type {aa,dna}
                        Type of data
```
Aqui vemos que necesitamos proveer obligatoriamente tres argumentos, archivos que queremos concatenar, el formato en que se encuentran y que tipo de data es, dna o aminoácidos (aa).

```
AMAS.py concat -i Hexurella2-80p/*.fasta \
-f fasta \
-d dna \
-c 12 \
-u fasta \
-t Hexurella_Concatenated.fasta
```

Si abrimos el archivo podemos ver que tenemos un archivo concatenado en un solo archivo fasta y también tenemos un archivo `partition.txt` de particiones indicando los intervalos de cada loci.

Nota el uso del wildcard en el argumento `-i` AMAS espera de “input” un solo archivo, al usar el wildcard hacemos que AMAS cree una lista de todos esos archivos que terminan en `.fasta` y los combine todos en uno solo.

Ahora vamos a obtener un resumen estadístico de nuestros alineamientos:

```bash
AMAS.py summary -h
```
```
usage: AMAS.py [-h] [-o SUMMARY_OUT] [-s] [-e] [-c CORES] -i IN_FILES
               [IN_FILES ...] -f {fasta,phylip,nexus,phylip-int,nexus-int} -d
               {aa,dna}

Write alignment summary

optional arguments:
  -h, --help            show this help message and exit
  -o SUMMARY_OUT, --summary-out SUMMARY_OUT
                        File name for the alignment summary. Default:
                        'summary.txt'
  -s, --by-taxon        In addition to alignment summary, write by
                        sequence/taxon summaries. Default: Don't write
  -e, --check-align     Check if input sequences are aligned. Default: no
                        check
  -c CORES, --cores CORES
                        Number of cores used. Default: 1

required arguments:
  -i IN_FILES [IN_FILES ...], --in-files IN_FILES [IN_FILES ...]
                        Alignment files to be taken as input. You can specify
                        multiple files using wildcards (e.g. --in-files
                        *fasta)
  -f {fasta,phylip,nexus,phylip-int,nexus-int}, --in-format {fasta,phylip,nexus,phylip-int,nexus-int}
                        The format of input alignment
  -d {aa,dna}, --data-type {aa,dna}
                        Type of data
```
Si observas los argumentos obligatorios, son los mismos que en el paso anterior, pero podemos obtener un “summary” por taxon o por alineamiento, en este caso obtengamos por alineamiento (loci).

```
AMAS.py summary -i Hexurella2-80p/*.fasta \
-f fasta \
-d dna \
```

Este comando ha creado un archivo con nombre: `summary.txt` abre este archivo en excel. Vamos a analizar su contenido.

Analiza el contenido de cada columna, estos son valores asociados a cada alineamiento, nuestro folder `Hexurella-80p` contiene 365 alineamientos, entonces esperamos obtener 365 lines en nuestro archivo una por alineamiento.

Ordena tu archivo por mayor proporción de sitios parsimoniosamente informativos (PI), si quisiéramos retener solo aquellos alineamientos con 10% o mas de sitios PI, ¿cuántos alineamientos tendríamos?

Que otra métrica en esta tabla utilizarías para ordenar tus alineamientos y potencialmente filtrarlos?