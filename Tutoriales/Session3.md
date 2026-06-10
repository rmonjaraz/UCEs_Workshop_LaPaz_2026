# Procesamiento de datos genómicos

## Short Read Archive (SRA):

Dirigete al portal del SRA:

https://www.ncbi.nlm.nih.gov/sra

Cambia el campo de búsqueda por BioProject y busca el BioProject de *Hexurella* `PRJNA953506` aqui puedes descargar todas las muestras asociadas a ese proyecto o crear una lista de muestras de interes usando los números de Accession.

- Cuantas muestras hay asociadas a este BioProject?
- ¿De qué tamaño es todo el set de datos?
- Tomate tu tiempo y explora los contenidos de la pagina
- ¿Que notas aquí? Da click en BioSample, ¿Qué representan estas?
- Navega a alguna de las muestras en la lista, ¿que especie es? ¿Que tipo de secuenciación se uso?
- ¿Quien subió los datos y en que fecha?

### Descargando los datos
Necesitamos descargar dos archivos los códigos de Accession y los Metadatos de cada muestra. Vamos a trabajar solo con 5 muestras para simplificar el trabajo:
```
SAMN34118186
SAMN34118198
SAMN34118156
SAMN34118201
SAMN34118159
```
Puedes copiar estos códigos y pegarlos en la barra del buscador utilizando como base de búsqueda `BioSample` podríamos bajarlos de forma manual, pero esto es un poco mas complicado, así que utilizaremos la linea de comandos para ello. Para eso crearemos una lista con estos codigos y crearemos dos archivos: `biosample_result_SRA.txt` con los códigos y `SraRunInfo.csv` con los metadatos.

- Send to > File > Accession List -> `biosample_result_SRA.txt`
- Send to > File > RunInfo -> `SraRunInfo.csv`

Este proceso puede ser un poco complejo cuando se trabaja con muchas muestras dado que los archivos Fastq suelen ser bastante pesados, así que necesitamos trabajar con bastante espacio en disco y comprimir archivos al momento de descargarlos, utilizaremos la paquetería `sra-tools` para poder hacer esto.

Primero necesitamos obtener los archivos que vamos a bajar, a esto se le conoce como `prefetch` y este es un programa dentro del set de herramientas de `sra-tools`. Vamos a crear un folder nuevo donde correremos el `prefetch`.
```bash
mkdir prefetchSRA
cd prefetchSRA
```
Activar nuestro ambiente donde instalamos `sra-tools`:
```bash
conda activate phylogenetics
cd prefetchSRA
```

Obtengamos los códigos de SRA que están listados en el archivo txt `biosample_result_SRA.txt`
```bash
while read -r line
do
prefetch $line
done < ../biosample_result_SRA.txt
```
*NOTA: Si esto falla o se tarda bastante puede ir al folder `prefetchSRA` de la carpeta compartida `Data` y descargarlos de ahi.*

Los Archivos debieron descargarse en un folder con el nombre de la corrida que empieza con `SRR*` y dentro hay otro archivo con el mismo nombre pero con terminación `.sra`

Ahora tenemos que descargar los datos reales utilizando `fasterq-dump`, otro programa de el set de `sra-tools`. El argumento `--split-files` aqui es muy importante para poder separar secuencias en “forward” (R1) y “reverse” (R2). De lo contrario se descargaran todas en un solo archivo combinado.

Vamos a crear otro folder para guardar los datos
```bash
mkdir raw_SRA_fastqs
```
Navegamos a nuestro folder de `prefetchSRA`
```bash
cd prefetch
```
*NOTA: Recuerda nuestra clase de rutas absolutas y relativas, esto cobra sentido en este punto, para mantener las cosas organizadas necesitamos trabajar en diferentes folders y re-dirigir los resultados a otro folder usando las rutas relativas o absolutas.*

