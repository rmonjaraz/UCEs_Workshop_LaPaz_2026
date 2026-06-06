# Estimación Filogenética
Ahora que ya tenemos una serie de alineamientos podados y filtrados por loci y por secuencia, podemos comenzar a estimar arboles filogenéticos.

Uno de los programas mas utilizados por su eficiencia y rapidez es [IQTree](https://iqtree.github.io/), este puede utilizarse de forma local (correr análisis en tu propia computadora) o de forma remota utilizando el servidor del programa. Cabe mencionar que las versiones de servidor no permiten analizar grandes numero de datos, un análisis con mas de 15 muestras y mas de 100 loci puede estar en los limited de lo que permiten los servidores. Por ejemplo el Servidor de [IQTREE en el HIV Database](https://www.hiv.lanl.gov/content/sequence/IQTREE/iqtree.html) permite un máximo de 20mb por archivo, esto aun así podría fallar si se trata de un análisis con parámetros mas complejos.

De cualquier forma correrlo de forma local es posible en computadores o laptops convencionales, a expensas de que tomara un poco mas de tiempo. Aconsejo seguir con detalle los tutoriales de `IQTREE` sobre todo el de principiantes y después el avanzado para familiarizarse mas con la Lina de comandos, aqui revisaremos dos opciones, genera un árbol concatenado utilizando “ultrafast” bootstrap y posteriormente obtendremos arboles de genes, esto es una árbol por cada alineamiento. Utilizaremos la Matriz al 80%

Afortunadamente `IQTREE` es bastante intuitivo y nos permite utilizar multiples formatos y si tenemos multiples alineamientos podemos proveer de nuestro folder y `IQTREE` lo concatenará por nosotros.

## IQTree

Un ejemplo muy sencillo, utilizando la matriz concatenada que ya generamos con `AMAS` anteriormente seria:

Activa tu ambiente donde instalaste IQTREE, en mi caso `phylogenetics` si tienes activo tu ambiente de phyluce descativalo primero usando `conda deactivate`

```bash
conda activate phylogenetics
```

Vamos a crear un nuevo folder para almacenar nuestros arboles y mantener todo organizado, directamente en el folder de inicio creamos un folder y lo nombramos como `Trees` y navegamos al nuevo folder.

Ya ahi corremos vamos a crear otro folder para almacenar los archivos de salida de esta corrida, llamemos `Run1` y creemos una variable para indicar la ruta de nuestro archivo 

```bash
file="/Users/Roderick/Desktop/Hexurella_UCEs_Exercise/Hexurella_FUSe/Hexurella2-Alignments/Hexurella_Concatenated.fasta"
```
Ahora si corremos a `iqtree`, incluye el argumento `--prefix` para nombrar tus archivos y también para que el resultado se almacene en el nuevo folder.
```bash
iqtree -s $file --prefix Hexurella1
```
Este comando ha creado una corrida sencilla de `iqtree` contiene el árbol final `.trees` que puedes abrir con `Figtree`. Por default, `iqtree` corre una búsqueda del mejor modelo evolutivo para tu “super matriz" utilizando `ModelFinder` (que es equivalente a proporcionar el argumento `-m`). Abre el archivo con temrinación `.iqtree` y examina su contenido.

- ¿Cuál ha sido el mejor modelo para este análisis?
- ¿Qué criterio se ha utilizado para elegir el mejor modelo?

Si observas este árbol carece de soporte de ramas y por consiguiente no podemos saber que tan robusto es, vamos a adicionar un análisis de bootstrap, `iqtree` tiene una aproximación de bootstrap que es ordenes de magnitud mas rápida que un bootstrap convencional llamadas ultrafast bootstrap (UFBoot) para utilizarla solo necesitamos agregar el argumento `-B` y especificar cuantas replicamos queremos. Adicionalmente vamos a indicar a `iqtree` que muestra representa nuestro grupo externo, en este caso `Megahexura_fulva_SDSU_MY4841`:

Vamos a crear otro folder paraesta segunda corrida:

```bash
cd ../
mkdir Run2
cd Run2
```

```bash
iqtree -s $file -B 100 -o Megahexura_fulva_SDSU_MY4841 --prefix Hexurella2
```
Abre tu archivo en `FigTree` y observa si tenemos soporte de ramas esta vez.

### Análisis particionado
UN análisis mas realista requiere que participemos los datos, ya sea por loci o por codon, etc. en este caso vamos a participar por loci y pedirle a `iqtree` que estime el mejor esquema de partición para nuestros datos utilizando, similar a análisis de `PartitionFinder`.

Podemos seguir utilizando nuestro archivo concatenado y proveer el archivo de partición al programa, sin embargo también podemos proveer el folder completo de alineamientos de forma mas sencilla, hagamoslo de esta forma, utilizando el argumento `-p` este indica el folder con alineamientos y le indica que queremos hacer una análisis particionado.

Una vez mas, mantengamos todo ordenado y creemos un nuevo folder para el análisis particionado:
```bash
cd ../
mkdir Run3
cd Run3
```

Creemos una nueva variable para indicar la ruta de nuestro folder:

```bash
folder=/Users/Roderick/Desktop/Hexurella_UCEs_Exercise/Hexurella_FUSe/Hexurella2-Alignments/Hexurella2-80p
```
Corremos el análisis:
```bash
iqtree -p $folder -B 100 -T 4 -mset mrbayes --prefix Hexurella3
```

¿Qué indican los argumentos `-T` y `-mset` en este comando? Ve a la documentación de `iqtree` [aqui](https://iqtree.github.io/doc/Command-Reference) y buscalos.

### Estimación de arboles de genes
Ahora vamos a realizar un análisis de genes, anteriormente hemos estado realizando un análisis de una sola matriz concatenada y estimando un solo árbol para toda la matríz. Esto es también conocido como análisis de “Super Matriz” o Análisis Concatenado mas recientemente. Existen método como ASTRAL o BEAST que requieren de estimar arboles de genes individuales y después utilizan estos arboles para estimar un árbol final aveces denominado “Arbol de especies” o “Arbol Consenso”.

Para estimar árboles de genes `iqtree` nos provee de un comando extremadamente simple, en este caso haremos selección del mejor modelo y estimaremos UFBoot para cada loci, esto es importante en pasos subsecuentes.

Creemos nuevamente otro folder:
```bash
cd ../
mkdir Run4_loci
cd Run4_loci
```

Utilizando el mismo folder creamos una variable:

```bash
folder=/Users/Roderick/Desktop/Hexurella_UCEs_Exercise/Hexurella_FUSe/Hexurella2-Alignments/Hexurella2-80p
```
Y utilizamos el argumento o “flag” `-S` (en mayusculas) para indicar a `iqtree` realizar un análisis de genes a partior de los archivos en nuestro folder.

Corremos el análisis:
```bash
iqtree -S $folder -B 100 --prefix Hexurella3 -T AUTO --prefix loci
```
Abre el archivo `loci.treefile` en `FigTree` ¿cuántos árboles tenemos?

## ASTRAL (wASTRAL)
Existe un método bastante popular llamado [ATRAL](https://github.com/chaoszhang/ASTER/blob/master/tutorial/astral4.md) que estima árboles de especies a partir de árboles de genes, es un método que se basa en el modelo `multi-species coalescent` y que es bastante robusto para estimar filogenias en casos de eventos de sorteo de linajes incompleto (Incomplete Lineage Sorting). En este método ha sido demostrado que al considerar y eliminar ramas cortas y valores de soporte bajos en cada árbol de genes, mediante la creación de politomias, resulta en una estimación mas precisa [Zhang y Mirarab, 2022](https://academic.oup.com/mbe/article/39/12/msac215/6750035?login=true).

Esta es la razón por la cual estimar valores de soporte previamente en nuestros arboles de genes era importante. Antiguamente estos pasos de generar politomias y colapsar nodos con bajo soporte tenia que hacerse de forma manual y a esto se le llamaba `Weighted ASTRAL` “pesar” tus alineamientos por longitud de ramas o por valores de soporte. Afortunadamente existe un nuevo algoritmo denominado [wASTRAL](https://github.com/chaoszhang/ASTER/blob/master/tutorial/wastral.md) parte de la familia [ASTER](https://github.com/chaoszhang/ASTER/tree/master) que es una colección de algoritmos y programas asociados a ASTRAL, que nos permite estimar wASTRAL de forma extremadamente sencilla.

Para ver los parámetros a mas detalle referirse a la documentación [aqui](https://github.com/chaoszhang/ASTER/blob/master/tutorial/wastral.md). Ten en mente que muchas veces para análisis de ASTRAL, podemos agrupar individuos de la misma especie para que sean representados como una sola terminal en nuestro árbol final de `ASTRAL`, por ejemplo si tenemos 2 especies y 5 individuos de esas dos especies, podemos agruparlos y usar la información conjunta para estimar el árbol de especies final. Utilizando un archivo de configuración con la opción `-a`:

```
individual_A1 species_name_A
individual_A2 species_name_A
individual_B1 species_name_B
individual_B2 species_name_B
individual_B3 species_name_B
...
```

En nuestro caso, vamos a correr una análisis sencillo, asumiendo que cada terminal es una especie sin indicar un archivo de mapeo de individuos a especies:
```bash
wastral -t 12 -i loci.tre -o Hexurella_wAstral.tre 2>wastral.log
```
Abre el archivo y examina el árbol, que tipo de soporte de ramas tenemos? R.= LPP

Si quisiéramos obtener valores de rama mas complejos podemos ajustar la opción `-u 2` para también incluir los famosos `Quartet Score (QT)` que nos proporcionan información sobre que topologías alternativas están recibiendo mas o menor soporte, estos valores son muy tules para estudiar sorteo incompleto de linajes.

```bash
wastral -t 12 -u 2 -i loci.tre -o Hexurella_wAstral_u2.tre 2>wastral_u2.log
```
Abre el archivo `.treefile` y explora su contenido.