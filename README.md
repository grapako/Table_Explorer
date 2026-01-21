JIP Table Explorer

JIP Table Explorer es una herramienta ligera y rápida escrita en Python para visualizar, filtrar y ordenar tablas de datos (CSV, DAT, TXT) de gran tamaño sin necesidad de abrir Excel o software pesado.

Incluye un lanzador inteligente (.bat) para Windows que detecta automáticamente entornos de Anaconda/Miniconda, facilitando la ejecución inmediata.

Características

🚀 Carga Inteligente: Detecta automáticamente separadores (coma, punto y coma, tabulación, espacios múltiples/formato científico).

⚡ Rendimiento: Utiliza PyQt5 y Pandas para manejar grandes volúmenes de datos con fluidez.

🔍 Filtrado en Tiempo Real: Barra de búsqueda con soporte para expresiones regulares (RegEx).

📂 Multi-ventana: Abre múltiples archivos simultáneamente en ventanas independientes.

🛠 Smart Batch Launcher: Script .bat que encuentra tu instalación de Conda y activa el entorno necesario automáticamente.

Requisitos

Python 3.x

Pandas

PyQt5

Instalación

Clona este repositorio:

git clone [https://github.com/TU_USUARIO/Table_Explorer.git](https://github.com/TU_USUARIO/Table_Explorer.git)


Instala las dependencias:

pip install -r requirements.txt


(O usa tu entorno de Conda preferido)

Uso

En Windows (Recomendado)

Simplemente haz doble clic en el archivo run_explorer.bat.

El script buscará automáticamente tu instalación de Anaconda o Miniconda.

Activará el entorno (puedes configurar el nombre del entorno en el .bat, por defecto JIP_env).

Si no encuentra Conda, intentará usar el Python del sistema.

En Terminal (Cualquier SO)

python table_explorer.py


Créditos y Autoría

Autor: JIP
Co-desarrollado con asistencia de IA: Google Gemini 3.0 PRO

Este proyecto fue creado para solucionar la necesidad de explorar rápidamente archivos de datos científicos con formatos heterogéneos.