Vamos a utilizar un bucle aqui para poder automatizar el proceso, descargando todas las muestras de nuestra lista. Copia y pega el bucle.
```bash
for i in *
do
fasterq-dump $i -O ../raw_SRA_fastqs --split-files --include-technical
gzip ../raw_SRA_fastqs/$i_*.fastq
done
```
Analicemos que pasa, estamos interactuando con cada folder en `prefetchSRA`, descargando los datos usando usando `fasterq-dump`, creando los archivos R1 y R2 usando el argumento `--split-files` y luego estamos utilizando `gzip` otro programa adicional para compactar nuestros archivos gunzip es un programa de compresion muy popular en bioinformática.

Pregunta: ¿De que tamaño son los archivos antes y después de ser compactados con `gunzip`?

## Archivos Fastq y Limpieza
Ver Presentación

--------------------------------------

Naveguemos de regreso a nuestro directorio SRA y dirígete a `Examples_FastQs`:
```bash
cd ../Examples_FastQs/
ls
```
- Exploremos un poco el contenido de los archivos fastq como lo hicimos en la sesión anterior utilizando `cat`, `head` y `tail`
- Examina ambos archivos READ1 y READ2, ¿puedes determinar si estos corresponden con el tipo de secuenciación pareada?
- Mirando a los valores de Q ¿parece ser una buena secuencia corta en cuestión de calidad?
- ¿Qúe longitud tienen la primera y última secuencia corta del Archivo R1?

Utilicemos el programa `FastQC` para explorar la calidad de nuestras secuencias cortas. Este programa tiene una interfaz gráfica lo que nos permite utilizarla de la misma forma que utilizamos cualquier otro programa, una vez instalado da doble click sobre el logo para abrirlo. `File > Open > Sample1-READ1.fastq` utiliza el navegador para buscar tus archivos en tu computadora.

- ¿Que observas son de buena calidad las secuencias?
- ¿Existen adaptadores en la secuencia?
- ¿Que promedio de longitud tienen las secuencias? ¿Es esto algo que esperarías de acuerdo a la teoría de secuenciación?

Ahora abre alguno de los archivos que recién descargamos del SRA, y comparado con los anteriores, en términos de calidad, longitud y adaptadores.

### Remover Adaptadores
Si recuerdas de nuestra sesión de secuenciación los adaptadores que contienen primers e indices no se requieren a este punto una ves que las muestras han sido “demultiplexed”. Para esto necesitamos remover los adaptadores, remover secuencias de muy baja calidad por base, secuencias con solo datos faltantes como “Ns” o secuencias cortas, en otras palabras, realizar un control de calidad de nuestras secuencias, uno de los programas mas populares es [Trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic) este es el mismo paso que se sugiere en el tutorial de Phyluce para limpiar secuencias usando [Illumiprocessor](https://phyluce.readthedocs.io/en/latest/tutorials/tutorial-1.html) en realidad este programa de python también utiliza `Trimmomatic`. Vamos a realizar ambos pasos para entender como hacer este paso cuando phyluce o fuera de phyluce.

Para usar `Trimmomatic` con los datos de SRA vamos a utilizar un programa de python llamado `trimmobatch.py` que nos ayudará a procesar múltiples muestras de forma automátizada y por lotes de muestras. También nos facilita el ingresar los datos utilizando un archivo de configuración simplificado que es un simple archivo CSV (valores separados por comas), lo cual hace más accesible este paso incluso que `Illimiprocessor`. Otra ventaja de `trimmobatch.py` es que podemos usarlo aun cuando desconocemos los datos de indices utilizados en la creación de bibliotecas, y que es requerido en `Illumiprocessor`.

Necesitamos una lista de archivos, vamos a utilizar la información en `SraRunInfo.csv` tenemos que hacer coincidir el numero de accession de SRA usado para descargar los datos con sus metadatos (especie, código de voucher, etc.). "Ver diapositiva de Adaptadores"

NOTA: Aqui es una excelente oportunidad para renombrar nuestros archivos a algo mas util e informativo, esto nos evitara dolores de cabeza en el futuro, evita utilizar cualquier característica especial, no espacios, acentos, comas, puntos, etc. Utiliza `_` Guin bajo para reemplazar espacios y no combines guiones bajos `_` con guiones `-` mantenlo todo parejo. Otro tip es mantener tus nombres por debajo de 34 caracteres para también evitar conflictos mas adelante. Las reglas de buen uso serian: Especie_NoCatalogo.

`trimmobatch.py` se encuentra en el repository de GitHub en la carpeta de [Scripts](https://github.com/rmonjaraz/UCEs_Workshop_LaPaz_2026/blob/main/Scripts). El archivo requerido es un archivo separado por comas `csv` y la estructura es algo así:
```
Sample1_R1.fastq.gz,Sample1_R2.fastq.gz,Sample_name_1 
Sample2_R1.fastq.gz,Sample2_R2.fastq.gz,Sample_name_2
... 
```
Para crearlo vamos a navegar al folder con nuestros dastos del SRA `raw_SRA_fastqs` y usar `ls -1` para crear una lista de archivos R1 y luego R2 usando un wildcard `*`:
```
ls -1  *_1.fastq.gz > ../R1.txt
ls -1  *_2.fastq.gz > ../R2.txt
```

Existen muchas formas de hacer la lista final de nombres, se pueden exportar directamente desde el archivo de metadatos y copiarlos de forma manual. La forma en que procederé en este caso es con una combinación de Excel (o cualquier otro programa de hojas de calculo) y SublimeTex )o cualquier otro editor de texto). Ten en cuenta que estos pasos son útiles cuando se tienen mas de 20 muestras.

