# Filogenómica moderna basada en Elementos Ultra Conservados (UCEs)
**Rodrigo Monjaraz-Ruedas**, Natural History Museum Los Angeles County

Información de contacto:

email: rmonjarazruedas [at] nhm [dot] org

Webpage: https://rmonjaraz.github.io/

## Introducción
Este es un curso corto e intensivo sobre el procesamiento de datos provenientes de secuenciación de captura hibrida como son los Elementos Ultraconservados, la finalidad es familiarizarse con el uso de estas herramientas y el uso de la linea de comandos para descargar, limpiar, ensamblar, alinear y filtrar secuencias, con el objetivo final de crear una serie de alineamientos listos para su análisis. Se proporcionaron los fundamentos básicos de secuenciación de nueva generación y se introducirá brevemente con herramientas como Mesquite, las cuales mas recientemente permiten el análisis de estos datos utilizando una interfaz gráfica. 

## Programa

| Fecha | Hora | Tema |
|:----|:---|:---|
| Lunes 8 de Junio | 8:30 – 11:30 | Session 1: Introducción a Secuenciación de Nueva Generación y Manejo de datos |
| Lunes 8 de Junio | 11:30 – 12:00 | Receso |
| Lunes 8 de Junio | 12:00 – 14:30 | Session 2: Introducción a la Bioinformática |
| Martes 9 de junio | 8:30 – 11:30 | Session 3: Procesamiento de datos genómicos - NCBI, FASTQ files, Trimommatic|
| Martes 9 de junio | 11:30 – 12:00 | Receso |
| Martes 9 de junio | 12:00 – 14:30 | Session 4: Procesamiento de datos genómicos - Ensamblaje - SPADES|
| Miércoles 10 de junio | 8:30 – 11:30 | Session 5: Procesamiento de datos genómicos - Extracción de sequencias - Phyluce |
| Miércoles 10 de junio | 11:30 – 12:00 | Receso |
| Miércoles 10 de junio | 12:00 – 14:30 | Session 6: Filogenómica - Alineamientos, Poda y Datos Faltantes - phyluce |
| Jueves 11 de junio | 8:30 – 10:00 | Session 7: Filogenómica - FUSe |
| Jueves 11 de junio | 10:00 – 12:00 | Session 8: Filogenómica - Estimación de árboles - IQTree y ASTRAL |
| Jueves 11 de junio | 12:00 – 12:30 | Receso |
| Jueves 11 de junio | 12:00 – 14:30 | Session 9: Filogenómica -  Mesquite |

## Materiales
### Diapositivas
Aqui encontraran las diapositivas del curso por día:

- [Diapositivas Día 1](https://drive.google.com/file/d/1Cauk9yruRRMydlX1HZIckdQhaGnmfXM4/view?usp=sharing)
- Diapositivas Día 2
- Diapositivas Día 3
- Diapositivas Día 4

### Datos
Aquí encontraran todos los archivos de entrada y salida para los ejercicios, en caso de que algún paso no se pueda reproducir o se atrasen durante la clase, aqui pueden retomar los archivos, organizados por programa y tipo de análisis:

[Datos y Arvhivos](https://drive.google.com/drive/folders/1nNVErZg9nKXas9wLejYGuCEVTtDaM_Q8?usp=drive_link)

### Tutoriales
Instrucciones y scripts necesarios para reproducir los análisis y ejercicios del curso por session:

- [Instalación][0]
- [Session 2: Introducción a la Bioinformática][2]
- [Session 3: Procesamiento de datos genómicos - Limpieza y Control de calidad][3]
- [Session 4: Procesamiento de datos genómicos - Ensamblaje][4]
- [Session 5: Procesamiento de datos genómicos - Extracción de sequencias]<!--[5]-->
- [Session 6: Filogenómica - Alineamientos, Poda y Datos Faltantes]<!--[6]-->
- [Session 7: Filogenómica - FUSe]<!--[7]-->
- [Session 8: Filogenómica - Estimación de árboles - IQTree y ASTRAL]<!--[8]-->
<!-- - [Session 9: Filogenómica - Mesquite][9] -->

### Literatura
Carpeta con artículos de referencia y/o de interés para el curso.

[Literatura](https://drive.google.com/drive/folders/1hoYlKACopRpwfPqRiVEP_DMWWnqjKx6W?usp=drive_link)

## Software
Para detalles de como instalar estos programas revisar el [tutorial de instalación][0] o los sitios de cada programa. Mesquite provee de instrucciones bastante detalladas para la instalación. SublimeText, FigTree y FastQC tienen interfaz grafica que puede ser instalada de forma convencional.
- [SublimeText](https://www.sublimetext.com/) o cualquier Editor de Texto
- [Phyluce](https://phyluce.readthedocs.io/en/latest/index.html)
- [Mesquite](https://www.mesquiteproject.org/)
- [FigTree](https://tree.bio.ed.ac.uk/software/figtree/)
- [IQTree](https://iqtree.github.io/)
- [ASTRAL](https://github.com/chaoszhang/ASTER/blob/master/tutorial/wastral.md)
- [FUSe](https://github.com/rmonjaraz/FUSe)
- [AMAS](https://github.com/marekborowiec/AMAS)
- [sra-tools](https://github.com/ncbi/sra-tools)
- [FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- [AliView](http://www.ormbunkar.se/aliview/)


[0]:https://github.com/rmonjaraz/UCEs_Workshop_LaPaz_2026/blob/main/Tutoriales/Instalacion.md
[2]:https://github.com/rmonjaraz/UCEs_Workshop_LaPaz_2026/blob/main/Tutoriales/Session2.md
[3]:https://github.com/rmonjaraz/UCEs_Workshop_LaPaz_2026/blob/main/Tutoriales/Session3.md
[4]:https://github.com/rmonjaraz/UCEs_Workshop_LaPaz_2026/blob/main/Tutoriales/Session4.md
[5]:https://github.com/rmonjaraz/UCEs_Workshop_LaPaz_2026/blob/main/Tutoriales/Session5.md
[6]:https://github.com/rmonjaraz/UCEs_Workshop_LaPaz_2026/blob/main/Tutoriales/Session6.md
[7]:https://github.com/rmonjaraz/UCEs_Workshop_LaPaz_2026/blob/main/Tutoriales/Session7.md
[8]:https://github.com/rmonjaraz/UCEs_Workshop_LaPaz_2026/blob/main/Tutoriales/Session8.md