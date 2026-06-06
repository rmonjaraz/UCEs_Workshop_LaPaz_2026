# Instalación
La mayoría de paqueterías para el procesamiento de datos en filogenómica tienen dependencias de Python, adicionalmente el manejo de archivos y procesamiento en masa de archivos se realiza de forma mas simple utilizando Linux shell también conocido como Bash. Los sistemas de Linux mas comúnes como Ubuntu o MacOS funcionan con commandos similares en Bash, por consiguiente para poder estandarizar el lenguaje en windows es necesario instalar un intérprete.

Por otro lado es importante poder compartamentalizar diferentes paqueterías y programas para su correcto funcionamiento, para esto utilizaremos principalmente conda, este nos permite crear “ambientes” independientes con versiones de programas especificas que nos permitan correr software sin necesidad de tener conflictos con programas internos de la computadora o con algún otro programa independiente que se necesite para operaciones distintas.

## Windows WSL

`NOTA: Si estas trabajando en un computadora con Linux o MacOS ve al paso siguiente CONDA`

Primero necesitamos installar Windows Subsistem for Linux (WSL) checa el sitio de [WSL Github](https://github.com/microsoft/WSL) para mas detalles e instrucciones avanzadas (en Ingles)
   
1. Abre la terminal en Windows PowerShell
2. Escribe el siguiente comando para instalar WSL:
   	
```
wsl --install
```
3. Reinicia tu computadora, desde la terminal escribe:
```
Restart-Computer
```
4. Una vez se reinicio tu computadora, abre el menu de windows y da click en el recién instalado WSL icono con la 	imagen del pingüino.
<img src="https://github.com/microsoft/WSL/blob/master/Images/Square44x44Logo.targetsize-256.png?raw=true" width="5%">
5. Crea tu usuario de Unix, puedes agregar cualquier nombre por ejemplo `Jose` y seguido de un password
`NOTA: Guarda o recuerda estos datos en algún lugar porque serán pedidos por el sistema cada que inicies en WSL y para hacer cambios durante las instalaciones de programas.`

**Felicidades has instalado correctamente WSL!**

***NOTA:** Si estas teniendo problemas checa [este video](https://www.youtube.com/watch?v=luM5kwH6tjQ) (en Ingles) con una muy buena explicación paso a paso para instalar WSL y CONDA.*

## CONDA
Recomiendo instalar miniconda para estas situaciones, esta es una versión mas ligera de Anaconda que será útil para este curso. [Aquí](https://www.anaconda.com/docs/getting-started/miniconda/install/overview) pueden seguir las instrucciones mas detalladas sobre la instalación. Recomiendo utilizar la Terminal o Linea de Comandos para la instalación.

1. Asegurate de descargar la versión de miniconda de a cuerdo a tu sistema operativo, si utilizas windows y estas corriendo WSL necesitaras una version de Linux en Ubuntu, checa si tu sistema es de 32 o 64 bit. Si estas en MacOS debes descargar la version de Intel o ARM64 dependiendo tu computadora.
2. [Aqui](https://repo.anaconda.com/miniconda/) se encuentran todas las distribuciones de miniconda copia la dirección de la version que se ajusta a tu sistema.
3. Navega al el directorio (folder) base donde quieres descargar tu archivo usando `cd`
4. Descarga miniconda, para la versión de 64 bit de Linux la dirección es: `https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh` 

Linux:
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

Para la versión ARM64 de MacOS la version mas reciente seria:
`https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh`

MacOS:
```
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
```
5. Corre el programa que ejecutara la instalación de conda, ajusta el comando dependiendo tu version de conda
```
bash ./Miniconda3-latest-Linux-x86_64.sh
```
6. Lee y acepta los términos y condiciones presionando <kbd>Enter</kbd>
7. Acepta los términos y condiciones `Yes`
8. Presiona <kbd>Enter</kbd> para aceptar la ubicación por default de la instalación
9. `IMPORTANTE!` Cuando te pregunte el sistema si deseas “inicializar conda” escribe `Yes`
10. Cierra y vuelve a abrir la terminal para reiniciar el sistema.
11. Si vees la leyenda `(base)` antes de tu nombre de usuario, significa que la instalación fue exitosa, compruébalo escribiendo
```
conda --version
```
Debdrias ver la versión de tu instalación de conda `conda 25.3.0`

**Felicidades has instalado correctamente CONDA!**

Si obtienes algún error durante la instalación puedes checar la sección [Troubleshooting](https://www.anaconda.com/docs/getting-started/miniconda/install/linux-install) de la pagina de CONDA o [este video](https://www.youtube.com/watch?v=luM5kwH6tjQ) bastante informativo.

`Opcional`: Es importante revisar que los canales (channels) de conda están disponibles para instalar paquetes, en particular bioconda y conda-forge, corre el comando 
```
conda config --show channels
```
Si ves `bioconda` y `conda-forge` en la lista, estas listo para continuar si no, puedes correr los siguientes comandos:
```
conda config --add channels bioconda
```
```
conda config --add channels conda-forge
```

## Phyluce
Las instrucciones para [instalar Phyluce](https://phyluce.readthedocs.io/en/latest/installation.html) están bastante claras y simplificadas en la pagina, aqui hago un resumen de los pasos a seguir, tenemos que crear un ambiente independiente para instalar phyluce, esto nos permitirá mantener todos los paquetes y versiones independientes del resto del sistema. Aconsejo instalar la versión mas actual `phyluce v1.7.3`

1. Ve a la pagina [github de phyluce](https://github.com/faircloth-lab/phyluce/releases)
2. Descarga el archivo correspondiente a tu sistema operativo, aqui vienen instrucciones especificas para cada sistema operativo, ya sea Linux, Windows usando WSL o Mac con Intel o M-Series/AMR64 CPU.
`NOTA:` Es importante seguir las instrucciones para MacOS M-Series CPU como se detallan en la pagina ya que estos pasos son cruciales.
3. Para Linux, Windows (WSL) o Mac Intel las instrucciones son sencillas:
4. Descarga el archivo utilizando `wget`
   ```
   wget https://raw.githubusercontent.com/faircloth-lab/phyluce/v1.7.3/distrib/phyluce-1.7.3-py36-Linux-conda.yml
   ```
5. Crea el ambiente de phyluce:
   ```
   conda env create -n phyluce-1.7.3 --file phyluce-1.7.3-py36-Linux-conda.yml
   ```
	---
    Para MacOS - M-Series CPU:

	```
	wget https://raw.githubusercontent.com/faircloth-lab/phyluce/v1.7.3/distrib/phyluce-		1.7.3-py36-macOS-conda.yml
	```

	La siguiente parte se ejecuta en un solo comando seguido, copia y pega el texto de este 	bloque, esto crea un ambiente x86 importante para correr phyluce:
	```
	CONDA_SUBDIR=osx-64 conda create -n phyluce-1.7.3-x86 python=3.6
	conda activate phyluce-1.7.3-x86
	conda config --env --set subdir osx-64
	```
	Finalmente crea e instala a través del archivo `.yml`
	```
    conda env update --name phyluce-1.7.3-x86 --file phyluce-1.7.3-py36-macOS-conda.yml --prune
	```
	---
6. Para activar tu ambiente y entrar en el utiliza los comandos `conda activate phyluce-1.7.3-x86` o para desactivar `conda deactivate`

`TIP: Si quieres simplificar el nombre del ambiente para que sea mas sencillo activarlo puedes cambiar el nombre al momento de crear tu ambiente, reemplazando —-name phyluce-1.7.3-x86 por algo como: --name phyluce1.7 o cualquier nombre que te parezca adecuado.`

## Paquetes adicionales
Necesitamos instalar una serie adicional de herramientas para procesar datos durante el trabajo con secuencias, aconsejo crear una ambiente adicional para poder instalar estos sin conflictos directos con `phyluce`.

Vamos a instalar [sra-tools](https://github.com/ncbi/sra-tools) que nos permitirá descargar y manipular datos de NCBI SRA. [AMAS](https://github.com/marekborowiec/AMAS) by Marek Borowiek, para obtener estadísticos de nuestros alineamientos, ademas de poder usarlo para concatenar o manipular alineamientos, [FUSe](https://github.com/rmonjaraz/FUSe) by Rodrigo Monjaraz-Ruedas para poder automatizar todo el proceso de UCEs, [IQTree](https://iqtree.github.io/) para poder correr análisis directamente desde nuestra computadora y [ASTRAL](https://github.com/chaoszhang/ASTER/blob/master/tutorial/wastral.md) o mejor conocido ahora como ASTER para estimar arboles de especies.

Estos programas se instalan principalmente utilizando CONDA, lo cual simplifica la forma de instalar programas y paqueterías en CONDA, otra ventaja de utilizar este tipo de ambientes.

1. Vamos a crear un ambiente para almacenar estos programas, a mi me gusta nombrarlo `phylogenetics` pero puedes asignarle el nombre que quieras, solo recuerda el nombre para poderlo usar después.
   ```
   conda create --name phylogenetics python=3
   ```
2. Una vez creado entramos a nuestro ambiente
   ```
   conda activate phylogenetics
   ```
3. Instalamos AMAS
   ```
   pip install amas
   ```
4. Instalamos sra-tools
   ```
   conda install bioconda::sra-tools
   ```
5. Instalamos sra-tools
   ```
   pip install gunzip
   ```
6. Instalamos iqtree
   ```
   conda install bioconda::iqtree
   ```
7. Instalamos ASTER (ASTRAL)
   ```
   conda install aster
   ```
Para el caso de **FUSe**, este tiene que ser instalado directamente en el mismo ambiente de `phyluce` que creamos previamente ya que utiliza muchos de los programas que vienen en la instalación de `phyluce`, esto permite flexibilidad y simplicidad. De igual forma no require instalación, puede ser ejecutado directamente desde el folder de trabajo. Para simplicidad se puede copiar el archivo python directamente el la carpeta `bin` de phyluce para poder correr el programa sin necesidad de proveer la dirección completa del programa. Para ello, descarga la versión provista en este repositorio y pégala en bin usando el siguiente comando, asegúrate de ajustar la dirección (path) acorde con tu sistema:
```
cp FUSe.py /User/miniconda3/envs/phyluce-X.x.x/bin/
chmod 775 /User/miniconda3/envs/phyluce-X.x.x/bin/FUSe.py
```
Test the script by running:
```
FUSe.py --help
```
## Mesquite
Para instalar Mesquite, referirse a la [pagina de instalación](https://www.mesquiteproject.org/Installation.html) del programa donde se proveen de indicaciones detalladas acerca de la instalación para multiples sistemas operativos. Este requiere JAVA y descargar la paquetería mas actualizada de Mesquite.