Primero copiaré los contenidos de mis archivos `R1.txt` y `R2.txt` creados anteriormente, en dos diferentes columnas, estos ya se encuentran ordenados pero siempre puedes volver a ordenarlos si es necesario.

Luego copiaré y pegaré las columnas de interés de mi archivo `SraRunInfo.csv` en la nueva hoja, esto incluye el número SRA (que se usaré para asociarlos con los archivos), la especie y el número de catálogo.

En Excel ordenaré mis tres nuevas columnas por número SRR, asegurándome de que coincidan con los nombres de los archivos. Después usaré esta fórmula para crear un único nombre de archivo con la combinación de dos columnas, asumiendo que mis columnas están en D, E y F y que mi primera fila tiene encabezados:
```
=E2&"_"&F2
```
Esto creará el nombre de la especie más el número de colección separados por un guion bajo. Luego simplemente copia y pega "solo valores" para que los nombres no sean fórmulas.

Por último, me gusta copiar este texto a SublimeText y terminar de editarlo ahi, buscando y reemplazando cualquier espacio, punto o palabra ineccesaria. 

- Sustituir espacios por guiones bajos
- Sustituir los puntos que siguen al guiándotelos bajo por un solo guion bajo
- Eliminar las palabras "UCE_" y "RMR-2023a_" de todos los nombres para reducir su longitud (recordemos idealmente menos de 34 caracteres).

