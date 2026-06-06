# Alineamientos, Poda y Datos Faltantes
A este punto vamos a comenzar finalmente con el post procesamiento de nuestras secuencias, cabe mencionar que para realizar esta serie de pasos existen una infinidad de programas y estrategias que utilizando diversos algoritmos y teoría detrás, no hay métodos correcto o incorrecto, así como tampoco existe un orden de pasos correcto o incorrecto, esto depende principalmente de tus datos y el tipo de factores que quieras evitar o promover, sea datos faltantes, informatividad, etc.

En este curso revisaremos las pasos utilizado en `phyluce` debido a que es la paquetería mas utilizada, después en las siguientes sesiones veremos formas alternativas de realizar estos pasos como son [FUSe](https://github.com/rmonjaraz/FUSe) y [Mesquite](https://www.mesquiteproject.org/), este ultimo con una interfaz gráfica que puede ser extremadamente útil y que es único en la gigantesca cantidad de programas disponibles.

## Alineamiento
El programa mas recomendado para alinear es MAFFT, pero existen otras opciones como Muscle y CLustalW, utilizaremos el “wrapper” (pieza de código que corre otros programas internamente) de `phyluce` para alinear utilizando `mafft`.

Empezaremos a partir de nuestro archivo fasta monolítico, top sugiero copiarlo y pegarlo en un folder completamente nuevo.

```bash
mkdir Hexurella_Alignments
cp Hexurella-incomplete.fasta ../../../Hexurella_Alignments/
```
*NOTA: No copies y pegues estos comandos directamente en tu terminal, siempre utiliza SublimeText u otro editor de texto para modificar las rutas, en mi caso la parte `../../../` significa que mi archivo esta dentro de varios directorios, en tu sistema esto puede ser diferente.*

Una ves en el folder `Hexurella_Alignments` que contiene nuestro archivo monolítico, empezaremos a alinear utilizando `mafft`. Nota que el tutorial de `phyluce` a este punto hace referencia sobre poda de alineamientos interna y externa, nosotros no realizaremos ese paso aun, es mejor alinear y después lidiar con poda, usando otras herramientas.

Para mantener las cosas mas limpias también crearemos un folder para almacenar todos los archivos `.log` estos contienen información sobre los programas, es bueno mantenerlos para recordar parámetros usados, etc.

```bash
mkdir logs
```

Utilizaremos `phyluce_align_seqcap_align` para alinear todas nuestras secuencias. Nota los argumentos a cambiar, `--taxa` es el numero total de muestras en nuestro caso 5, `--aligner` es el programa a utilizar, en este caso `mafft`, `--output-format` es el formato de archivos que necesitamos en este caso utilizaremos fasta, por último `--log-path` es el folder que acabamos de crear, para redirigir el archivo `.log`.
```bash
phyluce_align_seqcap_align \
    --input Hexurella-incomplete.fasta \
    --output Hexurella-mafft \
    --taxa 5 \
    --aligner mafft \
    --cores 12 \
    --incomplete-matrix \
    --output-format fasta \
    --no-trim \
    --log-path logs
```

`WARNING - DROPPED locus uce-2075. Too few taxa (N < 3).`

NOTA: Observa que `phyluce` hace un ore-filtrado por default, el **WARNING** que obtenemos es resultado de este filtrado, descartando alineamientos con menos de 3 muestras, estos no son informativos así que `phyluce` los descarta. Dado que tenemos pocas muestras esta cantidad de alineamientos es muy grande, pero con un set de datos real esto debería reducirse.

- ¿Cuantos alineamientos tenemos a este punto?

TIP: una forma de contar archivos en un folder con linea de comandos es usando el comando `wc -l`:
```bash
ls Hexurella-mafft/ | wc -l
```
`811`

Este comando utiliza un “pipe” `|` para redirigir el resultado de `ls` al siguiente programa `wc`.

Examina algunos de estos abriéndolos en algún visualizador de alineamientos, puedes utilizar [AliView](http://www.ormbunkar.se/aliview/).

Podemos estimar un resumen de todos nuestros alineamientos utilizando `phyluce`:

```bash
phyluce_align_get_align_summary_data \
    --alignments Hexurella-mafft/ \
    --cores 12 \
    --input-format fasta \
    --log-path logs
```
Resultado:
```
----------------------- Alignment summary -----------------------
[Alignments] loci:	811
[Alignments] length:	924,652
[Alignments] mean:	1140.14
[Alignments] 95% CI:	25.99
[Alignments] min:	284
[Alignments] max:	3,493
------------------- Informative Sites summary -------------------
[Sites] loci:	811
[Sites] total:	10,096
[Sites] mean:	12.45
[Sites] 95% CI:	0.96
[Sites] min:	0
[Sites] max:	73
------------------------- Taxon summary -------------------------
[Taxa] mean:		4.10
[Taxa] 95% CI:	0.05
[Taxa] min:		3
[Taxa] max:		5
-------------------- Character count summary --------------------
[All characters]	3,916,187
[Nucleotides]		2,350,402
---------------- Data matrix completeness summary ---------------
[Matrix 50%]		811 alignments
[Matrix 55%]		811 alignments
[Matrix 60%]		811 alignments
[Matrix 65%]		613 alignments
[Matrix 70%]		613 alignments
[Matrix 75%]		613 alignments
[Matrix 80%]		613 alignments
[Matrix 85%]		277 alignments
[Matrix 90%]		277 alignments
[Matrix 95%]		277 alignments
```
- ¿Cuál es xaximo numero de muestras en los alineamientos? ¿Y el mínimo?
- ¿Cual es el porcentaje de sitios informativos en promedio?
- ¿Qué te dice la diferencia en numero de Nucleotidos vs. todos los caracteres?

## Poda
Los alineamientos no se ven tan parejos, esto se debe a lo que revisamos previamente en teoría, los flancos de los alineamientos contienen mucha variabilidad y se alinean de forma pobre, la gran diferencia de Nucleotidos contra caracteres totales se debe al gran numero de “gaps” en cada alineamiento, por tal motivo necesitamos podar nuestros alineamientos.

Para realizar poda de igual forma existen muchos programas el “wrapper” de phyluce tiene la opción de `Gblocks` y `trimAL` Aquí utilizaremos `trimAL` con la opción `-automated1` si buscas mas flexibilidad en algoritmos o programas revisaremos mas adelante `FUSe` o `Mesquite`, este ultimo implementa un algoritmo mas reciente creado por Wayne Maddison que es bastante prometedor y mejor que `GBlocks` y `trimAL`

```bash
phyluce_align_get_trimal_trimmed_alignments_from_untrimmed \
    --alignments Hexurella-mafft \
    --output Hexurella-mafft-trimal \
    --input-format fasta \
    --output-format nexus \
    --cores 12 \
    --log logs
```

*TIP: Cuando trabajemos solo con `phyluce` es importante obtener alineamientos después de la poda en formato `nexus`, esto para evitar problemas con el siguiente paso de limpieza (ver abajo).*

Deberiamos tener el mismo numero de alineamientos, si corren de nuevo el comando de resumen de alineamientos usando como “input” el folder de alineamientos podados, deberían ver diferencias en la longitud de los alineamientos y el numero de Nucletoidos vs. Todos los caracteres.

Visualmente abramos el alineamiento `uce-1630.fasta` primero el alineado y luego el alineado+poda

- ¿Que diferencia ves?

## Limpar

Por último dentro del flujo de trabajo sugerido por `phyluce` tenemos que limpiar nuestros alineamientos, este paso es crucial para los siguientes pasos. Abre los archivos fastas utilizando `AliView` 

- ¿Qué observas con los nombres de las secuencias?

Si queremos concatenar esos archivos para alguna analysis filogenético, los programas fallaran porque cada secuencia tiene un nombre único, tenemos que remover el nombre de los genes (uces) del nombre del taxon.

Para esto utilizaremos otro comando de `phyluce`:

```bash
phyluce_align_remove_locus_name_from_files \
    --alignments Hexurella-mafft-trimal \
    --output Hexurella-mafft-trimal-clean \
    --cores 12 \
    --log-path logs
```
Corrobora que tus alineamientos ya tienen solo el nombre del taxón, así están listos para ser concatenados o utilizados en la gran mayoría de programas de filogenética.

## Filtrar
Por último vamos a hacer un filtrado básico de los datos, este paso es principalmente para controlar la cantidad de datos faltantes, podemos obtener matrices de completitud explicadas anteriormente en teoría, eliminar alineamientos que tengan una longitud promedio específica (ejemplo 50bp) o un número de muestras especifico (ejemplo mínimo 6 muestras).

Empecemos primero con filtrar por número de muestras y longitud de alineamientos, en nuestro ejercicio no tiene mucho sentido filtrar por numero de muestras ya que contamos solo con 5, pero es solo para fines de demostración.

Filtremos alineamientos con longitud menor a 50bp `--min-length 50` y que tengan mínimo 4 muestras `--min-taxa 4`.

```bash
phyluce_align_filter_alignments \
  --alignments Hexurella-mafft-trimal-clean \
  --output Hexurella-mafft-trimal-clean-filtered \
  --input-format nexus \
  --min-length 50 \
  --min-taxa 4 \
  --log-path logs
```

Despise de correr este comando deberíamos tener solo alineamientos con 4 o mas taxa y de longitud mayor a 50bp.

- ¿Cuántos alineamientos quedaron en el folder?

Después de este paso podríamos proceder a filtrar por completitud o cobertura, es decir una matriz completa al 75, 80 0 90%. Dado que en nuestro ejercicio tenemos un total de 5 muestras, una matriz al 80% seria equivalente al comando que realizamos anteriormente, es decir filtrar alineamientos con 4 o menos secuencias. Vamos a realizarlo y ver si obtenemos el mismo resultado. El comando de `phyluce` que usamos para filtrar por completitud o cobertura es `phyluce_align_get_only_loci_with_min_taxa`.

```bash
phyluce_align_get_only_loci_with_min_taxa \
  --alignments Hexurella-mafft-trimal-clean \
  --taxa 5 \
  --percent 0.80 \
  --output Hexurella-80p \
  --input-format nexus \
  --cores 12 \
  --log-path logs
```
- ¿Obtuvimos el mismo numero de alineamientos?

Esto quiere decir que nuestro filtro en el comando anterior de remover alineamientos menores de 50bp no tuvo efecto, probablemente porque todos nuestros alineamientos tenían una longitud mayor.

Para probar su efecto hagamos algo mas extremo, removamos alineamientos menores a 500 bp.

```bash
phyluce_align_filter_alignments \
  --alignments Hexurella-mafft-trimal-clean \
  --output Hexurella-mafft-trimal-clean-filtered-500 \
  --input-format nexus \
  --min-length 500 \
  --min-taxa 4 \
  --log-path logs
```
- ¿Cuantos alineamientos con longitud mayor a 500bp y mas de 4 taxa tenemos?

Otro uso importante de este programa de filtrado en `phyluce` es cuando queremos obtener alineamientos con algún o algunas muestras en especifico, es decir la muestra X es muy importante en nuestro análisis y solo queremos retener loci donde esta muestra esta presente es decir esta presente en el 100% de los alineamientos. Imaginemos que queremos mantener la muestra `Megahexura_fulva_SDSU_MY4841` en todos nuestros alineamientos, entonces usaríamos el siguiente comando:

```bash
phyluce_align_filter_alignments \
  --alignments Hexurella-mafft-trimal-clean \
  --output Hexurella-mafft-trimal-clean-filtered-Megahexura \
  --input-format nexus \
  --containing-data-for Megahexura_fulva_SDSU_MY4841 \
  --log-path logs
```

- ¿En cuantos alineamientos esta presente esta muestra?

NOTA: De esta misma forma puedes proveer una lista de muestras, separadas por espacio, así el programa filtrara lineamientos que presenten la condición de tener todas las muestras listadas.

## Conversion de formatos
Por último vamos a revisar como convertir nuestros alineamientos, muchas veces dependiendo el programa que usemos, estos requieren formatos específicos, ya sea Nexus, Fasta, Phylip, etc. `phyluce` también tiene una forma muy conveniente de convertir entre formatos:

Hasta ahora hemos estado trabajando con formato Nexus, convirtamos nuestros alineamientos a formato Fasta, trabajemos con nuestros alineamientos al 80%:

```bash
phyluce_align_convert_one_align_to_another \
  --alignments Hexurella-80p \
  --output Hexurella-80p-Fasta \
  --input-format nexus \
  --output-format fasta \
  --cores 12 \
  --log-path logs
```

Listo! Ahora tienes un set de alineamientos listo para los siguientes pasos, quizás estimar un árbol filogenético.




