# Ensamblaje *De Novo*
Considerando las limitaciones computacionales, vamos a utilizar unas muestras de practica “dummy” para poder realizar los comandos necesarios para el ensamblaje, cabe señalar que cada día las computaros son mas eficientes, si tienes una computadora con bastante memoria RAM, puedes intentar correr la practica con las muestras reales en tu tiempo libre. Esto puede ser muy tardado, quizás días, por consiguiente ten esto en cuenta.

Vamos a utilizar el programa [SPAdes](https://ablab.github.io/spades/index.html), que viene preinstalado con la distribución de `phyluce`. Este programa fue desarrollado por investigadores Rusos y es uno de los ensambladores mas eficientes y poderosos actuales, mostrando ser util en recuperar mas `contigs` y de mayor tamaño en comparación a otros como `Trinity` o `Velvet`.

Para poder correr estos comandos de forma “local” es decir en nuestra computadora, tenemos que cambiar la cantidad de memoria asignada por default en `SPAdes`, ya que esta es por default bastante alta.

Otros cambios importantes es que correremos `SPAdes` utilizando un bucle, es decir fuera del “wrapper” de `phyluce`, esto nos permitira cambiar las opciones de ensamblaje para optimizar recursos y tiempo utilizando los argumentos `--isolate` y `--only-assembler` estos son importantes.

`--isolate` Es un buen compromiso entre corrección de errores y uso de memoria, nos permite hacer un ensamblaje reduciendo considerablemente el paso de corrección de errores (que es el paso que utiliza mas memoria), sin embargo este comando espera obtener valores altos de cobertura. 

`--only-assembler` Evita completamente la corrección de errores, esto resulta en ensamblajes rápidos y sin grandes cantidades de memoria, posibles en computadoras locales, pero a expensas de obtener `contigs` de tamaño reducido, es decir mas cortos, que los obtenidos con las opciones `—isolate` o `—careful`. Estos pueden ser corregidos en pasos posteriores utilizando algún otro método de corrección mas eficiente como `Pilon` en lugar de `BayesHammer`. Pero estos pasos están mas allá del objetivo de este tutorial y requieren ser validados.

Corramos el bucle para ensamblar nuestros datos, vamos a crear primero unas variables:
```bash
folder="/Users/Roderick/Desktop/Hexurella_Workshop/Data/Assembly/clean-reads-phyluce"
output="/Users/Roderick/Desktop/Hexurella_Workshop/Data/Assembly/assemblies-phyluce"
cores=12
```
folder = Folder de secuencias cortas limpias, resultado de `trimmobatch` o `Illimiprocessor`
output = Folder donde almacenaremos nuestros ensambles

Naveguemos a nuestro folder de secuencias cortas limpias de practica “dummy”, estas están en la carpeta `Assembly/clean-reads-phyluce`:
```bash
cd $folder
```
Desde aqui corremos nuestro bucle:
```bash
for i in *
do
spades.py --isolate \
--pe1-1 $folder/$i/split-adapter-quality-trimmed/*-READ1.fastq.gz \
--pe1-2 $folder/$i/split-adapter-quality-trimmed/*-READ2.fastq.gz \
--pe1-s $folder/$i/split-adapter-quality-trimmed/*-READ-singleton.fastq.gz \
-m 500 \
-t $cores \
-o $output/$i
done
```
*NOTA: `-m` que indica la memoria a usar fue cambiada a 500Gb para que el programa utilice toda la memoria disponible y no termine con error.*

### Renombrar
Una vez que estos terminaron, los archivos se encueran dentro de carpetas con el nombre de nuestras muestras y los archivos están nombrados como `contigs.fasta` (utilizaremos contigs en lugar de scaffolds). Para poder renombrarlos y utilizarlos en futuros pasos es muy fácil hacerlo con linea de comandos, para evitar renombrar manualmente cada uno de ellos. Podemos copiarlos a un nuevo folder y renombrarlos o crear “symlinks” es decir enlaces simbólicos a esos archivos, esto es preferible si tienes poco espacio de disco en tu computadora, los comandos son esencialmente los mismos.

Vamos a crear un folder donde almacenaremos estos archivos o los enlaces a estos archivos, dependiendo la opción que elijas.
```bash
mkdir contigs_phyluce
```
Navega al folder con nuestro recién creados ensambles:
```bash
cd assemblies-phyluce
```
Crea los enlaces, para esto usaremos el programa `ln -s` aquí tienes que proporcionar la ruta absoluta de tus archivos para evitar problemas, observa el uso de la variable `$i` en el bucle, en mi computadora sería algo así:
```bash
for i in *
do
  ln -s /Users/Roderick/Desktop/Hexurella_Workshop/Data/Assembly/assemblies-phyluce/$i/contigs.fasta /Users/Roderick/Desktop/Hexurella_Workshop/Data/Assembly/contigs_phyluce/$i.fasta
done
```
Si prefieres copiar los archivos, solo tienen que reemplazar `ln -s` por `cp`.

### QC
Por último, vamos a realizar un control de calidad con los ensambles, para asegurarnos que nuestras muestras tienen una cantidad aceptable de contigs y de tamaños aceptables, la cantidad de contigs recuperados a este punto afectaran enteramente el numero de secuencias por muestra en los pasos siguientes, asi que este es un buen momento para detenernos y observar la calidad de los datos.

Creemos un archivo con headings para almacenar nuestros valores de QC
```bash
echo samples,contigs,total bp,mean length,95 CI length,min length,max length,median legnth,contigs1kb > AssemblyQC.csv
```
Utilicemos el programa de `phyluce`: `phyluce_assembly_get_fasta_lengths` para estimar QC por muestra y corramos en un bucle. Para este paso hagamos sobre los contigs de hexurella para obetener valores mas reales, el folder con contigs lo puedes descargar del folder de `Data` en el repositorio, llamado `contigs_Hexurella`.
```bash
for i in /Users/Roderick/Desktop/Hexurella_Workshop/Data/Assembly/contigs_Hexurella/*.fasta;
do
	phyluce_assembly_get_fasta_lengths --input $i --csv >> AssemblyQC.csv;
done
```