Cuando estés satisfecho con tus nombres, sustituye TAB por coma (para crear un archivo `.csv`, añade una última línea (espacio al final del documento), esto se llama línea de final de documento (es importante incluirla para REGEX en línea de comandos). Finalmente guárdalo como `list_of_samples.txt`.

*NOTA: Este archivo se encuentra en el folder de `Data` por si prefieres usar este.*

Una vez obtenido este archivo estamos listos para correr `trimmobatch.py` usando argumentos para indicar las opciones:

Activamos primero nuestro ambiente conda de `phyluce` donde tenemos instalado `trimmomatic`


```bash
conda activate phyluce1.7
```

Ahora corremos `trimmobatch.py`
```bash
python trimmobatch.py \
-I list_of_samples.txt \
-O Hexurella \
-R raw_SRA_fastqs/ \
-n 12
```
`-I` Esta opción es para proveer de la lista de especies que creamos.
`-O` es un prefijo para nombrar nuestro folder de salida.
`-R` es el folder con todos nuestros archivos Fastq bajados del SRA
`-n` Indica el numero de núcleos de tu computadora a usar.

### Illumiprocessor
Por cuestiones didácticas, vamos a limpiar estas secuencias utilizando `Illumiprocessor` que es el programa por default utilizado en `Phyluce`. Este paso esta pensado en un caso en el que tienes secuencias completamente nuevas, generadas por un proyecto propio, por consiguiente tienes información respecto al tipo de secuenciación y en específico las secuencias índice o “barcodes” que marcan cada muestra durante el proceso de “demultiplexing”. Sin esta información, por ejemplo al descargar secuencias del SRA, es mas complicado usar `Illumiprocesor`.

En este caso, las secuencias de *Hexurella* fueron originalmente secuenciadas por mi en el laboratorio así que tengo esa información disponible, simulemos un caso en el que obtienen sus datos crudos de una empresa de secuenciación.

La información se encuentra en el archivo de excel `Indexing_Info.xlsx` aquí hay siete columnas `Pool` es el nombre de la linea de secuenciación, `Library Name` es el nombre de esa muestra en particular, en este caso es un código de colección de San Diego State University, `Name in SRA` fue agregado solo para asociar los nombres en SRA con las muestras, finalmente `i7-i5 Index Name` y `i7-i5 Sequence` son nuestras secuencias y los nombres de los indices, estos pueden variar dependiendo los indices utilizados.

El archivo de configuración de `Illumiprocesor` contiene esta información en diferentes bloques, abre al archivo y analiza su contenido y comparado con la información en `Indexing_Info.xlsx`.

Una vez creado este archivo, correr `Illumiprocesor` es muy similar a correr `trimmobatch`, solo necesitamos proveer de algunos argumentos.

```bash
illumiprocessor \
--input raw_SRA_fastqs/ \
--output illumiprocessor_clean_fastqs \
--config illumiprocessor.conf \
--cores 12 \
--r1-pattern '{}_(1).fastq.gz' \
--r2-pattern '{}_(2).fastq.gz'
```
Indicar el REGEX ("regular expression") adecuado en los argumentos `--r1-pattern` y `--r2-pattern` es importante cuando se trabaja con archivos de SRA ya que estos no tienen el clásico nombre que se obtiene de compañías de secuenciación.

## QC - Fastq Control de Calidad
En esta sección podemos checar calidad de la misma forma anterior utilizando FastQC, hay formas de utilizar linea de comandos para automatizar el proceso y obtener un reporte general de cada muestra, cuando tienes cientos de muestras esto es algo tedioso, podemos utilizar un programa de `phyluce` llamado `phyluce_assembly_get_fastq_lengths` para obtener un reporte general de todas nuestras muestras.

Creemos primero un archivo para almacenar nuestro reporte y asignemos algunos nombres de columnas:
```bash
echo sample,reads,total bp,mean length, 95 CI length,min,max,median > CleanQC.csv
```
Naveguemos al folder que contiene nuestras secuencias cortas ya limpias
```bash
cd Hexurella_clean_fastq/
```
Activa tu ambiente con `phyluce` si aun no lo habías hecho.
```bash
conda activate phyluce1.7
```
Corramos el programa utilizando un bucle:
```
for i in *;
do
phyluce_assembly_get_fastq_lengths --input $i/split-adapter-quality-trimmed/ --csv >> ../CleanQC.csv;
done   
```
Abre el archivo creado `CleanQC.csv` una vez que termina el comando.

- ¿Que puedes observar de este reporte?
- ¿Que parámetros son importantes para determinar la calidad de las secuencias?
- ¿Removerías alguna muestra por considerarla de poca o baja calidad?
